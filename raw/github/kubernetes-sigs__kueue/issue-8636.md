# Issue #8636: TAS: Investigate and fix (if needed) the case when one node is prefix for other nodes in assignment

**Summary**: TAS: Investigate and fix (if needed) the case when one node is prefix for other nodes in assignment

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8636

**Last updated**: 2026-01-19T20:34:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-16T13:29:39Z
- **Updated**: 2026-01-19T20:34:44Z
- **Closed**: 2026-01-19T20:34:43Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to investigate and add an e2e test for the scenario when one node is a prefix of other nodes in the clusters for TAS. 

Example:

```yaml
topologyAssignment:
  levels:
  - kubernetes.io/hostname
  slices:
  - domainCount: 3
    podCounts:
      universal: 1
    valuesPerLevel:
    - individual:
        prefix: kind-worker
        roots:
        - "2"
        - "3"
        - "4"
```
This is example for 3 nodes: `kind-worker2`, `kind-worker3`, `kind-worker4`, and it works well, but in kind we may also have an assignment which has the fourth node `kind-worker`, so then the "root" would need to be empty, but I'm not sure we allow that and handle correctly on all layers.

**Why is this needed**:

To make sure this scenario works, as this naming scheme may happen on kind: https://github.com/kubernetes-sigs/kueue/issues/8635#issuecomment-3759998404

This might be an overlooked corner case when we introduced v1beta2.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T13:30:01Z

cc @tenzen-y @olekzabl

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-01-16T13:32:34Z

/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-01-19T12:48:27Z

For the start, I checked it manually (without writing a test).

On a local kind cluster, I submitted a Job large enough to occupy all `kind-worker*` nodes.
It got admitted successfully, including the `kind-worker` node (the one without any suffix).

Workload's admission status (including `""` as `root`):
<img width="1912" height="1009" alt="Image" src="https://github.com/user-attachments/assets/0cb50411-aebb-4333-8fb1-8050d8d91f47" />

List of running child Pods (including one on `kind-worker`):
<img width="1912" height="1009" alt="Image" src="https://github.com/user-attachments/assets/9e574fcc-dc7b-47fc-992c-ac9e37a2ab2f" />

---

GIven this, I won't treat writing an e2e test for this as urgent.
Please LMK if I still should.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:27:41Z

Thank you @olekzabl for confirming it is working ok 👍 

Actually I now think this e2e test already proves this is working fine: https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/tas/job_test.go#L137-L154

It is just hidden behind the `V1Beta2From` helper, wdyt?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:28:49Z

If this is the case I'm happy to close it (feel free to do so @olekzabl )

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T16:35:42Z

I'm fine with closing this issue as well.
Thank you for confirming that! @olekzabl

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-01-19T20:34:39Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-19T20:34:44Z

@olekzabl: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8636#issuecomment-3770037808):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
