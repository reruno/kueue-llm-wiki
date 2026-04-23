# Issue #9222: Automate adding kind/* labels to cherry-pick PRs

**Summary**: Automate adding kind/* labels to cherry-pick PRs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9222

**Last updated**: 2026-03-04T16:10:57Z

---

## Metadata

- **State**: open
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-13T13:49:21Z
- **Updated**: 2026-03-04T16:10:57Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Automatically apply kind/ prefixed labels (e.g. kind/bug, kind/feature, kind/cleanup, etc.) to cherry-pick pull requests.

**Why is this needed**:

Cherry-pick PRs currently require manual addition of the appropriate kind/* label(s) by the author or reviewer.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-13T13:49:35Z

/cc @mimowo @tenzen-y @vladikkuzn

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-13T16:43:50Z

I agree with you.
I always manually add labels to cherry-pick PRs 😓 
The Prow cherry-pick plugin might have a configuration to deliver the original PR labels to cherry-pick PRs.

Otherwise, we might need to expand the cherry-pick plugin.
As an alternative short-term solution, we might add GH action to deliver labels. But I would look at the native cherry-pick plugin solution first.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-15T16:31:45Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-19T09:48:24Z

@tenzen-y I've added it to the cherry-pick script. Where can I find "The Prow cherry-pick plugin"?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-20T16:00:27Z

> [@tenzen-y](https://github.com/tenzen-y) I've added it to the cherry-pick script. Where can I find "The Prow cherry-pick plugin"?

Maybe this one https://github.com/kubernetes-sigs/prow/tree/main/cmd/external-plugins/cherrypicker?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-20T16:05:26Z

Probably we need to extend this function https://github.com/kubernetes-sigs/prow/blob/main/cmd/external-plugins/cherrypicker/lib/lib.go#L25-L37.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-04T16:10:56Z

https://github.com/kubernetes-sigs/prow/pull/638
