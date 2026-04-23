# Issue #2121: Unclear reason in Admitted condition when using admission checks

**Summary**: Unclear reason in Admitted condition when using admission checks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2121

**Last updated**: 2024-05-08T18:48:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-03T19:22:18Z
- **Updated**: 2024-05-08T18:48:46Z
- **Closed**: 2024-05-08T18:48:46Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently, when a Workload has a quota reservation, but pending admission checks, the reason is `NoChecks`.

I suggest we `UnsatisfiedChecks` or `PendingChecks`. Similarly,
`NoReservationNoChecks` can be renamed to match the decision above.

The only tricky thing is that this is somewhat of a breaking change. Luckily, the strings didn't make it to the api package and both ProvisioningRequest and MultiKueue are alpha features.
I think we can change these.

**Why is this needed**:

`NoChecks` sounds ambiguous. There are checks, but they are not satisfied.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-03T19:22:25Z

@tenzen-y thoughts?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-03T20:07:05Z

Also it looks like the Admitted condition isn't always set:

https://github.com/kubernetes-sigs/kueue/blob/b088365f13ebc37d8e18d997b2a8d356b95c2d09/pkg/scheduler/scheduler.go#L517-L520

I saw this outcome in a real cluster running v0.6.2

```yaml
status:
  admission:
    clusterQueue: dws-cluster-queue
    podSetAssignments:
    - count: 1
      flavors:
        cpu: default-flavor
        memory: default-flavor
        nvidia.com/gpu: default-flavor
      name: main
      resourceUsage:
        cpu: 100m
        memory: 100Mi
        nvidia.com/gpu: "1"
  admissionChecks:
  - lastTransitionTime: "2024-05-03T20:01:59Z"
    message: ""
    name: dws-prov
    state: Pending
  conditions:
  - lastTransitionTime: "2024-05-03T20:01:59Z"
    message: Quota reserved in ClusterQueue dws-cluster-queue
    reason: QuotaReserved
    status: "True"
    type: QuotaReserved
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-03T20:07:18Z

/assign @trasc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-03T20:47:59Z

> @tenzen-y thoughts?

That makes sense. But, I believe that we should notify this change to users via `ACTION REQUIRED` because AdmissionCheck is not an alpha stage feature, although both MultiKueue and the ProvisioningACC are still alpha.
