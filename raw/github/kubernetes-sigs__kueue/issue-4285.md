# Issue #4285: Allow running integration tests in vs-code without specifying PROJECT_DIR

**Summary**: Allow running integration tests in vs-code without specifying PROJECT_DIR

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4285

**Last updated**: 2025-02-18T12:24:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-17T11:34:38Z
- **Updated**: 2025-02-18T12:24:15Z
- **Closed**: 2025-02-18T12:24:15Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 1

## Description

**What would you like to be cleaned**:

Currently to run integration tests in vs-code I need to specify PROJECT_DIR env variable under `go.testEnvVars` in my settings.json.

Maybe we could default the env. variable by walking up the tree of folders until we encounter a folder with `Makefile`, only as a fallback when `PROJECT_DIR` is not specified. On CI this fallback would not be needed because `PROJECT_DIR` is set by the makefile itself.

**Why is this needed**:

For the ease of local debugging and testing in vs-code. This was not required prior to introduction of PROJECT_DIR.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-17T11:34:46Z

/assign @mszadkow
