# Issue #7372: Pods with Terminating cannot be deleted or exited

**Summary**: Pods with Terminating cannot be deleted or exited

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7372

**Last updated**: 2026-04-18T12:16:59Z

---

## Metadata

- **State**: open
- **Author**: [@Panlq](https://github.com/Panlq)
- **Created**: 2025-10-24T01:54:23Z
- **Updated**: 2026-04-18T12:16:59Z
- **Closed**: —
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: Pods with Terminating cannot be deleted or exited

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
For the moment, I don't know what caused it either. Right now, I can't delete it unless I stop the kueue controller-manager pod or the pod webhook.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 
Client Version: v1.33.4
Kustomize Version: v5.6.0
Server Version: v1.28.3-vke.16

- Kueue version (use `git describe --tags --dirty --always`): v0.11.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:


https://github.com/kubernetes-sigs/kueue/issues/6919 @amy 

<img width="1001" height="60" alt="Image" src="https://github.com/user-attachments/assets/dc3d70bb-5841-44f0-8e15-6fe8f3c5d1c8" />

<img width="1006" height="324" alt="Image" src="https://github.com/user-attachments/assets/bf696216-d76a-4b40-9911-f410681407c3" />

```bash
k get deployment -n xxx | grep xx       ⎈ k8s-xxxxxxxx-cluster
Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens.
xxxxx-55                        1/1       1            1           4h36m
```
The last time the deployment was deleted, the pod finalizers were not successfully removed, which caused the pod to remain stuck in the terminating state.

This is a single-replica deployment of mine. In what circumstances would the removal of the finalizer fail? 

There are two workload records of 55. I tried to delete the workload record corresponding to the Terminating pod, but the pod still did not exit automatically


```bash
{"level":"error","ts":"2025-10-23T10:31:24.753195283Z","caller":"controller/controller.go:316","msg":"Reconciler error","controller":"v1_pod","namespace":"media","name":"xxxxxxxxxx-57f9dc6f47-l2rmf","reconcileID":"1a5573bc-5686-4116-b0f2-a2536bc9b510","error":"Pod \"xxxxxxxxxx-57f9dc6f47-l2rmf\" is invalid: spec: Forbidden: pod updates may not change fields other than `spec.containers[*].image`,`spec.initContainers[*].image`,`spec.activeDeadlineSeconds`,`spec.tolerations` (only additions to existing tolerations),`spec.terminationGracePeriodSeconds` (allow it to be set to 1 if it was previously negative)\n  core.PodSpec{\n  \t... // 27 identical fields\n  \tOverhead:                  nil,\n  \tEnableServiceLinks:        &true,\n- \tTopologySpreadConstraints: nil,\n+ \tTopologySpreadConstraints: []core.TopologySpreadConstraint{\n+ \t\t{\n+ \t\t\tMaxSkew:           1,\n+ \t\t\tTopologyKey:       \"topology.kubernetes.io/zone\",\n+ \t\t\tWhenUnsatisfiable: \"ScheduleAnyway\",\n+ \t\t\tLabelSelector:     s\"&LabelSelector{MatchLabels:map[string]string{app: online-dev-cod\"...,\n+ \t\t},\n+ \t\t{\n+ \t\t\tMaxSkew:           1,\n+ \t\t\tTopologyKey:       \"kubernetes.io/hostname\",\n+ \t\t\tWhenUnsatisfiable: \"ScheduleAnyway\",\n+ \t\t\tLabelSelector:     s\"&LabelSelector{MatchLabels:map[string]string{app: online-dev-cod\"...,\n+ \t\t},\n+ \t},\n  \tOS:              nil,\n  \tSchedulingGates: nil,\n  \tResourceClaims:  nil,\n  }\n","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224"}
```

The above is the log of kueue controller-manager

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-10-24T14:42:01Z

Did you still have replicasets running?

### Comment by [@Panlq](https://github.com/Panlq) — 2025-10-24T14:46:43Z

> Did you still have replicasets running?

The scenario in the image example I provided is as follows: the pod from the previous deployment is stuck in the Terminating state. This is because its finalizer was not removed, preventing it from exiting properly.
The ReplicaSet (RS) corresponding to this Terminating pod no longer exists.
The image shows the second newly created deployment. Since both the old and new deployments share the same app-label, the pod that cannot exit (even when force-deleted) interferes with the retrieval of normal pods.

You can identify the difference between the old pod and the new deployment by checking their age values.

### Comment by [@amy](https://github.com/amy) — 2025-10-24T23:14:52Z

When parsing the logging error:
```
-  TopologySpreadConstraints: nil,
+  TopologySpreadConstraints: []core.TopologySpreadConstraint{
+    {
+      MaxSkew:           1,
+      TopologyKey:       "topology.kubernetes.io/zone",
+      WhenUnsatisfiable: "ScheduleAnyway",
+      LabelSelector:     ...
+    },
+    {
+      MaxSkew:           1,
+      TopologyKey:       "kubernetes.io/hostname",
+      WhenUnsatisfiable: "ScheduleAnyway",
+      LabelSelector:     ...
+    },
+  },
```

Looks like something is trying to change immutable fields on the pod spec. Did you change that @Panlq?

### Comment by [@ehorning](https://github.com/ehorning) — 2025-11-20T16:45:23Z

@Panlq are you able to add more details on how to reproduce this issue? I was able to create a kueue-managed deployment and delete pods successfully.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:43:47Z

I consider closing the issue as it seems like user-specific problem: https://github.com/kubernetes-sigs/kueue/issues/7372#issuecomment-3445188344

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:23Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:55Z

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
