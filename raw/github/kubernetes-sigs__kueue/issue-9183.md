# Issue #9183: Bump python from 3.12-slim to 3.14-slim in /hack/testing/ray

**Summary**: Bump python from 3.12-slim to 3.14-slim in /hack/testing/ray

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9183

**Last updated**: 2026-03-03T05:54:41Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-12T17:10:23Z
- **Updated**: 2026-03-03T05:54:41Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

To unblock upgrade by dependabot: https://github.com/kubernetes-sigs/kueue/pull/9148

**Why is this needed**:

To enable future upgrades by dependabot

## Discussion

### Comment by [@skools-here](https://github.com/skools-here) — 2026-02-16T17:47:02Z

/unassign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-20T14:23:59Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-03T05:12:07Z

There's still no support in https://github.com/ray-project/ray

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-03T05:17:05Z

There is no support for what? Is it maybe already present on the main btanch, and we are waiting for release? 

If there is some library the kuberay needs to buno then please open an issue in KubeRay and work with the maintainers of the project. cc @vladikkuzn @mbobrovskyi

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-03T05:51:28Z

Python lib ray (which is built upon) currently supports all versions up to python 3.13, we must wait until they release it [here](https://pypi.org/project/ray/#files) for cPython314 interpreter. Kuberay already supports latest version of ray though, so I think we can bump to 3.13-slim

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-03T05:53:51Z

Here's the issue: https://github.com/ray-project/ray/issues/56434
They are actively working on it
