Proposed spec: ghboot
Package name: ghboot (or git-bootstrap, open to discussion)

Purpose
A small CLI tool + importable library that takes a directory from "empty folder" to "git repo with a GitHub remote, .gitignore, README, and an initial commit" — interactively.

CLI interface

ghboot [PATH]
PATH defaults to .. That's the only argument needed. Everything else is interactive.

Behavior (sequential steps)
1. Git init

If not already a git repo → prompt: Initialize git repo here? [Y/n]
On yes: git init
On no: exit early
2. .gitignore

If .gitignore already exists → skip
Auto-detect project type (Python, Node, Go, Rust, Ruby, Java) from files present
Fetch matching template from GitHub API (api.github.com/gitignore/templates/{name})
Fall back to a minimal generic template if no match or network fails
Write .gitignore
3. README

If README.md already exists → skip
Create a minimal README.md with just the project name (derived from the directory name)
No LLM, no magic — leclair can overwrite this with forge later
4. Initial commit

git add -A
git commit -m "Initial commit"
5. GitHub remote (requires gh CLI)

If gh not available → skip with notice
If remote origin already set → skip
Fetch gh api user for login
Fetch gh api user/orgs for org list (up to 10)
Prompt: repo name (default: dirname)
Prompt: owner (personal or org list, numbered)
Prompt: visibility (private / public, default: private)
Run: gh repo create {owner}/{name} --{visibility} --source=. --push
Python API

from gh_bootstrap import bootstrap

bootstrap(path=".")  # runs all steps non-interactively with defaults
bootstrap(path=".", interactive=True)  # prompts at each decision point
What it explicitly does NOT do
No LLM calls
No framework-specific config (no .leclair/, no agent config)
No branch management beyond main/master
No CI/CD setup
How leclair uses it
leclair init would:

Set up .leclair/ config (its own concern)
Call bootstrap(path=".", interactive=True) — or just depend on the CLI
Optionally run forge to regenerate README with LLM content
Open questions before we commit to this:

Package name — ghboot? git-bootstrap? repo-init? Something else?
README step — minimal template only, or skip entirely and let the caller handle it?
Non-interactive mode — should it accept flags like --name, --owner, --visibility for scripting? Or keep it purely interactive for now?
Where does it live — new repo under your GitHub account? Monorepo alongside leclair?