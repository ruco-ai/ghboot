import sys
from pathlib import Path

from .bootstrap import bootstrap


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "."

    if not Path(path).exists():
        print(f"Error: path '{path}' does not exist.")
        sys.exit(1)

    bootstrap(path=path, interactive=True)


if __name__ == "__main__":
    main()
