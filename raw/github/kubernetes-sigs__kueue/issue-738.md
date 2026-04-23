# Issue #738: Support JobSet in Kueue

**Summary**: Support JobSet in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/738

**Last updated**: 2023-06-29T13:11:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-02T21:51:21Z
- **Updated**: 2023-06-29T13:11:38Z
- **Closed**: 2023-06-29T13:11:38Z
- **Labels**: `kind/feature`
- **Assignees**: [@mcariatm](https://github.com/mcariatm)
- **Comments**: 10

## Description

**What would you like to be added**:

The ability to control JobSet startup through Kueue.

**Why is this needed**:

To support a wide variety of workloads

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-02T21:51:51Z

The first release of jobset came up https://github.com/kubernetes-sigs/jobset/releases/tag/v0.1.0

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-02T21:51:58Z

/assign @trasc

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-05-03T12:26:09Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T12:38:48Z

/unassign @trasc

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-03T12:44:00Z

I helped write the suspend code in Jobset so feel free to tag if you find issues.

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-05-10T14:39:52Z

For initially unsuspend, setting NodeAffinity foreach  ReplicatedJob Template should be enough.
But if the jobs are already created the node selectors should be updated on each of them.
I propose to do that in jobset_contolled in resumeJobSetIfNecessary function on Jobset Operator.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-25T16:41:53Z

Any progress on this?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-25T16:44:49Z

@mcariatm is working on this at the jobset side.

https://github.com/kubernetes-sigs/jobset/issues/134

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-25T16:45:37Z

So it will take a bit of time.

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-05-25T16:47:48Z

Yes, I'm still working on it. On both sides kueue and jobset. I think tomorrow I will put all changes for kueue. Working on tests now.
