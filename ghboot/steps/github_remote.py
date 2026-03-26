import json
import shutil
import subprocess
from pathlib import Path


def _gh(*args) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _remote_set(path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(path), "remote", "get-url", "origin"],
        capture_output=True,
    )
    return result.returncode == 0


def run(path: Path, interactive: bool = True) -> None:
    if not shutil.which("gh"):
        print("gh CLI not found — skipping GitHub remote setup.")
        return

    if _remote_set(path):
        return

    user_json = _gh("api", "user")
    login = json.loads(user_json)["login"]

    orgs_json = _gh("api", "user/orgs", "--paginate", "-q", ".[].login")
    orgs = [o for o in orgs_json.splitlines() if o][:10]

    default_name = path.resolve().name

    if interactive:
        name = input(f"Repo name [{default_name}]: ").strip() or default_name

        owners = [login] + orgs
        print("Owner:")
        for i, owner in enumerate(owners):
            tag = " (personal)" if owner == login else ""
            print(f"  {i + 1}. {owner}{tag}")
        choice = input(f"Select [1]: ").strip()
        try:
            owner = owners[int(choice) - 1] if choice else owners[0]
        except (ValueError, IndexError):
            owner = owners[0]

        vis_input = input("Visibility [private/public, default: private]: ").strip().lower()
        visibility = "public" if vis_input == "public" else "private"
    else:
        name = default_name
        owner = login
        visibility = "private"

    subprocess.run(
        [
            "gh", "repo", "create",
            f"{owner}/{name}",
            f"--{visibility}",
            "--source=.",
            "--push",
        ],
        cwd=str(path),
        check=True,
    )
    print(f"Created https://github.com/{owner}/{name}")
