# Issue #3737: Action Required: Replace Deprecated gcr.io/kubebuilder/kube-rbac-proxy

**Summary**: Action Required: Replace Deprecated gcr.io/kubebuilder/kube-rbac-proxy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3737

**Last updated**: 2024-12-16T13:14:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-12-04T14:14:14Z
- **Updated**: 2024-12-16T13:14:55Z
- **Closed**: 2024-12-16T13:14:55Z
- **Labels**: `kind/feature`
- **Assignees**: [@kannon92](https://github.com/kannon92), [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

See https://github.com/kubernetes-sigs/kubebuilder/discussions/3907.

TLDR gcr.io/kubebuilder/kube-rbac-proxy is going away early next year.  We patch the kueue deployment with it [here](https://github.com/kubernetes-sigs/kueue/blob/main/config/default/manager_auth_proxy_patch.yaml)

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-12-04T18:03:24Z

/assign

I'm working on https://github.com/kubernetes-sigs/jobset/issues/721 to prove this out and then I can take this work.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T10:12:22Z

It would be great to fix before 0.10, but maybe we can also cherry-pick the fix for 0.10.1. 
cc @PBundyra @mbobrovskyi 
in case you have some ideas what might be fix here, for reference, the slack thread: https://kubernetes.slack.com/archives/CAR30FCJZ/p1733334367510749

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-05T16:34:07Z

/assign
