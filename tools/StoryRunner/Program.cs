using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

if (args.Length < 3 || args[0] != "generate" || args[1] != "--scene")
{
    Console.Error.WriteLine("Usage: StoryRunner generate --scene <scene.md>");
    return 1;
}

try
{
    var scenePath = Path.GetFullPath(args[2]);
    if (!File.Exists(scenePath))
    {
        Console.Error.WriteLine($"Scene file not found: {scenePath}");
        return 1;
    }

    var repo = FindRepoRoot(Directory.GetCurrentDirectory());
    var relative = Path.GetRelativePath(repo, scenePath).Split(Path.DirectorySeparatorChar);
    if (relative.Length < 8 || relative[0] != "series" || relative[2] != "books" ||
        relative[4] != "stories" || relative[6] != "scenes" || Path.GetExtension(scenePath) != ".md")
        throw new InvalidOperationException("Scene must be inside series/<series>/books/<book>/stories/<story>/scenes/.");
    var seriesDir = Path.Combine(repo, "series", relative[1]);
    var bookDir = Path.Combine(seriesDir, "books", relative[3]);
    var storyDir = Path.Combine(bookDir, "stories", relative[5]);
    // Required ownership metadata prevents accidental fallback to another continuity.
    foreach (var file in new[] { Path.Combine(seriesDir, "series.json"), Path.Combine(bookDir, "book.json") })
        if (!File.Exists(file)) throw new FileNotFoundException("Missing ownership metadata", file);
    var story = JsonSerializer.Deserialize<StoryContext>(
        await File.ReadAllTextAsync(Path.Combine(storyDir, "story.json")), JsonOptions())
        ?? throw new InvalidOperationException("Story metadata must be a JSON object.");
    if (story.ContextFiles is null) throw new InvalidOperationException("contextFiles must be an array.");
    var baseUrl = Environment.GetEnvironmentVariable("LLM_BASE_URL") ?? "http://127.0.0.1:8080";
    var model = Environment.GetEnvironmentVariable("LLM_MODEL") ?? "local-gguf";

    var generation = JsonSerializer.Deserialize<GenerationConfig>(
        await File.ReadAllTextAsync(Path.Combine(repo, "llm", "config", "generation.json")),
        JsonOptions()) ?? new();

    var systemPrompt = await File.ReadAllTextAsync(Path.Combine(repo, "llm", "prompts", "system.md"));
    var scenePrompt = await BuildScenePrompt(repo, seriesDir, scenePath, story.ContextFiles);

    using var http = new HttpClient
    {
        BaseAddress = new Uri(baseUrl.TrimEnd('/') + "/"),
        Timeout = TimeSpan.FromMinutes(30)
    };

    var request = new ChatRequest
    {
        Model = model,
        Messages =
        [
            new("system", systemPrompt),
            new("user", scenePrompt)
        ],
        Temperature = generation.Temperature,
        TopP = generation.TopP,
        MinP = generation.MinP,
        RepeatPenalty = generation.RepeatPenalty,
        MaxTokens = generation.MaxTokens
    };

    Console.WriteLine($"Calling {http.BaseAddress}v1/chat/completions ...");

    using var response = await http.PostAsJsonAsync("v1/chat/completions", request, JsonOptions());
    var body = await response.Content.ReadAsStringAsync();

    if (!response.IsSuccessStatusCode)
    {
        Console.Error.WriteLine(body);
        return 2;
    }

    var result = JsonSerializer.Deserialize<ChatResponse>(body, JsonOptions());
    var text = result?.Choices?.FirstOrDefault()?.Message?.Content;

    if (string.IsNullOrWhiteSpace(text))
    {
        Console.Error.WriteLine("Model returned no text.");
        Console.Error.WriteLine(body);
        return 3;
    }

    var draftDir = Path.Combine(storyDir, "generated");
    Directory.CreateDirectory(draftDir);

    var sceneName = Path.GetFileNameWithoutExtension(scenePath);
    var stamp = DateTime.UtcNow.ToString("yyyyMMdd-HHmmss-fffffff");
    var output = Path.Combine(draftDir, $"{sceneName}-{stamp}.md");

    await File.WriteAllTextAsync(output, text.Trim() + Environment.NewLine, Encoding.UTF8);

    Console.WriteLine($"Saved: {output}");
    return 0;
}
catch (Exception ex) when (ex is IOException or InvalidOperationException or JsonException or ArgumentException or HttpRequestException or TaskCanceledException)
{
    Console.Error.WriteLine(ex.Message);
    return 1;
}

static async Task<string> BuildScenePrompt(string repo, string seriesDir, string scenePath, string[] contextFiles)
{
    var files = new List<string> { Path.Combine(repo, "authoring", "guidance.md") };
    foreach (var path in contextFiles)
    {
        var file = Path.GetFullPath(Path.Combine(seriesDir, path));
        var relative = Path.GetRelativePath(seriesDir, file);
        if (Path.IsPathRooted(path) || relative == ".." || relative.StartsWith(".." + Path.DirectorySeparatorChar))
            throw new InvalidOperationException($"Context escapes selected series: {path}");
        // This is a text-only client: images are indexed by metadata, never sent as binary text.
        if (Path.GetExtension(file) is not (".md" or ".json"))
            throw new InvalidOperationException($"Context must be Markdown or JSON: {path}");
        files.Add(file);
    }
    files.Add(Path.Combine(repo, "llm", "prompts", "scene-generation.md"));
    files.Add(scenePath);
    var sb = new StringBuilder();
    foreach (var file in files.Distinct())
    {
        var name = Path.GetRelativePath(repo, file);
        sb.AppendLine($"\n--- BEGIN {name} ---");
        sb.AppendLine(await File.ReadAllTextAsync(file));
        sb.AppendLine($"--- END {name} ---");
    }
    return sb.ToString();
}

static string FindRepoRoot(string start)
{
    var dir = new DirectoryInfo(start);

    while (dir is not null)
    {
        if (File.Exists(Path.Combine(dir.FullName, "llm", "config", "generation.json")))
            return dir.FullName;

        dir = dir.Parent;
    }

    throw new InvalidOperationException("Could not find repository root.");
}

static JsonSerializerOptions JsonOptions() => new(JsonSerializerDefaults.Web)
{
    WriteIndented = true
};

sealed class GenerationConfig
{
    public double Temperature { get; init; } = 1.0;
    [JsonPropertyName("top_p")] public double TopP { get; init; } = 0.95;
    [JsonPropertyName("min_p")] public double MinP { get; init; } = 0.05;
    [JsonPropertyName("repeat_penalty")] public double RepeatPenalty { get; init; } = 1.05;
    [JsonPropertyName("max_tokens")] public int MaxTokens { get; init; } = 4096;
}

sealed class ChatRequest
{
    public string Model { get; init; } = "";
    public List<ChatMessage> Messages { get; init; } = [];
    public double Temperature { get; init; }
    [JsonPropertyName("top_p")] public double TopP { get; init; }
    [JsonPropertyName("min_p")] public double MinP { get; init; }
    [JsonPropertyName("repeat_penalty")] public double RepeatPenalty { get; init; }
    [JsonPropertyName("max_tokens")] public int MaxTokens { get; init; }
}

sealed record ChatMessage(string Role, string Content);

sealed class ChatResponse
{
    public List<Choice> Choices { get; init; } = [];
}

sealed class Choice
{
    public ChatMessage? Message { get; init; }
}

sealed class StoryContext
{
    public required string[] ContextFiles { get; init; }
}
