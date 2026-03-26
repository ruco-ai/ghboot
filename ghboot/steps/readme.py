from pathlib import Path


def run(path: Path) -> None:
    readme = path / "README.md"
    if readme.exists():
        return
    project_name = path.resolve().name
    readme.write_text(f"# {project_name}\n")
