# Issue #2168: kueuectl command to get job + workload

**Summary**: kueuectl command to get job + workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2168

**Last updated**: 2024-06-11T16:04:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-08T19:44:31Z
- **Updated**: 2024-06-11T16:04:04Z
- **Closed**: 2024-06-11T16:04:04Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 6

## Description

**What would you like to be added**:

A single command that would output the status (and potentially events) of both workload and job objects.

Maybe it should look something like:

```
kubectl kueue describe <job type> <job name>
```

Ideally, this should work not just for CRDs supported by Kueue, but also external extensions. This should be possible using the discovery API and searching for a corresponding Workload object for it that has the matching UID label.

**Why is this needed**:

A common question users ask is "why is my job not running".

While most of this can be answered by looking at the Workload object, we don't want to force users to understand what the difference is between job and workload.

Furthermore, Kueue might have admitted the job and the job could be pending due to scale ups or failing scheduling (kube-scheduler) attempts.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-08T19:44:42Z

cc @mwielgus

### Comment by [@trasc](https://github.com/trasc) — 2024-05-15T14:35:12Z

@alculquicondor could extending the filter/lookup capabilities of `list workload` be sufficient for this?

https://github.com/kubernetes-sigs/kueue/blob/90689f60902fe9d2ad8127a37b253065547af197/keps/2076-kueuectl/README.md?plain=1#L202-L227

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-15T14:52:53Z

It could help, something like:

`kubectl list workloads --for job/my-job-name`

But it could also help to have a dedicated command that shows you both the job and the workload.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-15T15:57:39Z

Let's start with just `--for`

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-05-16T06:00:06Z

/assign @IrvingMg 

In my opinion the format for `--for` can be something like `[<type>[.<api-group>]/]<name>` so : 

- `--for=my-job`  includes all the workloads with a parent called `my-job` regardless of type and api-group
- `--for=job/my-job`  includes all the workloads with a parent called `my-job` and type `job` regardless of its api-group
- `--for=job.batch/my-job`  includes all the workloads with a parent called `my-job` and type `job` in api-group `batch`

The filtering is done on the client side so having the filter relaxed when it comes to owner type should not have any performance penalties.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-16T12:16:03Z

> * `--for=my-job`  includes all the workloads with a parent called `my-job` regardless of type and api-group
> * `--for=job/my-job`  includes all the workloads with a parent called `my-job` and type `job` regardless of its api-group

To avoid confusion if there happen to be 2 jobs with the same name, I hope we can include the full api name for the owning job in the list table.

The fact that multiple jobs matched will be less obvious if using `-o=yaml`, but I suppose users of this format are more savvy.
