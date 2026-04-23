# Issue #3497: Upgrade path from v0.8.0 to v0.9.0 is broken

**Summary**: Upgrade path from v0.8.0 to v0.9.0 is broken

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3497

**Last updated**: 2024-11-12T10:10:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@avrittrohwer](https://github.com/avrittrohwer)
- **Created**: 2024-11-09T01:29:54Z
- **Updated**: 2024-11-12T10:10:59Z
- **Closed**: 2024-11-12T10:10:59Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Running `kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.9.0/manifests.yaml` has two failures:

```
Error from server (Invalid): CustomResourceDefinition.apiextensions.k8s.io "multikueueclusters.kueue.x-k8s.io" is invalid: status.storedVersions[0]: Invalid value: "v1alpha1": must appear in spec.versions
Error from server (Invalid): CustomResourceDefinition.apiextensions.k8s.io "multikueueconfigs.kueue.x-k8s.io" is invalid: status.storedVersions[0]: Invalid value: "v1alpha1": must appear in spec.versions
```

This results in crash-looping kueue-controller-manager:

```
$ k get pods -n kueue-system
NAME                                        READY   STATUS             RESTARTS     AGE
kueue-controller-manager-6f8ccbd7b8-ld6qp   2/2     Running            0            53s
kueue-controller-manager-74c44b9d78-mkdfl   1/2     CrashLoopBackOff   3 (6s ago)   48s
```

**What you expected to happen**:

v0.9.0 successfully installs into a cluster with v0.8.0 installed

**How to reproduce it (as minimally and precisely as possible)**:

1. Create kind cluster
2. `kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.8.0/manifests.yaml`
3. `kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.9.0/manifests.yaml`

**Anything else we need to know?**:

Uninstalling kueue then re-installing fresh mitigates the issue.  Is not an option for customers however because it would wipe their kueue installation

**Environment**:
- Kubernetes version (use `kubectl version`):

```
Client Version: v1.31.1
Kustomize Version: v5.4.2
Server Version: v1.31.1
```

- Kueue version (use `git describe --tags --dirty --always`): v0.9.0
- Cloud provider or hardware configuration: kind
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2024-11-09T01:33:06Z

Probably has something to do with these CRDs being v1alpha1 on release-0.0.8 https://github.com/kubernetes-sigs/kueue/blob/release-0.8/charts/kueue/templates/crd/kueue.x-k8s.io_multikueueclusters.yaml and flipping to v1beta1 on release-0.9.0 https://github.com/kubernetes-sigs/kueue/blob/release-0.9/charts/kueue/templates/crd/kueue.x-k8s.io_multikueueclusters.yaml

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-09T13:48:05Z

I also noticed this.

https://github.com/kubernetes-sigs/kueue/issues/3486

I realize now that I didn’t see it again because I installed Kueue on an empty cluster.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-11T08:47:21Z

/cc @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-11T08:54:12Z

We may need to keep both versions for at least one release.

### Comment by [@trasc](https://github.com/trasc) — 2024-11-11T09:19:28Z

> We may need to keep both versions for at least one release.

Not based on [Kubernetes Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/) . `Rule #4a: API lifetime is determined by the API stability level`

```
- Alpha API versions may be removed in any release without prior deprecation notice
```

The multikueue APIs being moved from alpha to beta is documented in v0.9.0 release notes.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-11T09:27:45Z

OK. But it shouldn't crash on upgrade.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-11T10:54:32Z

## How to upgrade Kueue to 0.9.x

### 1. Backup MultiKueue Resources (skip if you are not using MultiKueue):
```
kubectl get multikueueclusters.kueue.x-k8s.io,multikueueconfigs.kueue.x-k8s.io -A -o yaml > mk.yaml
```

### 2. Update apiVersion in Backup File (skip if you are not using MultiKueue):
Replace `v1alpha1` with `v1beta1` in `mk.yaml` for all resources:
```
sed -i -e 's/v1alpha1/v1beta1/g' mk.yaml
```

### 3. Delete old CRDs:
```
kubectl delete crd multikueueclusters.kueue.x-k8s.io
kubectl delete crd multikueueconfigs.kueue.x-k8s.io
```

### 4.Install Kueue v0.9.x: 
Follow the instruction [here](https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version) to install.

### 5. Restore MultiKueue Resources (skip if you are not using MultiKueue):
```
kubectl apply -f mk.yaml
```

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2024-11-11T16:57:40Z

There are also tools like https://github.com/kubernetes-sigs/kube-storage-version-migrator which would possibly help make this kind of upgrade path easier

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-12T05:53:45Z

> There are also tools like https://github.com/kubernetes-sigs/kube-storage-version-migrator which would possibly help make this kind of upgrade path easier

I considered that, but it won't help with the installation. With this tool we need to keep both versions before migration as I mentioned here https://github.com/kubernetes-sigs/kueue/issues/3497#issuecomment-2467575772. If we have only new version we need to delete previous one and install new one.
