# Issue #9270: MultiKueue: allow configuring step size in the incremental dispatcher

**Summary**: MultiKueue: allow configuring step size in the incremental dispatcher

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9270

**Last updated**: 2026-02-20T12:52:10Z

---

## Metadata

- **State**: open
- **Author**: [@mpsanj](https://github.com/mpsanj)
- **Created**: 2026-02-16T07:59:57Z
- **Updated**: 2026-02-20T12:52:10Z
- **Closed**: —
- **Labels**: `kind/feature`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 8

## Description

Hi Team,

  Support for priority/weight-based cluster selection in MultiKueue, so that workloads
  are preferentially dispatched to higher-priority worker clusters before falling back
  to lower-priority ones.

  ## Why is this needed?

  Currently, MultiKueue uses a race model — workloads are dispatched to **all** worker
  clusters listed in `MultiKueueConfig.spec.clusters` simultaneously, and the first
  cluster to admit wins. There is no mechanism to express cluster preference or ordering.

  ### Use case

  We run 3 worker clusters across regions (e.g., JP, US, SG) for GPU workloads. We want
  to prefer scheduling on our primary cluster (cheaper/closer), and only overflow to
  secondary and tertiary clusters when the primary lacks resources. 


 ## Proposed solution

  Add a `priority` or `weight` field to `MultiKueueConfig.spec.clusters`:

  ```yaml
  apiVersion: kueue.x-k8s.io/v1beta2
  kind: MultiKueueConfig
  metadata:
    name: multikueue-default
  spec:
    clusters:
      - name: "jp-osa"
        priority: 1        # highest priority, try first
      - name: "us-002"
        priority: 2        # try if jp-osa is full
      - name: "sg-001"
        priority: 3        # last resort
```

Expected behavior with ordered dispatch

  1. Submit workload to the highest-priority cluster only
  2. If that cluster's ClusterQueue cannot admit (quota full / pending) within a configurable timeout, try the next cluster
  3. Clean up remote workloads on clusters that lost
  4. Fall back to race-all if all clusters are above threshold

  Environment

  - Kueue version: v0.16.1
  - Kubernetes version: 1.33
  - MultiKueue with 3 worker clusters 


If there are already workaround, please suggest.

Thank You,
Sanjay

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T08:04:40Z

> Currently, MultiKueue uses a race model — workloads are dispatched to all worker

Actually, the incremental mode doesn't do it, but it goes in steps by three clusters, ptal https://github.com/kubernetes-sigs/kueue/blob/main/apis/config/v1beta2/configuration_types.go#L301-L303

> We run 3 worker clusters across regions (e.g., JP, US, SG) for GPU workloads. We want
to prefer scheduling on our primary cluster (cheaper/closer), and only overflow to
secondary and tertiary clusters when the primary lacks resources.

Would the incremental mode be sufficient for your use-case if there was some configuration to allow going in steps one-by-one?

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:48:18Z

/area multikueue

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T11:26:51Z

> > We run 3 worker clusters across regions (e.g., JP, US, SG) for GPU workloads. We want
> to prefer scheduling on our primary cluster (cheaper/closer), and only overflow to
> secondary and tertiary clusters when the primary lacks resources.
> 
> Would the incremental mode be sufficient for your use-case if there was some configuration to allow going in steps one-by-one?

I think so too. Additionally, if you want to handle cluster selection fine-grained, you can implement your custom multikueue-dispatcher.

### Comment by [@mpsanj](https://github.com/mpsanj) — 2026-02-16T15:36:44Z

> > Currently, MultiKueue uses a race model — workloads are dispatched to all worker
> 
> Actually, the incremental mode doesn't do it, but it goes in steps by three clusters, ptal https://github.com/kubernetes-sigs/kueue/blob/main/apis/config/v1beta2/configuration_types.go#L301-L303
> 
> > We run 3 worker clusters across regions (e.g., JP, US, SG) for GPU workloads. We want
> > to prefer scheduling on our primary cluster (cheaper/closer), and only overflow to
> > secondary and tertiary clusters when the primary lacks resources.
> 
> Would the incremental mode be sufficient for your use-case if there was some configuration to allow going in steps one-by-one?

Yes, incremental mode with a configurable step size would solve our use case. With 3 clusters and step=1, the dispatcher would try the first cluster, and only expand to the next if it can't admit.

Thanks for the quick response!

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T15:41:20Z

Awesome! would you have cycles yourself to work on the PR? We need to align on the API field name (maybe `IncrementalModeConfig.StepSize`), so a small KEP update for MultiKueue would be great.

Since this is a small change, I think we could probably couple KEP and impl in one PR.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T15:45:26Z

> Awesome! would you have cycles yourself to work on the PR? We need to align on the API field name (maybe `IncrementalModeConfig.StepSize`), so a small KEP update for MultiKueue would be great.
> 
> Since this is a small change, I think we could probably couple KEP and impl in one PR.

I remember that we discussed exposing the step size to user facing place.
So, basically, +1 on this enhancement.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-18T16:51:14Z

/remove-kind support
/kind feature

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-20T12:52:07Z

/retitle MultiKueue: allow configuring step size in the incremental dispatcher

If you don't mind - because the current title sounds like quite another feature.
