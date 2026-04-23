# Issue #8987: Can "Cannot specify MultiKueue AdmissionCheck per flavor" constraint be relaxed?

**Summary**: Can "Cannot specify MultiKueue AdmissionCheck per flavor" constraint be relaxed?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8987

**Last updated**: 2026-02-16T10:48:50Z

---

## Metadata

- **State**: open
- **Author**: [@fg91](https://github.com/fg91)
- **Created**: 2026-02-04T14:49:22Z
- **Updated**: 2026-02-16T10:48:50Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 7

## Description

I would like to understand whether we can relax the constraint that the MultiKueue admission check cannot be applied per flavour because applying per flavor would in fact work in my tests.

I would like to achieve the following:

```yaml
kind: ClusterQueue
metadata:
   ...
spec:
  admissionChecksStrategy:
    admissionChecks:
    - name: multi-kueue
      onFlavors:
      - nvidia-l4-flex
  resourceGroups:
  - coveredResources:
    - nvidia.com/gpu
    ...
    flavors:
    - name: nvidia-l4-on-demand
      resources:
      - name: nvidia.com/gpu
        nominalQuota: "1"
      ...
    - name: nvidia-l4-flex
      resources:
      - name: nvidia.com/gpu
        nominalQuota: 10k
      ...
```

If there is still gpu quota in the manager cluster (set to 1 in the example), use it. If there is no more quota, move to MultiKueue.

Currently, when applying this `ClusterQueue`, it becomes pending and won't admit workloads due to this constraint:

```console
Cannot specify MultiKueue AdmissionCheck per flavor
```

However, when modifying the controller code as follows ...

* Remove the check `len(c.perFlavorMultiKueueAdmissionChecks) > 0 ||` [here](https://github.com/kubernetes-sigs/kueue/blob/9c1be20a3d390f398ca3059e545b85010a5a8f88/pkg/cache/scheduler/clusterqueue.go#L217C3-L217C51)
* Remove `if len(c.perFlavorMultiKueueAdmissionChecks) > 0 { messages = append(messages, fmt.Sprintf("Cannot specify MultiKueue AdmissionCheck ...` [here](https://github.com/kubernetes-sigs/kueue/blob/9c1be20a3d390f398ca3059e545b85010a5a8f88/pkg/cache/scheduler/clusterqueue.go#L292)

... the behaviour is exactly as I would expect:

* Quota in manager cluster 1, launch 4 pods, one is admitted in manager, 3 go to multi kueue worker clusters
* Quota in manager cluster 0, launch 4 pods, all go for worker clusters
* ...


I would like to understand whether this constraint might not be necessary anymore, hence a "Clean Up Request" issue, or whether I'm overlooking something else.

If this can in fact be relaxed, I'd be happy to make a PR.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-04T15:33:34Z

Hopefully, but it is not that easy because the 'managedBy' field on a Job is immutable, and this field is injected at the job creation time based on the targeted CQ.

 I can see two approaches:
1. instead of using the managedBy field use scheduling gates which are injected at admission time similarly as we do for TAS scheduling gates
2. support for role sharing of a cluster, so that manager can be one of the workers. In that case we would create a copy of the Job on the manager cluster, with cleared managedBy field, and thus run it locally. 

For 2. I imagine we need some mapping between CQ and Job names, otherwise we will have a conflict that the Job already exists, when attempting to  create the mirror copy of the Job on the same cluster.

Both 1. and 2. are actually some form of role sharing by the manager. 

cc @tenzen-y @olekzabl @kshalot

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-04T15:34:06Z

cc @ichekrygin

### Comment by [@fg91](https://github.com/fg91) — 2026-02-04T17:35:27Z

>  it is not that easy because the 'managedBy' field on a Job is immutable, and this field is injected at the job creation time based on the targeted CQ.

I overlooked this - I was testing this with pods and they of course use scheduling gates so there this issue doesn't appear.

When I try the same with e.g. a RayJobs, the ones the manager cluster has quota for stay unscheduled in the manager cluster because as you said the controller has been disabled for them.

Thanks for explaining what I overlooked!

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-04T19:07:59Z

Nice so it shows that (1.) can work, and we already do it for Pod groups.

Maybe we could make it configurable to use scheduling gates for MultiKueue, then I believe it should be possible. It requires some more discussion, if you need it then I would suggest proposing the topic for wg-batch

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-04T20:37:32Z

Nit on metadata: for me, it feels like a feature request, not a cleanup.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-04T21:33:59Z

For sure
/remove-kind cleanup
/kind feature
/priority important-longterm

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:48:47Z

/area multikueue
