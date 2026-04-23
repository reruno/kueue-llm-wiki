# Issue #4143: Kueue helm charts 0.8.X (0.8.3 0.8.2 0.8.1 0.8.0) have been deleted from registry

**Summary**: Kueue helm charts 0.8.X (0.8.3 0.8.2 0.8.1 0.8.0) have been deleted from registry

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4143

**Last updated**: 2025-02-25T16:50:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mtparet](https://github.com/mtparet)
- **Created**: 2025-02-04T09:04:41Z
- **Updated**: 2025-02-25T16:50:15Z
- **Closed**: 2025-02-21T18:56:24Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 24

## Description

**What happened**:

v0.8.x images disappeared from container registry.

```
$ docker pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.8.3
Error response from daemon: manifest for us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.8.3 not found: manifest unknown: Failed to fetch "v0.8.3"
```

```
$ docker pull us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1
v0.10.1: Pulling from k8s-staging-images/kueue/kueue
688513194d7a: Pull complete
bfb59b82a9b6: Pull complete
efa9d1d5d3a2: Pull complete
a62778643d56: Pull complete
7c12895b777b: Pull complete
3214acf345c0: Pull complete
5664b15f108b: Pull complete
0bab15eea81d: Pull complete
4aa0ea1413d3: Pull complete
da7816fa955e: Pull complete
9aee425378d2: Pull complete
905a5f508b4e: Pull complete
Digest: sha256:60f813c1ba2fd1b94d2345957e7690b61bc716f5725d20bb08ac4239cd9433a8
Status: Downloaded newer image for us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1
us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.10.1
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-04T10:32:24Z

The released image is published to registry.k8s.io/kueue/kueue. So, could you try `registry.k8s.io/kueue/kueue:v0.8.3`?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-04T10:32:36Z

/remove-kind bug
/kind support

### Comment by [@mtparet](https://github.com/mtparet) — 2025-02-04T14:48:16Z

Good know because the helm chart is pointing to it https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml#L19

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-04T14:53:02Z

> Good know because the helm chart is pointing to it https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml#L19

Here, we have released Chart, and then it uses the released image registry: 
- https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.3
- https://github.com/kubernetes-sigs/kueue/releases/download/v0.8.3/kueue-chart-v0.8.3.tgz

### Comment by [@mtparet](https://github.com/mtparet) — 2025-02-04T14:54:31Z

Thank you !

### Comment by [@mtparet](https://github.com/mtparet) — 2025-02-04T16:05:19Z

There is the same issue at the helm chart layer https://github.com/kubernetes-sigs/kueue/tree/main/charts/kueue#install-chart-using-helm-v30 

It indicates  `helm install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/charts/kueue --version="v0.10.1"` 

but for 0.8.3 it does not exist anymore, do you have any published version to registry.k8s.io too ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-05T10:28:54Z

Good point, we don't publish charts into `registry.k8s.io` which makes them disappear after 90 days. I guess we could extend the docs to show how to use the tgz helm charts for that. 

Also, in a longer run we could consider "promoting" the charts to `registry.k8s.io` as we do it for images, but it requires a but of research. Here is an example how we promote an image: https://github.com/kubernetes/k8s.io/pull/7696. Not sure the same method would work for charts, probably not

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-05T12:56:40Z

> Good point, we don't publish charts into `registry.k8s.io` which makes them disappear after 90 days. I guess we could extend the docs to show how to use the tgz helm charts for that.
> 
> Also, in a longer run we could consider "promoting" the charts to `registry.k8s.io` as we do it for images, but it requires a but of research. Here is an example how we promote an image: [kubernetes/k8s.io#7696](https://github.com/kubernetes/k8s.io/pull/7696). Not sure the same method would work for charts, probably not

That sounds reasonable. I'm wondering if we can install chart with `helm install kueue https://github.com/kubernetes-sigs/kueue/releases/download/v0.8.3/kueue-chart-v0.8.3.tgz`.

@mtparet Could you check it? If this works fine, we can mention it in our documentations.

### Comment by [@mtparet](https://github.com/mtparet) — 2025-02-05T16:33:19Z

We are using fluxcd and it does not seems supporting referencing directly a version .tgz https://fluxcd.io/flux/components/source/helmrepositories/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-06T07:42:24Z

/retitle Kueue helm charts 0.8.X (0.8.3 0.8.2 0.8.1 0.8.0) have been deleted from registry

Proposal, to scope the remaining issue clearly by title, WDYT @mtparet ?

### Comment by [@mtparet](https://github.com/mtparet) — 2025-02-06T08:13:45Z

Thanks, that's the real issue at the end (images are ok when properly registry is used)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-08T16:25:36Z

/remove-kind support
/kind feature

We need to investigate how we can register the Helm Chart OCI image as a persistent one.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-18T09:01:47Z

Asked on slack k8s-infra channel: https://kubernetes.slack.com/archives/CCK68P2Q2/p1739869280030129, let's see what is the recommendation.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-21T12:02:31Z

> Asked on slack k8s-infra channel: https://kubernetes.slack.com/archives/CCK68P2Q2/p1739869280030129, let's see what is the recommendation.

We discussed which solutions we should take based on https://docs.google.com/document/d/1xa2me_O0N5sHMD_np9ztr2O9GL3uX1yKBgDcApDqV_8/.

In conclusion, we decided to take the `Model1` to provide complete compatibility for Helm.
Thank you for this great investigation, @mimowo !

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-21T12:32:19Z

Promotion Hashes are the following:

- v0.8.4: This has already been removed

- v0.9.3: https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/charts/kueue/sha256:577b280e31a978a82d82da097c236b8ec4ae8323f1c3bfcc06d25eed45d0d874?inv=1&invt=AbqKYQ

```shell
$ git log --oneline --no-abbrev-commit 
269534b66ad20657c852ee4756721586653b59cc (HEAD, tag: v0.9.3) Prepare v0.9.3 (#4010)
```

- v0.10.1: https://console.cloud.google.com/artifacts/docker/k8s-staging-images/us-central1/charts/kueue/sha256:56acd0d3805fee0ec8f071e0dfa41b926d4e5b6f5cf60436ffa42300f6dc17d5?inv=1&invt=AbqKYQ

```shell
$ git log --oneline --no-abbrev-commit 
404a0cd659b2331b232cf5ddf93a1b67d5cc146c (HEAD, tag: v0.10.1) Prepare release v0.10.1 (#4011)
````

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-21T17:13:00Z

I verified the released images work fine in the following. @mtparet Could you verify if these work fine as well?

- v0.9.3

```shell
$ helm install kueue oci://registry.k8s.io/charts/kueue --version=v0.9.3 --namespace kueue-system
Pulled: registry.k8s.io/charts/kueue:v0.9.3
Digest: sha256:577b280e31a978a82d82da097c236b8ec4ae8323f1c3bfcc06d25eed45d0d874
NAME: kueue
LAST DEPLOYED: Sat Feb 22 02:11:04 2025
NAMESPACE: kueue-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

- v0.10.1

```shell
$ helm install kueue oci://registry.k8s.io/charts/kueue --version=v0.10.1 --namespace kueue-system
Pulled: registry.k8s.io/charts/kueue:v0.10.1
Digest: sha256:56acd0d3805fee0ec8f071e0dfa41b926d4e5b6f5cf60436ffa42300f6dc17d5
NAME: kueue
LAST DEPLOYED: Sat Feb 22 02:08:29 2025
NAMESPACE: kueue-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-21T17:20:08Z

/assign @mimowo @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-21T17:27:12Z

The remaining work:
- update the README for the installation of Kueue from Helm
- update the release steps with the step to promote the 
- (optional) but I think would be nice: apply for ownership of the charts folder with images in kubernetes/k8s.io. The k8s infra team seemed ok with giving that ownership.

Then, I would close

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-21T17:32:18Z

> update the README for the installation of Kueue from Helm


I would add Helm installation to the documentation instead of README since we want to keep minimized README.
We pointed the installation guide: https://github.com/kubernetes-sigs/kueue?tab=readme-ov-file#installation

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-21T17:33:43Z

> I would add Helm installation to the documentation instead of README since we want to keep minimized README.

sgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-21T18:56:19Z

> The remaining work:
> 
> * update the README for the installation of Kueue from Helm
> * update the release steps with the step to promote the
> * (optional) but I think would be nice: apply for ownership of the charts folder with images in kubernetes/k8s.io. The k8s infra team seemed ok with giving that ownership.
> 
> Then, I would close

I think all including optional task done.
/close

@mtparet If you face different / same issue, feel free to open issues. Thank you for reporting this problems!

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-21T18:56:25Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4143#issuecomment-2675313969):

>> The remaining work:
>> 
>> * update the README for the installation of Kueue from Helm
>> * update the release steps with the step to promote the
>> * (optional) but I think would be nice: apply for ownership of the charts folder with images in kubernetes/k8s.io. The k8s infra team seemed ok with giving that ownership.
>> 
>> Then, I would close
>
>I think all including optional task done.
>/close
>
>@mtparet If you face different / same issue, feel free to open issues. Thank you for reporting this problems!
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-25T16:45:20Z

> I verified the released images work fine in the following. [@mtparet](https://github.com/mtparet) Could you verify if these work fine as well?
> 
> * v0.9.3
> 
> $ helm install kueue oci://registry.k8s.io/charts/kueue --version=v0.9.3 --namespace kueue-system
> Pulled: registry.k8s.io/charts/kueue:v0.9.3
> Digest: sha256:577b280e31a978a82d82da097c236b8ec4ae8323f1c3bfcc06d25eed45d0d874
> NAME: kueue
> LAST DEPLOYED: Sat Feb 22 02:11:04 2025
> NAMESPACE: kueue-system
> STATUS: deployed
> REVISION: 1
> TEST SUITE: None
> * v0.10.1
> 
> $ helm install kueue oci://registry.k8s.io/charts/kueue --version=v0.10.1 --namespace kueue-system
> Pulled: registry.k8s.io/charts/kueue:v0.10.1
> Digest: sha256:56acd0d3805fee0ec8f071e0dfa41b926d4e5b6f5cf60436ffa42300f6dc17d5
> NAME: kueue
> LAST DEPLOYED: Sat Feb 22 02:08:29 2025
> NAMESPACE: kueue-system
> STATUS: deployed
> REVISION: 1
> TEST SUITE: None

We see a slight problem in this previous release process only for v0.9.3 and v0.10.1.
The helm chart image is appropriately promoted to registry.k8s.io/charts/kueue and persistence. However, the persistence helm chart (`registry.k8s.io/charts/kueue`) is using staging image (`us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue`) and we can not re-release the same OCI image based on infrastructure specification.

So, we highly recommend to replace kueue-controller-manager image with promoted image (`registry.k8s.io/kueue/kueue`) by your values.yaml.

cc: @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-25T16:50:12Z

We also released 0.9.4 and 0.10.2 already which don't have the issue, so we recommend to start using new latest patch releases.
