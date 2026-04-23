# Issue #4122: TAS: topology request validation doesn't work for JobSet

**Summary**: TAS: topology request validation doesn't work for JobSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4122

**Last updated**: 2025-02-03T12:18:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-03T08:20:44Z
- **Updated**: 2025-02-03T12:18:59Z
- **Closed**: 2025-02-03T12:18:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:

The topology request validation of the TAS annotations for JobSet does not work, because it is applied at the level of the JobTemplate rather than PodTemplate.

The code reading the TAS annotations is using PodTemplate: https://github.com/kubernetes-sigs/kueue/blob/418091a13236a731b66fab76e2fe79a8635fb44c/pkg/controller/jobs/jobset/jobset_controller.go#L127C94-L129

(note `replicatedJob.Template.Spec.Template.ObjectMeta`).

The code validation the TAS annotations is using JobTemplate: 
https://github.com/kubernetes-sigs/kueue/blob/418091a13236a731b66fab76e2fe79a8635fb44c/pkg/controller/jobs/jobset/jobset_webhook.go#L125

(note `ReplicatedJobs[i].Template.ObjectMeta`)

**What you expected to happen**:

The validation code should be applied at the PodTemplate level.

**How to reproduce it (as minimally and precisely as possible)**:

Create the following JobSet with configuration which should be prohibited:

```yaml
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: example
  labels:
    kueue.x-k8s.io/queue-name: tas-user-queue
spec:
  suspend: true
  successPolicy:
    operator: All
    targetReplicatedJobs:
    - workers
  replicatedJobs:
  - name: leader
    replicas: 1
    template:
      spec:
        completions: 1
        parallelism: 1
        template:
          metadata:
            annotations:
              kueue.x-k8s.io/podset-required-topology: "kubernetes.io/hostname"
              kueue.x-k8s.io/podset-preferred-topology: "kubernetes.io/hostname"
          spec:
            containers:
            - name: leader
              image: bash:latest
              command: ["bash", "-xc", "sleep 10000"]
              resources:
                limits:
                  cpu: 1
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-03T08:20:51Z

cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-02-03T10:07:46Z

/assign
