# Issue #4446: Adding observability for admitted pods

**Summary**: Adding observability for admitted pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4446

**Last updated**: 2025-05-13T10:15:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yuvalaz99](https://github.com/yuvalaz99)
- **Created**: 2025-03-02T13:27:24Z
- **Updated**: 2025-05-13T10:15:17Z
- **Closed**: 2025-05-13T10:15:17Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

In our dashboard, we would like the ability to differentiate between different types of pending pods.
With Kueue, a pod can be pending for two main reasons:

1. It has not yet been admitted and still contains a scheduling gate.
2. It has been admitted, but no available nodes have the capacity to accommodate it.

To achieve this, we propose:

- A metric (potentially limited to pods managed by Kueue) that indicates whether a pod has a scheduling gate.
- Alternatively, a label added to the pod once it has been admitted.

This metric will typically be used when joined with other pod metrics to provide a clearer understanding of the pod’s current state in the cluster.
If adding a label to the pod is chosen as the approach, the same information can be obtained using the already existing kube_pod_labels metric.

We have implemented an in-house exporter that exposes this data for us, and the metric looks like this:

```
# Admitted pod - without scheduling gates
pod_scheduling_gates{condition="false", endpoint="http", instance="x.x.x.x:9469", job="scheduling-gated-pods-exporter", namespace="default", pod="example-pod-1", service="scheduling-gated-pods-exporter"} = 1  
pod_scheduling_gates{condition="true", endpoint="http", instance="x.x.x.x:9469", job="scheduling-gated-pods-exporter", namespace="default", pod="example-pod-1", service="scheduling-gated-pods-exporter"} = 0

# Non-admitted pod - with scheduling gates
pod_scheduling_gates{condition="false", endpoint="http", instance="x.x.x.x:9469", job="scheduling-gated-pods-exporter", namespace="default", pod="example-pod-2", service="scheduling-gated-pods-exporter"} = 0  
pod_scheduling_gates{condition="true", endpoint="http", instance="x.x.x.x:9469", job="scheduling-gated-pods-exporter", namespace="default", pod="example-pod-2", service="scheduling-gated-pods-exporter"} = 1  
```

**Why is this needed**:

Understanding why a pod is pending is crucial for observability. Since Kueue does not provide a one-size-fits-all mechanism for capacity checks during admission, we need a way to distinguish between pods that are waiting for admission and those that are unschedulable due to resource constraints. This will improve monitoring, and decision-making for workload management.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-02T13:41:17Z

https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/#observability

Can you use this metric to determine pods that are gated?

### Comment by [@yuvalaz99](https://github.com/yuvalaz99) — 2025-03-02T14:32:06Z

> https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/#observability
> 
> Can you use this metric to determine pods that are gated?

This metric is a Gauge which counts the number of gated pods. 
We need to know this information about individual pods :)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T13:16:14Z

> This metric is a Gauge which counts the number of gated pods.
> We need to know this information about individual pods :)

Right, but this metric can be used to have a "coarse-grained" understanding of what is going on in the cluster, similarly to the one which is proposed in the issue. I'm not sure we need more detailed metric in Kueue. Note that Kueue by default does not track Pods, so it would need to probably be an opt-in metric in configuration.

Also, if you need to know if a specific pod is gates or not, then this information is in `.spec.schedulingGates`, for example by `kubectl get pod/<podname> -oyaml`.

> we need a way to distinguish between pods that are waiting for admission and those that are unschedulable due to resource constraints.

Right, I think in the majority of cases this could be determined by `.spec.schedulingGates`. Maybe what is needed is an extension to the troubleshooting guide for Pods: https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/troubleshooting_pods/

### Comment by [@yuvalaz99](https://github.com/yuvalaz99) — 2025-03-25T11:59:41Z

> > This metric is a Gauge which counts the number of gated pods.
> > We need to know this information about individual pods :)
> 
> Right, but this metric can be used to have a "coarse-grained" understanding of what is going on in the cluster, similarly to the one which is proposed in the issue. I'm not sure we need more detailed metric in Kueue. Note that Kueue by default does not track Pods, so it would need to probably be an opt-in metric in configuration.
> 
> Also, if you need to know if a specific pod is gates or not, then this information is in `.spec.schedulingGates`, for example by `kubectl get pod/<podname> -oyaml`.
> 
> > we need a way to distinguish between pods that are waiting for admission and those that are unschedulable due to resource constraints.
> 
> Right, I think in the majority of cases this could be determined by `.spec.schedulingGates`. Maybe what is needed is an extension to the troubleshooting guide for Pods: https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/troubleshooting_pods/

Thank you for the detailed answer :) 
So this observability knowledge is required to understand the day-to-day state of the system, and not for troubleshooting purposes, which can be used in a lot of places. for example:
1. Helping developers quickly understand why their workload is pending. We don’t want them to manually troubleshoot each workload using specific commands.
2. Enabling administrators to estimate fragmentation in the cluster (e.g., workloads that cannot fit on any node due to capacity constraints), which helps identify wasted GPU resources.

I agree that this information can be determined from scheduling gates, but currently, there is no metric that represents it at the per-pod level.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-24T13:11:00Z

> I agree that this information can be determined from scheduling gates, but currently, there is no metric that represents it at the per-pod level.

I see, generally in Kubernetes metrics with such [high cardinality](https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/#metric-cardinality-enforcement) are problematic. On some clusters exposing the metric means 100k (for such a number of pods) lines, probably around 100Mi of output just for the metric. PTAL also at the [blog post](https://kubernetes.io/blog/2021/04/13/kube-state-metrics-v-2-0/#what-is-new-in-v2-0) saying "We also removed some metrics that caused unnecessarily high cardinality in Prometheus!".

Moreover, if this metric is "counter" type then it will keep information about all past pods.

So, I think this would need to be opt-in, and guage, probably something like this:

```golang
	KueueSchedulingGatedPods = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: constants.KueueName,
			Name:      "scheduling_gated_pods",
			Help:      "The current number of scheduling gated pods managed by Kueue which are scheduling gated",
		}, []string{"name", "namespace"},
	)
```

I imagine there is a small opt-in controller (probably enabled by the global Kueue config) which monitors all events for pods (add, delete, update), and based on the events it increments or decrements the Pods. 

I assume these are "Kueue"-managed Pods only. Otherwise it seems to be more generic observability tool than just for Kueue.

A potentially useful modification of the metric is:

```golang
	KueuePendingPods = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: constants.KueueName,
			Name:      "pending_pods",
			Help:      "The current number of pending pods managed by Kueue which by the reason",
		}, []string{"name", "namespace", "reason"},
// reason could be 
// "scheduling gated" - has at least one scheduling gate
//  "not scheduled" - does not have scheduling gates, but does not have "spec.nodeName"
// "starting" - has "spec.nodeName"
	)
```
Let me know your thoughts @yuvalaz99.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-08T06:48:16Z

Exploring the label idea:
> Alternatively, a label added to the pod once it has been admitted.

We already have this label which is added to every Pod admitted by Kueue: https://github.com/kubernetes-sigs/kueue/blob/9d2919ea7b682a9e22b185347d286fe7e82591d4/apis/kueue/v1alpha1/topology_types.go#L60-L63

This label in conjunction with the pod `status.Phase` could be probably used for fast filtering to identify Pods which are admitted by not Running.

This label was introduced for a different purpose (TopologyAwareScheduling), but seems to match the requirements so I would prefer to go with the label rather than introduce yet another. So, the MVP would be extract setting of the label out of the TopologyAwareScheduling feature gate.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-08T07:17:27Z

I consulted this with @mwysokin who collaborates with the user, and we believe the label is what is needed. 

In that case, I suggest we go ahead and extract the label from the TAS feature gate.

cc @mbobrovskyi @mszadkow @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-08T08:03:31Z

/assign @mszadkow
