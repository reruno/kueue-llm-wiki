# Issue #5523: [HELM] Allow to label and annotate the kueue-system namespace

**Summary**: [HELM] Allow to label and annotate the kueue-system namespace

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5523

**Last updated**: 2025-06-18T07:52:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwysokin](https://github.com/mwysokin)
- **Created**: 2025-06-05T16:02:32Z
- **Updated**: 2025-06-18T07:52:52Z
- **Closed**: 2025-06-18T07:52:52Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I've heard some feedback recently that our helm chart is missing the following settings:
- ~~Kueue controller manager feature gates (there is `--set "controllerManager.featureGates[0].name=TopologyAwareScheduling,controllerManager.featureGates[0].enabled=true"` but it's a bit hacky),~~
Seems like we already support it. Thanks @mbobrovskyi 🙇‍♂️
- Additional properties for the kueue-system namespace. We could start with at least labels and annotations.

**Why is this needed**:

~~Currently Kueue has some hot features that are still in alpha like TAS. It'd be good to provide a reliable and repeatable way to perform an initial installation and upgrades.~~

As for namespaces it's a common practice to use labels and annotations at the namespace level for some additional network setup like with service meshes or to enable certain monitoring features for pods within a namespace.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-05T17:49:01Z

I'd like to discourage the use of CLI arguments on the deployment for feature gates. Most features can add new configuration fields. We should either encourage the use of config map for configuration or CLI arguments. If we continue to support both it can lead to headaches. 

We allow either config map or deployment. 

https://github.com/kubernetes-sigs/kueue/blob/main/apis/config/v1beta1/configuration_types.go#L104

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-05T17:50:36Z

The second option I have no problem with.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-06-05T17:52:50Z

Yeah, I mentioned the CLI example just as hacky way of achieving this today but I agree that it's awful. That's why it'd be good to have native support for feature gates in the helm chart.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-05T18:01:11Z

We support featureGates in Helm:

https://github.com/kubernetes-sigs/kueue/blob/750dc52a707b6b7e9e7c6101c49d8bbea611d308/charts/kueue/values.yaml#L13-L16

https://github.com/kubernetes-sigs/kueue/blob/750dc52a707b6b7e9e7c6101c49d8bbea611d308/charts/kueue/templates/manager/manager.yaml#L28

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-06-05T18:12:47Z

That's great! I must've missed it!

In that case let me edit the issue  to leave only the second request.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-05T18:24:04Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T07:33:45Z

Well, it is supported, but:
1. lacks documentation in [here](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/README.md)
2. the API is very inconvenient use set via "--set" parameter, as mentioned, above, and there is no mention of using the overrides file

I don't want to scope creep the issue, but I would still propose:
1. documenting featureGates inside the HELM README.md
2. inside the helm readme add a short note indicating that for more advanced parametrization of Kueue we recommend using a local overrides file used via `--values overrides.yaml`, for example:
```yaml
controllerManager:
  replicas: 2
  manager:
    resources:
      limits:
        cpu: "2" 
        memory: 2Gi 
      requests:
        cpu: "2" 
        memory: 2Gi 
```
because often users wouldn't know that
3. add a note on that in the [Productization](https://kueue.sigs.k8s.io/docs/tasks/manage/productization/) page that if a user is customizing the local installation of Kueue, then we recommend using helm, with local overrides file) which makes it easier to update Kueue on upgrades.

wdyt @mwysokin @mbobrovskyi ?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-06-06T07:46:32Z

SGTM 🖖

I'll update the issue.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-06T08:08:42Z

> Additional properties for the kueue-system namespace. We could start with at least labels and annotations.

This is a tricky area in Helm. The helm install command uses the `--create-namespace` flag to automatically create the namespace:

```
$ helm install kueue kueue/ --create-namespace --namespace kueue-system
```

However, Helm does not support setting labels or annotations on the namespace when using `--create-namespace`, and it doesn’t provide `--labels` or `--annotations` flags.

One workaround is to add a namespace manifest (template) in the chart, but this is not a common practice in Helm. It also causes conflicts if the namespace already exists, breaking the `--create-namespace` behavior:

```
$ helm install kueue charts/kueue/ --namespace kueue-system --create-namespace

Error: INSTALLATION FAILED: 1 error occurred:
        * namespaces "kueue-system" already exists
```

Additionally, this approach breaks helm upgrade due to missing ownership metadata:

```
Error: UPGRADE FAILED: Unable to continue with update: Namespace "kueue-system" in namespace "" exists and cannot be imported into the current release: invalid ownership metadata; 
label validation error: missing key "app.kubernetes.io/managed-by": must be set to "Helm"; 
annotation validation error: missing key "meta.helm.sh/release-name": must be set to "kueue"; 
annotation validation error: missing key "meta.helm.sh/release-namespace": must be set to "kueue-system"
```

Recommendation:
The best approach is to create the namespace manually before installing the Helm chart, allowing users to set any desired labels or annotations. Alternatively, labels and annotations can be added to the namespace after the Helm install.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T08:17:17Z

> Recommendation:
The best approach is to create the namespace manually before installing the Helm chart, allowing users to set any desired labels or annotations. Alternatively, labels and annotations can be added to the namespace after the Helm install.

Sounds reasonable to me. Indeed, the lifetime of the namespace is longer than the lifetime of Kueue version (as it would typically survive upgrades). So, I can see why this is tricky.

I think preparing the kueue-system namespace with custom labels and annotations could also be part of the Productization page.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-13T14:49:41Z

@mbobrovskyi could you follow up extending (2.) with the example for setting an example feature gate, and (3.)?
