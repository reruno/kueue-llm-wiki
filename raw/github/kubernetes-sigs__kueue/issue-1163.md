# Issue #1163: Does PodSetAssignments count have to be equal to podset count?

**Summary**: Does PodSetAssignments count have to be equal to podset count?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1163

**Last updated**: 2023-10-11T15:29:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@GhangZh](https://github.com/GhangZh)
- **Created**: 2023-09-25T10:15:23Z
- **Updated**: 2023-10-11T15:29:58Z
- **Closed**: 2023-10-11T11:28:24Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 10

## Description

![image](https://github.com/kubernetes-sigs/kueue/assets/92301646/d9c86bd9-7ddf-4b7e-a1a9-cb9bb68f715a)
If mincount is set, is workload count and PodSetAssignments count required to be the same here? Otherwise the workload will keep rebuilding, causing scheduling problems.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-27T23:26:37Z

we are comparing the `count`  in the job spec with the `count` coming from the assignment (the number of pods kueue allow the job to run).

we are not comparing `count` and `minCount`.

### Comment by [@trasc](https://github.com/trasc) — 2023-09-29T14:48:07Z

In sort the answer is no., in case of partial admission,  the admission `count` will be somewhere between  the `minCount` and the`count` of the podset depending on how many pod instances can fit the queue quota. There is also the chance for the assignment count to be less than the podSet count if while working with dynamicReclaim  a workload is preempted after some partial completion and readmitted later on.

### Comment by [@GhangZh](https://github.com/GhangZh) — 2023-10-07T03:04:19Z

> we are comparing the `count` in the job spec with the `count` coming from the assignment (the number of pods kueue allow the job to run).
>
> we are not comparing `count` and `minCount`.

If minCount=1;count=4. And the PodSetAssignments count between minCount and Count, the function will always return false and the workload will always be rebuilt. @alculquicondor @trasc

### Comment by [@trasc](https://github.com/trasc) — 2023-10-09T10:15:18Z

In case of partial admission, the job should start running (be unsuspended) with an updated  count (the one coming from admission).

### Comment by [@GhangZh](https://github.com/GhangZh) — 2023-10-09T11:22:13Z

> In case of partial admission, the job should start running (be unsuspended) with an updated count (the one coming from admission).

Do you mean that the count of the podset is modified in case of partial admission? I understand that the count of the podset is constant, right?

### Comment by [@trasc](https://github.com/trasc) — 2023-10-09T12:25:39Z

The count of pod replicas that are actually run by the job (`min(Parallelism, Completions) `)  is changed, not the one found in  Workload.Spec.PodSet[*].Count. 

More on partial admission: https://github.com/kubernetes-sigs/kueue/tree/main/keps/420-partial-admission

### Comment by [@GhangZh](https://github.com/GhangZh) — 2023-10-11T11:28:25Z

> PodSetAssignments

Problem solved,  thanks. At startJob it changes Parallelism to stay consistent with PodSetAssignments count.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-11T14:43:45Z

Talked with @GhangZh offline, his team is using kueue in production, I think his team can also be an adopter of kueue, feel free to fill in the list @GhangZh https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/, thanks.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-11T15:13:48Z

It looks like the link is wrong :)

here is the file with adopters https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/adopters/index.md

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-11T15:29:15Z

> here is the file with adopters https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/adopters/index.md

Sorry, I just replied in the slack for another question, error pasted the link, thanks Aldo.
