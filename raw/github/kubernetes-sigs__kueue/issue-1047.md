# Issue #1047: Revisit `pkg/util/maps` and `pkg/util/slices` after switching to go 1.21

**Summary**: Revisit `pkg/util/maps` and `pkg/util/slices` after switching to go 1.21

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1047

**Last updated**: 2023-09-27T12:22:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-08-09T06:20:33Z
- **Updated**: 2023-09-27T12:22:24Z
- **Closed**: 2023-09-27T12:22:24Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
[Go 1.21](https://tip.golang.org/doc/go1.21) some cages that could simplify our `slices` and `maps` like:
  
New slices package
The new [slices](https://tip.golang.org/pkg/slices) package provides many common operations on slices, using generic functions that work with slices of any element type.

New maps package
The new [maps](https://tip.golang.org/pkg/maps/) package provides several common operations on maps, using generic functions that work with maps of any key or element type.

[min and max](https://tip.golang.org/ref/spec#Min_and_max)

**Why is this needed**:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-09T13:32:41Z

Sounds exciting!

Although I would prefer to wait for 1.21.1 to be released before we upgrade. Ideally k/k also moves.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2023-09-18T13:56:34Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-18T18:18:01Z

I asked some sig-architecture folks, and there doesn't seem to be a date for upgrading k/k to golang 1.21

Since 1.21.1 was already released, I'm ok upgrading kueue now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-27T07:47:00Z

/reopen

I think `slices` still remain.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-09-27T07:47:05Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1047#issuecomment-1736878672):

>/reopen
>
>I think `slices` still remain.
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@PBundyra](https://github.com/PBundyra) — 2023-09-27T08:55:57Z

> /reopen
> 
> I think `slices` still remain.

I've gone through ```slices``` and didn't find anything that can be useful for our current use cases

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-27T12:22:20Z

> > /reopen
> > I think `slices` still remain.
> 
> I've gone through `slices` and didn't find anything that can be useful for our current use cases

I see. Thank you!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-09-27T12:22:24Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1047#issuecomment-1737284877):

>> > /reopen
>> > I think `slices` still remain.
>> 
>> I've gone through `slices` and didn't find anything that can be useful for our current use cases
>
>I see. Thank you!
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
