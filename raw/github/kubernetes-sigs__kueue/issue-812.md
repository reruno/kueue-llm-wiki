# Issue #812: Samples folder is hard to find and not a common place to look for examples.

**Summary**: Samples folder is hard to find and not a common place to look for examples.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/812

**Last updated**: 2023-05-26T15:08:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2023-05-25T18:21:07Z
- **Updated**: 2023-05-26T15:08:54Z
- **Closed**: 2023-05-26T15:08:54Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We should move config/samples/* to a top level directory.  I'm unclear if we have code/docs that reference this so I want this as a separate issue from where it was brought up.  

**Why is this needed**:

https://github.com/kubernetes-sigs/kueue/pull/778#discussion_r1195871208

As this project matures I think we should start putting example integrations in an examples directory so people can glance quickly and see how to use other workloads.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-25T18:54:29Z

+1

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-25T18:55:15Z

We can update the links where needed, but I don't think the docs link to them. They have their own inline examples.
