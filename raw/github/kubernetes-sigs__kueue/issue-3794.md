# Issue #3794: Kueue should be able to install into different namespace

**Summary**: Kueue should be able to install into different namespace

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3794

**Last updated**: 2024-12-12T09:17:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ambersun1234](https://github.com/ambersun1234)
- **Created**: 2024-12-10T13:25:24Z
- **Updated**: 2024-12-12T09:17:33Z
- **Closed**: 2024-12-12T09:17:33Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Kueue can only installed in `kueue-system` namespace\
If install it into a different namespace webhook will failed

```shell
Error from server (InternalError): error when creating "mykueue.yaml": Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.mynamespace.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s": no endpoints available for service "kueue-webhook-service"
```

**What you expected to happen**:
To work on different namespace

**How to reproduce it (as minimally and precisely as possible)**:
```shell
$ helm install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/charts/kueue \
  --version="v0.9.1" \
  --create-namespace \
  --namespace=mynamespace

$ cat mykueue.yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default-flavor

$ kubectl apply -n mynamespace -f mykueue.yaml
Error from server (InternalError): error when creating "mykueue.yaml": Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.mynamespace.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s": no endpoints available for service "kueue-webhook-service"
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.30.1
- Kueue version (use `git describe --tags --dirty --always`): 0.9.1
- Cloud provider or hardware configuration: x86_64
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04.5 LTS
- Kernel (e.g. `uname -a`): Linux 6.8.0-49-generic
- Install tools: Helm
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-11T18:51:49Z

I'm trying to reproduce this issue:

```
$ kind create cluster --image kindest/node:v1.30.0

$ helm install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/charts/kueue \
  --version="v0.9.1" \
  --create-namespace \
  --namespace=mynamespace

$ kubectl apply -f mykueue.yaml 
```

Looks like working fine.

Did I miss something?

### Comment by [@ambersun1234](https://github.com/ambersun1234) — 2024-12-12T06:01:54Z

@mbobrovskyi I forgot to include namespace in applying yaml file
the command should be `$ kubectl apply -n mynamespace -f mykueue.yaml`(I've also update the original post)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-12T08:21:18Z

> @mbobrovskyi I forgot to include namespace in applying yaml file the command should be `$ kubectl apply -n mynamespace -f mykueue.yaml`(I've also update the original post)

You don't need namespace for resourceflavor. This is cluster-scoped resource.

Anyway, it works for me too.

```
kubectl apply -n mynamespace -f mykueue.yaml
resourceflavor.kueue.x-k8s.io/default-flavor created
```

### Comment by [@ambersun1234](https://github.com/ambersun1234) — 2024-12-12T09:17:33Z

I think I found the issue, it's because kueue webhook service is not ready yet, so resource flavor will not install successfully

Thanks
