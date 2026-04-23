# Issue #777: Document how to integrate a custom Job with Kueue

**Summary**: Document how to integrate a custom Job with Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/777

**Last updated**: 2023-08-14T12:35:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-16T19:43:28Z
- **Updated**: 2023-08-14T12:35:22Z
- **Closed**: 2023-08-14T12:35:22Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 2

## Description

We have successfully integrated Kueue with MPIJob and we are in the process of integrating JobSet and RayJob.
It would be useful to document what needs to be done in user docs.

cc @trasc @mcariatm @kerthcet

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-16T19:48:12Z

As a next step, creating a separate controller to integrate frameworks would be good.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-19T05:53:06Z

I think this is still valid, so /assign @BinL233
