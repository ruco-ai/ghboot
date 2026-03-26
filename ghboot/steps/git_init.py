import subprocess
from pathlib import Path


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def run(path: Path, interactive: bool = True) -> bool:
    """Initialize a git repo. Returns True if we should continue, False to abort."""
    if is_git_repo(path):
        return True

    if interactive:
        answer = input("Initialize git repo here? [Y/n] ").strip().lower()
        if answer in ("n", "no"):
            print("Aborted.")
            return False

    subprocess.run(["git", "init", str(path)], check=True)
    return True
