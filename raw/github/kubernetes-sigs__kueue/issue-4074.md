# Issue #4074: Failed to restart microshift cluster after install kueue

**Summary**: Failed to restart microshift cluster after install kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4074

**Last updated**: 2025-01-29T14:45:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yasaidev](https://github.com/yasaidev)
- **Created**: 2025-01-28T09:09:19Z
- **Updated**: 2025-01-29T14:45:53Z
- **Closed**: 2025-01-29T14:45:51Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


## **What happened**:

After installing Kueue on MicroShift following the official guide, I restarted the cluster using `systemctl restart microshift`. However, the cluster failed to start due to an error.

When I remove Kueue, the cluster starts without issues.


## **What you expected to happen**:

The cluster should successfully restart even after Kueue is installed.

## **How to reproduce it (as minimally and precisely as possible)**:

1. Set up the MicroShift cluster as described in [the official documentation](https://docs.redhat.com/ja/documentation/red_hat_build_of_microshift/4.12/html-single/installing/index#microshift-install-rpm-preparing_microshift-install-rpm)  

2. Install Kueue by running:
   ```sh
   kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.10.1/manifests.yaml
   ```
3. Restart the MicroShift cluster:
   ```sh
   systemctl restart microshift
   ```
   This results in an error:
   ```sh
   Job for microshift.service failed because the service did not take the steps required by its unit configuration.
   See "systemctl status microshift.service" and "journalctl -xeu microshift.service" for details.
   ```

## **Anything else we need to know?**:
I attached [jornalctl_microshift_n_5000.log](https://github.com/user-attachments/files/18570808/jornalctl_microshift.log)  to this issue.

From log, it seems that the key error is `Internal error occurred: failed calling webhook \"mdeployment.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s\": no endpoints available for service \"kueue-webhook-service\"" service="infrastructure-services-manager" since-start="86.252342ms"`.

But, I think I have deployed `kueue-webhook-servise` via manifests.yaml.

### `journalctl -xeu microshift | grep -i "kueue"`  
```
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.345389  779521 patch_genericapiserver.go:201] Loopback request to "/api/v1/namespaces/kueue-system" (user agent "kubectl/4.16.0 (linux/arm64) kubernetes/cf533b5") before server is ready. This client probably does not watch /readyz and might get inconsistent answers.
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.426036  779521 controller.go:222] Updating CRD OpenAPI spec because admissionchecks.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.426092  779521 controller.go:222] Updating CRD OpenAPI spec because clusterqueues.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.426119  779521 controller.go:222] Updating CRD OpenAPI spec because cohorts.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.426300  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.426781  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1alpha1 to ResourceManager
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428081  779521 controller.go:222] Updating CRD OpenAPI spec because localqueues.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428159  779521 controller.go:222] Updating CRD OpenAPI spec because multikueueclusters.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428180  779521 controller.go:222] Updating CRD OpenAPI spec because multikueueconfigs.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428241  779521 controller.go:222] Updating CRD OpenAPI spec because provisioningrequestconfigs.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428305  779521 controller.go:222] Updating CRD OpenAPI spec because resourceflavors.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428398  779521 controller.go:222] Updating CRD OpenAPI spec because topologies.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428467  779521 controller.go:222] Updating CRD OpenAPI spec because workloadpriorityclasses.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428485  779521 controller.go:222] Updating CRD OpenAPI spec because workloads.kueue.x-k8s.io changed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.428986  779521 patch_genericapiserver.go:201] Loopback request to "/apis/apiextensions.k8s.io/v1/customresourcedefinitions/resourceflavors.kueue.x-k8s.io/status" (user agent "microshift/v1.29.10 (linux/arm64) kubernetes/67d3387") before server is ready. This client probably does not watch /readyz and might get inconsistent answers.
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.432909  779521 patch_genericapiserver.go:201] Loopback request to "/apis/apiextensions.k8s.io/v1/customresourcedefinitions/clusterqueues.kueue.x-k8s.io/status" (user agent "microshift/v1.29.10 (linux/arm64) kubernetes/67d3387") before server is ready. This client probably does not watch /readyz and might get inconsistent answers.
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.439618  779521 handler.go:275] Adding GroupVersion visibility.kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.441898  779521 handler.go:275] Adding GroupVersion visibility.kueue.x-k8s.io v1alpha1 to ResourceManager
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver E0128 17:55:32.447691  779521 controller.go:146] Error updating APIService "v1alpha1.visibility.kueue.x-k8s.io" with err: failed to download v1alpha1.visibility.kueue.x-k8s.io: failed to retrieve openAPI spec, http error: ResponseCode: 503, Body: service unavailable
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver E0128 17:55:32.447800  779521 controller.go:146] Error updating APIService "v1beta1.visibility.kueue.x-k8s.io" with err: failed to download v1beta1.visibility.kueue.x-k8s.io: failed to retrieve openAPI spec, http error: ResponseCode: 503, Body: service unavailable
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver E0128 17:55:32.447854  779521 handler_proxy.go:146] error resolving kueue-system/kueue-visibility-server: no endpoints available for service "kueue-visibility-server"
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver E0128 17:55:32.449128  779521 handler_proxy.go:146] error resolving kueue-system/kueue-visibility-server: no endpoints available for service "kueue-visibility-server"
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.478595  779521 store.go:1579] "Monitoring resource count at path" resource="resourceflavors.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/resourceflavors"
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.480446  779521 cacher.go:461] cacher (resourceflavors.kueue.x-k8s.io): initialized
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.480700  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=ResourceFlavor from storage/cacher.go:/kueue.x-k8s.io/resourceflavors
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.485247  779521 crd_finalizer.go:243] resourceflavors.kueue.x-k8s.io waiting for 1 items to be removed
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.502581  779521 store.go:1579] "Monitoring resource count at path" resource="clusterqueues.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/clusterqueues"
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.506066  779521 cacher.go:461] cacher (clusterqueues.kueue.x-k8s.io): initialized
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.506117  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=ClusterQueue from storage/cacher.go:/kueue.x-k8s.io/clusterqueues
 1月 28 17:55:32 jetson07 microshift[779521]: kube-apiserver I0128 17:55:32.519475  779521 crd_finalizer.go:243] clusterqueues.kueue.x-k8s.io waiting for 2 items to be removed
 1月 28 17:55:33 jetson07 microshift[779521]: kube-apiserver E0128 17:55:33.439885  779521 controller.go:102] loading OpenAPI spec for "v1beta1.visibility.kueue.x-k8s.io" failed with: failed to download v1beta1.visibility.kueue.x-k8s.io: failed to retrieve openAPI spec, http error: ResponseCode: 503, Body: service unavailable
 1月 28 17:55:33 jetson07 microshift[779521]: kube-apiserver I0128 17:55:33.439902  779521 controller.go:109] OpenAPI AggregationController: action for item v1beta1.visibility.kueue.x-k8s.io: Rate Limited Requeue.
 1月 28 17:55:33 jetson07 microshift[779521]: kube-apiserver E0128 17:55:33.441890  779521 controller.go:102] loading OpenAPI spec for "v1alpha1.visibility.kueue.x-k8s.io" failed with: failed to download v1alpha1.visibility.kueue.x-k8s.io: failed to retrieve openAPI spec, http error: ResponseCode: 503, Body: service unavailable
 1月 28 17:55:33 jetson07 microshift[779521]: kube-apiserver I0128 17:55:33.441905  779521 controller.go:109] OpenAPI AggregationController: action for item v1alpha1.visibility.kueue.x-k8s.io: Rate Limited Requeue.
 1月 28 17:55:33 jetson07 microshift[779521]: kube-apiserver E0128 17:55:33.442106  779521 controller.go:113] loading OpenAPI spec for "v1beta1.visibility.kueue.x-k8s.io" failed with: Error, could not get list of group versions for APIService
 1月 28 17:55:33 jetson07 microshift[779521]: kube-apiserver I0128 17:55:33.442922  779521 controller.go:126] OpenAPI AggregationController: action for item v1beta1.visibility.kueue.x-k8s.io: Rate Limited Requeue.
 1月 28 17:55:33 jetson07 microshift[779521]: kube-apiserver E0128 17:55:33.443010  779521 controller.go:113] loading OpenAPI spec for "v1alpha1.visibility.kueue.x-k8s.io" failed with: Error, could not get list of group versions for APIService
 1月 28 17:55:33 jetson07 microshift[779521]: kube-apiserver I0128 17:55:33.443147  779521 controller.go:126] OpenAPI AggregationController: action for item v1alpha1.visibility.kueue.x-k8s.io: Rate Limited Requeue.
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.399185  779521 controller.go:222] Updating CRD OpenAPI spec because admissionchecks.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.399569  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.416492  779521 controller.go:222] Updating CRD OpenAPI spec because admissionchecks.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.497397  779521 crd_finalizer.go:243] resourceflavors.kueue.x-k8s.io waiting for 1 items to be removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.507203  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1alpha1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.507486  779521 controller.go:222] Updating CRD OpenAPI spec because cohorts.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.524263  779521 controller.go:222] Updating CRD OpenAPI spec because cohorts.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.525354  779521 crd_finalizer.go:243] clusterqueues.kueue.x-k8s.io waiting for 2 items to be removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.534005  779521 controller.go:222] Updating CRD OpenAPI spec because localqueues.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.534824  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.551421  779521 controller.go:222] Updating CRD OpenAPI spec because localqueues.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.552291  779521 controller.go:222] Updating CRD OpenAPI spec because multikueueclusters.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.552407  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.553033  779521 store.go:1579] "Monitoring resource count at path" resource="admissionchecks.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/admissionchecks"
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.555089  779521 cacher.go:461] cacher (admissionchecks.kueue.x-k8s.io): initialized
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.555171  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=AdmissionCheck from storage/cacher.go:/kueue.x-k8s.io/admissionchecks
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.564308  779521 controller.go:222] Updating CRD OpenAPI spec because multikueueconfigs.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.564466  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.569303  779521 controller.go:210] Updating CRD OpenAPI spec because admissionchecks.kueue.x-k8s.io was removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.569557  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.575375  779521 controller.go:222] Updating CRD OpenAPI spec because provisioningrequestconfigs.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.575558  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.578418  779521 store.go:1579] "Monitoring resource count at path" resource="cohorts.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/cohorts"
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.580581  779521 cacher.go:461] cacher (cohorts.kueue.x-k8s.io): initialized
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.580647  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1alpha1, Kind=Cohort from storage/cacher.go:/kueue.x-k8s.io/cohorts
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.581524  779521 controller.go:222] Updating CRD OpenAPI spec because multikueueclusters.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.600223  779521 store.go:1579] "Monitoring resource count at path" resource="localqueues.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/localqueues"
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.602745  779521 cacher.go:461] cacher (localqueues.kueue.x-k8s.io): initialized
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.602794  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=LocalQueue from storage/cacher.go:/kueue.x-k8s.io/localqueues
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.604538  779521 controller.go:210] Updating CRD OpenAPI spec because cohorts.kueue.x-k8s.io was removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.604618  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1alpha1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.608739  779521 controller.go:222] Updating CRD OpenAPI spec because topologies.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.608761  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1alpha1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.621292  779521 store.go:1579] "Monitoring resource count at path" resource="multikueueclusters.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/multikueueclusters"
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.621403  779521 controller.go:222] Updating CRD OpenAPI spec because multikueueconfigs.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.624316  779521 cacher.go:461] cacher (multikueueclusters.kueue.x-k8s.io): initialized
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.624604  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=MultiKueueCluster from storage/cacher.go:/kueue.x-k8s.io/multikueueclusters
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.626162  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.626196  779521 controller.go:222] Updating CRD OpenAPI spec because workloadpriorityclasses.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.628041  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.628588  779521 controller.go:210] Updating CRD OpenAPI spec because localqueues.kueue.x-k8s.io was removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.640448  779521 store.go:1579] "Monitoring resource count at path" resource="multikueueconfigs.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/multikueueconfigs"
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.640489  779521 controller.go:222] Updating CRD OpenAPI spec because provisioningrequestconfigs.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.642391  779521 cacher.go:461] cacher (multikueueconfigs.kueue.x-k8s.io): initialized
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.642494  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=MultiKueueConfig from storage/cacher.go:/kueue.x-k8s.io/multikueueconfigs
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.643681  779521 controller.go:210] Updating CRD OpenAPI spec because multikueueclusters.kueue.x-k8s.io was removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.643692  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.660614  779521 store.go:1579] "Monitoring resource count at path" resource="provisioningrequestconfigs.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/provisioningrequestconfigs"
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.660830  779521 controller.go:222] Updating CRD OpenAPI spec because topologies.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.663659  779521 cacher.go:461] cacher (provisioningrequestconfigs.kueue.x-k8s.io): initialized
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.663724  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=ProvisioningRequestConfig from storage/cacher.go:/kueue.x-k8s.io/provisioningrequestconfigs
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.666083  779521 controller.go:210] Updating CRD OpenAPI spec because multikueueconfigs.kueue.x-k8s.io was removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.666441  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.676061  779521 controller.go:222] Updating CRD OpenAPI spec because workloadpriorityclasses.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.679408  779521 controller.go:210] Updating CRD OpenAPI spec because provisioningrequestconfigs.kueue.x-k8s.io was removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.679477  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.689243  779521 store.go:1579] "Monitoring resource count at path" resource="topologies.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/topologies"
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.692426  779521 cacher.go:461] cacher (topologies.kueue.x-k8s.io): initialized
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.692711  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1alpha1, Kind=Topology from storage/cacher.go:/kueue.x-k8s.io/topologies
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.707013  779521 store.go:1579] "Monitoring resource count at path" resource="workloadpriorityclasses.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/workloadpriorityclasses"
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.708873  779521 cacher.go:461] cacher (workloadpriorityclasses.kueue.x-k8s.io): initialized
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.708927  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=WorkloadPriorityClass from storage/cacher.go:/kueue.x-k8s.io/workloadpriorityclasses
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.709875  779521 controller.go:210] Updating CRD OpenAPI spec because topologies.kueue.x-k8s.io was removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.717062  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.717077  779521 controller.go:210] Updating CRD OpenAPI spec because workloadpriorityclasses.kueue.x-k8s.io was removed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.772824  779521 controller.go:222] Updating CRD OpenAPI spec because workloads.kueue.x-k8s.io changed
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.772866  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:37 jetson07 microshift[779521]: kube-apiserver I0128 17:55:37.949791  779521 controller.go:222] Updating CRD OpenAPI spec because workloads.kueue.x-k8s.io changed
 1月 28 17:55:38 jetson07 microshift[779521]: kube-apiserver I0128 17:55:38.015040  779521 store.go:1579] "Monitoring resource count at path" resource="workloads.kueue.x-k8s.io" path="<storage-prefix>//kueue.x-k8s.io/workloads"
 1月 28 17:55:38 jetson07 microshift[779521]: kube-apiserver I0128 17:55:38.016994  779521 cacher.go:461] cacher (workloads.kueue.x-k8s.io): initialized
 1月 28 17:55:38 jetson07 microshift[779521]: kube-apiserver I0128 17:55:38.017181  779521 reflector.go:351] Caches populated for kueue.x-k8s.io/v1beta1, Kind=Workload from storage/cacher.go:/kueue.x-k8s.io/workloads
 1月 28 17:55:38 jetson07 microshift[779521]: kube-apiserver I0128 17:55:38.241826  779521 handler.go:275] Adding GroupVersion kueue.x-k8s.io v1beta1 to ResourceManager
 1月 28 17:55:38 jetson07 microshift[779521]: kube-apiserver I0128 17:55:38.242564  779521 controller.go:210] Updating CRD OpenAPI spec because workloads.kueue.x-k8s.io was removed
 1月 28 17:55:39 jetson07 microshift[779521]: kube-apiserver W0128 17:55:39.893221  779521 dispatcher.go:225] Failed calling webhook, failing closed mdeployment.kb.io: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service"
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager W0128 17:55:39.896032  779521 recorder_logging.go:53] &Event{ObjectMeta:{dummy.181ecf653abfee97  dummy    0 0001-01-01 00:00:00 +0000 UTC <nil> <nil> map[] map[] [] [] []},InvolvedObject:ObjectReference{Kind:Pod,Namespace:dummy,Name:dummy,UID:,APIVersion:v1,ResourceVersion:,FieldPath:,},Reason:DeploymentUpdateFailed,Message:Failed to update Deployment.apps/service-ca -n openshift-service-ca: Internal error occurred: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service",Source:EventSource{Component:,Host:,},FirstTimestamp:2025-01-28 17:55:39.895893655 +0900 JST m=+81.618815254,LastTimestamp:2025-01-28 17:55:39.895893655 +0900 JST m=+81.618815254,Count:1,Type:Warning,EventTime:0001-01-01 00:00:00 +0000 UTC,Series:nil,Action:,Related:nil,ReportingController:,ReportingInstance:,}
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager W0128 17:55:39.896066  779521 apps.go:101] Failed to apply apps api components/service-ca/deployment.yaml: Internal error occurred: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service"
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager W0128 17:55:39.896091  779521 controllers.go:99] Failed to apply apps [components/service-ca/deployment.yaml]: Internal error occurred: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service"
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager W0128 17:55:39.896104  779521 components.go:13] Failed to start service-ca controller: Internal error occurred: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service"
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager E0128 17:55:39.896141  779521 manager.go:132] "SERVICE FAILED - stopping MicroShift" err="Internal error occurred: failed calling webhook \"mdeployment.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s\": no endpoints available for service \"kueue-webhook-service\"" service="infrastructure-services-manager" since-start="86.252342ms"
 1月 28 17:55:40 jetson07 microshift[779521]: kubelet I0128 17:55:40.963540  779521 kubelet.go:2447] "SyncLoop ADD" source="api" pods=["mpi-operator/mpi-operator-7477b5bdbd-8mhdk","openshift-dns/dns-default-j8xf6","openshift-ovn-kubernetes/ovnkube-node-67tzf","kube-system/csi-snapshot-controller-76f8596b6-v2tgl","default/job-test-multi-cluster-lsfqj","default/job-test-multi-cluster-nzqqv","openshift-ovn-kubernetes/ovnkube-master-hc8ld","default/job-test-multi-cluster-5fkt6","kueue-system/kueue-controller-manager-6bcc4495d-dwmxv","nvidia-device-plugin/nvidia-device-plugin-daemonset-xb55m","openshift-storage/topolvm-controller-7948bc7c65-qzrp7","kubeflow/training-operator-6f4d5d95f8-8lsv8","jobset-system/jobset-controller-manager-64bb765c4c-v7vgv","kube-system/csi-snapshot-webhook-586884d57b-8hvcz","openshift-dns/node-resolver-bqw7v","openshift-ingress/router-default-85d97687d6-zrlpm","openshift-service-ca/service-ca-559647f8b-7kxht","openshift-storage/topolvm-node-8nwdc","default/job-teste-87rqb"]
 1月 28 17:55:40 jetson07 microshift[779521]: kubelet I0128 17:55:40.976979  779521 topology_manager.go:215] "Topology Admit Handler" podUID="c9c48532-1160-42f8-9b0e-09da3657828f" podNamespace="kueue-system" podName="kueue-controller-manager-6bcc4495d-dwmxv"
 1月 28 17:55:41 jetson07 microshift[779521]: kubelet I0128 17:55:41.001406  779521 reflector.go:351] Caches populated for *v1.ConfigMap from object-"kueue-system"/"kube-root-ca.crt"
 1月 28 17:55:41 jetson07 microshift[779521]: kubelet I0128 17:55:41.001966  779521 reflector.go:351] Caches populated for *v1.ConfigMap from object-"kueue-system"/"openshift-service-ca.crt"
 1月 28 17:55:41 jetson07 microshift[779521]: kubelet I0128 17:55:41.003035  779521 reflector.go:351] Caches populated for *v1.ConfigMap from object-"kueue-system"/"kueue-manager-config"
 1月 28 17:55:41 jetson07 microshift[779521]: kubelet I0128 17:55:41.008202  779521 reflector.go:351] Caches populated for *v1.Secret from object-"kueue-system"/"kueue-webhook-server-cert"

```


## **Environment**:
Kubernetes version (use kubectl version):
```
[root@jetson07 repos]# oc version
Client Version: 4.16.0-202410172045.p0.gcf533b5.assembly.stream-cf533b5
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Kubernetes Version: v1.29.8
[root@jetson07 ~]# microshift version
MicroShift Version: 4.16.27
Base OCP Version: 4.16.27
```

Kueue version (use git describe --tags --dirty --always): `v0.10.1`

Cloud provider or hardware configuration: Jetson AGX Orin 64GB Single Cluster

OS (e.g: cat /etc/os-release):
```
NAME="Red Hat Enterprise Linux"
VERSION="9.4 (Plow)"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="9.4"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Red Hat Enterprise Linux 9.4 (Plow)"
ANSI_COLOR="0;31"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:redhat:enterprise_linux:9::baseos"
HOME_URL="https://www.redhat.com/"
DOCUMENTATION_URL="https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9"
BUG_REPORT_URL="https://bugzilla.redhat.com/"

REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 9"
REDHAT_BUGZILLA_PRODUCT_VERSION=9.4
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.4"
```
Kernel (e.g. uname -a):
```
Linux jetson07 5.14.0-427.22.1.el9_4.aarch64 #1 SMP PREEMPT_DYNAMIC Mon Jun 10 15:57:50 UTC 2024 aarch64 aarch64 aarch64 GNU/Linux
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T09:30:50Z

@yasaidev does it help if you wait a little with the restart until Kueue is available with:
```
kubectl wait deploy/kueue-controller-manager -nkueue-system --for=condition=available --timeout=5m
```
as in the Kueue docs: https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version

### Comment by [@yasaidev](https://github.com/yasaidev) — 2025-01-28T11:17:29Z

@mimowo
Thank you for your reply.
I tried your suggestion, but unfortunately, I’m still encountering the same error.

Here are the steps I followed:
```shell
[root@jetson07 ~]# kubectl wait deploy/kueue-controller-manager -nkueue-system --for=condition=available --timeout=5m
deployment.apps/kueue-controller-manager condition met
[root@jetson07 ~]# kubectl get services --all-namespaces 
NAMESPACE           NAME                                        TYPE           CLUSTER-IP      EXTERNAL-IP                                 PORT(S)                      AGE
default             kubernetes                                  ClusterIP      10.43.0.1       <none>                                      443/TCP                      39d
jobset-system       jobset-controller-manager-metrics-service   ClusterIP      10.43.74.177    <none>                                      8443/TCP                     36d
jobset-system       jobset-webhook-service                      ClusterIP      10.43.182.91    <none>                                      443/TCP                      36d
kube-system         csi-snapshot-webhook                        ClusterIP      10.43.12.69     <none>                                      443/TCP                      39d
kubeflow            training-operator                           ClusterIP      10.43.140.126   <none>                                      8080/TCP,443/TCP             36d
kueue-system        kueue-controller-manager-metrics-service    ClusterIP      10.43.177.81    <none>                                      8443/TCP                     9m15s
kueue-system        kueue-visibility-server                     ClusterIP      10.43.230.243   <none>                                      443/TCP                      9m15s
kueue-system        kueue-webhook-service                       ClusterIP      10.43.171.131   <none>                                      443/TCP                      9m15s
openshift-dns       dns-default                                 ClusterIP      10.43.0.10      <none>                                      53/UDP,53/TCP,9154/TCP       39d
openshift-ingress   router-default                              LoadBalancer   10.43.102.222   10.42.0.2,10.44.0.0,10.88.0.1,172.20.6.23   80:31613/TCP,443:31379/TCP   39d
openshift-ingress   router-internal-default                     ClusterIP      10.43.28.178    <none>                                      80/TCP,443/TCP,1936/TCP      39d
[root@jetson07 ~]# systemctl restart microshift
Job for microshift.service failed because the service did not take the steps required by its unit configuration.
See "systemctl status microshift.service" and "journalctl -xeu microshift.service" for details.
```

Below is the relevant output from journalctl: 
> [journalctl_microshift_n_1000.log](https://github.com/user-attachments/files/18572436/journalctl_microshift_n_1000.log)

```
1月 28 20:02:40 jetson07 microshift[866025]: infrastructure-services-manager E0128 20:02:40.250076  866025 manager.go:132] "SERVICE FAILED - stopping MicroShift" err="Internal error occurred: failed calling webhook \"mdeployment.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s\": dial tcp 10.42.0.12:9443: connect: connection refused" service="infrastructure-services-manager" since-start="140.957804ms"
```

I would be very grateful if you could let me know of any other suggestions or ideas I could try.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T11:59:44Z

I'm not familiar with microshift, and the issue seems specific. Maybe @kannon92 or @dgrove-oss would have some ideas.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-28T12:40:43Z

I see logs related to service-ca which is internal Openshift for managing certificates. I’m noticing that Openshift really does not like how Kueue handles certs.

I would maybe look at installing cert manager and configuring Kueue with CertManager.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-28T14:37:15Z

>  1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager W0128 17:55:39.896032  779521 recorder_logging.go:53] &Event{ObjectMeta:{dummy.181ecf653abfee97  dummy    0 0001-01-01 00:00:00 +0000 UTC <nil> <nil> map[] map[] [] [] []},InvolvedObject:ObjectReference{Kind:Pod,Namespace:dummy,Name:dummy,UID:,APIVersion:v1,ResourceVersion:,FieldPath:,},Reason:DeploymentUpdateFailed,Message:Failed to update Deployment.apps/service-ca -n openshift-service-ca: Internal error occurred: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service",Source:EventSource{Component:,Host:,},FirstTimestamp:2025-01-28 17:55:39.895893655 +0900 JST m=+81.618815254,LastTimestamp:2025-01-28 17:55:39.895893655 +0900 JST m=+81.618815254,Count:1,Type:Warning,EventTime:0001-01-01 00:00:00 +0000 UTC,Series:nil,Action:,Related:nil,ReportingController:,ReportingInstance:,}
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager W0128 17:55:39.896066  779521 apps.go:101] Failed to apply apps api components/service-ca/deployment.yaml: Internal error occurred: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service"
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager W0128 17:55:39.896091  779521 controllers.go:99] Failed to apply apps [components/service-ca/deployment.yaml]: Internal error occurred: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service"
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager W0128 17:55:39.896104  779521 components.go:13] Failed to start service-ca controller: Internal error occurred: failed calling webhook "mdeployment.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s": no endpoints available for service "kueue-webhook-service"
 1月 28 17:55:39 jetson07 microshift[779521]: infrastructure-services-manager E0128 17:55:39.896141  779521 manager.go:132] "SERVICE FAILED - stopping MicroShift" err="Internal error occurred: failed calling webhook \"mdeployment.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-apps-v1-deployment?timeout=10s\": no endpoints available for service \"kueue-webhook-service\"" service="infrastructure-services-manager" since-start="86.252342ms"


So reading this I think that the kueue webhook is interfering with core openshift services. It seems that the service-ca controller is getting patched by kueue webhook for deployment and that fails.

I don't know very much about microshift but you may need to add these services to the exclude namespace in the mutating/validating webhooks.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-28T16:18:32Z

If you have enabled `manageJobsWithoutQueueName` then at least part of the problem is that the defaulting logic for `managedJobsNamespaceSelector` uses values appropriate for Kubernetes.  See here: https://github.com/kubernetes-sigs/kueue/blob/f955feb55a0686085c23b71b0d288c849876ae69/apis/config/v1beta1/defaults.go#L182-L194

You'd have to change this in your custom config to exempt OpenShift system namespaces.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-28T16:23:55Z

You'll also need to use kustomize to do a similar change to the webhooks.  There are quite a few stanzas like this in the manifests.yaml that need to be fixed for OpenShift.

```
- admissionReviewVersions:
  - v1
  clientConfig:
    service:
      name: kueue-webhook-service
      namespace: kueue-system
      path: /validate-apps-v1-deployment
  failurePolicy: Fail
  name: vdeployment.kb.io
  namespaceSelector:
    matchExpressions:
    - key: kubernetes.io/metadata.name
      operator: NotIn
      values:
      - kube-system
      - kueue-system
```

### Comment by [@yasaidev](https://github.com/yasaidev) — 2025-01-29T13:07:17Z

@dgrove-oss @kannon92 

Thank you for the advice.
Following your recommendation, I configured the webhooks to ignore the OpenShift-related namespaces, and I was able to successfully restart the cluster.

I applied the following kustomize.yaml.
```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../bases

vars:
  - name: EXCLUDED_NAMESPACES
    value: >-
      ["kube-system", "kueue-system", "openshift-controller-manager",
       "openshift-dns", "openshift-infra", "openshift-ingress",
       "openshift-kube-controller-manager", "openshift-ovn-kubernetes",
       "openshift-route-controller-manager", "openshift-service-ca",
       "openshift-storage"]

patches:
- patch: |
    - op: replace
      path: /webhooks/0/namespaceSelector/matchExpressions/0/values
      value: $(EXCLUDED_NAMESPACES)
  target:
    kind: MutatingWebhookConfiguration
    name: kueue-mutating-webhook-configuration
- patch: |
    - op: replace
      path: /webhooks/1/namespaceSelector/matchExpressions/0/values
      value: $(EXCLUDED_NAMESPACES)
  target:
    kind: MutatingWebhookConfiguration
    name: kueue-mutating-webhook-configuration
- patch: |
    - op: replace
      path: /webhooks/0/namespaceSelector/matchExpressions/0/values
      value: $(EXCLUDED_NAMESPACES)
  target:
    kind: ValidatingWebhookConfiguration
    name: kueue-validating-webhook-configuration
- patch: |
    - op: replace
      path: /webhooks/1/namespaceSelector/matchExpressions/0/values
      value: $(EXCLUDED_NAMESPACES)
  target:
    kind: ValidatingWebhookConfiguration
    name: kueue-validating-webhook-configuration
```

On a side note, @kannon92 do you have any information about the forked [Kueue](https://github.com/openshift/kubernetes-sigs-kueue) in the openshift organization?
I figured you might be aware if you’re from Red Hat. I’m thinking of using it if it’s optimized for OpenShift, but I haven’t been able to find any documentation, which has left me somewhat puzzled.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-29T14:02:12Z

Yes, I am aware of this fork. For now I recommend going with the approach that you are doing.

We are working on a way to streamline this for openshift users (openshift fork + kueue operator) but it is not ready yet.

### Comment by [@yasaidev](https://github.com/yasaidev) — 2025-01-29T14:45:51Z

Thank you for the information. That makes sense.
