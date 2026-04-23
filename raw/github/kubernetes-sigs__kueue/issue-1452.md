# Issue #1452: E2E Tests should export kind logs

**Summary**: E2E Tests should export kind logs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1452

**Last updated**: 2023-12-18T17:07:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2023-12-13T22:58:26Z
- **Updated**: 2023-12-18T17:07:31Z
- **Closed**: 2023-12-18T17:07:31Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 0

## Description

Currently, in Kueue, we directly get the logs of the components of a kind cluster. We are missing some logs and Kind provides a better approach for getting logs of the kind control plane (+ kubelet and others that we are missing).

xpost from https://github.com/kubernetes-sigs/jobset/issues/351#issue-2040591348.

In case of Kueue, we could update https://github.com/kubernetes-sigs/kueue/blob/main/hack/e2e-common.sh#L20 to use `kind export logs $ARTIFACTS`.
