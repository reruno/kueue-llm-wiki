# Issue #2975: [kueuectl] delete workload command should delete the Job & workload

**Summary**: [kueuectl] delete workload command should delete the Job & workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2975

**Last updated**: 2024-09-24T07:18:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-04T09:29:53Z
- **Updated**: 2024-09-24T07:18:02Z
- **Closed**: 2024-09-24T07:18:02Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 29

## Description

**What happened**:

The `kueuectl delete workload` command only deletes the workload, rather than the Job.
This means that the job gets restarted rather than deleted.

**What you expected to happen**:

The Job & workload gets deleted. If the workload is deleted by the core Kueue, then deleting the Job by kueuectl is enough.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a Job
2. Get the workload name by `kueuectl list workload`
3. Invoke `kueuectl delete workload <name>`

Issue: the Job remains. As a result `kueuectl list workload` keeps displaying the workload (now recreated).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T09:30:14Z

/cc @mwielgus @mwysokin @trasc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-04T09:36:29Z

The `kueuectl delete workload <name>` command currently acts as a passthrough to `kubectl delete workload <name>`. Should we consider improving this in Kueue?"

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T09:47:47Z

The command should delete the Job rather than the workload, the workload will be deleted by Kueue.

> Should we consider improving this in Kueue?"

I assume a fix in kueuectl is enough, but let me know if I'm missing something.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-04T13:25:41Z

> I assume a fix in kueuectl is enough, but let me know if I'm missing something.

I just think it might confuse the user. If I correct understood, on the [KEP](https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#pass-through) it should just execute `kubectl delete` command. Or I missed something?

Perhaps we could introduce an additional flag that allows users to delete both the Workload and the associated Job. WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T13:40:51Z

> I just think it might confuse the user. 

the current behavior is more confusing. User deletes the workload, but it remains listed (after getting recreated). Workload recreation (keeping the Job) is rarely the intention of the user. Kueuectl's objective is to support the main usage scenarios.

> If I correct understood, on the [KEP](https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#pass-through) it should just execute kubectl delete command. Or I missed something? 

cc @mwielgus as the author. IIUC invoking `kubectl delete` for the Job should be enough.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-04T13:53:04Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-09-05T14:45:52Z

In my opinion deleting the job when a wl is deleted is more confusing taking into account that the ownership work in the opposite direction and deleting the workload can be used a requeue mechanism. 

If going with this the behavior should be optional.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-05T14:53:40Z

Still, it is user's feedback who found the current behavior confusing, so I think we should somehow address it. The fact that a user calls delete workload, and it is listed on the next workload list is confusing.

My understanding of the "workload" in the command is more abstract, representing the computation, rather than the internal Kueue API.

cc @mwielgus @mwysokin in case you have some other views here.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-05T14:56:41Z

> deleting the workload can be used a a requeue mechanism.

I know, but it seems a niche use case, about which most users are not aware of. I think kueuectl should aim to support main use cases. If we want to support "requeue" I would suggest we have a dedicated command for that. The command could delete the workload underneath.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-06T09:12:29Z

> > deleting the workload can be used a a requeue mechanism.
> 
> I know, but it seems a niche use case, about which most users are not aware of. I think kueuectl should aim to support main use cases. If we want to support "requeue" I would suggest we have a dedicated command for that. The command could delete the workload underneath.

We could also have a different command (`purge` or something similar) that deletes the wl and job and keep the current `delete wl` as is.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-06T11:48:31Z

We could, but I don't think the current command "delete" expresses the user's intention. At least from the feedback I got it doesn't. I agree doing "requeue" is a potentially valid use case, but having a command like "requeue" will nicely reflect the intention.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2024-09-06T18:47:00Z

+1 on what @mimowo wrote. We should not use delete for requeueing in kueuectl. We should have a separate command for that, if workload stop for some reason is not enough. However I understand the concern here - generally speaking, kueuectl should not do things differently than kubectl but I believe we have a valid case here.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-09T04:21:50Z

> +1 on what @mimowo wrote. We should not use delete for requeueing in kueuectl. We should have a separate command for that, if workload stop for some reason is not enough. However I understand the concern here - generally speaking, kueuectl should not do things differently than kubectl but I believe we have a valid case here.

Requeue is just a usecase, the bigger probblem is the reversed ownership, the job owns the workload not the other way around.
For me the proposal sounds like the  implementation of an `rm` command that will remove a directory if a '*.csv' file from within it is removed.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T07:55:35Z

The ownership you are referring to is between the Job object and the Kueue Workload API. However, I think the "workload" word in the command does not indicate the Kueue Workload API, as this is an API object which is aimed to be transparent to the users (ideally). I think the CLI users don't need to think about the Workload API, or about its ownerReferences.

I think the "workload" in this context means a computation unit created by the user. We use the word workload as we recently started to also support serving workloads (not just Jobs).

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-09-09T12:27:12Z

TLDR; +1 to @mimowo and @mwielgus 

For me requeuing would definitely be an unexpected behavior if not even an unwanted one if encountered during deletion. I'd consider it a bug if I want to delete something and it's requeued and run again.

Since Jobs (or actually any supported Kind) and Workloads are strictly bound and they are expected to mostly live together in a consistent state maybe both of them should be deleted in a close to transaction-like way?

### Comment by [@trasc](https://github.com/trasc) — 2024-09-09T12:34:13Z

Requeue is just a usecase, the bigger problem is the reversed ownership, the job owns the workload not the other way around.

kueuectl implements `delete` for multiple object types and we are acting just like kubectl is, having `delete workload` be that different (delete the parent object, refer to some other concept then an API object) will create a lot of confusion.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-09-09T13:18:12Z

> (...) the bigger problem is the reversed ownership, the job owns the workload not the other way around.

I do agree that the relationship is not straightforward. Job might own a Workload in terms of how it was implemented (I think it's out of scope of this issue to discuss whether it's a good or bad thing and whether implementing it was the right call, it's just where we are right now) but a Workload is something more general and an abstraction to some extent which can have specific manifestations like Jobs, Deployments, Pods etc.

The goal here is to delete the Workload and whatever its specific manifestation is. So if we have a Workload that needs to run a Job ideally both should be deleted when removing the Workload. If that's not possible for some reason or problematic I'd focus on achieving the same goal by removing the parent which is the Job in this case since the Workload will also be deleted.

I agree that `kubectl` works differently but I'd like to ask that we prioritize delivery of the feature instead of trying to be like `kubectl` especially since it might cause bigger changes and also the change requested by @mimowo is like the KEP author has imagined it according to their own feedback.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-09T14:19:00Z

To do not miss the idea. On the weekly meeting we take a decision to add user confirmation `Do you want to delete corresponding Job? [yes/no]` when deleting a Workload. If the user selects `yes`, both the Workload and related Job will be deleted. If `no`, only the Workload will be deleted as before.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-09T14:22:42Z

More like `This operation will also remove the job associated with this workload. Do you want to proceed (y/n)?`. No just exits the command. And users can add a `-y` argument that skips the question.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T14:27:06Z

I think if 'no', then we do nothing.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T14:34:48Z

I like the idea, we may just consider a slightly different phrasing to also be inclusive of potentially serving workloads (not just Jobs).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-09T15:50:57Z

`This operation will also remove <apigroup>/<object-name> associated with this workload`. Then there is no place for misinterpretation.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-09T15:52:26Z

> `This operation will also remove <apigroup>/<object-name> associated with this workload`. Then there is no place for misinterpretation.

We can delete multiple objects. Should we confirm for each one?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T16:03:47Z

In case of regular Jobs/ serving workloads it should be enough to just ask about deleting the Job and message about the user object. The Workload APi will be deleted by Kueue. I think we don't need to warn about it.

I think in the case of Pod group a single message should also be enough, but we may modify the message to use the plural form.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-09T16:06:00Z

No, I mean that we can delete multiple Workloads. Like this `kueuectl delete workload wl1 wl2`.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T16:24:01Z

I would suggest a slight modification to the message: 


```
This operation will also remove <apigroup>/<object-name> associated with the <workload-name> workload". Then, ask the message per each workload. 
```

But this is not a strong view, one message combining the list of Job objects is also fine for me.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-09T16:48:11Z

Maybe there could be a line for each workload/job pair to be deleted, but just a single question.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-09T17:06:12Z

> Maybe there could be a line for each workload/job pair to be deleted, but just a single question.

I think, it's a very long message in this case, as we have a lot of workloads that we need to delete. WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-09T17:15:12Z

When doing `kubectl delete workload x y z`, there shouldn't be that many.

When doing `kubectl delete workload --all`, we can probably just show a single line without specifics about the names of the objects.
