# Issue #1519: Failed to get resource list for visibility.kueue.x-k8s.io/v1alpha1

**Summary**: Failed to get resource list for visibility.kueue.x-k8s.io/v1alpha1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1519

**Last updated**: 2024-02-23T16:05:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-12-26T08:27:53Z
- **Updated**: 2024-02-23T16:05:44Z
- **Closed**: 2024-02-22T08:09:59Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Once we run `kubectl get resourceflavor`, we received the following error:

```shell
$ kubectl get resourceflavor
E1215 18:17:09.715081   24954 memcache.go:255] couldn't get resource list for visibility.kueue.x-k8s.io/v1alpha1:
 the server is currently unable to handle the request
E1215 18:17:09.723755   24954 memcache.go:106] couldn't get resource list for visibility.kueue.x-k8s.io/v1alpha1:
 the server is currently unable to handle the request
No resources found
```

**What you expected to happen**:
No error happens.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:
We found this bug in #1459

Also, we haven't faced this error in K8s v1.27, v1.28, and v1.29.

**Environment**: KinD
- Kubernetes version (use `kubectl version`): v1.26.3
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-26T08:28:07Z

cc: @mimowo @B1F030

### Comment by [@jrleslie](https://github.com/jrleslie) — 2024-02-05T14:47:08Z

@tenzen-y - are there any plans to address this one? Can confirm we're seeing the same error on kubernetes version 1.26 with latest helm chart deployment via the main branch.

### Comment by [@B1F030](https://github.com/B1F030) — 2024-02-06T03:01:04Z

If we use the default config to install kueue via helm, we can see logs in kube-apiserver like this:
```
E0206 02:48:46.207798       1 available_controller.go:527] v1alpha1.visibility.kueue.x-k8s.io failed with:
failing or missing response from https://10.233.23.237:443/apis/visibility.kueue.x-k8s.io/v1alpha1:
Get "https://10.233.23.237:443/apis/visibility.kueue.x-k8s.io/v1alpha1":
dial tcp 10.233.23.237:443: connect: connection refused
```
@jrleslie As I tried in my environment, maybe you can enable the feature `VisibilityOnDemand` in `kueue/charts/kueue/values.yaml` first, so that the error will not happen.
```
controllerManager:
  featureGates:
    - name: VisibilityOnDemand
      enabled: true
```
And I think this error may be caused by this feature too. If we want to catch the bug, this is where we can start. @tenzen-y

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-02-06T07:14:08Z

I think this is a regression on https://github.com/kubernetes/kubernetes/pull/115978, but cherry-picked to 1.26. Can you version v1.26.5?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-02-06T11:43:37Z

Let me take back the words. New clues found.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-12T15:32:39Z

The visibility server is disabled by default, so maybe that has something to do with it?

@trasc can you take a look?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-12T15:35:39Z

In helm, we could make the installation of the API optional https://github.com/kubernetes-sigs/kueue/blob/main/config/components/visibility/apiservice.yaml

But in kustomize... I guess we should comment out this line https://github.com/kubernetes-sigs/kueue/blob/4c1c6d67a3344fff3512d76b46c70aaac0bae2f5/config/default/kustomization.yaml#L20

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-12T15:35:53Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-02-15T15:49:26Z

We can add a dedicated overlay like we have for prometheus, and include it in [alpha-enabled](https://github.com/kubernetes-sigs/kueue/tree/main/config/alpha-enabled) as well. For help maybe add `enableVisibility` value.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-15T16:34:30Z

Those sound like good plans

### Comment by [@minierm](https://github.com/minierm) — 2024-02-23T16:05:30Z

FYI and help others until the issue is fixed:
I enabled the feature by adding a line after 11182 in manifests.yaml and no errors anymore:

      containers:
      - args:
        - --config=/controller_manager_config.yaml
        - --zap-log-level=2
**+        - --feature-gates=VisibilityOnDemand=true**
        command:
        - /manager
