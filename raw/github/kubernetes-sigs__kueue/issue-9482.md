# Issue #9482: Kueue will say a workload is admitted if its scheduling gates are removed.

**Summary**: Kueue will say a workload is admitted if its scheduling gates are removed.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9482

**Last updated**: 2026-02-26T21:49:43Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-02-25T16:12:17Z
- **Updated**: 2026-02-26T21:49:43Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

If pods have additional scheduling gates, Kueue will say the pod is admitted even if the scheduling gates are present.

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  generateName: kueue-sleep-
  namespace: kueue-test
  labels:
    kueue.x-k8s.io/queue-name: user-queue-no-exclude-cpu
spec:
  schedulingGates:
    - name: test
  containers:
    - name: sleep
      image: busybox
      command:
        - sleep
      args:
        - 100s
      resources:
        requests:
          memory: 100Mi
  restartPolicy: OnFailure
```

```bash
kehannon@kehannon-thinkpadp1gen4i:~/Work/kueue-release-testing/ai/rhbok$ k get pods -n kueue-test
NAME                READY   STATUS            RESTARTS   AGE
kueue-sleep-qw5hb   0/1     SchedulingGated   0          2m3s
```
Even though pod is still gated, Kueue thinks its admitted because its own scheduling gate was added.

```bash
  Normal  Admitted       2m25s  kueue-admission  Admitted by ClusterQueue cluster-queue, wait time since reservation was 0s

```

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T16:29:31Z

Interesting, I think we never really thought about extra gates, so the behavior is underspecified here.

Currently, regardless of the Pod's scheduling gates Kueue will "Admit" the workload and reserve quota, do you think we should not be reserving the quota for such Pods? 

This might be actually related to https://github.com/kubernetes-sigs/kueue/pull/7295 and https://github.com/kubernetes-sigs/kueue/issues/6915. 

Technically speaking Kueue could respect the Pod's scheduling gate for Pod integration and behave as we are planning for the new annotation (which is Job agnostic so still valuable). Then it would be a good argument for using the "scheduling-gates" for the annotation name

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T16:31:19Z

cc @mwielgus @tenzen-y @VassilisVassiliadis

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-25T16:43:36Z

> This might be actually related to https://github.com/kubernetes-sigs/kueue/pull/7295 and https://github.com/kubernetes-sigs/kueue/issues/6915.

I don't think they are related because @VassilisVassiliadis is mostly focused on suspend workloads (so I don't expect schedling gates here. Its actually suspend).

I have another bug I am chasing down where on openshift pod workloads can get rejected on updates. And in that case the workload will say its admitted but the gate wasn't removed.

Still trying to figure out how to reproduce that without openshift but having trouble replicating the security rules on Kind.

I mentioned this issue to @amy once before and I figured I should file this one so we record it as a known issue.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-25T19:06:43Z

> Currently, regardless of the Pod's scheduling gates Kueue will "Admit" the workload and reserve quota, do you think we should not be reserving the quota for such Pods?

If there is a scheduling gate or the workload is suspended the workload doesn't really have the resource or even got scheduled on a node.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T19:14:11Z

Yes, but Im not sure this is a bug. 

Currently, Admitted <> Scheduled, if there are custom scheduling gates, then it is up to the external controller to remove them post Admission to allow Scheduling

### Comment by [@amy](https://github.com/amy) — 2026-02-26T00:32:49Z

I think I previously submitted this related one: https://github.com/kubernetes-sigs/kueue/issues/7433

Even though it may not be a bug, I think the user experience is still weird when you encounter it in the wild.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-26T00:50:17Z

> Yes, but Im not sure this is a bug.
> 
> Currently, Admitted <> Scheduled, if there are custom scheduling gates, then it is up to the external controller to remove them post Admission to allow Scheduling

I agree with you. Additionally, we have a couple of problems if we consider Pods with other gates as inadmissible Workloads.
That is kind of the chicken and egg problem. Some external controllers might want to ungate after admission, but others might want to before admission. So, if we consider this as a bug, we need to introduce a knob (or FG) on how to handle the other gates when admission.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-26T21:33:18Z

Maybe we can start with a note in our documentation around pod integration.

If there are existing scheduling gates Kueue will report the workload as admitted but you will have to remove those separately to get the workload to scheduled.

I'll open up a PR for this.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-26T21:33:45Z

I'm fine to consider this a feature.

/remove-kind bug
/kind feature

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-26T21:49:43Z

I opened up a docs PR: https://github.com/kubernetes-sigs/kueue/pull/9541
