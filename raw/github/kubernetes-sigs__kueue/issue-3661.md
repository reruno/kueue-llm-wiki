# Issue #3661: TAS: cleanup and introduce node wrapper for testing

**Summary**: TAS: cleanup and introduce node wrapper for testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3661

**Last updated**: 2024-12-02T11:03:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-27T08:16:56Z
- **Updated**: 2024-12-02T11:03:08Z
- **Closed**: 2024-12-02T11:03:08Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 6

## Description

**What would you like to be cleaned**:

Introduce NodeWrapper for testing, similarly as we have a wrapper for creating pods.

**Why is this needed**:

Currently creating nodes for testing is quite verbose, [example](https://github.com/kubernetes-sigs/kueue/blob/560e4340b746aa811cec06b7a072a1a3faedc80f/pkg/cache/tas_cache_test.go#L48-L114).
For comparison, pods can be created much more compactly, [example](https://github.com/kubernetes-sigs/kueue/blob/560e4340b746aa811cec06b7a072a1a3faedc80f/pkg/controller/tas/topology_ungater_test.go#L143C17-L147)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T08:17:13Z

cc @mbobrovskyi @tenzen-y @kaisoz

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-11-27T13:24:29Z

/assign

I can take care of this one if this is ok for you 😊

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T13:25:19Z

sure, thanks!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-27T13:26:01Z

> /assign
> 
> I can take care of this one if this is ok for you 😊

Awsome contribution!

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-02T07:03:18Z

/reopen
To refactor remaining tests

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-02T07:03:24Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3661#issuecomment-2510728805):

>/reopen
>To refactor remaining tests


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
