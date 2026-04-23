# Issue #1459: Helm install Error

**Summary**: Helm install Error

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1459

**Last updated**: 2023-12-26T08:25:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@B1F030](https://github.com/B1F030)
- **Created**: 2023-12-15T05:57:24Z
- **Updated**: 2023-12-26T08:25:18Z
- **Closed**: 2023-12-26T08:25:18Z
- **Labels**: `kind/bug`
- **Assignees**: [@B1F030](https://github.com/B1F030)
- **Comments**: 27

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
```
[root@test-1 charts]# helm install kueue kueue/ --create-namespace --namespace kueue-system
Error: INSTALLATION FAILED: unable to build kubernetes objects from release manifest:
 error validating "": error validating data: [apiVersion not set, kind not set]
```
**What you expected to happen**:
install success
**How to reproduce it (as minimally and precisely as possible)**:
```
git clone https://github.com/kubernetes-sigs/kueue.git
cd kueue/charts
helm install kueue kueue/ --create-namespace --namespace kueue-system
```
**Anything else we need to know?**:
I tried `helm template ./charts/kueue --values ./charts/kueue/values.yaml` to debug where did this error happen,
then I find out:
```
---
# Source: kueue/templates/visibility/kustomization.yaml
resources:
- apiservice.yaml
- role_binding.yaml
- service.yaml
---
```
This is where helm got Error, so I tried to remove `kueue/templates/visibility/kustomization.yaml`, it works.
So I wonder, should we remove this file?

**Environment**:
- Kubernetes version (use `kubectl version`): v1.26.0
- Kueue version (use `git describe --tags --dirty --always`): main
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools: Helm
- Others: helm version: v3.9.0

## Discussion

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-15T06:00:42Z

I can help fix that, just need to make sure if that is feasible first.
/assign

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-15T06:06:56Z

@PBundyra What do you think?

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-15T08:00:17Z

I found that this bug may not be easily fixed by removing the kustomization.yaml.
Maybe we need to keep the file, but still have to fix this bug.
I tried add apiVersion and kind for it:
```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - apiservice.yaml
  - role_binding.yaml
  - service.yaml
```
But it still don't work:
```
[root@test-1 charts]# helm install kueue kueue/ --namespace kueue-system
Error: INSTALLATION FAILED: unable to build kubernetes objects from release manifest:
 resource mapping not found for name: "" namespace: "" from "": 
no matches for kind "Kustomization" in version "kustomize.config.k8s.io/v1beta1"
```
I'll keep trying to fix this.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T08:02:10Z

@B1F030 We can remove the `kueue/templates/visibility/kustomization.yaml` file since helm doesn't recognize customization files.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T08:02:19Z

cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-15T08:19:52Z

Here is where we copy the visibility files for helm: https://github.com/kubernetes-sigs/kueue/blob/a68c95860549a85061ae53db73d32de4df3c3446/hack/update-helm.sh#L99-L120. I think we should omit this file.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T08:25:05Z

> Here is where we copy the visibility files for helm:
> 
> https://github.com/kubernetes-sigs/kueue/blob/a68c95860549a85061ae53db73d32de4df3c3446/hack/update-helm.sh#L99-L120
> 
> . I think we should omit this file.

Yes, that's right.

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-15T10:22:40Z

If we simply remove the `kustomization.yaml`, there will be new problems:
```
[root@test-1 charts]# kubectl get resourceflavor
E1215 18:17:09.715081   24954 memcache.go:255] couldn't get resource list for visibility.kueue.x-k8s.io/v1alpha1:
 the server is currently unable to handle the request
E1215 18:17:09.723755   24954 memcache.go:106] couldn't get resource list for visibility.kueue.x-k8s.io/v1alpha1:
 the server is currently unable to handle the request
No resources found
```
Is this another bug?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-15T10:40:01Z

Are you asking about `config/components/visibility/kustomization.yaml`, or  `charts/kueue/templates/visibility/kustomization.yaml`?

I think we should remove it from `charts/kueue/templates/visibility/kustomization.yaml`, and make sure it does not get copied during `./hack/update-helm.sh`. Is there an issue in that case?

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-15T10:41:59Z

> Are you asking about `config/components/visibility/kustomization.yaml`, or `charts/kueue/templates/visibility/kustomization.yaml`?

charts/kueue/templates/visibility/kustomization.yaml

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-15T10:51:34Z

Oh, in that case I'm not sure, it requires investigation.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T10:55:21Z

@B1F030 Which kubernetes version do you use? You're using v1.26.0 the same as kubectl version?

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-16T18:41:52Z

> @B1F030 Which kubernetes version do you use? You're using v1.26.0 the same as kubectl version?

yes

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-19T11:53:09Z

@B1F030 Recently, we fixed some permission errors related to the visibility server. So, could you verify if this error still happens?

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-21T05:50:33Z

> @B1F030 Recently, we fixed some permission errors related to the visibility server. So, could you verify if this error still happens?

I repulled the git repositry, and try the steps again:
```
git clone https://github.com/kubernetes-sigs/kueue.git
cd kueue/charts
helm install kueue kueue/ --namespace kueue-system
```
still the same problem...
```
[root@test-1 charts]# helm install kueue kueue/ --namespace kueue-system
Error: INSTALLATION FAILED: unable to build kubernetes objects from release manifest: 
error validating "": error validating data: [apiVersion not set, kind not set]
```
The file `kueue/templates/visibility/kustomization.yaml` still exists.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-22T06:53:13Z

> The file `kueue/templates/visibility/kustomization.yaml` still exists.

@B1F030 Yes, we haven't removed that file yet. I would like to ask if https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857626239 still happens.

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-22T06:56:55Z

> @B1F030 Yes, we haven't removed that file yet. I would like to ask if [#1459 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857626239) still happens.

Still the same. If I remove that kustomization.yaml and helm install, Errors still happen.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-22T07:00:35Z

> > @B1F030 Yes, we haven't removed that file yet. I would like to ask if [#1459 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857626239) still happens.
> 
> Still the same. If I remove that kustomization.yaml and helm install, Errors still happen.

That error happens only for helm charts? Have you seen the same error when using all-in-one installation manifests (`kubectl apply --server-side -k "github.com/kubernetes-sigs/kueue/config/default?ref=main"`) as well?

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-22T07:10:05Z

> That error happens only for helm charts? Have you seen the same error when using all-in-one installation manifests (`kubectl apply --server-side -k "github.com/kubernetes-sigs/kueue/config/default?ref=main"`) as well?

both.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-22T07:18:05Z

I could reproduce the above error in v1.26.3 cluster. Also, that error doesn't happen in v1.27.3 cluster.
If we disable VisibilityServer feature-gate in the v1.26 cluster, https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857626239 seems to happen.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-22T07:19:27Z

@B1F030 Should we work only on https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857440067 error in this issue? And then, should we work on https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857626239 in a separate issue?

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-22T07:20:00Z

> @B1F030 Should we work only on [#1459 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857440067) error in this issue? And then, should we work on [#1459 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857626239) in a separate issue?

SGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-22T07:20:45Z

@B1F030 So, can you create a PR to fix https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857440067 error?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-22T07:22:26Z

> @B1F030 So, can you create a PR to fix [#1459 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857440067) error?

I updated the above comment since I put the incorrect link :(

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-22T07:23:30Z

> @B1F030 So, can you create a PR to fix [#1459 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857440067) error?

This part could be fixed by simply remove the file `kueue/templates/visibility/kustomization.yaml`, right?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-22T07:24:40Z

> > @B1F030 So, can you create a PR to fix [#1459 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857440067) error?
> 
> This part could be fixed by simply remove the file `kueue/templates/visibility/kustomization.yaml`, right?

Also, we should improve scripts to generate helm charts:

https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857465076

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-22T07:25:18Z

> Also, we should improve scripts to generate helm charts:
> 
> [#1459 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1459#issuecomment-1857465076)

Got it. I'm glad to help.
