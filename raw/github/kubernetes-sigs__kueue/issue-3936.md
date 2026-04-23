# Issue #3936: Workload is admitted, but job remains suspended

**Summary**: Workload is admitted, but job remains suspended

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3936

**Last updated**: 2025-06-14T01:29:23Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@arvind-v](https://github.com/arvind-v)
- **Created**: 2025-01-07T01:49:37Z
- **Updated**: 2025-06-14T01:29:23Z
- **Closed**: 2025-06-14T01:29:22Z
- **Labels**: `kind/bug`, `triage/needs-information`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What happened**: 
I am trying to get a simple test case with Kueue running. The Workload is admitted, but the Job named `test-job-one`  remains in a suspended state. 

```
$ kubectl get workloads -A
NAMESPACE    NAME                     QUEUE               RESERVED IN     ADMITTED   FINISHED   AGE
kueue-jobs   job-test-job-one-5e3de   ml-training-queue   cluster-queue   True                  92s

$ kubectl get jobs -A
NAMESPACE        NAME              STATUS      COMPLETIONS   DURATION   AGE
kubemod-system   kubemod-crt-job   Complete    1/1           4s         64m
kueue-jobs       test-job-one      Suspended   0/1                      112s

```

**What you expected to happen**:
I was expecting that the job would run once admitted. 

**How to reproduce it (as minimally and precisely as possible)**:

ResourceFlavor, ClusterQueue, LocalQueue and Job specs: 

```
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default-flavor
spec: {}
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cluster-queue
spec:
  namespaceSelector: {} # match all
  resourceGroups:
  - coveredResources: ["cpu", "memory", "pods"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: "300m"
      - name: "memory"
        nominalQuota: "512Mi"
      - name: "pods"
        nominalQuota: 5
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: ml-training-queue
  namespace: kueue-jobs
spec:
  clusterQueue: cluster-queue
---
apiVersion: batch/v1
kind: Job
metadata:
  name: test-job-one
  namespace: kueue-jobs
  labels:
    kueue.x-k8s.io/queue-name: ml-training-queue
spec:
  suspend: true
  template:
    spec:
      containers:
      - name: test
        image: busybox
        command: ["sh", "-c", "echo 'Hello from Kueue!' && sleep 30"]
        resources:
          requests:
            cpu: "200m"
            memory: "256Mi"
      restartPolicy: Never
---
```

Here is the output from the troubleshooting steps. This is the only job in the cluster. 

```
$ kubectl describe job  -n kueue-job
Name:             test-job-one
Namespace:        kueue-jobs
Selector:         batch.kubernetes.io/controller-uid=d01cd96b-e986-4533-b9ab-50965226e5a0
Labels:           kueue.x-k8s.io/queue-name=ml-training-queue
Annotations:      <none>
Parallelism:      1
Completions:      1
Completion Mode:  NonIndexed
Suspend:          true
Backoff Limit:    6
Pods Statuses:    0 Active (0 Ready) / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  batch.kubernetes.io/controller-uid=d01cd96b-e986-4533-b9ab-50965226e5a0
           batch.kubernetes.io/job-name=test-job-one
           controller-uid=d01cd96b-e986-4533-b9ab-50965226e5a0
           job-name=test-job-one
  Containers:
   test:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      echo 'Hello from Kueue!' && sleep 30
    Requests:
      cpu:         200m
      memory:      256Mi
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Events:
  Type    Reason           Age                    From                        Message
  ----    ------           ----                   ----                        -------
  Normal  Suspended        4m22s                  job-controller              Job suspended
  Normal  CreatedWorkload  4m22s                  batch/job-kueue-controller  Created Workload: kueue-jobs/job-test-job-one-5e3de
  Normal  Started          4m22s (x2 over 4m22s)  batch/job-kueue-controller  Admitted by clusterQueue cluster-queue
```

**Environment**:
- Kubernetes version (use `kubectl version`): Client Version: v1.30.2, Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3, Server Version: v1.31.4-eks-2d5f260
- Kueue version (use `git describe --tags --dirty --always`):  v0.10.0
- Cloud provider or hardware configuration: Amazon EKS
- OS (e.g: `cat /etc/os-release`): Amazon Linux 2
- Install tools: helm

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-07T07:26:48Z

I tried testing it locally. It seems to be working fine. 

```
kind create cluster

helm install kueue kueue/ --create-namespace --namespace kueue-system
kubectl wait deploy/kueue-controller-manager -nkueue-system --for=condition=available --timeout=5m

kubectl create ns kueue-jobs
kubectl apply -f manifests.yaml

kubectl get po -n kueue-jobs                                          
NAME                 READY   STATUS    RESTARTS   AGE
test-job-one-4scls   1/1     Running   0          24s

kubectl describe job -n kueue-jobs
Name:             test-job-one
Namespace:        kueue-jobs
Selector:         batch.kubernetes.io/controller-uid=4e82e59b-4aee-4446-8a8a-6004faabcf43
Labels:           kueue.x-k8s.io/queue-name=ml-training-queue
Annotations:      <none>
Parallelism:      1
Completions:      1
Completion Mode:  NonIndexed
Suspend:          false
Backoff Limit:    6
Start Time:       Tue, 07 Jan 2025 09:24:32 +0200
Pods Statuses:    1 Active (1 Ready) / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  batch.kubernetes.io/controller-uid=4e82e59b-4aee-4446-8a8a-6004faabcf43
           batch.kubernetes.io/job-name=test-job-one
           controller-uid=4e82e59b-4aee-4446-8a8a-6004faabcf43
           job-name=test-job-one
  Containers:
   test:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      echo 'Hello from Kueue!' && sleep 30
    Requests:
      cpu:         200m
      memory:      256Mi
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Events:
  Type    Reason            Age   From                        Message
  ----    ------            ----  ----                        -------
  Normal  Suspended         15s   job-controller              Job suspended
  Normal  CreatedWorkload   15s   batch/job-kueue-controller  Created Workload: kueue-jobs/job-test-job-one-223a0
  Normal  Started           15s   batch/job-kueue-controller  Admitted by clusterQueue cluster-queue
  Normal  SuccessfulCreate  15s   job-controller              Created pod: test-job-one-k56js
  Normal  Resumed           15s   job-controller              Job resumed
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-07T07:46:33Z

Could you please check logs ?

```
kubectl logs -f -l app.kubernetes.io/name=kueue -n kueue-system
```

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-15T01:12:31Z

/triage needs-information

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-15T01:18:36Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-15T01:22:25Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-14T01:29:17Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-14T01:29:23Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3936#issuecomment-2972087361):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
