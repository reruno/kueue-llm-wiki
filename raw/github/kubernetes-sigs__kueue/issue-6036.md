# Issue #6036: Multikueue for local KIND development automate setting up: AdmissionCheck, MultiKueueConfig, MultiKueueConfig

**Summary**: Multikueue for local KIND development automate setting up: AdmissionCheck, MultiKueueConfig, MultiKueueConfig

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6036

**Last updated**: 2026-04-18T09:13:59Z

---

## Metadata

- **State**: open
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-07-18T23:00:25Z
- **Updated**: 2026-04-18T09:13:59Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`, `lifecycle/rotten`, `area/multikueue`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I want to be able to run 1 command that sets up a local KIND multikueue configuration and seeds the AdmissionCheck, MultiKueueConfig, MultiKueueConfig  for the worker clusters for me. 

Today if I run something like: `make kind-image-build test-multikueue-e2e E2E_RUN_ONLY_ENV=true PLATFORMS=linux/arm64` I still need to manually setup the relevant configuration.

**Why is this needed**:
Development speed for MultiKueue. I want to just be able to apply workloads to the manager cluster without doing the rest of the setup.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-07-18T23:02:41Z

/assign

Initial idea is to create a separate make command that borrows most of the e2e setup, but just doesn't run E2E tests so that it doesn't interfere with the blank multikueue clusters needed for e2e. (I see that the e2e tests explicitly test things like applying the admission checks, etc.)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-16T23:22:03Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-16T00:21:12Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:46:42Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:47:21Z

I proposed some generic solution which would help here: https://github.com/kubernetes-sigs/kueue/issues/8093

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:25:58Z

/area multikueue
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:25Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T09:13:54Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/
