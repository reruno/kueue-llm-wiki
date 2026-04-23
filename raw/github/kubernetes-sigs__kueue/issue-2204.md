# Issue #2204: kueuectl: list pods for a job

**Summary**: kueuectl: list pods for a job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2204

**Last updated**: 2024-08-21T15:52:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-15T16:01:57Z
- **Updated**: 2024-08-21T15:52:42Z
- **Closed**: 2024-08-21T15:52:42Z
- **Labels**: `kind/feature`
- **Assignees**: [@Kavinraja-G](https://github.com/Kavinraja-G)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

The ability to list all the pods that belong to a job. This probably will have to be specialized for every kind of job.

```
kubectl kueue list pods --for job/my-job-name
```

**Why is this needed**:

To simplify the experience of users who are not very familiar with kubernetes, and label selectors.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-15T16:02:06Z

/assign @trasc

### Comment by [@Kavinraja-G](https://github.com/Kavinraja-G) — 2024-05-19T14:13:38Z

@alculquicondor @trasc  I'm happy to contribute if this is not started already?

### Comment by [@trasc](https://github.com/trasc) — 2024-05-20T07:41:57Z

I am OK with this, @alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-21T18:27:34Z

Sounds good.

@Kavinraja-G please write `/assign` in a comment.

### Comment by [@Kavinraja-G](https://github.com/Kavinraja-G) — 2024-05-22T08:20:14Z

/assign

### Comment by [@Kavinraja-G](https://github.com/Kavinraja-G) — 2024-05-25T08:53:41Z

> will have to be specialized for every kind of job

@alculquicondor Can you elobrate this part? My understanding is to list the pods even when the user specifies `[cronjobs|jobs]/<job-name>` Let me know if I'm wrong.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-27T12:13:43Z

We also have mpijobs, kubeflow, ray clusters, etc.

The way to obtain the pods for all these different types might differ.
