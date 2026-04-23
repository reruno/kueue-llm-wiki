# Issue #2923: Broken preemption on TFJob with non default `runPolicy.ttlSecondsAfterFinished`

**Summary**: Broken preemption on TFJob with non default `runPolicy.ttlSecondsAfterFinished`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2923

**Last updated**: 2024-08-28T12:29:05Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2024-08-28T11:10:01Z
- **Updated**: 2024-08-28T12:29:05Z
- **Closed**: 2024-08-28T12:29:04Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Preemption of TFJob is not done properly and keep the job in Running condition.
That prevents other jobs to pick up and run.

```yaml
│ Status:                                                                                                                                                        │
│   Conditions:                                                                                                                                                  │
│     Last Transition Time:  2024-08-28T10:21:23Z                                                                                                                │
│     Last Update Time:      2024-08-28T10:21:23Z                                                                                                                │
│     Message:               TFJob default/tensorflow-dist-mnist2 is running.                                                                                    │
│     Reason:                TFJobRunning                                                                                                                        │
│     Status:                True                                                                                                                                │
│     Type:                  Running                                                                                                                             │
│   Replica Statuses:                                                                                                                                            │
│     PS:                                                                                                                                                        │
│       Active:  1                                                                                                                                               │
│     Worker:                                                                                                                                                    │
│       Active:  1                                                                                                                                               │
│   Start Time:  2024-08-28T10:21:22Z  

│   Normal  CreatedWorkload          88s   kubeflow.org/tfjob-kueue-controller  Created Workload: default/tfjob-tensorflow-dist-mnist2-c6ba7                     │
│   Normal  Started                  88s   kubeflow.org/tfjob-kueue-controller  Admitted by clusterQueue cluster-queue                                           │
│   Normal  SuccessfulCreatePod      88s   tfjob-controller                     Created pod: tensorflow-dist-mnist2-worker-0                                     │
│   Normal  SuccessfulCreateService  88s   tfjob-controller                     Created service: tensorflow-dist-mnist2-worker-0                                 │
│   Normal  SuccessfulCreatePod      88s   tfjob-controller                     Created pod: tensorflow-dist-mnist2-ps-0                                         │
│   Normal  SuccessfulCreateService  88s   tfjob-controller                     Created service: tensorflow-dist-mnist2-ps-0                                     │
│   Normal  Stopped                  64s   kubeflow.org/tfjob-kueue-controller  Preempted to accommodate a workload (UID: c8eb139e-b434-41b3-9b30-4292ec91f36a)  │
│ due to prioritization in the ClusterQueue                                                                                                                      │
│   Normal  SuccessfulDeletePod      64s   tfjob-controller                     Deleted pod: tensorflow-dist-mnist2-worker-0                                     │
│   Normal  SuccessfulDeleteService  64s   tfjob-controller                     Deleted service: tensorflow-dist-mnist2-worker-0                                 │
│   Normal  SuccessfulDeletePod      64s   tfjob-controller                     Deleted pod: tensorflow-dist-mnist2-ps-0                                         │
│   Normal  SuccessfulDeleteService  64s   tfjob-controller                     Deleted service: tensorflow-dist-mnist2-ps-0     

```


**What you expected to happen**:
Preempted TFJob status should be Suspended and there should be no active replicas.

```yaml
│   Replica Statuses:                                                                                                                                            │
│     PS:                                                                                                                                                        │
│     Worker:                                                                                                                                                    │
│   Start Time:  2024-08-28T11:12:02Z                                                                                                                            │
│ Events:                                                                                                                                                        │
│   Type    Reason                   Age                From                                 Message                                                             │
│   ----    ------                   ----               ----                                 -------                                                             │
│   Normal  SuccessfulCreatePod      19s                tfjob-controller                     Created pod: tensorflow-dist-mnist2-worker-0                        │
│   Normal  CreatedWorkload          19s                kubeflow.org/tfjob-kueue-controller  Created Workload: default/tfjob-tensorflow-dist-mnist2-c3c39        │
│   Normal  Started                  19s                kubeflow.org/tfjob-kueue-controller  Admitted by clusterQueue cluster-queue                              │
│   Normal  TFJobResumed             19s (x2 over 19s)  tfjob-controller                     TFJob tensorflow-dist-mnist2 is resumed.                            │
│   Normal  SuccessfulCreatePod      19s                tfjob-controller                     Created pod: tensorflow-dist-mnist2-ps-0                            │
│   Normal  SuccessfulCreateService  19s                tfjob-controller                     Created service: tensorflow-dist-mnist2-ps-0                        │
│   Normal  SuccessfulCreateService  19s                tfjob-controller                     Created service: tensorflow-dist-mnist2-worker-0                    │
│   Normal  Stopped                  10s                kubeflow.org/tfjob-kueue-controller  Preempted to accommodate a workload (UID: a8028237-e9b0-4bfb-aa13-9 │
│ 6163d74c7e2) due to prioritization in the ClusterQueue                                                                                                         │
│   Normal  SuccessfulDeletePod      10s                tfjob-controller                     Deleted pod: tensorflow-dist-mnist2-ps-0                            │
│   Normal  SuccessfulDeleteService  10s                tfjob-controller                     Deleted service: tensorflow-dist-mnist2-ps-0                        │
│   Normal  SuccessfulDeletePod      10s                tfjob-controller                     Deleted pod: tensorflow-dist-mnist2-worker-0                        │
│   Normal  SuccessfulDeleteService  10s                tfjob-controller                     Deleted service: tensorflow-dist-mnist2-worker-0                    │
│   Normal  TFJobSuspended           9s (x13 over 19s)  tfjob-controller                     TFJob tensorflow-dist-mnist2 is suspended. 
```

**How to reproduce it (as minimally and precisely as possible)**:

Create TFJob first and any other Job with higher priority as  second  to trigger a preemption.
TFJob has to have the `runPolicy.ttlSecondsAfterFinished` set above 0.


**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.30.0
- Kueue version (use `git describe --tags --dirty --always`): v0.9.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): macOS Sonoma 14.6.1
- Kernel (e.g. `uname -a`): Darwin EPPLGDAW003D 23.6.0 Darwin Kernel Version 23.6.0: Mon Jul 29 21:14:30 PDT 2024; root:xnu-10063.141.2~1/RELEASE_ARM64_T6000 arm64
- Install tools:
- Others: Kubeflow v1.8.0

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-08-28T11:59:31Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-08-28T12:29:05Z

Wrong component, was destined for Kubeflow Training-Operator - https://github.com/kubeflow/training-operator/issues/2239
