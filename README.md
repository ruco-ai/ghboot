# ghboot

> From empty folder to GitHub repo in one command.

`ghboot` is a small CLI tool and importable Python library that bootstraps a directory into a fully initialized git repository — with a `.gitignore`, a `README.md`, an initial commit, and a GitHub remote — interactively, in seconds.

---

## What it does

```
ghboot /path/to/my-project
```

1. **`git init`** — prompts before initializing, skips if already a repo
2. **`.gitignore`** — auto-detects your project type (Python, Node, Go, Rust, Ruby, Java) and fetches the matching template from the GitHub API; falls back to a generic template if offline or undetected
3. **`README.md`** — creates a minimal `# project-name` file; skips if one exists
4. **Initial commit** — stages everything and commits with `"Initial commit"`
5. **GitHub remote** — uses the `gh` CLI to create the remote repo, prompt for name/owner/visibility, and push; skips gracefully if `gh` is not installed

---

## Install

```bash
pip install ghboot
```

Or install in editable mode from source:

```bash
git clone https://github.com/you/ghboot
cd ghboot
pip install -e .
```

---

## Usage

### CLI

```bash
# bootstrap the current directory
ghboot

# bootstrap a specific path
ghboot ~/projects/my-new-thing
```

Interactive prompts guide you through each decision point:

```
Initialize git repo here? [Y/n]
Using Python .gitignore template.
Repo name [my-new-thing]:
Owner:
  1. yourname (personal)
  2. your-org
Select [1]:
Visibility [private/public, default: private]:
Created https://github.com/yourname/my-new-thing
```

### Python API

```python
from ghboot import bootstrap

# non-interactive, all defaults
bootstrap(path=".")

# interactive — prompts at each decision point
bootstrap(path=".", interactive=True)
```

---

## Requirements

- Python 3.10+
- `git` available in `PATH`
- [`gh` CLI](https://cli.github.com/) — optional, only needed for the GitHub remote step

---

## What it explicitly does NOT do

- No LLM calls
- No framework-specific config
- No branch management beyond `main`/`master`
- No CI/CD setup

It does one thing and does it well. Anything beyond that is someone else's job.

---

## License

MIT
