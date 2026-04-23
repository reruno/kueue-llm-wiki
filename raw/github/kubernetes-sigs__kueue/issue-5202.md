# Issue #5202: [release-0.10] Flaky E2E Test: TopologyAwareScheduling for JobSet when Creating a JobSet Should place pods based on the ranks-ordering

**Summary**: [release-0.10] Flaky E2E Test: TopologyAwareScheduling for JobSet when Creating a JobSet Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5202

**Last updated**: 2025-08-06T11:31:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-05-08T10:41:20Z
- **Updated**: 2025-08-06T11:31:03Z
- **Closed**: 2025-08-06T11:31:02Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

End To End TAS Suite: kindest/node:v1.32.3: [It] TopologyAwareScheduling for JobSet when Creating a JobSet Should place pods based on the ranks-ordering

```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/jobset_test.go:135 with:
Expected
    <[]v1.Pod | len:4, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-jobset-replicated-job-1-0-1-qx9t6",
                GenerateName: "ranks-jobset-replicated-job-1-0-1-",
                Namespace: "e2e-tas-jobset-cllmk",
                SelfLink: "",
                UID: "a41ca18a-1005-4ffc-a636-7d98e31bacc0",
                ResourceVersion: "2715",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-05-08T09:56:51Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "jobset.sigs.k8s.io/replicatedjob-name": "replicated-job-1",
                    "batch.kubernetes.io/controller-uid": "8a6d2126-e95b-4b71-8c7e-d31028581536",
                    "jobset.sigs.k8s.io/job-global-index": "0",
                    "jobset.sigs.k8s.io/replicatedjob-replicas": "3",
                    "kueue.x-k8s.io/tas": "true",
                    "batch.kubernetes.io/job-name": "ranks-jobset-replicated-job-1-0",
                    "kueue.x-k8s.io/podset": "replicated-job-1",
                    "controller-uid": "8a6d2126-e95b-4b71-8c7e-d31028581536",
                    "jobset.sigs.k8s.io/job-index": "0",
                    "jobset.sigs.k8s.io/jobset-name": "ranks-jobset",
                    "jobset.sigs.k8s.io/restart-attempt": "0",
                    "batch.kubernetes.io/job-completion-index": "1",
                    "job-name": "ranks-jobset-replicated-job-1-0",
                    "jobset.sigs.k8s.io/global-replicas": "3",
                    "jobset.sigs.k8s.io/job-key": "1c87ef58126b6c7bd3178fbab379374a34d37ec4",
                },
                Annotations: {
                    "jobset.sigs.k8s.io/replicatedjob-name": "replicated-job-1",
                    "kueue.x-k8s.io/workload": "jobset-ranks-jobset-b8ed4",
                    "batch.kubernetes.io/job-completion-index": "1",
                    "jobset.sigs.k8s.io/job-global-index": "0",
                    "jobset.sigs.k8s.io/job-index": "0",
                    "jobset.sigs.k8s.io/job-key": "1c87ef58126b6c7bd3178fbab379374a34d37ec4",
                    "jobset.sigs.k8s.io/jobset-name": "ranks-jobset",
                    "jobset.sigs.k8s.io/replicatedjob-replicas": "3",
                    "jobset.sigs.k8s.io/restart-attempt": "0",
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-block",
                    "jobset.sigs.k8s.io/global-replicas": "3",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "ranks-jobset-replicated-job-1-0",
                        UID: "8a6d2126-e95b-4b71-8c7e-d31028581536",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: [
                    "batch.kubernetes.io/job-tracking",
                ],
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-05-08T09:56:51Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:batch.kubernetes.io/job-completion-index\":{},\"f:jobset.sigs.k8s.io/global-replicas\":{},\"f:jobset.sigs.k8s.io/job-global-index\":{},\"f:jobset.sigs.k8s.io/job-index\":{},\"f:jobset.sigs.k8s.io/job-key\":{},\"f:jobset.sigs.k8s.io/jobset-name\":{},\"f:jobset.sigs.k8s.io/replicatedjob-name\":{},\"f:jobset.sigs.k8s.io/replicatedjob-replicas\":{},\"f:jobset.sigs.k8s.io/restart-attempt\":{},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 6 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/jobset_test.go:135 with:
Expected
    <[]v1.Pod | len:4, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "ranks-jobset-replicated-job-1-0-1-qx9t6",
                GenerateName: "ranks-jobset-replicated-job-1-0-1-",
                Namespace: "e2e-tas-jobset-cllmk",
                SelfLink: "",
                UID: "a41ca18a-1005-4ffc-a636-7d98e31bacc0",
                ResourceVersion: "2715",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-05-08T09:56:51Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "jobset.sigs.k8s.io/replicatedjob-name": "replicated-job-1",
                    "batch.kubernetes.io/controller-uid": "8a6d2126-e95b-4b71-8c7e-d31028581536",
                    "jobset.sigs.k8s.io/job-global-index": "0",
                    "jobset.sigs.k8s.io/replicatedjob-replicas": "3",
                    "kueue.x-k8s.io/tas": "true",
                    "batch.kubernetes.io/job-name": "ranks-jobset-replicated-job-1-0",
                    "kueue.x-k8s.io/podset": "replicated-job-1",
                    "controller-uid": "8a6d2126-e95b-4b71-8c7e-d31028581536",
                    "jobset.sigs.k8s.io/job-index": "0",
                    "jobset.sigs.k8s.io/jobset-name": "ranks-jobset",
                    "jobset.sigs.k8s.io/restart-attempt": "0",
                    "batch.kubernetes.io/job-completion-index": "1",
                    "job-name": "ranks-jobset-replicated-job-1-0",
                    "jobset.sigs.k8s.io/global-replicas": "3",
                    "jobset.sigs.k8s.io/job-key": "1c87ef58126b6c7bd3178fbab379374a34d37ec4",
                },
                Annotations: {
                    "jobset.sigs.k8s.io/replicatedjob-name": "replicated-job-1",
                    "kueue.x-k8s.io/workload": "jobset-ranks-jobset-b8ed4",
                    "batch.kubernetes.io/job-completion-index": "1",
                    "jobset.sigs.k8s.io/job-global-index": "0",
                    "jobset.sigs.k8s.io/job-index": "0",
                    "jobset.sigs.k8s.io/job-key": "1c87ef58126b6c7bd3178fbab379374a34d37ec4",
                    "jobset.sigs.k8s.io/jobset-name": "ranks-jobset",
                    "jobset.sigs.k8s.io/replicatedjob-replicas": "3",
                    "jobset.sigs.k8s.io/restart-attempt": "0",
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-block",
                    "jobset.sigs.k8s.io/global-replicas": "3",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "ranks-jobset-replicated-job-1-0",
                        UID: "8a6d2126-e95b-4b71-8c7e-d31028581536",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: [
                    "batch.kubernetes.io/job-tracking",
                ],
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-05-08T09:56:51Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:batch.kubernetes.io/job-completion-index\":{},\"f:jobset.sigs.k8s.io/global-replicas\":{},\"f:jobset.sigs.k8s.io/job-global-index\":{},\"f:jobset.sigs.k8s.io/job-index\":{},\"f:jobset.sigs.k8s.io/job-key\":{},\"f:jobset.sigs.k8s.io/jobset-name\":{},\"f:jobset.sigs.k8s.io/replicatedjob-name\":{},\"f:jobset.sigs.k8s.io/replicatedjob-replicas\":{},\"f:jobset.sigs.k8s.io/restart-attempt\":{},\"f...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 6
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/jobset_test.go:136 @ 05/08/25 09:57:36.384
}
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5200/pull-kueue-test-e2e-tas-release-0-10/1920414770276601856

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-06T11:20:38Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T11:30:58Z

/close
0.10 is no longer supported version. I suspect this flake is already fixed by numerous changes since then, but if not we can reopen the issue if it occurs on a newer version.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-06T11:31:03Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5202#issuecomment-3159780238):

>/close
>0.10 is no longer supported version. I suspect this flake is already fixed by numerous changes since then, but if not we can reopen the issue if it occurs on a newer version. 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
