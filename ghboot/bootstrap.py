from pathlib import Path

from .steps import git_init, gitignore, readme, initial_commit, github_remote


def bootstrap(path: str = ".", interactive: bool = False) -> None:
    p = Path(path).resolve()

    if not git_init.run(p, interactive=interactive):
        return

    gitignore.run(p)
    readme.run(p)
    initial_commit.run(p)
    github_remote.run(p, interactive=interactive)
