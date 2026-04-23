# Issue #9477: make test-e2e not parsing GINKGO_ARGS properly

**Summary**: make test-e2e not parsing GINKGO_ARGS properly

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9477

**Last updated**: 2026-03-05T10:28:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-02-25T15:05:49Z
- **Updated**: 2026-03-05T10:28:28Z
- **Closed**: 2026-03-05T10:28:28Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

**What would you like to be cleaned**:

```
E2E_MODE=dev GINKGO_ARGS="--focus='should ensure the eviction'" make test-e2e
```
Results in the following failure:

```
ginkgo run failed
  Malformed arguments - detected a flag after the package liste
    Make sure all flags appear after the Ginkgo subcommand and before your list of
    packages (or './...').
    e.g. 'ginkgo run -p my_package' is valid but `ginkgo -p run my_package` is
    not.
    e.g. 'ginkgo -p -vet="" ./...' is valid but 'ginkgo -p ./... -vet=""' is not
```

LLM claims it is due to inability to parse spaces, and proposes the following solution: https://github.com/kubernetes-sigs/kueue/commit/50986834c7533f8cdfccc881dd6c8cae25929f5e

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-03T04:44:59Z

Cause: GINKGO_ARGS was used unquoted ($GINKGO_ARGS). With:
GINKGO_ARGS="--focus='should ensure the eviction'"
the shell splits on spaces, so ginkgo sees:
--focus='should
ensure
the
eviction'
then --junit-report=..., etc.
then ./test/e2e/...

Fix: Use GINKGO_ARGS as a single argument so the focus string is not split

/assign
