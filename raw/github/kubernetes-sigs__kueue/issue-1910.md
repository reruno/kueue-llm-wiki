# Issue #1910: sample-pytorchjob should update to cuda12+ and pytorch 2.0

**Summary**: sample-pytorchjob should update to cuda12+ and pytorch 2.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1910

**Last updated**: 2024-04-19T12:49:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@village-way](https://github.com/village-way)
- **Created**: 2024-03-26T01:59:25Z
- **Updated**: 2024-04-19T12:49:29Z
- **Closed**: 2024-04-19T12:49:29Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

sample-pytorchjob should update cuda and pytorch version, the image in the `examples/jobs/sample-pytorchjob.yaml` is too old. 

**Why is this needed**:

the sample pytorchjob failed to run on ubuntu 22.04 with cuda12.3

**Completion requirements**:

This enhancement requires the following artifacts:
the image `docker.io/kubeflowkatib/pytorch-mnist:v1beta1-45c5727` is from kubeflowkatib and the dockerfile is updated by https://github.com/kubeflow/katib/pull/2278 



The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-04-15T17:12:34Z

@village-way would you be willing to submit a PR? Generally, we should use examples from kubeflow.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-15T19:05:09Z

@village-way I'd be happy to review the opened PR :)

### Comment by [@village-way](https://github.com/village-way) — 2024-04-16T01:02:21Z

> @village-way I'd be happy to review the opened PR :)

I'm very excited to do this. I'll submit the PR a little later.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-04-17T12:53:33Z

Thank you @village-way for picking this up!
