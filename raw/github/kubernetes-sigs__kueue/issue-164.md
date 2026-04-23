# Issue #164: Use server-side apply for admission?

**Summary**: Use server-side apply for admission?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/164

**Last updated**: 2022-08-19T16:35:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-30T13:39:44Z
- **Updated**: 2022-08-19T16:35:53Z
- **Closed**: 2022-08-19T16:35:53Z
- **Labels**: `kind/feature`, `priority/backlog`, `kind/productionization`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Today, we use Update to admit a workload. If the workload resource version has changed, this request fails. This is good, it might prevent us from double scheduling if the workload is updated while we are scheduling an older version of it.

However, the update happens asynchronously. The workload is no longer at the queue, so a followup scheduling cycle might schedule a workload with lower priority.

SSA might allows to just modify the admission section and hopefully only fail if there is a conflict in there.

**Why is this needed**:

To guarantee priority when admitting workloads.

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-30T13:52:13Z

Can we re-get it before update? For latest version
And check for the admission if existed or other needed before upadting.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-30T17:04:54Z

I had a brief chat with @lavalamp. This is one of the points of SSA, so we should try to use it.

These are the options to fail if something changed:

1. you can "try" to set the generation field. That will cause the request to fail if the generation is different, since you can't change that field. As opposed to "resourceVersion" that covers the whole object (metadata and status included), the generation only covers the spec. This is great, because it would fail if something changed the resource requests or affinities, etc.
2. you can use the "fail on conflict" option and set the fields which you want to ensure don't change. This only works if the fields you want to change are unowned or already owned by you (this should be the case for the `.spec.admission`).

I think we should use SSA. Otherwise we are implementing conflict detection in the client, which will always have a chance to be outdated, even if we just got the object.

### Comment by [@lavalamp](https://github.com/lavalamp) — 2022-03-30T17:29:08Z

If you decide to fail on conflicts, you need a mechanism to notice when someone is trying to own your field. (Usually controllers ignore conflicts because it's more useful for humans to get the conflict messages.)

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-04T01:43:01Z

It seems to me that option 1 is the better choice; we should fail to set the admission field if the workload spec changed.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-05T15:39:21Z

Is this complicated to do? or just a flag we pass to the update call?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-05T16:01:31Z

There is a special client for it. It might just be a week of experimentation + implementation.

### Comment by [@lavalamp](https://github.com/lavalamp) — 2022-04-11T21:55:29Z

Fail or not on conflicts is just a flag passed to the special client (which was put together with existing controllers converting over to use it in mind; let us know how it goes).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T21:01:10Z

/assign
I'll try to get this done.
