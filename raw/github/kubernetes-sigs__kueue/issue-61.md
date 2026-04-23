# Issue #61: Add E2E test setup and first test

**Summary**: Add E2E test setup and first test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/61

**Last updated**: 2022-11-22T15:32:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-24T16:23:17Z
- **Updated**: 2022-11-22T15:32:16Z
- **Closed**: 2022-11-22T15:32:16Z
- **Labels**: `kind/feature`, `priority/important-longterm`, `kind/productionization`
- **Assignees**: [@kannon92](https://github.com/kannon92), [@kerthcet](https://github.com/kerthcet)
- **Comments**: 15

## Description

We can use a kind cluster.

The test should create basic Capacity, Queue and a batchv1/Job, and wait for it to complete.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T16:23:34Z

/kind feature
/priority important-longterm
/size M

### Comment by [@utkarsh-singh1](https://github.com/utkarsh-singh1) — 2022-05-24T10:40:33Z

Hi everyone , Is there anyone working on this issue, if there is none then I would like to contribute.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-30T19:24:26Z

For a change like this, maybe first give us an overview on how you plan to solve it. Otherwise, you can take it.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-07-16T11:45:34Z

I'll take a look of this when I have time.
/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-11T14:33:05Z

Hello @kerthcet, I'm interested in helping out.  Could I take this issue if you haven't made much progress on it?  

I was going to follow a similar pattern as what is done with https://github.com/kubeflow/mpi-operator/tree/master/v2/test/integration.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-10-11T14:56:25Z

Thanks Kevin, I made some progress months ago, see here https://github.com/kerthcet/kueue/commit/34c78bdb68cd016335d712d4bde1b799e2ee7145, but then moved on to other things. You can work on this if you like. If not, I'll work on the features required in v0.3 firstly and then turn to this feature. 

I hope we can have e2e tests in v0.3.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-11T15:04:29Z

Yea I'll take this then.  

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-11T15:19:36Z

So where do we want the e2e tests to run?  I see that we use Prow for running our CI.  Do I follow similar behavior for running the CI tests?  Or can I add a github action to run the e2e tests?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-11T15:47:45Z

Prow please.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-14T14:37:37Z

@alculquicondor Any notes on how to add these e2e tests to Prow?  I don't see anything in the repo and I'm unfamiliar with Prow.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-14T14:43:08Z

I'm not fully familiar, but here is where our presubmits are defined https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes-sigs/kueue/kueue-presubmits.yaml

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-14T14:44:08Z

Maybe you can take the descheduler as reference https://github.com/kubernetes/test-infra/blob/654386a21f6f378024dcedea7e6b167da0b25de7/config/jobs/kubernetes-sigs/descheduler/descheduler-presubmits-master.yaml#L56

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-14T14:51:48Z

Also, I notice that this project lacks examples (other than samples in config).

I was thinking that I could approach the e2e tests in two ways:

1) Define inline CQ and Workload in the e2e test and run them. 
    - I don't love this because users glancing at a project won't see these as examples
    - It is pretty easy for developers to add though. 
2) Point our e2e test to an example directory and have the e2e test suite run the examples files.  
  - We can create an examples directory and add new features as examples.

I like 2 because I find a project that has examples to be welcoming.  Having them integrated in the e2e test at least verifies that functionally they are correct.  

I'm open to either but I just wanted your thoughts.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-14T16:27:00Z

There is already a samples directory https://github.com/kubernetes-sigs/kueue/tree/main/config/samples (maybe it's worth moving it up to the root)

As long as it's easy to setup kubectl in Prow, I'm ok with option 2.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-10-19T18:03:44Z

Hello. I have https://github.com/kubernetes-sigs/kueue/pull/421 up but I need a little guidance on it.  I am having trouble with getting the webhooks working with Kind and the controller runtime.  Unsure if this is the right path or if I should try something different.
