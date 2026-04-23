# Issue #4360: Move off of gcr for distroless base image

**Summary**: Move off of gcr for distroless base image

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4360

**Last updated**: 2025-02-24T14:31:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-02-23T21:57:24Z
- **Updated**: 2025-02-24T14:31:03Z
- **Closed**: 2025-02-24T13:58:05Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 8

## Description

From what I understand, GCR is being deprecated in March.

Kueue (and JobSet also) uses `BASE_IMAGE ?= gcr.io/distroless/static:nonroot`.

We should switch to using a registry that is not being deprecated.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-02-24T08:03:36Z

/assign @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-24T08:25:53Z

FYI this was raised as a question also here: https://github.com/GoogleContainerTools/distroless/issues/1320.

PTAL: https://github.com/GoogleContainerTools/distroless/issues/1630#issuecomment-2336467872

So it seems like maybe we could stay using gcr.io/distroless, but I'm not entirely sure.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T12:12:23Z

> FYI this was raised as a question also here: [GoogleContainerTools/distroless#1320](https://github.com/GoogleContainerTools/distroless/issues/1320).
> 
> PTAL: [GoogleContainerTools/distroless#1630 (comment)](https://github.com/GoogleContainerTools/distroless/issues/1630#issuecomment-2336467872)
> 
> So it seems like maybe we could stay using gcr.io/distroless, but I'm not entirely sure.

I know this works fine. We could find Google Cloud documentation: 

> After May 22, 2025 all requests to gcr.io endpoints are served by Artifact Registry. Any existing images in Container Registry that haven't been copied to Artifact Registry won't be available in Artifact Registry. The Artifact Registry API must be enabled to serve gcr.io endpoint requests.

https://cloud.google.com/container-registry/docs/deprecations/container-registry-deprecation#shutdown

### Comment by [@loosebazooka](https://github.com/loosebazooka) — 2025-02-24T13:18:18Z

Distroless is running on AR but serving from gcr.io. we've done a full migration.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T13:57:59Z

> Distroless is running on AR but serving from gcr.io. we've done a full migration.

Thank you for confirming that!
Let's close this for now.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-24T13:58:06Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4360#issuecomment-2678493041):

>> Distroless is running on AR but serving from gcr.io. we've done a full migration.
>
>Thank you for confirming that!
>Let's close this for now.
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-24T14:22:37Z

Sorry for the noise! I saw this last night and I was concerned. Good to know that it is not a big deal.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T14:30:58Z

/unassign @mszadkow 
/kind cleanup
