# Issue #4098: Documentation specifies Kubeflow jobs, but not SparkApplication

**Summary**: Documentation specifies Kubeflow jobs, but not SparkApplication

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4098

**Last updated**: 2025-08-07T13:20:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@danc](https://github.com/danc)
- **Created**: 2025-01-29T16:57:11Z
- **Updated**: 2025-08-07T13:20:02Z
- **Closed**: 2025-08-07T13:20:02Z
- **Labels**: `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

Could doc clarify if [Kubeflow SparkApplications](https://www.kubeflow.org/docs/components/spark-operator/user-guide/writing-sparkapplication/) are supported by kueue ?

I'm currently able to submit Jobs to kueue, but SparkApplications appear not to be passing via the LocalQueue (maybe some info missing)
Example failing yaml. (SparkApplication succeeds, but is not managed by Queue) : 

```
apiVersion: "sparkoperator.k8s.io/v1beta2"
kind: SparkApplication
metadata:
  generateName: spark-pi-ingestion-
  namespace: mining
  labels:
    app: spark
    kueue.x-k8s.io/queue-name: lq-spark
spec:
  timeToLiveSeconds: 60
  type: Scala
  mode: cluster
  image: "apache/spark:3.4.1"
  imagePullPolicy: IfNotPresent
  mainClass: org.apache.spark.examples.SparkPi
  mainApplicationFile: "local:///opt/spark/examples/jars/spark-examples_2.12-3.4.1.jar"
  arguments:
    - "10"
  sparkVersion: "3.4.1"
  restartPolicy:
    type: Never
  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "512m"
    labels:
      version: 3.4.1
      app: spark
    serviceAccount: logpickr-api
  executor:
    cores: 1
    instances: 1
    memory: "512m"
    labels:
      version: 3.4.1
      app: spark
```

## Discussion

### Comment by [@everpeace](https://github.com/everpeace) — 2025-01-30T10:04:27Z

> Could doc clarify if [Kubeflow SparkApplications](https://www.kubeflow.org/docs/components/spark-operator/user-guide/writing-sparkapplication/) are supported by kueue ?

I think [Tasks / Run Workloads / Kubeflow Jobs](https://kueue.sigs.k8s.io/docs/tasks/run/) page clearly states so (the list does not contain Kubeflow Spark Operator(`SparkApplication`)).

And, [Tasks / Developer Tools / Integrate a custom Job with Kueue](https://kueue.sigs.k8s.io/docs/tasks/dev/integrate_a_custom_job/) also clearly instructs how to support custom jobs in Kueue.

By the way, Kueue community already aware the spark issue and already have grand design how to support spark workloards in Kueue: #1656

### Comment by [@danc](https://github.com/danc) — 2025-01-30T11:30:28Z

Thanks for the confirmation, shared links, and grand design perspective.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-31T15:59:08Z

It seems clear to me but you could add that the list of kubeflow jobs in that list are the ones that we support in-tree for Kueue.

Maybe adding something like:
 The following list are the supported frameworks for Kueue and Kubeflow.

You could add it [here](https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/tasks/run/kubeflow/_index.md).

### Comment by [@danc](https://github.com/danc) — 2025-01-31T16:28:02Z

I see some other works in progress : https://github.com/kubernetes-sigs/kueue/pull/4032

### Comment by [@everpeace](https://github.com/everpeace) — 2025-04-09T12:05:03Z

As you notieced, https://github.com/kubernetes-sigs/kueue/pull/4032 was closed because it does not follow the design doc(https://github.com/kubernetes-sigs/kueue/issues/1656) which is already written.

But, another PR that follows the design doc has been already opened: https://github.com/kubernetes-sigs/kueue/pull/4102 (in review)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-08T12:21:46Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-07T13:17:01Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-07T13:19:57Z

I don't think we need to keep this open.

I agree with @everpeace that the list of supported workloads is clear enough.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-07T13:20:02Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4098#issuecomment-3164178364):

>I don't think we need to keep this open.
>
>I agree with @everpeace that the list of supported workloads is clear enough.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
