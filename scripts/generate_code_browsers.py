from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
OUTPUT = ROOT / "docs" / "code-browser"
STARTERS = {
    "nginx": ("02-nginx-static-site", "NGINX static site"),
    "java-spring": ("04-jenkins-java-spring", "Java Spring Boot"),
    "python-fastapi": ("05-jenkins-python-fastapi", "Python FastAPI"),
    "generic-image": ("06-jenkins-generic-image", "Generic image"),
    "node": ("07-jenkins-node", "Node.js"),
    "spinnaker": ("08-spinnaker-kubernetes", "Spinnaker and Kubernetes"),
    "kubeblocks": ("09-kubeblocks-databases", "KubeBlocks data services"),
}

LANGUAGES = {
    "": "groovy",
    ".conf": "nginx",
    ".groovy": "groovy",
    ".java": "java",
    ".js": "javascript",
    ".json": "json",
    ".md": "markdown",
    ".py": "python",
    ".sh": "bash",
    ".toml": "toml",
    ".txt": "text",
    ".xml": "xml",
    ".yml": "yaml",
    ".yaml": "yaml",
}

INCLUDED_SUFFIXES = set(LANGUAGES) | {".dockerfile", ".jenkinsfile"}
INCLUDED_NAMES = {"Dockerfile", "Jenkinsfile"}


def language(path: Path) -> str:
    if path.name in {"Dockerfile", "Jenkinsfile"}:
        return "dockerfile" if path.name == "Dockerfile" else "groovy"
    return LANGUAGES.get(path.suffix.lower(), "text")


def escape_summary(path: Path) -> str:
    return path.as_posix().replace("&", "&amp;").replace("<", "&lt;")


def tree_lines(paths: list[Path]) -> list[str]:
    lines = [f"📁 {paths[0].parts[0]}"]
    previous = set()
    for path in paths:
        parts = path.parts
        for depth, part in enumerate(parts[1:-1], start=1):
            key = (depth, *parts[: depth + 1])
            if key not in previous:
                lines.append(f"{'│   ' * depth}├── 📁 {part}")
                previous.add(key)
        lines.append(f"{'│   ' * (len(parts) - 1)}└── 📄 {parts[-1]}")
    return lines


def generate(starter: str, page_id: str, title: str) -> None:
    source = EXAMPLES / starter
    files = sorted(
        path.relative_to(source)
        for path in source.rglob("*")
        if path.is_file()
        and (path.name in INCLUDED_NAMES or path.suffix.lower() in INCLUDED_SUFFIXES)
    )
    tree = tree_lines([Path(starter) / path for path in files])
    tutorial = f"../{page_id}.md"
    blocks = [
        f"# 💻 Browser IDE: {title}",
        "",
        f"Welcome to the copyable source browser for the [{title} tutorial]({tutorial}). "
        "Expand a file to read it. Select the code block's copy action, then save it using "
        "the displayed path.",
        "",
        "> [!NOTE]\n"
        "> This page requires no JavaScript. If Outline removes HTML details elements, "
        "the file contents remain visible as ordinary Markdown code blocks.",
        "",
        "## Explorer",
        "",
        "```text",
        *tree,
        "```",
        "",
        "## Save the complete starter",
        "",
        f"1. Create a local folder named `{starter}`.",
        "2. Expand each file below.",
        "3. Copy its code block into a file at the exact displayed path.",
        "4. Commit the copied folder as the root of a new application repository.",
        "",
        "A separate whole-folder ZIP/download link can be added later without changing "
        "any of the source shown on this page.",
        "",
        "## Files",
        "",
    ]

    for relative in files:
        content = (source / relative).read_text(encoding="utf-8").rstrip()
        fence = language(relative)
        blocks.extend(
            [
                "<details>",
                f"<summary><strong>📄 {escape_summary(relative)}</strong></summary>",
                "",
                f"**Save as:** `{relative.as_posix()}`",
                "",
                f"```{fence}",
                content,
                "```",
                "",
                "</details>",
                "",
            ]
        )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / f"{starter}.md").write_text("\n".join(blocks), encoding="utf-8")


def main() -> None:
    for starter, (page_id, title) in STARTERS.items():
        generate(starter, page_id, title)


if __name__ == "__main__":
    main()
