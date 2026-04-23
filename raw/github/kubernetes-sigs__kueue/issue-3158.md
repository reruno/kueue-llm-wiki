# Issue #3158: Job should list "Untolerated Taint" as reason for not being admitted

**Summary**: Job should list "Untolerated Taint" as reason for not being admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3158

**Last updated**: 2025-08-10T16:45:51Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@nfung-soundhound](https://github.com/nfung-soundhound)
- **Created**: 2024-09-27T20:18:12Z
- **Updated**: 2025-08-10T16:45:51Z
- **Closed**: 2025-08-10T16:45:50Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->
**What would you like to be added**:
Pending Jobs/Workloads should be verbose in listing the reasons why they are pending, in particular in the case where it cannot tolerate the taints of any of the ResourceFlavors of the ClusterQueue for which it has submitted to. 

**Why is this needed**:
Consider the following example ResourceFlavor with a taint, and job definition below.
Assume the `dev` LocalQueue submits to the `dev` ClusterQueue.
Also assume that the ClusterQueue contains the ResourceFlavor `node_type` defined below with sufficient quotas.
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: node_type
spec:
  nodeLabels:
    beta.kubernetes.io/instance-type: "node_type"
  nodeTaints:
  - key: taint_key
    value: "taint_value"
    effect: NoSchedule
```
```yaml
# job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myjob
  labels:
    kueue.x-k8s.io/queue-name: dev
spec:
  suspend: true
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: myapp
        image: busybox
        command: ["sleep", "500"]
        resources:
          requests:
            memory: "128Mi"
            cpu: "500m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

When submitting the job above, the controller will suspend the job. 
However, the job events yield very little information:
```
Events:
  Type    Reason           Age   From                        Message
  ----    ------           ----  ----                        -------
  Normal  Suspended        10m   job-controller              Job suspended
  Normal  CreatedWorkload  10m   batch/job-kueue-controller  Created Workload: default/job-myjob-d2369
```
After enabling the debug logs on the controller, it turns out the job was not scheduled because it couldn't tolerate the taints for that node type. This might be fine for an administrator, but this makes it not user friendly for developers, where they might accidentally miss a taint. Typically, when scheduling pods/jobs, if it's not schedulable kubernetes provides the fact that it can't tolerate certain taints on some nodes.

```
{"level":"debug",
 "ts":"2024-09-27T19:56:20.485176276Z",
 "logger":"events","caller":"recorder/recorder.go:104","msg":"couldn't assign flavors to pod set main: untolerated taint {taint_key taint_value NoSchedule <nil>} in flavor node_type","type":"Normal","object":{"kind":"Workload","namespace":"default","name":"job-myjob-d2369","uid":"f469c8b0-a23b-4854-bc05-048a38904520","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"654137093"},"reason":"Pending"}
```

My current workaround is to no longer use taints on the ResourceFlavors, instead relying on the taints on the nodes themselves, and not using any tolerations on the ResourceFlavors. This has the unintended side effect of reserving a portion of the Quota without actually running a workload (i.e., the job will be submitted, but the pods will be stuck in pending since they do not tolerate the taints.) 

I have just begun to use Kueue, so please suggest any workarounds (I've thought of but not tested all-or nothing scheduling in this instance).

**Completion requirements**:

TBD, but would require some changes to the controller that give pending jobs/workloads reasons why they cannot be scheduled when sufficient quotas exist.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-08T16:08:34Z

This ResourceFlavor behavior is expected as described in https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/#resourceflavor-taints.

But, I agree that the current condition is not helpful for the batch users. Adding more informable condition or event would be better in this case.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-06T16:35:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-05T17:07:02Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-06T07:29:25Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-06T07:39:12Z

This seems like a legitimate issue that could be improved, so I would welcome a contribution here.
I guess a good start is to repro the issue, because it could have got improved since the issue opening, and propose some improvements. I would expect the event being emitted (maybe it already is?): https://github.com/kubernetes-sigs/kueue/blob/44d50cb3784038d88f04c9b99f85e045b37c3b54/pkg/scheduler/scheduler.go#L596

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-06T07:40:03Z

cc @kaisoz @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-06T07:45:40Z

cc @gabesaba

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-02-24T09:36:14Z

/assign

I can work on this 😊

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-03-13T14:16:54Z

Hi @nfung-soundhound !

Sorry for this late reply. That information is present in the `Workload` object, so there's no need  to enable the debug logs in the controller to get it. 

I followed your instructions, and applied your manifests, and when I describe the `Workload` I can see:

```
Name:         job-myjob-40537
Namespace:    issue-3158
Labels:       kueue.x-k8s.io/job-uid=cef7e75b-e271-46cf-ab33-56ecc11e4d1e
Annotations:  <none>
API Version:  kueue.x-k8s.io/v1beta1
Kind:         Workload
Metadata:
  Creation Timestamp:  2025-03-13T14:12:04Z
  Finalizers:
    kueue.x-k8s.io/resource-in-use
  Generation:  1
  Owner References:
    API Version:           batch/v1
    Block Owner Deletion:  true
    Controller:            true
    Kind:                  Job
    Name:                  myjob
    UID:                   cef7e75b-e271-46cf-ab33-56ecc11e4d1e
  Resource Version:        131315
  UID:                     5d7129eb-18c6-402a-91e0-10bd5446224c
Spec:
  Active:  true
  Pod Sets:
    Count:  1
    Name:   main
    Template:
      Metadata:
      Spec:
        Containers:
          Command:
            sleep
            500
          Image:              busybox
          Image Pull Policy:  Always
          Name:               myapp
          Resources:
            Limits:
              Cpu:     500m
              Memory:  128Mi
            Requests:
              Cpu:                     500m
              Memory:                  128Mi
          Termination Message Path:    /dev/termination-log
          Termination Message Policy:  File
        Dns Policy:                    ClusterFirst
        Restart Policy:                Never
        Scheduler Name:                default-scheduler
        Security Context:
        Termination Grace Period Seconds:  30
  Priority:                                0
  Priority Class Source:                   
  Queue Name:                              dev
Status:
  Conditions:
    Last Transition Time:  2025-03-13T14:12:04Z
    Message:               couldn't assign flavors to pod set main: untolerated taint {taint_key taint_value NoSchedule <nil>} in flavor node-type
    Observed Generation:   1
    Reason:                Pending
    Status:                False
    Type:                  QuotaReserved
  Resource Requests:
    Name:  main
    Resources:
      Cpu:     500m
      Memory:  128Mi
Events:
  Type     Reason   Age   From             Message
  ----     ------   ----  ----             -------
  Warning  Pending  32s   kueue-admission  couldn't assign flavors to pod set main: untolerated taint {taint_key taint_value NoSchedule <nil>} in flavor node-type
```

note that the `untolerated taint...` message is in the `Workload` status and in an event. Would this be enough for you? Or you mean you'd prefer it to be also in the owner object? (in this case, the `job`)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-11T15:10:16Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-11T15:54:48Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-10T16:45:46Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-10T16:45:51Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3158#issuecomment-3172760165):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
