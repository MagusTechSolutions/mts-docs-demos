from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
OUTPUT = ROOT / "docs" / "code-browser"
REPOSITORY = "https://github.com/MagusTechSolutions/mts-docs-demos"
DEFAULT_BRANCH = "master"
STARTERS = {
    "nginx": ("17-nginx-static-site", "NGINX static site"),
    "java-spring": ("15-jenkins-java-spring", "Java Spring Boot"),
    "python-fastapi": ("14-jenkins-python-fastapi", "Python FastAPI"),
    "generic-image": ("13-jenkins-generic-image", "Generic image"),
    "node": ("12-jenkins-node", "Node.js"),
    "spinnaker": ("11-spinnaker-kubernetes", "Spinnaker and Kubernetes"),
    "kubeblocks": ("10-kubeblocks-databases", "KubeBlocks data services"),
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


def starter_url(starter: str) -> str:
    return f"{REPOSITORY}/tree/{DEFAULT_BRANCH}/examples/{starter}"


def file_url(starter: str, relative: Path) -> str:
    return (
        f"{REPOSITORY}/blob/{DEFAULT_BRANCH}/examples/"
        f"{starter}/{relative.as_posix()}"
    )


def raw_file_url(starter: str, relative: Path) -> str:
    return (
        f"{REPOSITORY}/raw/refs/heads/{DEFAULT_BRANCH}/examples/"
        f"{starter}/{relative.as_posix()}"
    )


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
        "Expand a file to read or copy it. Each file also includes GitHub view and raw "
        "download links.",
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
        f"[Browse the complete `{starter}` starter on GitHub]({starter_url(starter)}) · "
        f"[Download the repository as a ZIP]({REPOSITORY}/archive/refs/heads/{DEFAULT_BRANCH}.zip)",
        "",
        "## Use the complete starter",
        "",
        f"1. Create a local folder named `{starter}`.",
        "2. Expand and copy each file below, or download it from its raw link.",
        "3. Save it at the exact displayed path.",
        "4. Commit the copied folder as the root of a new application repository.",
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
                f"**Save as:** `{relative.as_posix()}` · "
                f"[View on GitHub]({file_url(starter, relative)}) · "
                f"[Download raw file]({raw_file_url(starter, relative)})",
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
