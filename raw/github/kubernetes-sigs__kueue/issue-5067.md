# Issue #5067: v0.10.1 image disappeared

**Summary**: v0.10.1 image disappeared

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5067

**Last updated**: 2025-04-22T20:21:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rptaylor](https://github.com/rptaylor)
- **Created**: 2025-04-22T17:11:43Z
- **Updated**: 2025-04-22T20:21:51Z
- **Closed**: 2025-04-22T20:21:49Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The controller manager was unavailable due to image pull failure:
```
$ sudo /usr/local/bin/crictl pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1
E0422 09:53:07.403464 2039060 remote_image.go:167] "PullImage from image service failed" err="rpc error: code = NotFound desc = failed to pull and unpack image \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1\": failed to resolve reference \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1\": us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1: not found" image="us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1"
FATA[0000] pulling image: rpc error: code = NotFound desc = failed to pull and unpack image "us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1": failed to resolve reference "us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1": us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1: not found 
```

Then new jobs could not be created in the cluster.  Is there some auto-cleanup (aka auto-disaster) policy in the image registry?

**What you expected to happen**:
The image should always remain available, so Kueue would keep running and users could still submit jobs.

**How to reproduce it (as minimally and precisely as possible)**:
`sudo /usr/local/bin/crictl pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1`

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@rptaylor](https://github.com/rptaylor) — 2025-04-22T17:13:08Z

On the same node I was able to pull 0.10.2 successfully, so it isn't a network issue:

```$ sudo /usr/local/bin/crictl pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.2
Image is up to date for sha256:78b186c64058b315e464f87aea1b1694db0a2e7f4777326a53b73eee3f4aa2f5
```

### Comment by [@rptaylor](https://github.com/rptaylor) — 2025-04-22T17:30:48Z

Might be a good idea to set IfNotPresent by default: 
https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml#L18

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-22T18:01:38Z

The main problem is that this is our staging repo and not what we expect users to pull from.

We publish these staging repos on tagged releases to registry.k8s.io.

So you should use registry.k8s.io/kueue/kueue:v0.10.1 instead of staging repo.

### Comment by [@rptaylor](https://github.com/rptaylor) — 2025-04-22T19:00:33Z

@kannon92 we're just using v0.10.1 of the Helm chart.
Is there a GA release version of the Helm chart that uses images that won't get deleted?

https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml#L17

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-22T19:32:28Z

Yes, https://github.com/kubernetes-sigs/kueue/tree/main/charts/kueue#install-chart-using-helm-v30.

For later versions of 0.10, we are publishing the charts to registry.k8s.io.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-22T19:32:36Z

cc @mimowo @tenzen-y

### Comment by [@rptaylor](https://github.com/rptaylor) — 2025-04-22T20:14:35Z

Ah hmm okay, it looks like charts started being published to oci://registry.k8s.io/kueue/charts/kueue  with version 0.10.3.

The values.yaml file in there uses the new registry:
```
  manager:
    image:
      repository: registry.k8s.io/kueue/kueue
```
but something overwrote what is in git (!!) which is a bit confusing.
Anyway we'll upgrade to the new version and registry. Thanks!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-22T20:21:45Z

Great!

I think we can close this.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-22T20:21:50Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5067#issuecomment-2822389479):

>Great!
>
>I think we can close this.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
