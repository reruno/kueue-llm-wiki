# Issue #593: workload page link to run a job leads to 404

**Summary**: workload page link to run a job leads to 404

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/593

**Last updated**: 2023-02-26T15:50:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@moficodes](https://github.com/moficodes)
- **Created**: 2023-02-24T22:37:08Z
- **Updated**: 2023-02-26T15:50:20Z
- **Closed**: 2023-02-26T15:50:20Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

https://kueue.sigs.k8s.io/docs/concepts/workload/#whats-next has links to run a job which has the wrong url.

**What you expected to happen**:

Open https://kueue.sigs.k8s.io/docs/tasks/task/ page

**How to reproduce it (as minimally and precisely as possible)**:

Click `Run Jobs`

**Anything else we need to know?**:

**Environment**:
- Kueue docsite
