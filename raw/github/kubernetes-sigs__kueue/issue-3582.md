# Issue #3582: [Multi Kueue] Client Connection Failures with removed integrations

**Summary**: [Multi Kueue] Client Connection Failures with removed integrations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3582

**Last updated**: 2024-11-25T10:14:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Bobbins228](https://github.com/Bobbins228)
- **Created**: 2024-11-18T14:45:14Z
- **Updated**: 2024-11-25T10:14:58Z
- **Closed**: 2024-11-25T10:14:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I set up Multi Kueue as per the [documentation](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/).
I removed `"jobset.x-k8s.io/jobset"` from the list of integrations in the kueue-manager-config Config Map as I did not intend on using JobSets. This was included in the application of the Kueue manifests.

After setting up my Multi Kueue environment I ran the example test commands to which I got the following errors:
```
CQ - Active: False Reason: AdmissionCheckInactive Message: Can't admit new workloads: references inactive AdmissionCheck(s): [sample-multikueue].
AC - Active: False Reason: NoUsableClusters Message: Inactive clusters: [multikueue-test-worker1]
MC - Active: False Reason: ClientConnectionFailed Message: no matches for kind "JobSet" in version "jobset.x-k8s.io/v1alpha2"
```

**What you expected to happen**:
I expected that when an integration is disabled in the Kueue manager config it should be reflected in MultiKueue meaning no additional CRDs should have to be installed for Job types the user has no intention on using.

**How to reproduce it (as minimally and precisely as possible)**:
* Setup your Clusters for Multi Kueue. (Ensure JobSet is removed from the list of integrations in the manager Config Map)
* Do not install the JobSet Controller/CRDs
* Remove JobSet Cluster Roles for the multikueue-sa
* Examine your Multi Kueue Cluster CR for the failure message.
 
**Anything else we need to know?**:
This same behaviour would happen if it was the MPI Operator that was not installed. 
See this [Slack thread](https://kubernetes.slack.com/archives/C032ZE66A2X/p1731687654180929) for more info.
**Environment**:
- Kubernetes version (use `kubectl version`): v1.28
- OpenShift version: 4.15.37
- Kueue version (use `git describe --tags --dirty --always`): v0.9.0
- Cloud provider or hardware configuration: AWS
- Install tools: kubectl
- Others:
- MPI Operator: v0.6.0
- KubeFlow Training Operator: v1.8.1

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T14:49:02Z

/assign @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T14:49:16Z

cc @mwielgus @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T14:49:21Z

cc @mbobrovskyi
