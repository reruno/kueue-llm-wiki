# Issue #5711: resourceflavor taints for RayJobs should account for submitter Job Pod

**Summary**: resourceflavor taints for RayJobs should account for submitter Job Pod

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5711

**Last updated**: 2025-11-22T04:02:22Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@j4ckstraw](https://github.com/j4ckstraw)
- **Created**: 2025-06-23T09:30:42Z
- **Updated**: 2025-11-22T04:02:22Z
- **Closed**: 2025-11-22T04:02:21Z
- **Labels**: `kind/support`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->



**What happened**:
I want to test default local queue function as in https://kueue.sigs.k8s.io/docs/tasks/manage/enforce_job_management/setup_default_local_queue/


I run rayjob according to https://docs.ray.io/en/master/cluster/kubernetes/k8s-ecosystem/kueue.html#step-4-gang-scheduling-with-kueue tutorial.

but submitter pod do not scheduled on given resourceflavor node.



related https://github.com/kubernetes-sigs/kueue/issues/1434

**What you expected to happen**:
only test-worker4 match the test resourceflavor which has label instance=test, and taint instance=test:NoSchedule.
expect all rayjob pods run on test-worker4, but rayjob-sample-l58qx-bbdcq(submitter) did not.

**How to reproduce it (as minimally and precisely as possible)**:

```bash
cat > kueue-config.yaml <<EOF
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "test"
spec:
  nodeLabels:
    instance: "test"
  tolerations:
  - key: "instance"
    operator: "Equal"
    value: "test"
    effect: "NoSchedule"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cq-test"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Any
    withinClusterQueue: Never
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "test"
      resources:
      - name: "cpu"
        nominalQuota: 24
      - name: "memory"
        nominalQuota: 30Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "default"
spec:
  clusterQueue: "cq-test"
EOF

kubectl create -f kueue-config.yaml

kubectl create -f https://raw.githubusercontent.com/ray-project/kuberay/master/ray-operator/config/samples/ray-job.kueue-toy-sample.yaml


k get pod -owide
NAME                                                            READY   STATUS    RESTARTS   AGE   IP            NODE           NOMINATED NODE   READINESS GATES
**rayjob-sample-l58qx-bbdcq                                       1/1     Running   0          9s    10.244.1.15   test-worker    <none>           <none>**
rayjob-sample-l58qx-raycluster-28rzk-head-8mkd5                 1/1     Running   0          35s   10.244.2.24   test-worker4   <none>           <none>
rayjob-sample-l58qx-raycluster-28rzk-small-group-worker-7nq7v   1/1     Running   0          35s   10.244.2.25   test-worker4   <none>           <none>

```
**Anything else we need to know?**:
workload  detail
```bash
k get workload rayjob-rayjob-sample-l58qx-52ced -oyaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  creationTimestamp: "2025-06-23T09:17:00Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  generation: 1
  labels:
    kueue.x-k8s.io/job-uid: 9f5410ee-b964-45b2-9679-3df212bbec51
  name: rayjob-rayjob-sample-l58qx-52ced
  namespace: default
  ownerReferences:
  - apiVersion: ray.io/v1
    blockOwnerDeletion: true
    controller: true
    kind: RayJob
    name: rayjob-sample-l58qx
    uid: 9f5410ee-b964-45b2-9679-3df212bbec51
  resourceVersion: "7470284"
  uid: fd8089fc-43e3-4fd1-a4db-f6b214df8fb8
spec:
  active: true
  podSets:
  - count: 1
    name: head
    template:
      metadata: {}
      spec:
        containers:
        - image: rayproject/ray:2.46.0
          name: ray-head
          ports:
          - containerPort: 6379
            name: gcs-server
            protocol: TCP
          - containerPort: 8265
            name: dashboard
            protocol: TCP
          - containerPort: 10001
            name: client
            protocol: TCP
          resources:
            limits:
              cpu: "1"
              memory: 2Gi
            requests:
              cpu: "1"
              memory: 2Gi
  - count: 1
    name: small-group
    template:
      metadata: {}
      spec:
        containers:
        - image: rayproject/ray:2.46.0
          name: ray-worker
          resources:
            limits:
              cpu: "1"
              memory: 2Gi
            requests:
              cpu: "1"
              memory: 2Gi
  - count: 1
    name: submitter
    template:
      metadata: {}
      spec:
        containers:
        - image: rayproject/ray:2.46.0
          name: ray-job-submitter
          resources:
            limits:
              cpu: "1"
              memory: 1Gi
            requests:
              cpu: 500m
              memory: 200Mi
        restartPolicy: Never
  priority: 0
  priorityClassSource: ""
  queueName: default
status:
  admission:
    clusterQueue: cq-test
    podSetAssignments:
    - count: 1
      flavors:
        cpu: test
        memory: test
      name: head
      resourceUsage:
        cpu: "1"
        memory: 2Gi
    - count: 1
      flavors:
        cpu: test
        memory: test
      name: small-group
      resourceUsage:
        cpu: "1"
        memory: 2Gi
    - count: 1
      flavors:
        cpu: test
        memory: test
      name: submitter
      resourceUsage:
        cpu: 500m
        memory: 200Mi
  conditions:
  - lastTransitionTime: "2025-06-23T09:17:00Z"
    message: Quota reserved in ClusterQueue cq-test
    observedGeneration: 1
    reason: QuotaReserved
    status: "True"
    type: QuotaReserved
  - lastTransitionTime: "2025-06-23T09:17:00Z"
    message: The workload is admitted
    observedGeneration: 1
    reason: Admitted
    status: "True"
    type: Admitted
```

local queue default detail
```bash
$ k get lq default  -oyaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  creationTimestamp: "2025-06-23T09:12:27Z"
  generation: 1
  name: default
  namespace: default
  resourceVersion: "7470323"
  uid: 5c9238c8-5063-456b-b044-a238fb9c0af3
spec:
  clusterQueue: cq-test
  stopPolicy: None
status:
  admittedWorkloads: 1
  conditions:
  - lastTransitionTime: "2025-06-23T09:12:27Z"
    message: Can submit new workloads to localQueue
    observedGeneration: 1
    reason: Ready
    status: "True"
    type: Active
  flavorUsage:
  - name: test
    resources:
    - name: cpu
      total: 2500m
    - name: memory
      total: 4296Mi
  flavors:
  - name: test
    nodeLabels:
      instance: test
    resources:
    - cpu
    - memory
  flavorsReservation:
  - name: test
    resources:
    - name: cpu
      total: 2500m
    - name: memory
      total: 4296Mi
  pendingWorkloads: 0
  reservingWorkloads: 1
```

**Environment**:
- Kubernetes version (use `kubectl version`): kind with kubernetes 1.32.2
- Kueue version (use `git describe --tags --dirty --always`): 0.12.2
- Kuberay verison: 1.4.0
`helm -n kuberay-operator install kuberay-operator --create-namespace kuberay/kuberay-operator --version 1.4.0`
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): 
```bash
$ cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04.2 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.2 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
```
- Kernel (e.g. `uname -a`):
```bash
$ uname -a
Linux joey 6.11.0-26-generic #26~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Apr 17 19:20:47 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```
- Install tools:
- Others:

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-21T10:19:48Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-22T14:02:45Z

Thank you for creating this issue.
It looks like your ResourceFlavor is not correct for your case.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "test"
spec:
  nodeLabels:
    instance: "test"                       // <- this one
  tolerations:
  - key: "instance"                      // <- this one
    operator: "Equal"
    value: "test"
    effect: "NoSchedule"
```

As you can see in https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/#resourceflavor-taints-for-user-selective-scheduling, if you specify the same key / value in nodeLabels and tolerations, the key / value are not considered by Kueue admission:

> For Kueue to [admit](https://kueue.sigs.k8s.io/docs/concepts/#admission) a Workload to use the ResourceFlavor, the PodSpecs in the Workload should have a toleration for it. On the other hand, when the ResourceFlavor has also set the matching tolerations in .spec.tolerations, then the taints are not considered during [admission](https://kueue.sigs.k8s.io/docs/concepts/#admission). As opposed to the behavior for [ResourceFlavor tolerations for automatic scheduling](https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/#ResourceFlavor-tolerations-for-automatic-scheduling), Kueue does not add tolerations for the flavor taints.

/remove-kind bug
/kind support

### Comment by [@j4ckstraw](https://github.com/j4ckstraw) — 2025-09-23T03:19:13Z

@tenzen-y Thank you for your reply. I change the resourceflavor as follow, the result remains the same.
```
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "test"
spec:
  nodeLabels:
    instance: "spot"
  tolerations:
  - key: "spot-taint"
    operator: "Exists"
    effect: "NoSchedule"
```

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-23T03:33:56Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-22T04:02:16Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-22T04:02:22Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5711#issuecomment-3565531699):

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
