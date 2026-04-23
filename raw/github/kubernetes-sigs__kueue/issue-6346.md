# Issue #6346: In Kubeviz, only shows the cohort of spec.cohort in clusterqueue.

**Summary**: In Kubeviz, only shows the cohort of spec.cohort in clusterqueue.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6346

**Last updated**: 2026-03-06T17:16:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@samzong](https://github.com/samzong)
- **Created**: 2025-08-01T07:24:49Z
- **Updated**: 2026-03-06T17:16:21Z
- **Closed**: 2026-03-06T17:16:21Z
- **Labels**: `kind/bug`, `help wanted`, `area/dashboard`
- **Assignees**: [@samzong](https://github.com/samzong)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**: 
In the kubeviz, the Cohorts tab only shows the cohort of spec.cohort referenced in the ClusterQueue?

**What you expected to happen**: 
Show all cohorts whether used or not

**How to reproduce it (as minimally and precisely as possible)**:

1. create a cohort
2. don't reference in any clusterqueue.
3. You will not see it on the page.

**Anything else we need to know?**:

https://github.com/kubernetes-sigs/kueue/blob/2f6b1607d486e5ce95774df83bd2f1edf1b3caa0/cmd/kueueviz/backend/handlers/cohorts.go#L44C1-L97C2


**Environment**:
- Kubernetes version (use `kubectl version`):  v1.33.1
- Kueue version (use `git describe --tags --dirty --always`): v0.13
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-01T12:22:58Z

/area dashboard

cc @akram @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-02T00:06:59Z

I wonder if this is because Cohorts used to be on the cluster queue and now they are a CRD. I think while Cohorts were alpha we didn’t support the Cohort CRD.

Maybe we should fetch cohorts and list those instead of CQ if the intention is to list all cohorts?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-02T00:07:08Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-02T00:07:10Z

@kannon92: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6346):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@samzong](https://github.com/samzong) — 2025-08-02T14:56:27Z

For now, cohort in the beta, I think it's can be considered to display all by default.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-02T15:22:06Z

I agree. Would you like to propose a patch?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-02T15:24:09Z

https://github.com/kubernetes-sigs/kueue/issues/5667

This may be a duplicate actually.

### Comment by [@samzong](https://github.com/samzong) — 2025-08-02T15:26:42Z

@kannon92 Ok, I'm very willing to do this.

In fact, I have already optimized this issue locally. Next, I will submit a PR

### Comment by [@samzong](https://github.com/samzong) — 2025-08-02T15:26:54Z

/assign @samzong
