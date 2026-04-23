# Issue #764: Document how to use MPIJobs with Kueue

**Summary**: Document how to use MPIJobs with Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/764

**Last updated**: 2023-05-25T18:56:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-11T13:33:22Z
- **Updated**: 2023-05-25T18:56:53Z
- **Closed**: 2023-05-25T18:56:53Z
- **Labels**: `kind/feature`, `kind/documentation`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 14

## Description

It should be very similar to the documentation for Flux MiniClusters

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-11T13:34:22Z

/kind documentation

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-16T19:53:04Z

I'm doing a bit more research into Kueue and I'd like to work on this.

I am running into some trouble with getting Kueue to work with MPIOperator.

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-16T19:55:00Z

So I basically took the pi example from MPIOperator:

```
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  name: pi
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  slotsPerWorker: 1
  runPolicy:
    cleanPodPolicy: Running
    ttlSecondsAfterFinished: 60
    suspend: true
...
```
I apply the simple CQ/Q yaml in config/samples but I see that my MPIJob stays in suspended.  Is there anything else I am missing?  

I used 0.3.0 release of Kueue.

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-16T19:55:08Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-16T19:59:13Z

@kannon92 Have you uncomment the below?

https://github.com/kubernetes-sigs/kueue/blob/cd747c596b2b56929c71abe7c6f94ab5c73609f9/config/components/manager/controller_manager_config.yaml#L33

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-16T20:02:04Z

Oh right, that should be part of the documentation too :)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-16T20:05:28Z

Actually, I'm using the following manifests :)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: kueue-system
resources:
- https://github.com/kubernetes-sigs/kueue/releases/download/v0.3.1/manifests.yaml
configMapGenerator:
- namespace: kueue-system
  name: kueue-manager-config
  behavior: replace
  files:
  - controller_manager_config.yaml
```

```yaml
apiVersion: config.kueue.x-k8s.io/v1beta1
kind: Configuration
....
controller:
  groupKindConcurrency:
    Job.batch: 5
    MPIJob.kubeflow.org: 5
...
integrations:
  frameworks:
  - "batch/job"
  - "kubeflow.org/mpijob"
```

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-16T20:06:52Z

Should this just be enabled by default?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-16T20:18:29Z

No, because if the user doesn't install mpi-operator, Kueue will produce errors in the logs

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-16T20:41:51Z

So I'm trying to approach this as a user:

I install Kueue this way:

```
VERSION=v0.3.1
kubectl apply -f https://github.com/kubernetes-sigs/kueue/releases/download/$VERSION/manifests.yaml
```
Is there an easy way to modify the manifests to enable MPI-Operator?  I guess I could download these manifest files and uncomment that yaml file?  It just seems to be a bit confusing for a user to have to do this?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-16T20:44:19Z

> So I'm trying to approach this as a user:
> 
> I install Kueue this way:
> 
> ```
> VERSION=v0.3.1
> kubectl apply -f https://github.com/kubernetes-sigs/kueue/releases/download/$VERSION/manifests.yaml
> ```
> 
> Is there an easy way to modify the manifests to enable MPI-Operator? I guess I could download these manifest files and uncomment that yaml file? It just seems to be a bit confusing for a user to have to do this?

You don't need to edit manifests.
You can use the below kustomization.

https://github.com/kubernetes-sigs/kueue/issues/764#issuecomment-1550289219

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-17T12:06:08Z

Thank you!!  After I figured out how to use Kustomize, I was able to get an example running with Kueue

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-17T17:36:47Z

@tenzen-y it might be useful to add to the documentation how to configure parameters via kustomize, as an alternative to https://kueue.sigs.k8s.io/docs/installation/#install-a-custom-configured-released-version

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-17T18:44:37Z

> @tenzen-y it might be useful to add to the documentation how to configure parameters via kustomize, as an alternative to https://kueue.sigs.k8s.io/docs/installation/#install-a-custom-configured-released-version

@alculquicondor Agree. I will create a PR to update the docs (probably this weekend).
