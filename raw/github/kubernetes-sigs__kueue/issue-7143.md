# Issue #7143: Manage tools version via dependabot

**Summary**: Manage tools version via dependabot

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7143

**Last updated**: 2025-10-03T14:43:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-10-02T14:12:29Z
- **Updated**: 2025-10-03T14:43:01Z
- **Closed**: 2025-10-03T14:43:01Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I would like to investigate how to manage tool versions via dependabot.

**Why is this needed**:
Currently, we leverage Go tool directive to manage third-party tools like golangci-lint, but we don't manage those versions. So, currently, some of tools versions are already a bit of outdated. For example, our golangci-lint version is v2.2.1 (https://github.com/kubernetes-sigs/kueue/blob/f6b867fd6095af8deec80eb4318548d7de17e18f/hack/internal/tools/go.mod#L227), but the latest version is v2.5.0 (https://github.com/golangci/golangci-lint/releases/tag/v2.5.0)

Go tool directive: https://github.com/kubernetes-sigs/kueue/blob/f6b867fd6095af8deec80eb4318548d7de17e18f/hack/internal/tools/go.mod#L5-L21

Thus, if we can manage tool versions via depandabot (automatically updates), same as the root go.mod, it would be really helpful.

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-02T21:42:34Z

Let's wait for the support first
https://github.com/dependabot/dependabot-core/issues/12050

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-03T13:30:02Z

> Let's wait for the support first [dependabot/dependabot-core#12050](https://github.com/dependabot/dependabot-core/issues/12050)

Thank you for letting us know!
