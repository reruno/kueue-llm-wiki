# Issue #1430: Fail to list APF resources when the Visibility API is turned on

**Summary**: Fail to list APF resources when the Visibility API is turned on

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1430

**Last updated**: 2023-12-11T08:26:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2023-12-08T15:42:35Z
- **Updated**: 2023-12-11T08:26:59Z
- **Closed**: 2023-12-11T08:26:59Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 1

## Description

**What happened**:

The following messages are repeatedly emitted in the operator logs: 

```
W1208 15:30:36.007289       1 reflector.go:535] pkg/mod/k8s.io/client-go@v0.28.4/tools/cache/reflector.go:229: failed to list *v1beta3.PriorityLevelConfiguration: prioritylevelconfigurations.flowcontrol.apiserver.k8s.io is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "prioritylevelconfigurations" in API group "flowcontrol.apiserver.k8s.io" at the cluster scope
E1208 15:30:36.007354       1 reflector.go:147] pkg/mod/k8s.io/client-go@v0.28.4/tools/cache/reflector.go:229: Failed to watch *v1beta3.PriorityLevelConfiguration: failed to list *v1beta3.PriorityLevelConfiguration: prioritylevelconfigurations.flowcontrol.apiserver.k8s.io is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "prioritylevelconfigurations" in API group "flowcontrol.apiserver.k8s.io" at the cluster scope

W1208 15:30:40.237300       1 reflector.go:535] pkg/mod/k8s.io/client-go@v0.28.4/tools/cache/reflector.go:229: failed to list *v1beta3.FlowSchema: flowschemas.flowcontrol.apiserver.k8s.io is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "flowschemas" in API group "flowcontrol.apiserver.k8s.io" at the cluster scope
E1208 15:30:40.237370       1 reflector.go:147] pkg/mod/k8s.io/client-go@v0.28.4/tools/cache/reflector.go:229: Failed to watch *v1beta3.FlowSchema: failed to list *v1beta3.FlowSchema: flowschemas.flowcontrol.apiserver.k8s.io is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "flowschemas" in API group "flowcontrol.apiserver.k8s.io" at the cluster scope
```

**How to reproduce it (as minimally and precisely as possible)**:

Install the Visibility API service and start the operator with `--feature-gates=VisibilityOnDemand=true`.

**Anything else we need to know?**:

APF is enabled by default when creating a generic API server. It could either be disabled, or the required RBAC be added.

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`): `v0.5.0-devel-396-g6d428f3-dirty`

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T15:49:41Z

Thank you for creating this! I also faced this issue in #1422. Then I was thinking of creating similar to this issue :)

/assign
