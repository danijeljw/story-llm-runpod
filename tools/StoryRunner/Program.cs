using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

if (args.Length < 3 || args[0] != "generate" || args[1] != "--scene")
{
    Console.Error.WriteLine("Usage: StoryRunner generate --scene <scene.md>");
    return 1;
}

var scenePath = args[2];
if (!File.Exists(scenePath))
{
    Console.Error.WriteLine($"Scene file not found: {scenePath}");
    return 1;
}

var repo = FindRepoRoot(Directory.GetCurrentDirectory());
var baseUrl = Environment.GetEnvironmentVariable("LLM_BASE_URL") ?? "http://127.0.0.1:8080";
var model = Environment.GetEnvironmentVariable("LLM_MODEL") ?? "local-gguf";

var generation = JsonSerializer.Deserialize<GenerationConfig>(
    await File.ReadAllTextAsync(Path.Combine(repo, "config", "generation.json")),
    JsonOptions()) ?? new();

var systemPrompt = await File.ReadAllTextAsync(Path.Combine(repo, "prompts", "system.md"));
var scenePrompt = await BuildScenePrompt(repo, scenePath);

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

var draftDir = Path.Combine(repo, "drafts");
Directory.CreateDirectory(draftDir);

var sceneName = Path.GetFileNameWithoutExtension(scenePath);
var stamp = DateTime.Now.ToString("yyyyMMdd-HHmmss");
var output = Path.Combine(draftDir, $"{sceneName}-{stamp}.md");

await File.WriteAllTextAsync(output, text.Trim() + Environment.NewLine, Encoding.UTF8);

Console.WriteLine($"Saved: {output}");
return 0;

static async Task<string> BuildScenePrompt(string repo, string scenePath)
{
    var files = new[]
    {
        Path.Combine(repo, "story-bible", "style-guide.md"),
        Path.Combine(repo, "story-bible", "timeline.md"),
        Path.Combine(repo, "story-bible", "relationships.md"),
        Path.Combine(repo, "prompts", "scene-generation.md"),
        Path.GetFullPath(scenePath)
    };

    var sb = new StringBuilder();

    foreach (var file in files.Where(File.Exists))
    {
        sb.AppendLine();
        sb.AppendLine($"--- BEGIN {Path.GetFileName(file)} ---");
        sb.AppendLine(await File.ReadAllTextAsync(file));
        sb.AppendLine($"--- END {Path.GetFileName(file)} ---");
    }

    return sb.ToString();
}

static string FindRepoRoot(string start)
{
    var dir = new DirectoryInfo(start);

    while (dir is not null)
    {
        if (File.Exists(Path.Combine(dir.FullName, "config", "generation.json")))
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
