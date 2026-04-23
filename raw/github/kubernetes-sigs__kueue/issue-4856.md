# Issue #4856: getting ImagePullBackOff for registry.k8s.io/kueue/kueue:v0.11.2

**Summary**: getting ImagePullBackOff for registry.k8s.io/kueue/kueue:v0.11.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4856

**Last updated**: 2025-04-01T22:58:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@linde](https://github.com/linde)
- **Created**: 2025-04-01T17:53:24Z
- **Updated**: 2025-04-01T22:58:25Z
- **Closed**: 2025-04-01T22:58:24Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 4

## Description


**What happened**:

was following [instructions for kubectl](https://kueue.sigs.k8s.io/docs/installation/#install-by-kubectl) and getting the following error on my pod for the `kueue-controller-manager` deployment:

```
     message: 'Back-off pulling image "registry.k8s.io/kueue/kueue:v0.11.2": ErrImagePull:
          failed to pull and unpack image "registry.k8s.io/kueue/kueue:v0.11.2": failed
          to copy: httpReadSeeker: failed open: failed to do request: Get "https://prod-registry-k8s-io-us-west-1.s3.dualstack.us-west-1.amazonaws.com/containers/images/sha256:74cc41449ca0c2c41ff5cd98432743520660f10cea552767289c0d2cf6be251b":
          dial tcp: lookup prod-registry-k8s-io-us-west-1.s3.dualstack.us-west-1.amazonaws.com
          on [2001:4860:4860::8844]:53: read udp [fc00:f853:ccd:e793::2]:48433->[2001:4860:4860::8844]:53:
          i/o timeout'
        reason: ImagePullBackOff
```
it is on a local kind cluster created in a vanilla way.

**What you expected to happen**:

successful installation!


**How to reproduce it (as minimally and precisely as possible)**:

```
kind create cluster --name=queue
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.11.2/manifests.yaml
```


**Anything else we need to know?**:

seems just like the image needs to be published.

**Environment**:

- Kubernetes version (use `kubectl version`):

```
$ kind version
kind v0.26.0 go1.24-20241213-RC00 cl/706019355 +e39e965e0e X:fieldtrack,boringcrypto linux/amd64
$ kubectl version
Client Version: v1.32.2
Kustomize Version: v5.5.0
Server Version: v1.32.0
$ uname -a
Linux stevenlinde58 6.12.12-1rodete2-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.12-1rodete2 (2025-02-28) x86_64 GNU/Linux
```

- Kueue version (use `git describe --tags --dirty --always`):

didn't clone the repo, but it's `kueue:v0.11.2` based on the image URL.

## Discussion

### Comment by [@linde](https://github.com/linde) — 2025-04-01T18:06:15Z

fwiw, the helm installation instructions also have a similar error:

```
$ helm install kueue oci://registry.k8s.io/kueue/charts/kueue \
  --version=0.11.2 \
  --namespace  kueue-system \
  --create-namespace \
  --wait --timeout 300s
Error: INSTALLATION FAILED: failed to copy: httpReadSeeker: failed open: failed to do request: Get "https://prod-registry-k8s-io-us-west-1.s3.dualstack.us-west-1.amazonaws.com/containers/images/sha256:77338a332f45d0d2ce5c018a739040ad9a9e878d21ab8544cf81c59839dcfdad": dial tcp: lookup prod-registry-k8s-io-us-west-1.s3.dualstack.us-west-1.amazonaws.com on 127.0.0.1:53: server misbehaving
```

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-01T18:31:41Z

/remove-kind bug
/kind support

Looking at your logs, I think you are hitting some environment issues.

```bash
podman inspect registry.k8s.io/kueue/kueue:v0.11.2
[
     {
          "Id": "74cc41449ca0c2c41ff5cd98432743520660f10cea552767289c0d2cf6be251b",
          "Digest": "sha256:a528976c99334226e3f6edf817610f93aefa213e519142ae1d4876cb93c24215",
          "RepoTags": [
               "registry.k8s.io/kueue/kueue:v0.11.2"
          ],
          "RepoDigests": [
               "registry.k8s.io/kueue/kueue@sha256:516dbe9dfba224936b1a9f01fd93f0d4a17de7284b4751803ac065a48b0d37c7",
               "registry.k8s.io/kueue/kueue@sha256:a528976c99334226e3f6edf817610f93aefa213e519142ae1d4876cb93c24215"
          ],

```

I just pulled the image and it was found correctly.

Your logs:

```
          failed to pull and unpack image "registry.k8s.io/kueue/kueue:v0.11.2": failed
          to copy: httpReadSeeker: failed open: failed to do request: Get "https://prod-registry-k8s-io-us-west-1.s3.dualstack.us-west-1.amazonaws.com/containers/images/sha256:74cc41449ca0c2c41ff5cd98432743520660f10cea552767289c0d2cf6be251b":
          dial tcp: lookup prod-registry-k8s-io-us-west-1.s3.dualstack.us-west-1.amazonaws.com
          on [2001:4860:4860::8844]:53: read udp [fc00:f853:ccd:e793::2]:48433->[2001:4860:4860::8844]:53:
          i/o timeout'
        reason: ImagePullBackOff
```

It sounds like there is something going wrong with your aws registry.

### Comment by [@linde](https://github.com/linde) — 2025-04-01T22:46:28Z

oh, interesting -- thanks so much for the quick response. let me check more in my environment.

### Comment by [@linde](https://github.com/linde) — 2025-04-01T22:58:24Z

yes, confirmed. it was a DNS issue in my environment. sorry for the bother!
