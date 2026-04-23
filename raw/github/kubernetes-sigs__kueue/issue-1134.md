# Issue #1134: Switch to k8s.io/code-generator/kube_codegen.sh

**Summary**: Switch to k8s.io/code-generator/kube_codegen.sh

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1134

**Last updated**: 2023-11-07T10:02:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-09-19T04:39:11Z
- **Updated**: 2023-11-07T10:02:22Z
- **Closed**: 2023-11-07T10:02:22Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
We should switch the tool to generate client-go libraries to [`k8s.io/code-generator/kube_codegen.sh`](https://github.com/kubernetes/code-generator/blob/e4611069dfb4b0c04c7751afae1b9fef64828964/kube_codegen.sh).

**Why is this needed**:
The `k8s.io/code-generator/generate-groups.sh` was deprecated.

https://github.com/kubernetes/code-generator/blob/e4611069dfb4b0c04c7751afae1b9fef64828964/generate-groups.sh#L52-L54

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2023-09-19T08:31:45Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T08:35:41Z

We can work on this issue after https://github.com/kubernetes-sigs/kueue/pull/1133 is merged as `k8s.io/code-generator/kube_codegen.sh` was introduced since K8s v1.28.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T16:35:06Z

@PBundyra FYI: #1133 is merged into the main.

### Comment by [@trasc](https://github.com/trasc) — 2023-09-22T15:33:34Z

We should check if now we have better support for out of `GOPATH` generation and potentiality drop the workaround: 
https://github.com/kubernetes-sigs/kueue/blob/f9273bef71e136c0eed659ae19fce178512a6f6a/hack/update-codegen.sh#L35-L46

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-22T20:10:50Z

> We should check if now we have better support for out of `GOPATH` generation and potentiality drop the workaround:
> 
> https://github.com/kubernetes-sigs/kueue/blob/f9273bef71e136c0eed659ae19fce178512a6f6a/hack/update-codegen.sh#L35-L46

That's right. I thought we may be able to remove this workaround using `--output-base`:

https://github.com/kubernetes/code-generator/blob/e4611069dfb4b0c04c7751afae1b9fef64828964/kube_codegen.sh#L393-L395
