# Issue #1065: [website] Add download icon next to file names

**Summary**: [website] Add download icon next to file names

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1065

**Last updated**: 2023-09-20T14:14:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-16T20:06:39Z
- **Updated**: 2023-09-20T14:14:04Z
- **Closed**: 2023-09-20T14:14:04Z
- **Labels**: `kind/feature`, `good first issue`
- **Assignees**: [@FZhg](https://github.com/FZhg)
- **Comments**: 1

## Description


**What would you like to be added**:

We have a shortcode that writes the contents of a static file into the website, along with a link for downloading it.
There should be:
- an icon before the file name.
- a box around the name

https://kubernetes.io/docs/concepts/workloads/controllers/job/#running-an-example-job

Perhaps we can adapt the shortcode that kubernetes uses https://github.com/kubernetes/website/blob/3c9c3afd2abd086f79b7d220884f39747d06496c/layouts/shortcodes/code.html

**Why is this needed**:

An icon would make it clear that it's a link for downloading the file

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@FZhg](https://github.com/FZhg) — 2023-09-06T01:39:33Z

/assign
