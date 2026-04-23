# Issue #2009: [WaitForPodsReady] The default configuration for `requeuingStrategy` is impractical

**Summary**: [WaitForPodsReady] The default configuration for `requeuingStrategy` is impractical

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2009

**Last updated**: 2024-04-24T15:59:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-18T16:17:50Z
- **Updated**: 2024-04-24T15:59:59Z
- **Closed**: 2024-04-24T15:59:59Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 9

## Description

**What happened**:

Consider the following configuration:

```yaml
waitForPodsReady:
  enable: true
  timeout: 1m
  blockAdmission: false
  requeuingStrategy:
    timestamp: Creation
    backoffLimitCount: 4
 ```
And let's say we have a workload which have unschedulable pods (for whatever reason).

If a job was timed-out after 1min (or 10min) of waiting, then requeue after 1s is not relevant to end-users.
it takes around 10 requeues for the backoff delay to be relevant (about 1min).

**What you expected to happen**:

The default base backoff should be larger than 10s to make it relevant to end-users.
Make the default and potentially (TBD) configurable.

If we agree on the default of 10s we could back-port it to 0.6 branch.

**How to reproduce it (as minimally and precisely as possible)**:

Example global configuration:
```yaml
waitForPodsReady:
  enable: true
  timeout: 1m
  blockAdmission: false
  requeuingStrategy:
    timestamp: Creation
    backoffLimitCount: 4
 ```
 Example cluster configuration:
 ```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 200
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
 ```
 Example Job:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: sample-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 1
  completions: 1
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["1800s"]
        resources:
          requests:
            cpu: "50"
            memory: "200Mi"
      restartPolicy: Never
```

Watching the events we can see:
```sh
> kubectl get workloads -w --output-watch-events       
EVENT      NAME                   QUEUE        ADMITTED BY   AGE
ADDED      job-sample-job-b1ca7   user-queue                 13m
MODIFIED   job-sample-job-b1ca7   user-queue                 13m
DELETED    job-sample-job-b1ca7   user-queue                 13m
ADDED      job-sample-job-08913   user-queue                 0s
MODIFIED   job-sample-job-08913   user-queue                 0s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   0s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   60s
MODIFIED   job-sample-job-08913   user-queue                   61s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   61s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   2m1s
MODIFIED   job-sample-job-08913   user-queue                   2m2s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   2m2s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   3m2s
MODIFIED   job-sample-job-08913   user-queue                   3m3s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   3m3s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   4m3s
MODIFIED   job-sample-job-08913   user-queue                   4m4s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   4m5s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   5m5s
MODIFIED   job-sample-job-08913   user-queue                   5m6s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   5m8s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   6m8s
MODIFIED   job-sample-job-08913   user-queue                   6m9s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   6m13s
MODIFIED   job-sample-job-08913   user-queue   cluster-queue   7m13s
MODIFIED   job-sample-job-08913   user-queue                   7m14s
```

**Anything else we need to know?**:

The algorithm is described [here](https://github.com/kubernetes-sigs/kueue/tree/main/keps/1282-pods-ready-requeue-strategy#exponential-backoff-mechanism).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-18T16:18:01Z

/cc @tenzen-y @alculquicondor

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-18T16:21:03Z

> The default base backoff should be larger than 10s to make it noticable to end-users.
> Make the default and potentially (TBD) configurable.
> 
> If we agree on the default of 10s we could back-port it to 0.6 branch.

I agree with this idea. I'm curious about whether we can override the backoff time with 10s when the backoff time is less than 10s.
WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-18T16:26:25Z

> I agree with this idea. I'm curious about whether we can override the backoff time with 10s when the backoff time is less than 10s.
> WDYT?

Do you mean `max(10s, computed backoff starting from 1s)`? I guess it makes the formula harder to explain to end-users (which is already hard).

Also, it would mean still 7-8 requeues with ~10s delay.

I was thinking about changing the default [here](https://github.com/kubernetes-sigs/kueue/blob/472ce6d2c6bbfab2903db065dbb8f117415bc8d5/pkg/controller/core/workload_controller.go#L401-L401), but making it configurable.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T13:31:46Z

@tenzen-y any reason the base is `1.41...`? It makes rough manual calculations unnecessarily trickier. 

I'm wondering if we could consider making the defaults as for [pod failure backoff](https://kubernetes.io/docs/concepts/workloads/controllers/job/#pod-backoff-failure-policy): 10s base and exponent of 2? 
`the back-off limit is set by default to 6. Failed Pods associated with the Job are recreated by the Job controller with an exponential back-off delay (10s, 20s, 40s ...) capped at six minutes.`

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-19T14:03:15Z

> Do you mean max(10s, computed backoff starting from 1s)? I guess it makes the formula harder to explain to end-users (which is already hard).
> 
> Also, it would mean still 7-8 requeues with ~10s delay.
> 
> I was thinking about changing the default [here](https://github.com/kubernetes-sigs/kueue/blob/472ce6d2c6bbfab2903db065dbb8f117415bc8d5/pkg/controller/core/workload_controller.go#L401-L401), but making it configurable.

That makes sense. I'm ok with replacing the `Duration` with 10s.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T14:04:36Z

> That makes sense. I'm ok with replacing the Duration with 10s.

How about changing the exponent to 2, as per: https://github.com/kubernetes-sigs/kueue/issues/2009#issuecomment-2066596645?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-19T14:05:24Z

> @tenzen-y any reason the base is 1.41...? It makes rough manual calculations unnecessarily trickier.
> 
> I'm wondering if we could consider making the defaults as for [pod failure backoff](https://kubernetes.io/docs/concepts/workloads/controllers/job/#pod-backoff-failure-policy): 10s base and exponent of 2?
> the back-off limit is set by default to 6. Failed Pods associated with the Job are recreated by the Job controller with an exponential back-off delay (10s, 20s, 40s ...) capped at six minutes.

@mimowo As I described there, I defined the magic number so that we can make the duration estimatable.

https://github.com/kubernetes-sigs/kueue/blob/472ce6d2c6bbfab2903db065dbb8f117415bc8d5/pkg/controller/core/workload_controller.go#L392-L399

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-19T14:10:48Z

> @tenzen-y any reason the base is `1.41...`? It makes rough manual calculations unnecessarily trickier.
> 
> I'm wondering if we could consider making the defaults as for [pod failure backoff](https://kubernetes.io/docs/concepts/workloads/controllers/job/#pod-backoff-failure-policy): 10s base and exponent of 2? `the back-off limit is set by default to 6. Failed Pods associated with the Job are recreated by the Job controller with an exponential back-off delay (10s, 20s, 40s ...) capped at six minutes.`

It sounds good to me, but no restricting requeuingCount as a default value would be better. (As my understanding, the pod failure policy set `6` as a default.)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T14:29:50Z

/assign
