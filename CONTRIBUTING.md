# Working on a Synvara project

Start with a GitHub issue that makes four things clear: what is wrong or missing, why it matters, what should change, and how we will know it is done. A few paragraphs and observable acceptance criteria are usually enough.

Use Feature, Bug, Refactor, Chore, Docs, Research, or Epic. Keep the title specific to the outcome. Use an Epic only when several deliverable issues share an outcome; attach those issues as native sub-issues. Small implementation steps belong in a checklist. A user story can describe a feature without adding another hierarchy level.

The issue is the source of truth for intent and specification. Keep implementation plans in linked comments, and evidence in the pull request. Update the existing description as understanding improves instead of appending competing specifications. Technical detail belongs only where it affects a build or review decision.

Use a branch named `<prefix>/<issue-number>-<short-slug>`. Prefixes are `feature`, `fix` (Bug), `refactor`, `chore`, and `docs`. Research normally ends in a decision; open a deliverable issue for resulting code. An Epic has no implementation branch.

Manual and agent implementation use the same issue, branch naming, acceptance criteria, and review. For automated work, a Ready status or label alone is not authorization: the runner must validate an explicit approval for the current intent, specification, and execution mode. An Epic's approval does not approve its children. Research and Epics are excluded from the implementation queue.

Keep changes focused. Verify the acceptance criteria and link the evidence in a pull request. Follow the target repository's instructions and checks. Request review before merging; agents must not infer merge or deployment permission from permission to implement.

Project statuses are Backlog, Defining, Ready, In progress, In review, and Done. Use native assignees, milestones, parent issues, and issue types instead of repeating them as labels or prose.
