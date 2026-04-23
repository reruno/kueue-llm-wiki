# Issue #3495: Vendored JobSet does not have Coordinator field in v0.8.0-

**Summary**: Vendored JobSet does not have Coordinator field in v0.8.0-

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3495

**Last updated**: 2024-11-12T08:11:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@avrittrohwer](https://github.com/avrittrohwer)
- **Created**: 2024-11-08T18:15:33Z
- **Updated**: 2024-11-12T08:11:52Z
- **Closed**: 2024-11-12T08:11:50Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Seen in https://github.com/kubernetes-sigs/jobset/issues/701.  When using JobSet and Kueue in the same cluster, Kueue needs to be at v0.9.0+ for the JobSet Coordinator field to not be nilled by the Kueue JobSet mutating webhook.

**What you expected to happen**:

Kueue mutating webhook does not remove valid JobSet fields.

**How to reproduce it (as minimally and precisely as possible)**:

Install kueue v0.8.0 and JobSet v0.7.0 in a cluster.  Create a JobSet with a non-nil Coordinator field.  The Kueue mutating webhook will cause the JobSet to be created with a nil Coordinator field.

**Anything else we need to know?**:

Kueue v0.9.0 is the first version with a copy of jobset API with coordinator field: https://github.com/kubernetes-sigs/kueue/blob/release-0.9/vendor/sigs.k8s.io/jobset/api/jobset/v1alpha2/jobset_types.go

v0.8.0 does not have the field: https://github.com/kubernetes-sigs/kueue/blob/release-0.8/vendor/sigs.k8s.io/jobset/api/jobset/v1alpha2/jobset_types.go

**Environment**:
- Kubernetes version (use `kubectl version`): 1.31
- Kueue version (use `git describe --tags --dirty --always`): v0.8.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T19:08:33Z

0.8.3 should have the fix. ptal https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.3

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2024-11-08T19:38:43Z

> 0.8.3 should have the fix. ptal https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.3

https://github.com/kubernetes-sigs/kueue/blob/v0.8.3/vendor/sigs.k8s.io/jobset/api/jobset/v1alpha2/jobset_types.go#L65 does not have Coordinator field

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T19:44:21Z

right, but if the root cause is that kueue webhook drops unknown field then this is fixed in 0.8.2 by a change to prevent dropping unknown fields; https://github.com/mimowo/kueue/blob/main/CHANGELOG%2FCHANGELOG-0.8.md: 'Prevent job webhooks from dropping fields for newer API fields when Kueue libraries are behind the latest released CRDs. (#3358, @mbobrovskyi)'

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2024-11-08T19:46:14Z

Ah I see

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2024-11-08T19:48:46Z

Updated https://github.com/kubernetes-sigs/jobset/pull/702 with the fixed v0.8.3+ version

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2024-11-08T20:26:32Z

For any other fixed versions please update https://github.com/kubernetes-sigs/jobset/blob/main/site/content/en/docs/concepts/_index.md?plain=1#L204

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-12T08:11:45Z

/close 
I think this issue is no longer actionable. The new JobSet field can be used in 0.8.3+ and 0.9.0+.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-12T08:11:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3495#issuecomment-2469855337):

>/close 
>I think this issue is no longer actionable. The new JobSet field can be used in 0.8.3+ and 0.9.0+.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
