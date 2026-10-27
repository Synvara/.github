# Branch names

Use `<prefix>/<issue-number>-<short-slug>`, for example `fix/42-duplicate-upload`.
The allowed prefixes are `feature`, `fix`, `refactor`, `chore`, and `docs`. The
issue number must be positive with no leading zero. Slugs use lowercase letters,
digits and single hyphens, up to 80 characters. Genuine Dependabot PRs from the
same repository may use its generated `dependabot/` names.

The check validates the name, not issue existence, issue type or permission to
implement. Review still checks scope and approval. GitHub Team can require this
check before merge; it does not prevent creation of a differently named branch.

## Use in another repository

Add a workflow with `pull_request` events (opened, synchronize, reopened, edited,
ready_for_review) and a job calling
`Synvara/.github/.github/workflows/branch-name.yml@<full-reviewed-commit-sha>`.
Set `permissions: {}` for the caller and do not pass secrets. The reusable check
reads GitHub event metadata only; it never checks out or runs PR code.

After the workflow passes, require the exact displayed check name in that
repository's default-branch rules. With a caller job named `branch-policy`, the
check is `branch-policy / branch-name`. Require that repository's own tests too.
Shared issue templates do not automatically install workflows or required checks.

Tests: `python3 -m unittest discover -s tests -v`.
