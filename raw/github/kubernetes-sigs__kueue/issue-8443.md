# Issue #8443: Kueue does not remove the scheduling gate from Ray’s redis-cleanup jobs

**Summary**: Kueue does not remove the scheduling gate from Ray’s redis-cleanup jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8443

**Last updated**: 2026-03-13T11:05:40Z

---

## Metadata

- **State**: open
- **Author**: [@ns-sundar](https://github.com/ns-sundar)
- **Created**: 2026-01-05T23:11:46Z
- **Updated**: 2026-03-13T11:05:40Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@ns-sundar](https://github.com/ns-sundar)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
In a K8s cluster with Kueue and KubeRay 1.4.0, I deployed a Ray Serve workload via Kueue-managed queue, with the `kueue.x-k8s.io/elastic-job: "true"` annotation and `spec.enableInTreeAutoscaling: true`. When the Ray Serve is being terminated, KubeRay launches a redis-cleanup batch job, which runs a pod to clean up the redis-cleanup config used by the Ray Cluster (RC), which was launched by Ray Serve.
With Kueue, the redis-cleanup pod remains schedule-gated and in Pending state. Some logic in KubeRay eventually kills it but the cleanup never happens.
This is because Kueue does not remove the pod scheduling gate in the redis-cleanup pod. Analysis below.

**What you expected to happen**:
I expected the redis-cleanup pod to run to completion and the RC to exit gracefully. 

**How to reproduce it (as minimally and precisely as possible)**:
- Deploy a Ray Serve CR via a Kueue-managed queue, with the annotation `kueue.x-k8s.io/elastic-job: "true"` and `spec.enableInTreeAutoscaling: true`. 
- Terminate the RayServe deployment.

**Anything else we need to know?**:
Here's my analysis so far:
  - User submits Ray Service CR with above specs.
  - KubeRay's Ray Service Controller creates a Ray Cluster (RC) from the above.
  - Kueue's Ray Cluster webhook intercepts it and sets the pod scheduler gate in the RC's pod spec. 
             schedulingGates:
                 - name: kueue.x-k8s.io/elastic-job
  - When the RC is terminated, KubeRay creates a batch/v1/Job named redis-cleanup, apparently from the head group spec of the RC. This job inherits the scheduling gate.
  - The batch/v1/Job creates a redis-cleanup pod, which also inherits the scheduling gate. This pod's owner reference is the batch/v1/Job, not the Ray Cluster.
  - Kueue reacts but does not remove the scheduling gate from the pod because it is owned by the Job. not the RC. Kueue only looks for pods owned by the RC.

*Candidate solution*: Modify the batch job webhook in Kueue to remove the scheduling gate from the job if (a) it is owned by a ray.io/v1/RayCluster, AND (b) has the label "ray.io/node-type = redis-cleanup" . 

*Rationale for the solution*: Kueue does not to handle autoscaling for the redis-cleanup pod; so, it need not be treated as an elastic job. 

**Environment**:
- Kubernetes version (use `kubectl version`): 
   - Client Version: v1.32.2
   - Kustomize Version: v5.5.0
   - Server Version: v1.32.9-eks-3025e55
- Kueue version (use `git describe --tags --dirty --always`): 0.14.3 
- Cloud provider or hardware configuration: AWS EKS v1.32.9 
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:33:19Z

/priority important-soon
@yaroslava-serdiuk @hiboyang ptal

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-01-07T17:42:42Z

@ns-sundar is testing a fix internally and will create a PR after verifying the fix.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-02-06T08:44:36Z

Could you provide more info on cluster setup, please? 
Could you provide the outcome for `kubectl describe job redis-cleanup` and `kubectl describe pod redis-cleanup`, please?

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-03-13T11:05:36Z

/assign @ns-sundar since he is already working on it

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-13T11:05:40Z

@yaroslava-serdiuk: GitHub didn't allow me to assign the following users: since, he, is, already, working, on, it.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8443#issuecomment-4054318542):

>/assign @ns-sundar since he is already working on it


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
