# Issue #3400: POD NodeSelector is not always consistent with their MPIJob node selector

**Summary**: POD NodeSelector is not always consistent with their MPIJob node selector

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3400

**Last updated**: 2026-02-17T12:34:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@GonzaloSaez](https://github.com/GonzaloSaez)
- **Created**: 2024-10-31T12:47:32Z
- **Updated**: 2026-02-17T12:34:40Z
- **Closed**: 2026-02-17T12:34:39Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 21

## Description

**What happened**:

We are launching MPIJobs using a `LocalQueue` with kueue (in particular `cpu-local-queue` from the Yaml fround at the end of the issue). The `ClusterQueue` associated `ResourceFlavor` uses the appropriate `nodeLabels` to target a specific GKE nodepool. We are not setting the MPIJob `NodeSelector` when launching it. When launching the job, kueue sets the correct `NodeSelector` on the MPI job. However, the pods `NodeSelector` is empty. Note that we are not setting the suspend field in the MPIJob, I let kueue do it for us.

**What you expected to happen**:

The MPIJob pods should have the same NodeSelector as the MPIJob. This is also documented in https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/

```
Kueue adds the ResourceFlavor labels to the .nodeSelector of the underlying Workload Pod templates. This occurs if the Workload didn’t specify the ResourceFlavor labels already as part of its nodeSelector.
```

**Environment**:

GKE 1.30 + kueue 0.8.1 + waitForPodsReady=true. These are the kueue resources

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: cpu
spec:
  nodeLabels:
    cloud.google.com/gke-nodepool: e2x4

---

apiVersion: kueue.x-k8s.io/v1beta1
kind: ProvisioningRequestConfig
metadata:
  name: cpu-prov-config
spec:
  provisioningClassName: check-capacity.autoscaling.x-k8s.io

---

apiVersion: kueue.x-k8s.io/v1beta1
kind: AdmissionCheck
metadata:
  name: check-capacity-cpu-prov
spec:
  controllerName: kueue.x-k8s.io/provisioning-request
  parameters:
    apiGroup: kueue.x-k8s.io
    kind: ProvisioningRequestConfig
    name: cpu-prov-config

---

apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cpu-cluster-queue"
spec:
  namespaceSelector: {}
  preemption:
    withinClusterQueue: LowerPriority
  resourceGroups:
    - coveredResources: ["cpu", "memory"]
      flavors:
        - name: "cpu"
          resources:
            - name: "cpu"
              nominalQuota: "12"
            - name: "memory"
              nominalQuota: 52000Gi
  admissionChecks:
    - check-capacity-cpu-prov

---

apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: cpu-local-queue
  namespace: mynamespace
spec:
  clusterQueue: cpu-cluster-queue
```

This can be replicated with the MPIOperator example. The launcher does not have NodeSelector set but the workers do have it.

```
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  name: pi
  namespace: mynamespace
  labels:
    kueue.x-k8s.io/queue-name: cpu-local-queue
spec:
  slotsPerWorker: 1
  runPolicy:
    cleanPodPolicy: None
  sshAuthMountPath: /home/mpiuser/.ssh
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        spec:
          containers:
            - image: mpioperator/mpi-pi:openmpi
              name: mpi-launcher
              securityContext:
                runAsUser: 1000
              command:
                - mpirun
              args:
                - -n
                - "2"
                - /home/mpiuser/pi
              resources:
                limits:
                  cpu: 1
                  memory: 1Gi
    Worker:
      replicas: 2
      template:
        spec:
          containers:
            - image: mpioperator/mpi-pi:openmpi
              name: mpi-worker
              securityContext:
                runAsUser: 1000
              command:
                - /usr/sbin/sshd
              args:
                - -De
                - -f
                - /home/mpiuser/.sshd_config
              resources:
                requests:
                  cpu: "1300m"
                  memory: 3Gi
                limits:
                  cpu: "1300m"
                  memory: 3Gi
```

## Discussion

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2024-10-31T16:31:11Z

I think this happens because the launcher job does not get the nodeselector that kueue is adding to the podset. So only the worker replicas get the correct NodeSelector

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-04T07:45:35Z

@GonzaloSaez thank you for the report - this clearly looks like a bug, does it only happen if you use AdmissionChecks, or is independent of that? Let us also know if you suspect where is the bug, and feel free to propose a fix.

cc @tenzen-y @mbobrovskyi 
who also may have some familiarity / insights where is the issue.

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2024-11-04T08:24:49Z

@mimowo I think https://github.com/kubeflow/mpi-operator/pull/670 sould fix it. That said, there are more open questions regarding NodeSelectors changing after a job is suspended (i.e. the need to change more internals of the MPIOperator launcher job in case the NodeSelector or other details change). Given that this seems related more to mpi-operator than kueue, should we consider closing this?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-04T08:32:58Z

I see, thanks for explaining and driving the fix. I think we may actually consider e2e tests for mpi-job in Kueue to cover such critical aspects of the integration. WDYT @tenzen-y ?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T11:43:53Z

FYI for some more context this also has slack discussion: https://kubernetes.slack.com/archives/C032ZE66A2X/p1730369507818399

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-06T12:17:04Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-06T12:23:24Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-07T12:29:19Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-06T13:19:06Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-06T14:00:42Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-06T14:00:48Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3400#issuecomment-3041688406):

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T16:42:44Z

/reopen

Recently, I have still seeing this problem. Even when the Kueue flavor assigner assigns nodeSelector to MPIJob, those scheduling directives occasionally are not propagated to the Launcher Job.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-08T16:42:49Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3400#issuecomment-3724722922):

>/reopen
>
>Recently, I have still seeing this problem. Even when the Kueue flavor assigner assigns nodeSelector to MPIJob, those scheduling directives occasionally are not propagated to the Launcher Job.
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T16:43:12Z

/remove-lifecycle rotten

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2026-01-09T07:59:09Z

@tenzen-y are you okay with https://github.com/kubeflow/mpi-operator/pull/670 to fix this issue? It won't fix the issue entirely if the job gets rescheduled in a different node after preemption or node failure but I don't know if we fully care about that scenario?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T22:36:28Z

> [@tenzen-y](https://github.com/tenzen-y) are you okay with [kubeflow/mpi-operator#670](https://github.com/kubeflow/mpi-operator/pull/670) to fix this issue? It won't fix the issue entirely if the job gets rescheduled in a different node after preemption or node failure but I don't know if we fully care about that scenario?

@GonzaloSaez Hi, thank you for keeping watching this problem. I summarized the MPI Operator problem in https://github.com/kubeflow/mpi-operator/issues/770.

Let me summarize what happened when I intersected with Kueue at that time.

1. Users: submit MPIJob
2. Kueue: Suspend MPIJob based on quota
3. Kueue: Resume and add nodeSelectors (and more Pod-level annotations) to MPIJob after admission.
4. MPI Operator: Just resume the Launcher batch/v1 Job and ignore PodSpec update as I described in https://github.com/kubeflow/mpi-operator/issues/770
5. Created Launcher Pods via batch/v1 Job has an inaccurate PodSpec.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T22:41:35Z

OTOH, your approach (https://github.com/kubernetes-sigs/kueue/issues/3400) is just postponing the Launcher batch/v1 Job creation to after resume.

As I described in https://github.com/kubeflow/mpi-operator/issues/770, I think the root cause is MPI Operator doesn't update batch/v1 Job PodSpec after MPIJob resume.

So, I would propose to introduce PodSpec update mechanism for resumed batch/v1 Job in https://github.com/kubeflow/mpi-operator/blob/4954c997b2748041f619f1244f8ce883827af2f9/pkg/controller/mpi_job_controller.go#L689-L697 instead of your current approach.

My approach could avoid breaking changes and keep consistency between JobSet and MPIJob behaviors. If we select your change, we probably need to some API field to handle batch/v1 Job creation orders.

@GonzaloSaez If you can handle implementations in the mpi-operator repository, I would appreciate it and be happy to review your PR again.

Otherwise, I can handle that and fix it as soon as possible.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T15:47:54Z

@GonzaloSaez took https://github.com/kubeflow/mpi-operator/issues/770, then is working on https://github.com/kubeflow/mpi-operator/pull/772 (thank you!)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-17T12:34:29Z

This issue is fixed by https://github.com/kubeflow/mpi-operator/pull/772.
@GonzaloSaez Thank you for working this harder. If you see additional issues, please let us know even mpi-operator or kueue side.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-17T12:34:34Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-17T12:34:40Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3400#issuecomment-3914468840):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
