# Contributing Guidelines

This document describes how **Team TENSORS** collaborates on the Smart Classroom and Timetable Scheduler backend. External contributions are not accepted.

---

## Team Rules

- Each member works on their assigned module in a dedicated branch.
- Sync with `dev` before starting new work and before opening a pull request.
- Never commit directly to `main` or `dev`. All changes go through a pull request.
- Keep pull requests small and focused on one change.

## Branching Model

| Branch | Purpose |
|--------|---------|
| `main` | Stable, production-ready code only |
| `dev` | Integration branch where finished work is combined and tested |
| `feature/<name>` | New features or modules, for example `feature/auth-module` |
| `fix/<name>` | Bug fixes, for example `fix/timetable-clash-check` |

Use lowercase names with hyphens. Branch from `dev`, and merge back into `dev` through a pull request. `main` is updated from `dev` only when the team agrees a release is stable.

## Daily Workflow

1. Update your local `dev` branch from the remote.
2. Create your branch from `dev`, for example `feature/auth-module`.
3. Make your changes in small, logical commits.
4. Push your branch to `origin`.
5. Open a pull request into `dev` and request a review.
6. Address review comments, then merge once approved.

## Commit Messages

Use a short prefix followed by a clear, imperative summary:

| Prefix | Use for |
|--------|---------|
| `feat:` | A new feature |
| `fix:` | A bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code changes that do not alter behaviour |
| `test:` | Adding or updating tests |
| `chore:` | Dependencies, configuration, tooling |

Example: `feat: add role field to custom user model`

## Django Conventions

- **Migrations:** After changing a model, run `makemigrations` and commit the generated file with your change. Never edit or delete a migration that has been merged.
- **Migration conflicts:** If two branches add migrations to the same app, tell the team before merging so the conflict is resolved deliberately.
- **Dependencies:** If you add or upgrade a package, update `requirements.txt` in the same commit.
- **Secrets:** Never commit `.env`, passwords, or keys. Add any new variable to `.env.example` with a safe placeholder and document it in the README.
- **Apps:** Keep each feature in its own Django app under `src/`, and register it in `INSTALLED_APPS`.

## Pull Request Checklist

Before requesting a review, confirm that:

- [ ] The branch is up to date with `dev`
- [ ] The project runs locally and `python manage.py migrate` succeeds
- [ ] Tests pass with `python manage.py test`, and new logic has tests
- [ ] Migrations are included and no unrelated files are changed
- [ ] `requirements.txt` and `.env.example` are updated if needed
- [ ] The README or other documentation is updated if behaviour changed
- [ ] The pull request description explains what changed and why

At least one team member must review and approve before merging.

## Reporting Issues

- Search existing issues first to avoid duplicates.
- Include clear steps to reproduce the problem, the expected result, and the actual result.
- Attach error logs or screenshots where possible.

## Suggesting Features

Open an issue with the `enhancement` label. Describe the idea, the problem it solves, and a possible approach.
