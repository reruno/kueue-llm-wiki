# Issue #6613: Kueueviz local queue workloads is using invalid field label

**Summary**: Kueueviz local queue workloads is using invalid field label

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6613

**Last updated**: 2026-04-16T10:47:54Z

---

## Metadata

- **State**: open
- **Author**: [@phoenix1712](https://github.com/phoenix1712)
- **Created**: 2025-08-18T22:59:48Z
- **Updated**: 2026-04-16T10:47:54Z
- **Closed**: —
- **Labels**: `kind/bug`, `lifecycle/rotten`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: 
Local Queue details page does not show workloads. The backend pod shows the following error: 
```
2025/08/18 21:47:41 ERROR Error fetching data %v error="error fetching workloads for local queue q-testing-np-2: field label not supported: spec.queueName"
```

**What you expected to happen**:
The local queues page should show the list of admitted workloads.

**How to reproduce it (as minimally and precisely as possible)**:
Simplest way to reproduce the issue is to just use kubectl
```
kubectl get workloads.kueue.x-k8s.io -n <NAMESPACE> --field-selector spec.queueName=<QUEUE_NAME>
```
This would throw the same error as the queueName on workload CRD is not marked selectable. 

**Anything else we need to know?**:
I did some basic digging and selectable fields can be used to index for fields on CRDs. Ref: https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#crd-selectable-fields

Workload CRD might need to be updated. However this would only work for K8s 1.31 and above. 

Ideally if workloads can be filtered by labels, it would be more generic. 

Code link for local queue workload list logic:  https://github.com/kubernetes-sigs/kueue/blame/main/cmd/kueueviz/backend/handlers/local_queue_workloads.go#L40

**Environment**:
- Kubernetes version (use `kubectl version`): 1.32
- Kueue version (use `git describe --tags --dirty --always`): v0.13.1
- Cloud provider or hardware configuration: EKS
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@phoenix1712](https://github.com/phoenix1712) — 2025-08-18T23:16:41Z

After updating Workload CRD to add
```
    selectableFields:
    - jsonPath: .spec.queueName
```

filtering works
```
➜ kubectl get workloads.kueue.x-k8s.io -n testproject --field-selector spec.queueName=q-testing-np-2

NAME                                             QUEUE            RESERVED IN      ADMITTED   FINISHED   AGE
pytorchjob-leviathan-smoke-test-job-high-6ab50   q-testing-np-2   q-testing-np-2   True                  16s
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-19T18:56:09Z

cc @akram @kannon92

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-19T18:56:17Z

/area dashboard

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-17T19:35:14Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T09:49:26Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-17T10:16:36Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-16T10:47:51Z

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
