import { globSync, readFileSync } from "node:fs";
import { lint } from "markdownlint/sync";
import { minimatch } from "minimatch";

// Keep the existing rules, ignores, and file-specific exceptions while avoiding
// the CLI's unpatched braces dependency.
const settings = JSON.parse(readFileSync(".markdownlint-cli2.jsonc", "utf8"));
const files = Array.from(globSync("**/*.md", {
  exclude: settings.ignores,
})).sort();
let errors = 0;
for (const file of files) {
  let config = { ...settings.config };
  for (const override of settings.overrides ?? []) {
    if (override.filter.some((pattern) => minimatch(file, pattern))) {
      config = override.combine === "merge"
        ? { ...config, ...override.config }
        : { ...override.config };
    }
  }
  const result = lint({ files: [file], config });
  errors += result[file].length;
  for (const error of result[file]) {
    console.error(`${file}:${error.lineNumber} ${error.ruleNames.join("/")} ${error.ruleDescription}${error.errorDetail ? ` [${error.errorDetail}]` : ""}`);
  }
}
console.log(`Linted ${files.length} Markdown files; ${errors} errors.`);
process.exitCode = errors ? 1 : 0;
