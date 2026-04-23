# Issue #1790: Non-admitted workloads with QuotaReserved condition are shown as Admitted by kubectl

**Summary**: Non-admitted workloads with QuotaReserved condition are shown as Admitted by kubectl

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1790

**Last updated**: 2024-04-18T13:51:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-03-04T11:00:49Z
- **Updated**: 2024-04-18T13:51:51Z
- **Closed**: 2024-04-18T13:51:51Z
- **Labels**: `kind/bug`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I have a workload in QuotaReserved condition, which is visible with kubectl describe:
```yaml
...
  Admission Checks:
    Last Transition Time:  2024-03-04T10:55:16Z
    Message:               
    Name:                  sample-multikueue
    State:                 Pending
  Conditions:
    Last Transition Time:  2024-03-04T10:55:16Z
    Message:               Quota reserved in ClusterQueue cluster-queue
    Reason:                QuotaReserved
    Status:                True
    Type:                  QuotaReserved
Events:
  Type    Reason         Age   From             Message
  ----    ------         ----  ----             -------
  Normal  QuotaReserved  43s   kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 1s
```
However, the output of kubectl get suggests it is already admitted (I find this misleading):

```
> kubectl get workloads -owide                                                      
NAME                           QUEUE        ADMITTED BY     AGE
jobset-sleep-job-5xh9k-af81b   user-queue   cluster-queue   2m5s
```

**What you expected to happen**:

The output of kubectl get should clearly indicate that the workload is not admitted yet. Note that a workload may remain in the
QuotaReserved state for a long time.

One idea would be to have a new column "STATUS" which could have values: "Pending" "QuotaReserved", "Admitted".

**How to reproduce it (as minimally and precisely as possible)**:

Use admission check for ProvisioningRequest or MultiKueue, then the workload may stay in "QuotaReserved" state long enough to observe the discrepancy.

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-04T11:08:26Z

I guess that this unintended description was brought by this: https://github.com/kubernetes-sigs/kueue/blob/38fee15a013552af42ea51feb002734a73c0b636/apis/kueue/v1beta1/workload_types.go#L319

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-04T11:14:06Z

> I guess that this unintended description was brought by this:

Yeah, not sure we can express more sophisticated checks in kubebuilder. Maybe we should have a dedicated field in Workload, say "phase" or status, which we would print. W do something similar with the "phase" field in pods, which is derived from the status of containers.

Then, we could have values like "Pending", "Reserving", "Admitted".

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-04T11:24:03Z

> > I guess that this unintended description was brought by this:
> 
> Yeah, not sure we can express more sophisticated checks in kubebuilder. Maybe we should have a dedicated field in Workload, say "phase" or status, which we would print. W do something similar with the "phase" field in pods, which is derived from the status of containers.
> 
> Then, we could have values like "Pending", "Reserving", "Admitted".

According to the API design docs, introducing the `phase` field would be deprecated and not recommended.

> Some resources in the v1 API contain fields called phase, and associated message, reason, and other status fields. The pattern of using phase is deprecated. Newer API types should use conditions instead. Phase was essentially a state-machine enumeration field, that contradicted [system-design principles](https://git.k8s.io/design-proposals-archive/architecture/principles.md#control-logic) and hampered evolution, since [adding new enum values breaks backward compatibility](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md). Rather than encouraging clients to infer implicit properties from phases, we prefer to explicitly expose the individual conditions that clients need to monitor. Conditions also have the benefit that it is possible to create some conditions with uniform meaning across all resource types, while still exposing others that are unique to specific resource types. See [#7856](http://issues.k8s.io/7856) for more details and discussion.

https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#typical-status-properties

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-04T11:34:13Z

I see, but in the core k8s we can define printers which output the column based on custom logic in Go -not sure this is feasible with subprojects. 

As an alternative, maybe we could rename "Admitted by" with "Reserving in", then add another column "Admittted" based on the condition status, saying just true/false.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-04T11:36:35Z

> I see, but in the core k8s we can define printers which output the column based on custom logic in Go -not sure this is feasible with subprojects.
> 
> As an alternative, maybe we could rename "Admitted by" with "Reserving in", then add another column "Admittted" based on the condition status, saying just true/false.

That makes sense. Anyway, we need some investigations.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-04-17T01:21:54Z

/assign
