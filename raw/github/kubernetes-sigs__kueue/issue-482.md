# Issue #482: Flaky e2e suite: Failed to create ResourceFlavor

**Summary**: Flaky e2e suite: Failed to create ResourceFlavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/482

**Last updated**: 2022-12-21T21:59:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-12-20T15:28:27Z
- **Updated**: 2022-12-21T21:59:32Z
- **Closed**: 2022-12-21T21:59:32Z
- **Labels**: `kind/bug`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The creation of the default ResourceFlavor failed

**What you expected to happen**:

To succeed

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/466/pull-kueue-test-e2e-main-1-23/1605115464738934784

**Anything else we need to know?**:

No idea how this would happen. There is only one test that creates a ResourceFlavor, as far as I can see.

But a couple of notes:

- In `AfterEach`, we issue the delete call, but we don't wait for the object to be deleted. Waiting is important (we do in integration tests), because deleting a ResourceFlavor is asynchronous.
- I don't see why we can't create the RF once for the entire suite.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-20T15:28:41Z

cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-20T15:38:35Z

The one thing I notice about resource flavors is that they won't delete if something is still using them.  I notice that they have a finalizer and you have to remove the CQ and Queues completely before you can remove a resource flavor.  

I don't think there is much effort in deleting a resource flavor so I wonder if CQ or Queue are still being utilized in that test.  

So I can fix this by deleting CQ and Queue.  And then verifying that these are completely deleted before aiming to delete the resource flavor.  

How should I detect if CQ and Queue are deleted completely?  Just check if they still exist?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-12-20T15:48:58Z

> The one thing I notice about resource flavors is that they won't delete if something is still using them. I notice that they have a finalizer and you have to remove the CQ and Queues completely before you can remove a resource flavor.
> 
> I don't think there is much effort in deleting a resource flavor so I wonder if CQ or Queue are still being utilized in that test.
> 
> So I can fix this by deleting CQ and Queue. And then verifying that these are completely deleted before aiming to delete the resource flavor.
> 
> How should I detect if CQ and Queue are deleted completely? Just check if they still exist?

@kannon92, In integration tests, we just check their existence.
Maybe, below helps you.

https://github.com/kubernetes-sigs/kueue/blob/ed57453794e53f6a74e7363be83c663873729f03/test/integration/framework/framework.go#L331-L339

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-20T15:50:44Z

> I don't think there is much effort in deleting a resource flavor so I wonder if CQ or Queue are still being utilized in that test.

Even if you delete the CQ and LQ, the controllers might see those updates a bit later and take some time to react.

I was about to share the same link as @tenzen-y :)

Still, I don't understand why the test failed if there is only one that uses a RF. Are we running the suite more than once?

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-20T15:57:29Z

This is mostly a code quality question.  Is it correct to use frameworks in the integration tests in the e2e tests?  Or should they be moved to a common utility for both?  I used the utils for making jobs but I was wary of pulling in utilites that were defined in the integration test suite?  

I think we could replace the delete with the corresponding deletes with the link you all sent if there is no objection.

> Still, I don't understand why the test failed if there is only one that uses a RF. Are we running the suite more than once?

I'm not entirely sure if the runs are completely isolated.  I think the test would fail if the resource flavor finalizers were still set and they weren't updated.  Maybe higher load on the runner?  I don't think these are completely isolated from one another.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-20T16:30:35Z

I'm fine having a common framework for e2e and integration in `test/framework`

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-20T16:31:39Z

> I don't think these are completely isolated from one another.

What I'm trying to say is that I didn't see another test where we create a RF. Did I miss something?

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-20T19:07:58Z

> > I don't think these are completely isolated from one another.
> 
> What I'm trying to say is that I didn't see another test where we create a RF. Did I miss something?

No I don't think you missed anything.

I more mean that the different jobs are not completely isolated in prow.  I don't think a job gets an isolated CI runner.  So I think maybe some runs could be slower than others.  And maybe the delete of CQ or queue didn't completely finish and that caused the RF to not be deleted.  

I'll push up a change to use a common framework and utilize those utilites for any cleanup.  

/assign @kannon92

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-20T19:18:56Z

but wouldn't each prow job create its own kind cluster?
