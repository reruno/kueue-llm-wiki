# Issue #3062: PRs opened by dependabot for  /hack/internal/tools fail for non-breaking changes

**Summary**: PRs opened by dependabot for  /hack/internal/tools fail for non-breaking changes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3062

**Last updated**: 2024-09-18T16:56:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-16T09:46:22Z
- **Updated**: 2024-09-18T16:56:47Z
- **Closed**: 2024-09-18T16:56:46Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

PRs opened by dependabot should not be failing, unless for breaking changes in the libraries. In our case they are failing for non-breaking changes. Examples:
- https://github.com/kubernetes-sigs/kueue/pull/3060
- https://github.com/kubernetes-sigs/kueue/pull/3061

Most often they fail on `pull-kueue-verify-main` because the bump is inconsitent. We bump in `/hack/internal/tools`, but not at the root.

A research of potential solutions is welcome. One idea is not to depend on the top-level dir in `/hack/internal/tools` by replace (which is not recognized by dependabot: https://github.com/kubernetes-sigs/kueue/blob/669d73d40e058c237c3ff3f8b820b75b1dc63a08/hack/internal/tools/go.mod#L25).

**Why is this needed**:

The PRs opened by dependabot still require manual chore, more than needed.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-16T09:46:43Z

/cc @alculquicondor @tenzen-y @mbobrovskyi @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-16T10:04:53Z

The https://github.com/kubernetes-sigs/kueue/blob/669d73d40e058c237c3ff3f8b820b75b1dc63a08/hack/internal/tools/go.mod#L25
depends only for `hack/internal/tools/kueuectl-docs`. So I think moving [kueuectl-docs](https://github.com/kubernetes-sigs/kueue/tree/main/hack/internal/tools/kueuectl-docs) to `cmd/kueuectl-docs` and using for it root `go.mod` dependencies should resolve this problem.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-09-16T11:01:39Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-17T12:41:08Z

As an alternative, I'm wondering if we can put all directories in a single dependabot directries field.

https://github.com/kubernetes-sigs/kueue/blob/ac77deaf14fab5955dab42f6c8196b860c9ebcbd/.github/dependabot.yml#L6-L9

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-17T12:43:10Z

The problem with "/" and "/hack/internal/tools"  that we already have it together.
