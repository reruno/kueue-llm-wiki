# Issue #9569: ./hack/releasing/prepare_pull.sh didnt generate helm docs

**Summary**: ./hack/releasing/prepare_pull.sh didnt generate helm docs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9569

**Last updated**: 2026-03-13T12:41:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-02-27T11:15:59Z
- **Updated**: 2026-03-13T12:41:38Z
- **Closed**: 2026-03-13T12:41:38Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 3

## Description

**What would you like to be cleaned**:
generate-helm-docs target should be included

**Why is this needed**:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-27T11:25:04Z

cc @mbobrovskyi @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T12:04:02Z

/assign @tenzen-y 
who is already looking into this. We found that the dependency is the wrong way. The idea to fix is to call `$(MAKE) generate-helm-docs` as the last step of `prepare-release-branch`. I don't see any reason why `generate-helm-docs` would depend on release-branch generation.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-13T12:07:51Z

cc: @vladikkuzn
