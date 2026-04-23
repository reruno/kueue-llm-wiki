# Issue #933: E2E tests: Use kindest/node image from ecr

**Summary**: E2E tests: Use kindest/node image from ecr

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/933

**Last updated**: 2023-07-06T12:23:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-29T17:03:43Z
- **Updated**: 2023-07-06T12:23:05Z
- **Closed**: 2023-07-06T12:23:04Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 4

## Description

**What would you like to be cleaned**:

The E2E test configurations use the kindest/node image. They should point to ecr.

Example:

https://github.com/kubernetes/test-infra/blob/0f79649617bb7d8035849a6e88b61a2dcb460ed8/config/jobs/kubernetes-sigs/kueue/kueue-presubmits-main.yaml#L78-L79

**Why is this needed**:

To avoid hitting the rate limit from dockerhub.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-04T18:15:11Z

/assign @trasc

### Comment by [@liangyuanpeng](https://github.com/liangyuanpeng) — 2023-07-05T13:28:24Z



> KIND v0.18.0 Comes with a big shoutout to [Docker, Inc.](https://www.docker.com/company/) for accepting us into the updated [Docker Sponsored OSS Program](https://www.docker.com/community/open-source/application/). Thanks Docker! 🎉
> Images should no longer have pull rate limits as a result.
> The project will still consider mirroring on or switching primarily to [registry.k8s.io](https://registry.k8s.io/) in the future, after determining an updated immutable tagging scheme to comply with requirements there.

The image of kind should no longer have pull rate limits as a result.

https://github.com/kubernetes-sigs/kind/releases/tag/v0.18.0

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-05T16:28:52Z

Oh, so this hasn't been a problem for us for a while. Thank you @liangyuanpeng 

Still, worth upgrading kind.

### Comment by [@trasc](https://github.com/trasc) — 2023-07-06T10:59:44Z

#953 will change the kind version

The builder image used ware changed in kubernetes/test-infra#29960
