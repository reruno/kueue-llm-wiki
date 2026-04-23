# Issue #9649: FailureRecovery: Pod deletion gets stuck even if FailureRecovery is used

**Summary**: FailureRecovery: Pod deletion gets stuck even if FailureRecovery is used

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9649

**Last updated**: 2026-03-04T12:00:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-03T10:57:24Z
- **Updated**: 2026-03-04T12:00:22Z
- **Closed**: 2026-03-04T12:00:22Z
- **Labels**: `kind/bug`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 1

## Description

**What happened**:

We have a case when Pod FailureRecovery is not helping, and Pod deletion is stuck. This is the order of events:

1. kubelet is disabled (eg. node crashed)
2. Job controller sends a graceful Delete to the Pod
3. Kueue's FailureRecovery controller sets status.phase=Failed
Issue: the Pod remains on the API server indefinitely. 

In particular, this blocks deletion of the Job in cascade=foreground mode which is used by JobSet: https://github.com/kubernetes-sigs/jobset/blob/e38bc265102d7dd9a68de38ff909246e261d479d/pkg/controllers/jobset_controller.go#L695-L703

**What you expected to happen**:

I expect the FailureRecovery controller to handle the Pod in such a way that the Job's deletion with the cascade=foreground mode not to be blocked by such a Pod.

I think force deleting the Pod is reasonable, and this is what the k8s GC controller is doing: https://github.com/kubernetes/kubernetes/blob/master/pkg/controller/podgc/gc_controller.go#L365

**How to reproduce it (as minimally and precisely as possible)**:

1. setup a kind cluster with 2 nodes
2. create a Job like this:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 1
  completions: 1
  podReplacementPolicy: Failed # Replace pods only if they are terminated
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/safe-to-forcefully-terminate: "true" # Opt-in to failure recovery
    spec:
      affinity:
        podAntiAffinity:
          # Schedule on a different node than kueue-controller-manager
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 1
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app.kubernetes.io/name
                  operator: In
                  values:
                  - kueue
              topologyKey: kubernetes.io/hostname
              namespaceSelector: {}
      containers:
      - name: dummy-job
        image: registry.k8s.io/e2e-test-images/agnhost:2.53
        command: [ "/bin/sh" ]
        args: [ "-c", "sleep 300" ]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
3. stop kubelet on the node by `docker exec -it kind-worker systemctl stop kubelet`
4. delete manually the Pod, by `kubectl delete pod/<pod name>`
5. delete the Job with `kubectl delete job/<job-name> --cascade=foreground` 
Issue: the job deletion is blocked on the Pod's deletion.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-03T10:58:02Z

/assign @kshalot 
Who is already working on the fix
