# ckan/ckan context
> refreshed 2026-09-24 | upstream default: master @ 4ccee8359cf73f93c9150fe22b831d182a85cf03

## Identity & policies
- upstream: ckan/ckan, default branch `master`, primary language Python (Jinja templates), English-first (yes — issues/UI/docs all English)
- CLA/DCO: none (no CLA bot, no DCO requirement)
- AI-assisted PR policy: unstated (no AI policy found in CONTRIBUTING/.github/README; org ckan/.github absent)
- signed commits required: no
- PR template: `.github/PULL_REQUEST_TEMPLATE.md` (Fixes # / Proposed fixes / Features checkboxes)
- external tracker: github
- changelog: towncrier `changes/<PR#>.bugfix` fragments required

## Conventions (verified from merged PRs)
- branch naming: `fix/...`, `chore/...`, `feature/...` (from merged PR headRefNames)
- commit style: Conventional Commits (`fix:`, `chore:`, `build(deps):`) + plain imperative
- CI checks that gate merge: ruff, pyright, pytest (12 splits), cypress, docs, towncrier
- how outside PRs get merged: responsive; maintainers (amercader, wardi, smotornyuk) merge small external fixes; towncrier fragment required

## Maintainer picture
- active maintainers: amercader, wardi, smotornyuk, ThrawnCA (external but active)
- areas actively worked: wardi — datastore, theme (midnight-blue default #9510), pkg_resources; smotornyuk — templates/HTMX/page-layout; amercader — resource sidebar (#9496 merged 2026-08-25)
- avoid: datastore internals, theme migration, template refactor territory

## Issue-area health
- resource/template area: active but small fixes welcome (see #9496 merged, #9048 open)
- open + accepted + unassigned candidates: #9048 (Good for Contribution, Beginner Friendly, open, unclaimed)

## Gap ledger (dedupe — READ FIRST, never re-pick)
- `2026-08-05` munge_title_to_name idempotency — pr-opened (fork PR #1, closed) — towncrier 9462.bugfix
- `2026-08-05` natural_number_validator crash — pr-opened (fork PR #2, closed) — towncrier 9460.bugfix
- `2026-08-26` PR #6/#7 kept open (same fixes as #1/#2) — pr-updated (body gate sweep)
- `2026-09-09` issue #9048 (Add resource page shows "Add new resource" button) — pr-opened (fork PR, this run) — mirror midnight-blue `no_new_res` param

## Mined gaps (discovered, not yet attempted)
- `2026-09-09` #9048: sidebar "Add new resource" button renders on the Add Resource page itself (regression from #7586). Repro: GET /dataset/{name}/resource/new as editor shows the button. Expected: no link to the page you are already on. Fix: add `no_new_res` param to `ckan/templates/package/snippets/resources.html` (mirror `templates-midnight-blue`), pass `no_new_res=true` from `new_resource.html` + `new_resource_not_draft.html`, add towncrier fragment + controller test. Status: attempted (this run)
