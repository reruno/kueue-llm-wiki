# Issue #8188: Finished workloads show ADMITTED=False and empty RESERVED IN when listing workloads

**Summary**: Finished workloads show ADMITTED=False and empty RESERVED IN when listing workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8188

**Last updated**: 2026-01-15T12:51:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2025-12-11T17:01:59Z
- **Updated**: 2026-01-15T12:51:22Z
- **Closed**: 2026-01-15T12:39:39Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

After a workload successfully finishes, `kubectl get workloads` shows `ADMITTED: False` and `RESERVED IN: empty`. As shown below:

```
NAME                         QUEUE        RESERVED IN   ADMITTED   FINISHED   AGE
job-sample-job-8xmgl-34ac3   user-queue                 False      True       5m59s
```

This happens in both single-cluster and multi-cluster setups.

**What you expected to happen**:

Workloads should show ADMITTED: True or False, whichever value applies, rather than always False, and should show RESERVED IN: <cluster-queue-name> for historical and audit purposes.

**How to reproduce it (as minimally and precisely as possible)**:
1. E2E_RUN_ONLY_ENV=true make kind-image-build test-e2e
2. kubectl apply -f https://kueue.sigs.k8s.io/examples/admin/single-clusterqueue-setup.yaml
3. kubectl create -f ./examples/jobs/sample-job.yaml 

**Anything else we need to know?**:

I believe this is an undesired side effect of #7724, which clears the admission status when a workload finishes.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-11T17:03:31Z

/cc @mbobrovskyi @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T17:08:22Z

This looks expected to me, I think this behavior was always underspecified and confusing. We got multiple asks from users why QuotaReserved=True for finished workloads. 

Ok maybe we could somehow display still the information where the workload was reserving. I think this would solve itself if we decoupled the Reserved in column into two CQ and QuotaReserved

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-11T17:33:52Z

> Ok maybe we could somehow display still the information where the workload was reserving. I think this would solve itself if we decoupled the Reserved in column into two CQ and QuotaReserved

I agree. I think having the cluster queue in its own column would be better, and I also suggest keeping the real value in the ADMITTED column. This could help users quickly understand when a workload was not actually admitted. Even though we can use the FINISHED column to see this, I am not sure if it is enough. Still, having both columns might make things less confusing.

Additionally, I think we should update our documentation with the new expected outputs, like in https://kueue.sigs.k8s.io/docs/tasks/run/jobs/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T17:48:41Z

> I agree. I think having the cluster queue in its own column would be better, and I also suggest keeping the real value in the ADMITTED column

What is "real" value here? I'm thinking the simplest model is one column per condition: QuotaReserved, Admitted, Finished. Plus column for CQ and LQ.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-11T17:54:23Z

> What is "real" value here?

By “real value,” I mean that the ADMITTED column should show True if the workload was admitted, or False otherwise. But currently, it seems to always show ADMITTED: False after a workload finishes, which seems confusing to me.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T18:00:06Z

Oh, I think we now also transition "Admitted" to "False" for finished workloads, so this columns shows the "real" value, but the undelying value of the condition (status) is changed in 0.15.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-11T18:08:34Z

Yes, as I understand it, the transition of ADMITTED to False is also happening in #7724. Currently, we see ADMITTED: True while the workload is running, but after it finishes, it transitions to False. I think it would avoid confusion to preserve it as True. WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T18:20:46Z

Hm, I think `Admitted=True` might also be confusing as `Admitted=False`. 

We could draw some similarities from Pods. 

So for Pods when they complete they transition `Ready=False`, with reason `PodCompleted`. OTOH, they keep `PodScheduled=True`. The reasoning to transition Ready=False when Pod completes is that Ready is a "liveness" condition rather than lifecycle milestone (terminal). PodScheduled and Initialized are "lifecycle milestones" which never change. 

In Kueue the model is more complex. QuotaReserved and Admitted aren't really "lifecycle milestones" (terminal), because they can change back and forth. So they are more like "liveness" point-in-time conditions.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-12T08:51:13Z

I see. Then it sounds like having a `Phase` column might be useful, similar to the status column we have in `kueuectl`. The values could be `Pending | QuotaReserved | Admitted | Finished`. This way, the workload information would look like:

```
NAME        QUEUE       CLUSTER QUEUE    PHASE      AGE                                                                                                                                      
my-wl-123   user-queue  cluster-queue    Finished   5m                                                                                                                                       
job-abc     dev-queue   cluster-queue    Admitted   2m  
```

However, I think this would require an API change, because we would need to add a new `Phase` field to the workload schema.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-12T09:25:10Z

Yes, I remember @tenzen-y has some reservations about adding the "Phase" field to workload, but this usecase of integration with kubectl would make it very handy. wdyt @tenzen-y ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:36:48Z

/priority important-soon

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T12:51:22Z

> Yes, I remember [@tenzen-y](https://github.com/tenzen-y) has some reservations about adding the "Phase" field to workload, but this usecase of integration with kubectl would make it very handy. wdyt [@tenzen-y](https://github.com/tenzen-y) ?

Sorry, I was missing this comment. If this indicates adding phase only to the kubectl column, I'm fine with that.
