# Issue #7222: The controller metrics (e.g., `workqueue_depth`) are not exposed as manager matrics server endpoint

**Summary**: The controller metrics (e.g., `workqueue_depth`) are not exposed as manager matrics server endpoint

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7222

**Last updated**: 2026-02-26T15:01:40Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-10-10T11:04:16Z
- **Updated**: 2026-02-26T15:01:40Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The kueue metrics are exposed via the manager metrics endpoint, but the controller metrics (e.g., `workqueue_depth`) [^1] can not be obtained from the manager metrics endpoint [^2].

[^1]: controller metrics: https://github.com/kubernetes-sigs/controller-runtime/blob/f48fe1c564dc8e418f302d3ab0086d3a7403233a/pkg/metrics/workqueue.go#L21-L28
[^2]: manager metrics endpoint: https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/config/default/manager_metrics_patch.yaml#L13

**What you expected to happen**:

The controller metrics can be obtained via the manager metrics endpoint.

**How to reproduce it (as minimally and precisely as possible)**:

```shell
# 0. Create cluster
$ kind create cluster

# 1. Install ServiceMonitor CRD
$ kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/kube-prometheus/refs/heads/main/manifests/setup/0servicemonitorCustomResourceDefinition.yaml

# 2. Install Kueue with Prometheus configurations
$ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.13.6/manifests.yaml
$ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.13.6/prometheus.yaml

# 3. Create metrics read ClusterRoleBinding
$ cat <<EOF| kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata: 
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/name: kueue
    control-plane: controller-manager
  name: kueue-metrics-reader-rolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kueue-metrics-reader
subjects:
- kind: ServiceAccount
  name: kueue-controller-manager
  namespace: kueue-system
EOF

# 4. Generate TOKEN
$ TOKEN=$(kubectl -n kueue-system create token kueue-controller-manager)

# 5. Set up port-forward (separate terminal or subprocess)
$ kubectl port-forward -n kueue-system svc/kueue-controller-manager-metrics-service 8443:8443
...

# 6. Obtain metrics
$ curl -ks -H "Authorization: Bearer $TOKEN" https://127.0.0.1:8443/metrics | grep workqueue_depth
# OUTPUT is nothing
```

**Anything else we need to know?**:

After some investigations, I found the controller metrics are registered to the vibility server's metrics server in the following.
So, I'm wondering if we are missing something to set up the manager and visibility server initializations.

```shell
# Connect Visibility Server Endpoint (separate terminal or subprocess)
$ kubectl -n kueue-system port-forward svc/kueue-visibility-server 8082:443
...

$ curl -skH "Authorization: Bearer $TOKEN" https://127.0.0.1:8082/metrics | grep workqueue_depth
# HELP workqueue_depth [ALPHA] Current depth of workqueue
# TYPE workqueue_depth gauge
workqueue_depth{name="DynamicCABundle-serving-cert"} 0
workqueue_depth{name="DynamicConfigMapCABundle-client-ca"} 0
workqueue_depth{name="DynamicServingCertificateController"} 0
workqueue_depth{name="RequestHeaderAuthRequestController"} 0
workqueue_depth{name="admissioncheck_controller"} 0
workqueue_depth{name="cert-rotator"} 0
workqueue_depth{name="clusterqueue_controller"} 0
workqueue_depth{name="cohort_controller"} 0
workqueue_depth{name="job"} 0
workqueue_depth{name="localqueue_controller"} 0
workqueue_depth{name="mpijob"} 0
workqueue_depth{name="multikueue_admissioncheck"} 0
workqueue_depth{name="multikueue_workload"} 0
workqueue_depth{name="multikueuecluster"} 0
workqueue_depth{name="priority_and_fairness_config_queue"} 0
workqueue_depth{name="resourceflavor_controller"} 0
workqueue_depth{name="statefulset"} 0
workqueue_depth{name="v1_pod"} 0
workqueue_depth{name="workload_controller"} 0
```

**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.2
- Kueue version (use `git describe --tags --dirty --always`): v0.14.1, v0.13.6, v0.12.10, v0.11.9, v0.10.6, v0.9.5
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T11:14:56Z

Is this a recent regresstion or were the metrics also missing on previous versions?

Maybe they stopped being exposed after controller runtime update?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-10T11:31:20Z

> Is this a recent regresstion or were the metrics also missing on previous versions?
> 
> Maybe they stopped being exposed after controller runtime update?

The curious thing is that the visibility server exposes those metrics, as I mentioned in `Anything else we need to know?:`
But, yes, I can check the previous Kueue version.

I will let you know after I check some previous Kueue version

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-10T11:49:33Z

As I checked the following Kueue version in KinD cluster by reproducing the step described in the issue description, I faced the same situation where the manager does not expose controller metrics, but the visibility server exposes those.

Confirmed Kueue versions:
- v0.14.1
- v0.13.6
- v0.12.10
- v0.11.9
- v0.10.6
- v0.9.5

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T11:53:24Z

Thank you for the archeology, in that case maybe it was always blocked?

We could also check something before the visibility server, 0.5 probably?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-10T12:01:25Z

> Thank you for the archeology, in that case maybe it was always blocked?
> 
> We could also check something before the visibility server, 0.5 probably?

Uhm that sounds good point. I checked the below 2 patterns.

1. v0.5.6 with reproduce step
2. v0.13.6 with VisibilityOnDemand=false

The opt (1. could work well which means manager metrics server exposed the proper controller metrics
The opt (2. could NOT work well which is the same situations as I reported in this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T12:07:08Z

I see, I think it is possible that binary search is our best option here. I think it may also be related to controller runtime upgrade at some point

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-10T12:19:33Z

> I see, I think it is possible that binary search is our best option here. I think it may also be related to controller runtime upgrade at some point

As I see the metrics documentation (https://book.kubebuilder.io/reference/metrics-reference.html), those controller metrics are still supported. So, I'm suspecting the visibility server go modules (`import` directives) interrupt the metrics registration via `func init()` function something else.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-10T13:24:50Z

As I debug something more, I found the problems which has races between kubernetes libraries and controller-runtime about metric provider registration:

- k/kubernetes
  - https://github.com/kubernetes/kubernetes/issues/127739
  - https://github.com/kubernetes/kubernetes/pull/114242

- k-sigs/controller-runtime
  - https://github.com/kubernetes-sigs/controller-runtime/issues/3054
  - https://github.com/kubernetes-sigs/controller-runtime/issues/2957
  - https://github.com/kubernetes-sigs/controller-runtime/issues/2238

### Comment by [@zouyee](https://github.com/zouyee) — 2025-12-17T04:09:51Z

The client-go metrics are also not exposed in the metrics endpoint.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:22:59Z

/priority important-longterm

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-26T15:01:40Z

I ran into this issue on 2024-03-27. Copying a comment of mine to an internal bug (NOTE: I'm by no means recommending this as a solution, just trying to point to the source of the issue). Perhaps it is still the same issue?

comment from 2024-03-27:
[controller-runtime/metrics/workqueue.go](https://github.com/kubernetes-sigs/controller-runtime/blob/v0.17.2/pkg/metrics/workqueue.go#L99) transitively calls [client-go/util/workqueue/metrics.go](https://github.com/kubernetes/client-go/blob/v0.29.3/util/workqueue/metrics.go#L223-L227), which is also transitively called by [component-base/metrics/prometheus/workqueue/metrics.go](https://github.com/kubernetes/component-base/blob/release-1.29/metrics/prometheus/workqueue/metrics.go#L108). Component base is imported by apiserver twice ([loc1](https://github.com/kubernetes/apiserver/blob/release-1.29/pkg/storageversion/manager.go#L30), [loc2](https://github.com/kubernetes/apiserver/blob/release-1.29/pkg/endpoints/filters/storageversion.go#L32)), which triggers the init call. Kueue depends on apiserver. If I comment out those two lines in apiserver, workqueue metrics start flowing for kueue.
