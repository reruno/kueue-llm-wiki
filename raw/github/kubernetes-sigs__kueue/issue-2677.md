# Issue #2677: Document how to use Kueue for Deployments

**Summary**: Document how to use Kueue for Deployments

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2677

**Last updated**: 2024-08-05T14:29:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-23T09:38:03Z
- **Updated**: 2024-08-05T14:29:01Z
- **Closed**: 2024-08-05T14:29:01Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 8

## Description

**What would you like to be added**:

A new page showing how Kueue can be used for Deployments. 

It can be a new sub-page "Run Deployments" this page: https://kueue.sigs.k8s.io/docs/tasks/run/.

I have tested that Deployments can already be supported with Kueue via the Plain pods integration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
        kueue.x-k8s.io/queue-name: user-queue
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 3
```

This allows to scale up and scale down the deployment, which should be mentioned in the docs.

**Note**: this requires enabling the "pod" integration, and setting the queue-name at the pod template level. We are considering making this easier for the users: webhook to copy the user-name  down to template, dedicated "deployment" integration in kueue config, 

However, this issue is just about documenting the status quo which would already works for users on 0.6+. Once the improvements are done we can extend the docs with the appropriate notes.

**Why is this needed**:

To increase awareness among users who would like to use Kueue for serving / AI inference workloads.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-23T09:41:06Z

/cc @trasc

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-23T09:42:14Z

/cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-23T09:51:31Z

LGTM

Actually, I tried to deploy Deployment with Kueue previously.

Maybe, it is helpful that kueue automatically deactivates Deployment with [`ProgressDeadlineExceeded `](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#failed-deployment) for the future. This is just a comment, though.

### Comment by [@trasc](https://github.com/trasc) — 2024-07-23T10:01:15Z

Do we have some real life examples of a deployment needing to run within kueue?

For me the pairing of kueue with deployments feels a bit unnatural , with maybe the exception when one may want to the a queue with Provisioning ACC to scale up and down the cluster to accommodate the deployment .

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-23T10:09:30Z

There are users who want to use GPUs for AI inference (serving). Depending on the user they would use Deployments / StatefulSets or [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws). The use case is to constrain the GPU quota with Kueue.

In the longer term we are going to extend and improve the support for AI inference, but this is out of scope for the issue. 

/cc @mwielgus

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-07-23T12:33:25Z

> There are users who want to use GPUs for AI inference (serving). Depending on the user they would use Deployments / StatefulSets or [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws). The use case is to constrain the GPU quota with Kueue.
> 

This is a use case we see as well.  We solve it by requiring users to wrap their Deployments/StatefulSets in [AppWrappers](https://github.com/project-codeflare/appwrapper).  This ensures that Kueue has a complete view on all GPU-consuming workloads on our clusters while allowing quota-management/pre-emption to happen at the logical workload level, not on individual pods that make up a multiple-pod workload.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-23T12:49:18Z

We are also considering the atomic admission / preemption for the serving workload, especially for StatefulSets.. However, for Deployments are often scaled so it could be too constraining. I think ideally, in the long run we would like to have something like https://github.com/kubernetes-sigs/kueue/pull/1851

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-07-24T14:36:35Z

/assign
