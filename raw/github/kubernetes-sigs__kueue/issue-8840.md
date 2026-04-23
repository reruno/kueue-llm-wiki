# Issue #8840: Support implicit borrowing of Cohort-defined resource flavors

**Summary**: Support implicit borrowing of Cohort-defined resource flavors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8840

**Last updated**: 2026-01-28T01:27:03Z

---

## Metadata

- **State**: open
- **Author**: [@jhwagner](https://github.com/jhwagner)
- **Created**: 2026-01-28T01:25:46Z
- **Updated**: 2026-01-28T01:27:03Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like ClusterQueues to borrow resource flavors defined at the Cohort level without requiring explicit `nominalQuota: 0` definitions for each flavor in every ClusterQueue.

Possible approaches:
1. Implicit inheritance - CQs can automatically borrow any flavor defined in their Cohort's `resourceGroups`. No need to re-define them in each CQ
2. Opt in - Flag on CQs, e.g. `inheritCohortFlavors: true`


**Why is this needed**:

Currently, the [Cohort documentation](https://kueue.sigs.k8s.io/docs/concepts/cohort/#configuring-quotas) states:

> In order for a ClusterQueue to borrow resources from its Cohort, it **must** define nominal quota for the desired Resource and Flavor - even if this value is 0.

This results in a lot of duplication across ClusterQueues that want to share resources within a Cohort. Every ClusterQueue must explicitly define every flavor it might want to borrow from.

To illustrate the level of duplication, here's an example scenario. We have a multi-tenant environment where multiple teams may have one or more GPU reservations. We model each reservation as a ResourceFlavor and each team has their own ClusterQueue defining their nominalQuota and lending limit for their reservation.

We have 3 teams: Team A, B, C
- Team A owns `b200-reservation-team-a` (100 GPUs, willing to lend up to 50 GPUs)
- Team B owns `b200-reservation-team-b` (50 GPUs, willing to lend up to 10 GPUs)
- Team C has no GPU reservations, only wants to borrow from cohort

The problem arises when each CQ also needs to re-define every other flavor with `nominalQuota: 0`. Every new team or new flavor/reservation we onboard means N updates across all CQs. Let's say Team D enters with a new reservation (or we simply want to add a new GPU types to the cohort), we now need to add these flavors to all CQs.

I've added a detailed example configuration below:

<details>
<summary><b>Current Behavior (configuration required today)</b></summary>

Every ClusterQueue must define every flavor:

```yaml
# RESOURCE FLAVORS
# Represent different GPU reservations owned by different teams

apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: gpu-reservation-team-a
spec:
  nodeLabels:
    cloud.google.com/reservation-name: "reservation-team-a"
    cloud.google.com/gke-accelerator: "nvidia-b200"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: gpu-reservation-team-b
spec:
  nodeLabels:
    cloud.google.com/reservation-name: "reservation-team-b"
    cloud.google.com/gke-accelerator: "nvidia-b200"

# COHORT
# A cohort all gpu-sharing teams belong to. Does not give additional quota to each flavor.

---
apiVersion: kueue.x-k8s.io/v1beta2
kind: Cohort
metadata:
  name: "gpu-sharing-cohort"
spec:
  resourceGroups:
    - coveredResources: ["nvidia.com/gpu"]
      flavors:
      - name: "gpu-reservation-team-a"
        resources:
        - name: "nvidia.com/gpu"
          nominalQuota: 0
      - name: "gpu-reservation-team-b"
        resources:
        - name: "nvidia.com/gpu"
          nominalQuota: 0

# CLUSTER QUEUES

# Team A's ClusterQueue - "owns" reservation-team-a (100 GPUs, lends 50)
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "team-a-cq"
spec:
  cohortName: "gpu-sharing-cohort"
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    - name: "gpu-reservation-team-a"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 100
        lendingLimit: 50
    # DUPLICATION: Team A must define Team B's flavor just to borrow
    - name: "gpu-reservation-team-b"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 0

# Team B's ClusterQueue - "owns" reservation-team-b (50 GPUs, lends 10)
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "team-b-cq"
spec:
  cohortName: "gpu-sharing-cohort"
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    - name: "gpu-reservation-team-b"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 50
        lendingLimit: 10
    # DUPLICATION: Team B must define Team A's flavor just to borrow
    - name: "gpu-reservation-team-a"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 0

# Team C's ClusterQueue - no GPU reservations, only borrows
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "team-c-cq"
spec:
  cohortName: "gpu-sharing-cohort"
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    # DUPLICATION: Team C must define Team A's flavor just to borrow
    - name: "gpu-reservation-team-a"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 0
    # DUPLICATION: Team C must define Team B's flavor just to borrow
    - name: "gpu-reservation-team-b"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 0
```
</details>

<details>
<summary><b>Desired configuration (with implicit borrowing)</b></summary>

ClusterQueues only define flavors they **own**. Borrowing from Cohort flavors is implicit:

```yaml
# RESOURCE FLAVORS (unchanged)

apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: gpu-reservation-team-a
spec:
  nodeLabels:
    cloud.google.com/reservation-name: "reservation-team-a"
    cloud.google.com/gke-accelerator: "nvidia-b200"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: gpu-reservation-team-b
spec:
  nodeLabels:
    cloud.google.com/reservation-name: "reservation-team-b"
    cloud.google.com/gke-accelerator: "nvidia-b200"

# COHORT
# Defines all flavors available for borrowing within the cohort

---
apiVersion: kueue.x-k8s.io/v1beta2
kind: Cohort
metadata:
  name: "gpu-sharing-cohort"
spec:
  resourceGroups:
    - coveredResources: ["nvidia.com/gpu"]
      flavors:
      - name: "gpu-reservation-team-a"
        resources:
        - name: "nvidia.com/gpu"
          nominalQuota: 0
      - name: "gpu-reservation-team-b"
        resources:
        - name: "nvidia.com/gpu"
          nominalQuota: 0

# CLUSTER QUEUES

# Team A's ClusterQueue - Only define what they "own" (or have nominalQuota to).
# Inherit borrowing from Cohort.
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "team-a-cq"
spec:
  cohortName: "gpu-sharing-cohort"
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    - name: "gpu-reservation-team-a"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 100
        lendingLimit: 50

# Team B's ClusterQueue - Only define what they "own" (or have nominalQuota to)
# Inherit borrowing from Cohort.
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "team-b-cq"
spec:
  cohortName: "gpu-sharing-cohort"
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    - name: "gpu-reservation-team-b"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 50
        lendingLimit: 10

# Team C's ClusterQueue - Has no nominal quota to any flavors, only inherits borrowing from Cohort
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "team-c-cq"
spec:
  cohortName: "gpu-sharing-cohort"
  resourceGroups: []
```
</details>



**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.
