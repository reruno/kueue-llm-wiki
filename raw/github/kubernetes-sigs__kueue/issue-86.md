# Issue #86: Brainstorm enhancing UX

**Summary**: Brainstorm enhancing UX

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/86

**Last updated**: 2022-04-10T15:40:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-02T18:29:33Z
- **Updated**: 2022-04-10T15:40:57Z
- **Closed**: 2022-04-10T15:40:57Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

We are adding more information to statuses of the various APIs we have (https://github.com/kubernetes-sigs/kueue/issues/7 and https://github.com/kubernetes-sigs/kueue/issues/5); but I am wondering what other UX-related enhancements we should pursue for the two personas: batch admin and batch user.

UX gets users excited about the system and I think should be a focal point as Kueue evolves.

## Discussion

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T19:07:19Z

- [ ] Prometheus integration for resource consumption of QueuedWorkloads / Queues

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-28T13:00:44Z

A kubectl plugin will be quite useful here for both admins and users.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-28T21:23:41Z

I think we should update the QueuedWorkloadAdmitted condition to True in a best-effort basis.

This means that we don't need to do it in the scheduling cycle. But we can do it in the controller (we will get an event for the addition of the .spec.admission field).

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-10T15:40:57Z

Created https://github.com/kubernetes-sigs/kueue/issues/201 and https://github.com/kubernetes-sigs/kueue/issues/199 to track updating the workload condition and adding metrics. Closing this one.
