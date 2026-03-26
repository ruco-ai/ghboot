import urllib.request
import urllib.error
import json
from pathlib import Path

DETECT_MAP = {
    "Python": ["*.py", "requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
    "Node": ["package.json", "node_modules"],
    "Go": ["go.mod", "go.sum", "*.go"],
    "Rust": ["Cargo.toml", "Cargo.lock"],
    "Ruby": ["Gemfile", "*.rb"],
    "Java": ["pom.xml", "build.gradle", "*.java"],
}

FALLBACK = """\
# Fallback .gitignore
.DS_Store
*.swp
*.swo
*~
.env
"""


def detect_project_type(path: Path) -> str | None:
    names = {f.name for f in path.iterdir() if f.is_file()}
    names |= {f.suffix for f in path.iterdir() if f.is_file()}
    for lang, indicators in DETECT_MAP.items():
        if any(indicator in names for indicator in indicators):
            return lang
    return None


def fetch_template(lang: str) -> str | None:
    url = f"https://api.github.com/gitignore/templates/{lang}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("source")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def run(path: Path) -> None:
    gitignore = path / ".gitignore"
    if gitignore.exists():
        return

    lang = detect_project_type(path)
    content = None

    if lang:
        content = fetch_template(lang)
        if content:
            print(f"Using {lang} .gitignore template.")
        else:
            print(f"Could not fetch {lang} template, using fallback.")
    else:
        print("No project type detected, using generic .gitignore.")

    gitignore.write_text(content or FALLBACK)
