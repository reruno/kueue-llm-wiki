# Issue #2878: Kueue mutating webhooks drops fields in KubeRay resources

**Summary**: Kueue mutating webhooks drops fields in KubeRay resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2878

**Last updated**: 2024-09-27T17:34:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@andrewsykim](https://github.com/andrewsykim)
- **Created**: 2024-08-22T16:13:08Z
- **Updated**: 2024-09-27T17:34:02Z
- **Closed**: 2024-09-27T17:34:02Z
- **Labels**: `kind/bug`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 9

## Description

**What happened**:

When using Kueue with KubeRay, new fields in KubeRay that are not recognized by Kueue are dropped during defaulting. Here's an example using Kind and RayJob:

Create cluster:
```
$ kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.27.3) 🖼
 ✓ Preparing nodes 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a nice day! 👋
```

Install Kueue:
```
$ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.8.0/manifests.yaml
namespace/kueue-system serverside-applied
...
...
```

Install latest release candidate of KubeRay:
```
$ helm install kuberay-operator kuberay/kuberay-operator --version 1.2.0-rc.0
NAME: kuberay-operator
LAST DEPLOYED: Thu Aug 22 16:03:11 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Deploy Kueue resources:
```
$ kubectl apply -f kueue-resources.yaml
resourceflavor.kueue.x-k8s.io/default-flavor created
clusterqueue.kueue.x-k8s.io/cluster-queue created
localqueue.kueue.x-k8s.io/local-queue created
```

Create a RayJob with a reference to the local queue:
```
$ cat rayjob.yaml
apiVersion: ray.io/v1
kind: RayJob
metadata:
  name: image-resize
  labels:
    kueue.x-k8s.io/queue-name: local-queue
spec:
  backoffLimit: 2
  shutdownAfterJobFinishes: true
  entrypoint: python ray-operator/config/samples/ray-data-image-resize/ray_data_image_resize.py
  runtimeEnvYAML: |
    pip:
      - torch
      - torchvision
      - numpy
      - google-cloud-storage
    working_dir: "https://github.com/ray-project/kuberay/archive/master.zip"
    env_vars:
      BUCKET_NAME: ray-images
      BUCKET_PREFIX: images
  # rayClusterSpec specifies the RayCluster instance to be created by the RayJob controller.
  rayClusterSpec:
    rayVersion: '2.34.0'
    headGroupSpec:
      rayStartParams: {}
      # Pod template
      template:
        spec:
          containers:
            - name: ray-head
              image: rayproject/ray:2.34.0
              ports:
                - containerPort: 6379
                  name: gcs-server
                - containerPort: 8265 # Ray dashboard
                  name: dashboard
                - containerPort: 10001
                  name: client
              resources:
                limits:
                  cpu: "2"
                  memory: "4Gi"
                requests:
                  cpu: "2"
                  memory: "4Gi"
    workerGroupSpecs:
      - replicas: 4
        minReplicas: 1
        maxReplicas: 5
        groupName: small-group
        rayStartParams: {}
        # Pod template
        template:
          spec:
            containers:
              - name: ray-worker
                image: rayproject/ray:2.34.0
                resources:
                  limits:
                    cpu: "2"
                    memory: "4Gi"
                  requests:
                    cpu: "2"
                    memory: "4Gi"
$ kubectl apply -f rayjob.yaml
rayjob.ray.io/image-resize created
```

Note the RayJob sets a new field introduced in v1.2.0 `spec.backoffLimit`. In this example it is set to 2. However, Kueue is defaulting the field to 0:
```
$ kubectl get rayjob image-resize -o yaml
apiVersion: ray.io/v1
kind: RayJob
metadata:
  ...
  labels:
    kueue.x-k8s.io/queue-name: local-queue
  name: image-resize
  ...
spec:
  backoffLimit: 0
  entrypoint: python ray-operator/config/samples/ray-data-image-resize/ray_data_image_resize.py
  rayClusterSpec:
  ...
```

**What you expected to happen**:

I believe we saw similar behavior while transition KubeRay v0.6.0 to v1.0.0, but I thought it was specific to the  v1apha1 -> v1 upgrade when we deleted fields in v1alpha1. 

I would not expect Kueue to drop new fields introduced in v1 APIs of KubeRay.

**How to reproduce it (as minimally and precisely as possible)**:

See steps above.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): v0.8.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-08-22T16:19:45Z

The immediate fix we could do is bump the kuberay dependency in Kueue to a version that includes all new fields, but this doesn't seem like a scalable approach. The defaulting behavior seems a bit unusual to me, maybe it's something specific to controller-runtime webhooks?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-22T16:25:39Z

In v0.8 we fixed the job reconcilers to use Patch instead of Update to avoid this problem https://github.com/kubernetes-sigs/kueue/pull/2501

But we didn't check the webhooks, so that's probably the problem.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-22T18:08:39Z

No, it doesn't look like it's the defaulter, because it's also using Patch https://github.com/kubernetes-sigs/controller-runtime/blob/e6c3d139d2b6c286b1dbba6b6a95919159cfe655/pkg/webhook/admission/defaulter_custom.go#L88-L93

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-22T19:00:31Z

Looking at GKE audit logs, the only API updates come from the ray operator. Thus, the only possible culprit is the webhook.

Thinking about this further:
Yes, the webhook uses patch, which is good.
However, the patch is build from the difference between the Raw object (which will have the field) and the marshalled object (which doesn't have the field).

```
PatchResponseFromRaw(req.Object.Raw, marshalled)
```

So it's a bug in controller-runtime.

I'll try to fix it there, but while waiting for a release there, our only chance is to update the APIs in Kueue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-22T20:44:49Z

Fix is up https://github.com/kubernetes-sigs/controller-runtime/pull/2931

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-22T20:47:31Z

/assign @alculquicondor

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-09-04T03:17:25Z

As a short-term fix should we update kuberay version to v1.2? cc @astefanutti

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-04T04:55:22Z

> As a short-term fix should we update kuberay version to v1.2? cc @astefanutti

We already done it on https://github.com/kubernetes-sigs/kueue/pull/2960.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-09-04T13:59:39Z

Ah I missed that, thank you!
