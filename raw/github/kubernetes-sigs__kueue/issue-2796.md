# Issue #2796: Support Gang Scheduling for PytorchJob on Kueue

**Summary**: Support Gang Scheduling for PytorchJob on Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2796

**Last updated**: 2025-02-10T16:17:12Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@FWCoder](https://github.com/FWCoder)
- **Created**: 2024-08-07T21:29:16Z
- **Updated**: 2025-02-10T16:17:12Z
- **Closed**: 2025-02-10T16:17:10Z
- **Labels**: `kind/bug`, `triage/needs-information`, `lifecycle/rotten`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When I submitted a PytorchJob that is required 8 GPUs on Master and 8 GPUs on Worker, it was admitted even though there is only 8 GPU available in the Cluster Queue. Both master and worker pods were created but only Master pod can move to `Init` and `Running` states. The Worker Pod is stuck on `Pending`  until the Master pod move to `Completed` state. At that point, the Worker Pod will stuck on `Init` state since it is waiting for the Master pod to come up. (Deadlock Scenario)

This happens with "waitForPodsReady" enable. 

**What you expected to happen**:
Kueue Controller Manager will evaluate the total requested resources between both Master and Workers. It should blocks the job being admitted until there is enough resources in the Cluster Queue. 

**How to reproduce it (as minimally and precisely as possible)**:

Job Details:
```
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  labels:
    kueue.x-k8s.io/queue-name: <LOCAL_QUEUE_NAME>
  name: hello-world-kueue
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      restartPolicy: Never
      template:
        metadata:
          annotations:
            sidecar.istio.io/inject: "false"
        spec:
          containers:
            - command:
                - "sleep"
                - "60"
              image: <PYTORCH_IMAGE>
              imagePullPolicy: Always
              name: pytorch
              resources:
                limits:
                  cpu: "86"
                  memory: 1037Gi
                  nvidia.com/gpu: "8"
                requests:
                  cpu: "86"
                  memory: 1037Gi
                  nvidia.com/gpu: "8"
          securityContext:
            runAsUser: 1000
    Worker:
      replicas: 1
      restartPolicy: Never
      template:
        metadata:
          annotations:
            sidecar.istio.io/inject: "false"
        spec:
          containers:
            - command:
                - "sleep"
                - "10"
              image:<PYTORCH_IMAGE>
              imagePullPolicy: Always
              name: pytorch
              resources:
                limits:
                  cpu: "86"
                  memory: 1037Gi
                  nvidia.com/gpu: "8"
                requests:
                  cpu: "86"
                  memory: 1037Gi
                  nvidia.com/gpu: "8"
          securityContext:
            runAsUser: 1000
  runPolicy:
    ttlSecondsAfterFinished: 604800
```
Create Job:
```
kubectl create -f hello-world-kueue.yaml
```
**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.28
- Kueue version (use `git describe --tags --dirty --always`): 0.6.1
- Cloud provider or hardware configuration: AWS
```[tasklist]
### Tasks
```

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-09-12T06:58:55Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-09-12T14:08:02Z

@FWCoder 
Can you share more on:
* the ClusterQueue configuration
* available nodes - like a list of them with resources
* node status after the job gets admitted

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-09-13T12:34:16Z

Let me explain why it's important.
The total amount of resources available to the clusterQueue on the basis of which the decision is made may match. 
However, it is possible that the node configuration caused the master to "fit" into one node but the worker does not have the same node at its disposal.
In other words, if there are 10 CPUs available in the cluster, the master needs 5 and the worker needs 5, but the nodes configuration is 5, 3, 2, the workload will be allocated.
Thus we need both cluster configuration and nodes setup, if that will prove correct.
Then we could look deeper, but so far I couldn't reproduce the issue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-13T14:33:42Z

/triage needs-information

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-12T15:32:02Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-11T16:12:06Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-10T16:17:06Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-10T16:17:11Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2796#issuecomment-2648558160):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
