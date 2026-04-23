# Issue #5289: cohort resources are getting over borrowed when multiple cluster queues are borrowing resources

**Summary**: cohort resources are getting over borrowed when multiple cluster queues are borrowing resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5289

**Last updated**: 2025-07-29T12:42:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alaypatel07](https://github.com/alaypatel07)
- **Created**: 2025-05-20T03:09:16Z
- **Updated**: 2025-07-29T12:42:29Z
- **Closed**: 2025-07-29T12:42:29Z
- **Labels**: `kind/support`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
1. A cohort was created for team-ab with 4 cpu and 4GiB memory
2. A cluster queue for team-a with nominal quota of 2 CPU and 2 GiB memory, with cohort of team-ab
3. A cluster queue for team-b with nominal quota of 2 CPU and 2 GiB memory, with cohort of team-ab
4. Two jobs were created in team-a namespace requesting total of 4 CPUs and 4GiB memory. This leads to borrowing from team-b quota
5. A job was created in team-b namespace requesting 4 CPU and 4GiB memory, this workload was admitted

**What you expected to happen**:

I expected the job in team-b to be in pending state because team-b doesnt have enough quota. Instead it was in running state.


**How to reproduce it (as minimally and precisely as possible)**:
1. create a cohort
    ```
    cat <<EOF | k apply -f -
    apiVersion: kueue.x-k8s.io/v1alpha1
    kind: Cohort
    metadata:
      name: team-ab
    spec:
      resourceGroups:
      - coveredResources: ["cpu", "memory"]
        flavors:
          - name: default-flavor
            resources:
              - name: cpu
                nominalQuota: 4  # Total CPU quota in the cohort (2 + 2)
              - name: memory
                nominalQuota: 4Gi  # Total memory quota in the cohort (2Gi + 2Gi)
    ```
2. create team-a, team-b clusterqueue and local queue
    ```
    cat <<EOF | k apply -f -
    apiVersion: kueue.x-k8s.io/v1beta1
    kind: ClusterQueue
    metadata:
      name: "team-a-cq"
    spec:
      namespaceSelector: {} # match all
      cohort: "team-ab"     # Join this cohort for resource sharing
      resourceGroups:
      - coveredResources: ["cpu", "memory"]
        flavors:
        - name: "default-flavor"
          resources:
          - name: "cpu"
            nominalQuota: 2  # Guaranteed quota
          - name: "memory"
            nominalQuota: 2Gi
    ---
    apiVersion: kueue.x-k8s.io/v1beta1
    kind: ClusterQueue
    metadata:
      name: "team-b-cq"
    spec:
      namespaceSelector: {} # match all
      cohort: "team-ab"     # Same cohort for resource sharing
      resourceGroups:
      - coveredResources: ["cpu", "memory"]
        flavors:
        - name: "default-flavor"
          resources:
          - name: "cpu"
            nominalQuota: 2
          - name: "memory"
            nominalQuota: 2Gi
    ---
    apiVersion: kueue.x-k8s.io/v1beta1
    kind: LocalQueue
    metadata:
      name: team-a-queue
      namespace: team-a
    spec:
      clusterQueue: team-a-cq
    ---
    apiVersion: kueue.x-k8s.io/v1beta1
    kind: LocalQueue
    metadata:
      name: team-b-queue
      namespace: team-b
    spec:
      clusterQueue: team-b-cq
    EOF
    ```
3. create team-a workload
    ```
    cat <<EOF | k apply -f -
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: team-a-job-0
      namespace: team-a
      annotations:
        kueue.x-k8s.io/queue-name: team-a-queue
        kueue.x-k8s.io/priority: "10" # Lower priority
    spec:
      parallelism: 1
      completions: 1
      template:
        spec:
          containers:
          - name: worker
            image: busybox
            command: ["sleep", "3600"] # Job runs for 1 hour
            resources:
              requests:
                cpu: "2"     # Using all team-a CPU quota
                memory: "2Gi" # Using all team-a memory quota
          restartPolicy: Never
    ---
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: team-a-job-1
      namespace: team-a
      annotations:
        kueue.x-k8s.io/queue-name: team-a-queue
        kueue.x-k8s.io/priority: "10" # Lower priority
    spec:
      parallelism: 1
      completions: 1
      template:
        spec:
          containers:
          - name: worker
            image: busybox
            command: ["sleep", "3600"] # Job runs for 1 hour
            resources:
              requests:
                cpu: "2"     # borrowing all team-b CPU quota
                memory: "2Gi" # borrowing all team-b memory quota
          restartPolicy: Never
    EOF
    ```
4. create team-b job
    ```
    $ cat <<EOF | k apply -f -
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: team-b-job
      namespace: team-b
      annotations:
        kueue.x-k8s.io/queue-name: team-b-queue
        kueue.x-k8s.io/priority: "10" # Lower priority
    spec:
      parallelism: 1
      completions: 1
      template:
        spec:
          containers:
          - name: worker
            image: busybox
            command: ["sleep", "3600"] # Job runs for 1 hour
            resources:
              requests:
                cpu: "2"     # Using all team-b CPU quota
                memory: "2Gi" # Using all team-b memory quota
          restartPolicy: Never
    ```
5. Check for running jobs
    ```
    $  kubectl get jobs -A
    NAMESPACE   NAME           STATUS    COMPLETIONS   DURATION   AGE
    team-a      team-a-job-0   Running   0/1           75s        75s
    team-a      team-a-job-1   Running   0/1           75s        75s
    team-b      team-b-job     Running   0/1           68s        68s
    ```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
      ```
      $ k version
      Client Version: v1.32.3
      Kustomize Version: v5.5.0
      Server Version: v1.32.0
      ```
- Kueue version (use `git describe --tags --dirty --always`): `v0.11.4`
- Cloud provider or hardware configuration: minikube
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T05:05:50Z

cc @gabesaba ptal

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T08:56:49Z

Hi @alaypatel07, this quota defined at Cohort level is additive: so there is a total of 8CPU/8Gi available in the entire Cohort

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T09:02:05Z

I will update the docs to make this more clear - this is not the first time a user expected this semantic. @alaypatel07, were there any docs in particular which gave you the impression that the resources defined at Cohort level worked in this way?

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2025-05-20T13:41:00Z

@gabesaba I was reading from this doc https://kueue.sigs.k8s.io/docs/concepts/cohort/#configuring-quotas, I dont see it being mentioned anywhere that quotas on cohorts are additive.

Can you please be more clear on what additive means? If there are 4 cluster queues belonging to a cohort and the cohort defines nominalquota of 2 CPU, then in total there will be quota of 10 CPUs, 2 for each clusterqueue?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T14:00:06Z

> [@gabesaba](https://github.com/gabesaba) I was reading from this doc https://kueue.sigs.k8s.io/docs/concepts/cohort/#configuring-quotas, I dont see it being mentioned anywhere that quotas on cohorts are additive.
> 
> Can you please be more clear on what additive means? If there are 4 cluster queues belonging to a cohort and the cohort defines nominalquota of 2 CPU, then in total there will be quota of 10 CPUs, 2 for each clusterqueue?

In that case, there will just be 2CPU quota, assuming that the ClusterQueues do not define any quota. I just meant that the Resources defined at the Cohort level is independent of quotas at ClusterQueue. These numbers may be added up to determine total capacity. E.g.:

**Structure**
- Cohort (1gb memory)
  - CQ (1 CPU, 1gb memory)

**Total Resources Available in Cohort**
- 1CPU, 2gb memory

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2025-05-20T14:11:25Z

Ohh I see, I think I had a different mental model of the system. I assumed that quota needs to be defined at cohort once and then ClusterQueues can take smaller slices of resources from the quota at cohort level. This is clearly not true.

Can you please help put this in documentation? I will be happy to review the doc PR.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-06-16T10:54:28Z

> Can you please help put this in documentation? I will be happy to review the doc PR.

#5659 :)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T05:08:04Z

/remove-kind bug
/kind support

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-24T08:59:01Z

/reopen
To address the comments requesting also API comment improvements in https://github.com/kubernetes-sigs/kueue/pull/5659

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-24T08:59:07Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5289#issuecomment-2999437291):

>/reopen
>To address the comments requesting also API comment improvements in https://github.com/kubernetes-sigs/kueue/pull/5659 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-07-29T11:06:31Z

/assign
