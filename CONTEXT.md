# ckan/ckan context
> refreshed 2026-10-02 | upstream default: master @ cb8172446c463316efdf12a3e5aa0e0d386adf32

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
- 2026-10-01 sweep: nearly every open "Good for Contribution" issue is already claimed by an OPEN upstream PR (9556<-9566, 9489<-9491, 9493<-9504, 9051<-9056, 9448<-9466, 9118<-9513, 9233<-9486, 9317<-9318) or assigned (9543 Zharktas, 9565 amercader). #9048 is attempted (fork PR #23). Remaining unclaimed: #9290 (featured_orgs hide bug), #9360 (api_token_create user_id; contributor asked to work on it 2026-07-22), #9125 (docs-only).
- #7144 / #7184 (opensource-joe "cannot reproduce" a11y) re-checked 2026-10-01: both already resolved on master (select2 4.x removed the focusser; iframes carry aria-labels) -> not pickable.

## Config-declaration audit (2026-10-01)
Parsed `ckan/config/config_declaration.yaml` against `config.get('ckan.*')` reads in `ckan/**/*.py` (tests excluded). Exactly 3 core reads are undeclared:
- `ckan.jobs.default_list_limit` (read `ckan/logic/action/get.py`; default `ckan.lib.jobs.DEFAULT_JOB_LIST_LIMIT`=200; announced in `changes/8070.feature`/CHANGELOG but never declared) -> real; being fixed this run.
- `ckan.datapusher.formats` (read `ckan/cli/views.py`) -> legacy/extension territory, not declared by design.
- `ckan.preview.image_formats` (read `ckan/cli/views.py`) -> declared by `ckanext/imageview/config_declaration.yaml`, fine when the plugin is enabled.
Method/repro: build a `Declaration`, `load_core_declaration()`, then diff `set(cfg)` against the declared keys exactly like `ckan config undeclared` (`ckan/cli/config.py`).

## Gap ledger (dedupe — READ FIRST, never re-pick)
- `2026-08-05` munge_title_to_name idempotency — pr-opened (fork PR #1, closed) — towncrier 9462.bugfix
- `2026-08-05` natural_number_validator crash — pr-opened (fork PR #2, closed) — towncrier 9460.bugfix
- `2026-08-26` PR #6/#7 kept open (same fixes as #1/#2) — pr-updated (body gate sweep)
- `2026-09-09` issue #9048 (Add resource page shows "Add new resource" button) — pr-opened (fork PR, this run) — mirror midnight-blue `no_new_res` param
- `2026-09-23` trivial-fix pass (fork PR #25) — pr-opened — packed 17 genuine typo/dead-link fixes (file-pinning API docstrings, config/help, SECURITY, 2 dead docs links); fork CI fully green

- `2026-09-24` trivial-fix pass (fork PR #26) — pr-opened — packed 10 genuine typo fixes across 8 files (config option help `resoure`->`resource`; CLI docstrings/comments; IAuthenticator docstring `accpets`->`accepts`; datastore backend+interface `dictonary`/`seach`/`mehtod`/`deferencing`; tracking model docstring `functinoality`); fork CI green (ruff/pyright/pytest/docs/towncrier)
- `2026-10-01` self-found config-declaration gap: `ckan.jobs.default_list_limit` read by `job_list` but never declared — pr-opened (fork PR #30) — declare it in config_declaration.yaml + regression test tying the declared default to `ckan.lib.jobs.DEFAULT_JOB_LIST_LIMIT`; pre-fix `ckan config undeclared` reports the option
- `2026-10-02` issue #8619 (`plugin-info ckan command fails due to named parameters`) — pr-opened (fork PR #31) — `ckan/cli/plugin_info.py::_function_info` builds its parameter list with `inspect.getargspec`, removed in Python 3.11, which raises `ValueError: Function has keyword-only parameters or annotations` for any enabled action/helper with kw-only args or annotations. Fix: walk `inspect.signature` instead, print kw-only params after a `*` marker, drop the old bound-method special case (signature already omits `self`/`cls`); regression test with a plugin action that has a kw-only arg. Re-verified live on upstream master @ cb81724 (line 75 still `getargspec`). Caveat: issue is assigned to contributor kowh-ai since 2025-01-23 (not an org member, 0 comments, no upstream PR in ~21 months) — the assignment is stale, but future runs should treat the spot as claimed unless it stays untouched.
- `2026-10-03` trivial-fix pass (fork PR #32) — pr-opened — packed 10 genuine typo/dead-link fixes across 10 files (+1 towncrier fragment `changes/32.misc`): dead links retargeted in `doc/extensions/translating-extensions.rst` and `contrib/cookiecutter/ckan_extension/{{cookiecutter.project}}/setup.py` (Babel `http://babel.pocoo.org/docs/messages/#...` -> `https://babel.pocoo.org/en/latest/messages.html`) and `doc/extensions/adding-custom-fields.rst` (2 Solr wiki links -> solr.apache.org guide); typos `ah.datset`->`ah.dataset` (`ckanext/activity/templates/snippets/activities/changed_resource.html`, real `UndefinedError` in the stream.html macro dict, render-verified), `funcitons`->`functions` (`ckanext/activity/views.py`), `futher`->`further` (`ckan/lib/jinja_extensions.py`), `incase`->`in case` (`ckan/lib/dictization/model_dictize.py`), `additonal`->`additional` (`ckan/public/base/javascript/module.js`), `overriden`->`overridden` (`ckan/public/base/javascript/modules/confirm-action.js`), `defaut`->`default` (`ckan/public/base/scss/_forms.scss`). Dedupe: every file/string diffed against open fork PR #25 (and #23/#30/#31) so nothing overlaps. CI caveat: `Test (Pytest) / pytest (3)` flaked on reruns on unrelated search-index tests (`test_organization_search_within_org_results`, then `test_name_multiple_results`); upstream master CI is also red at the same SHA — pre-existing flakiness, not caused by the diff; all other checks green.
## Mined gaps (discovered, not yet attempted)
- `2026-09-09` #9048: sidebar "Add new resource" button renders on the Add Resource page itself (regression from #7586). Repro: GET /dataset/{name}/resource/new as editor shows the button. Expected: no link to the page you are already on. Fix: add `no_new_res` param to `ckan/templates/package/snippets/resources.html` (mirror `templates-midnight-blue`), pass `no_new_res=true` from `new_resource.html` + `new_resource_not_draft.html`, add towncrier fragment + controller test. Status: attempted (this run)
- `2026-10-01` `ckan.jobs.default_list_limit` declaration gap (see Config-declaration audit). Status: attempted (fork PR #30)
- `2026-10-01` #9290 "Can't hide featured_orgs on home": `h.get_featured_organizations` -> `featured_group_org(items=config.get('ckan.featured_orgs'), ...)`; when the config list is empty the `items + extras` loop still walks `organization_list`, so the first org is shown anyway. Repro: set `ckan.featured_orgs =` (empty) and load the home page -> an org is still displayed. Fix: return early when `items` is empty (covers `get_featured_groups` too). Status: proposed (backup pick)
- `2026-10-01` #9360 "API Token Schemas": align `api_token_create` to accept `user_id` like `api_token_list` (wardi engaged, wants either param accepted for back-compat). Status: proposed (contributor Vedants06 asked to pick it up 2026-07-22, no PR)
