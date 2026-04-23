# Issue #9156: ClusterQueue and LocalQueue label on pods

**Summary**: ClusterQueue and LocalQueue label on pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9156

**Last updated**: 2026-02-23T19:25:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dkaluza](https://github.com/dkaluza)
- **Created**: 2026-02-12T10:22:58Z
- **Updated**: 2026-02-23T19:25:37Z
- **Closed**: 2026-02-23T19:25:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@dkaluza](https://github.com/dkaluza)
- **Comments**: 8

## Description

**What would you like to be added**:
A new label on pods created by Kueue workloads indicating from which Queues the pod originated. 
The implementation can be similar to `kueue.x-k8s.io/podset`, which is already added to the podtemplate.  

**Why is this needed**:
Currently there is no efficient way to monitor real resource usage of the pods related a particular queue, e.g. CPU utilization.  To achieve that one would have to first retrieve all of the workloads and then filter pods by their identifiers.

Addition of the labels can streamline the process and make it scalable.
 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@dkaluza](https://github.com/dkaluza) — 2026-02-12T10:41:15Z

I would be happy to work on that.
/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-18T18:19:47Z

> Currently there is no efficient way to monitor real resource usage of the pods related a particular queue, e.g. CPU utilization

To be clear Kueue would not provide this info. Kueue will assume that the cpu requests is the amount of CPU you requested but I don't see any way to report real resource usage.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-18T18:29:35Z

there are tools which can export the info per pod. by correleting the pods with cq/lq by labels the in house tools can aggregate and compute the real usage

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-18T18:38:01Z

> there are tools which can export the info per pod. by correleting the pods with cq/lq by labels the in house tools can aggregate and compute the real usage

This is a popular ask so I hope we could maybe highlight how this could be done.

### Comment by [@dkaluza](https://github.com/dkaluza) — 2026-02-19T12:57:34Z

Yes, Kueue will not be collecting the exact usage by itself, we will just provide the labels and it will be up to the user to setup the collection or filter the monitoring on existing metrics based on the labels.

But the pod labels will allow users to collect them more efficiently.
I'm not a specialist in this field (it was a request from other team members) but from what I found there are several ways to do it depending on what you actually need:
1. You can use  [Prometheus relabel config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config) with source  ` __meta_kubernetes_pod_label_<name_of_label>` to add them to a specific metric like `container/cpu/request_utilization` for example from [GKE metrics](https://docs.cloud.google.com/monitoring/api/metrics_kubernetes)
2. You can use Prometheus QL grouping to add additional labels to the metrics [docs](https://prometheus.io/docs/prometheus/latest/querying/operators/#many-to-one-and-one-to-many-vector-matches)  by "joining" it with another metric values.

Should I add the information to the docs?

### Comment by [@dkaluza](https://github.com/dkaluza) — 2026-02-19T14:39:52Z

Some more info about annotations - I believe one can export them as labels similarly as in 1 in previous comment.
It is generally advised to have label values in metrics of reasonable size as really large labels can cause performance [issues](https://github.com/prometheus/prometheus/issues/8198).  However the mentioned 400 KB is on a different level than our 253 chars of queue name, so I would guess it should not be an issue in this case.

There is a configuration of [length](https://github.com/prometheus/prometheus/issues/8291) on the Prometheus scraping job side - but I do not yet know if it is used in practice (default is no limit).

### Comment by [@dkaluza](https://github.com/dkaluza) — 2026-02-19T17:46:44Z

It looks like usually information suitable for joins (2 above) is exposed by  kube-state-metrics - which in recent versions requires allow-listing of both labels and annotations as metrics - none of them is exposed by default - [source](https://github.com/kubernetes/kube-state-metrics/blob/main/docs/developer/cli-arguments.md#command-line-arguments)

But Metrics-Server used by [Horizontal and Vertical Pod Autoscaling ](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/) allows only filtering by labels - [source](https://github.com/kubernetes/design-proposals-archive/blob/main/instrumentation/resource-metrics-api.md#endpoints)

For debugging purposes Metrics-Server also supplies `kubectl top` command, which can be used as follows:
```
kubectl top pod -l kueue.x-k8s.io/local-queue-name=user-queue
``` 

So taking this into the consideration in my opinion labels look more promising:
- enabling interaction with metrcs-server in the future if it becomes needed at some point
- intended for resource grouping according to kubernetes documentation

At the same time requirement of 63 characters name for ClusterQueue is not really restrictive - considering that currently LocalQueue names have to be at most 63 character and there can be many more LocalQueues in the cluster.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-23T18:53:52Z

> Should I add the information to the docs?

If you could craft such an example configuration scraping "real" usage from Pods and aggregating into LQ / CQ using OSS tooling, like Metrics Server then this will be super valuable. I imagine it could be a section in https://kueue.sigs.k8s.io/docs/tasks/manage/ like "Monitoring real usage".

Opened: https://github.com/kubernetes-sigs/kueue/issues/9435
