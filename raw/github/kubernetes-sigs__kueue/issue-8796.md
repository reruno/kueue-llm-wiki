# Issue #8796: Parameterize which PR to create in hack/releasing/prepare_pull.sh

**Summary**: Parameterize which PR to create in hack/releasing/prepare_pull.sh

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8796

**Last updated**: 2026-01-27T18:14:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-01-26T15:16:37Z
- **Updated**: 2026-01-27T18:14:02Z
- **Closed**: 2026-01-27T18:14:02Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ikchifo](https://github.com/ikchifo)
- **Comments**: 3

## Description

**What would you like to be cleaned**:
The script currently creates both the release-branch and main-branch PR all at once. I would like an option to decide which of these (or both) to create

**Why is this needed**:
The main branch can't be updated until later in the process. E.g. we need to generate security insights first

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-26T15:17:15Z

cc @mimowo @tenzen-y @mbobrovskyi

### Comment by [@ikchifo](https://github.com/ikchifo) — 2026-01-26T16:11:02Z

/assign

I'd like to work on this @gabesaba . Looking at the script, I'll add a `--target` flag (or similar) for options:
- `release` - only create the release branch PR
- `main` - only create the main branch PR
- `all` - create both (current default behavior)

This will allow the release manager to run the release branch PR first, then come back later to create the main branch PR after security insights are generated.

Let me know if you have a preference on the flag name or behavior.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-26T16:23:05Z

Hi @ikchifo. That sounds good to me, thanks for picking this up!
