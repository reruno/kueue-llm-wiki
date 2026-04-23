# Issue #8387: Setting workload active=false does not work

**Summary**: Setting workload active=false does not work

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8387

**Last updated**: 2025-12-25T10:13:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@izturn](https://github.com/izturn)
- **Created**: 2025-12-22T10:12:34Z
- **Updated**: 2025-12-25T10:13:36Z
- **Closed**: 2025-12-25T08:26:09Z
- **Labels**: `kind/support`, `needs-kind`
- **Assignees**: _none_
- **Comments**: 19

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I am using the latest version of **Kueue** and created a simple **PyTorchJob**.

After the job **started running** normally, I updated the corresponding Workload by setting **active=false**.

From the status and logs, the workload is correctly marked as **Evicted**, but the actual execution behavior is incorrect — the PyTorchJob continues running and eventually **completes**, instead of being stopped or suspended.

This suggests that the active field does not take effect for an already running PyTorchJob.

**What you expected to happen**:
suspend
**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:
the workload as follows: 
```apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  creationTimestamp: '2025-12-22T09:34:42Z'
  generation: 2
  labels:
    kueue.x-k8s.io/job-uid: c250a4b4-a69b-4872-ba98-8b29b83007a4
  name: pytorchjob-job-suspend-test-cea58
  namespace: default
  ownerReferences:
    - apiVersion: kubeflow.org/v1
      blockOwnerDeletion: true
      controller: true
      kind: PyTorchJob
      name: job-suspend-test
      uid: c250a4b4-a69b-4872-ba98-8b29b83007a4
  resourceVersion: '11337900'
  uid: f4e604f2-139a-4860-a742-e824c76fb20a
  selfLink: >-
    /apis/kueue.x-k8s.io/v1beta1/namespaces/default/workloads/pytorchjob-job-suspend-test-cea58
status:
  accumulatedPastExexcutionTimeSeconds: 103
  conditions:
    - lastTransitionTime: '2025-12-22T09:36:25Z'
      message: Workload has finished
      observedGeneration: 2
      reason: Finished
      status: 'False'
      type: QuotaReserved
    - lastTransitionTime: '2025-12-22T09:35:24Z'
      message: The workload is deactivated
      observedGeneration: 2
      reason: Deactivated
      status: 'True'
      type: Evicted
    - lastTransitionTime: '2025-12-22T09:36:25Z'
      message: Workload has finished
      observedGeneration: 2
      reason: Finished
      status: 'False'
      type: Admitted
    - lastTransitionTime: '2025-12-22T09:36:25Z'
      message: PyTorchJob default/job-suspend-test successfully completed.
      observedGeneration: 2
      reason: Succeeded
      status: 'True'
      type: Finished
  schedulingStats:
    evictions:
      - count: 1
        reason: Deactivated
        underlyingCause: ''
spec:
  active: false
  podSets:
    - count: 1
      name: worker
      template:
        metadata: {}
        spec:
          affinity: {}
          containers:
            - args:
                - |-
                  date
                  for i in {1..100}; do
                    echo "$i: hello"
                    sleep 1
                  done
              command:
                - /bin/bash
                - '-c'
              image: ''
              imagePullPolicy: Always
              name: pytorch
              resources:
                limits:
                  cpu: '1'
                  memory: 2Gi
                requests:
                  cpu: '1'
                  memory: 2Gi
          priorityClassName: test-medium-priority
          schedulerName: default-scheduler
          securityContext:
            fsGroup: 100
      topologyRequest:
        podIndexLabel: training.kubeflow.org/replica-index
  priority: 10000
  priorityClassName: test-medium-priority
  priorityClassSource: scheduling.k8s.io/priorityclass
  queueName: default-queue

```
**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

Any suggestions on how to further diagnose or resolve this issue would be greatly appreciated.

## Discussion

### Comment by [@izturn](https://github.com/izturn) — 2025-12-23T09:55:39Z

@mimowo @PBundyra gentle ping

### Comment by [@chengjoey](https://github.com/chengjoey) — 2025-12-23T10:05:18Z

Could you provide a reproduce? I tested a simple running pytorchjob with workload active==false, and it was successfully evicted.

### Comment by [@izturn](https://github.com/izturn) — 2025-12-23T10:22:36Z

Sorry about that — the related cluster has already been deleted.
However, the reproduction steps are quite simple:

Create a PyTorchJob that runs the following command:
 ```
containers:
            - args:
                - |-
                  date
                  for i in {1..100}; do
                    echo "$i: hello"
                    sleep 1
                  done
              command:
                - /bin/bash
                - '-c'

```

While the command is still running, update the corresponding Workload and set **active to false**.

According to feedback from QA (not personally verified), this issue does not occur in the 0.14.x series.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-24T09:56:17Z

I also tested this on my side, and everything looks to be working fine. This is the job I tested:

```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: pytorch-simple
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  pytorchReplicaSpecs:
    Worker:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: docker.io/kubeflowkatib/pytorch-mnist-cpu:v1beta1-21320b6
#              If you have gpu, pytorch-mnist-gpu would be helpful. pytorch-mnist-gpu is approximately 22GB
#              image: docker.io/kubeflowkatib/pytorch-mnist-cpu:latest
              imagePullPolicy: Always
              args:
                - |-
                  date
                  for i in {1..100}; do
                    echo "$i: hello"
                    sleep 1
                  done
              command:
                - /bin/bash
                - '-c'
              resources:
                limits:
                  cpu: '1'
                  memory: 2Gi
                requests:
                  cpu: '1'
                  memory: 2Gi
```

After deactivation pod terminating:

```
NAME                                READY   STATUS        RESTARTS   AGE
pytorch-simple-worker-0             1/1     Terminating   0          112s
```

### Comment by [@chengjoey](https://github.com/chengjoey) — 2025-12-24T10:14:10Z

> I also tested this on my side, and everything looks to be working fine. This is the job I tested:

+1

### Comment by [@izturn](https://github.com/izturn) — 2025-12-24T10:20:37Z

@mbobrovskyi Could you paste the `workload` YAML here for reference?

### Comment by [@chengjoey](https://github.com/chengjoey) — 2025-12-24T11:22:24Z

> [@mbobrovskyi](https://github.com/mbobrovskyi) Could you paste the `workload` YAML here for reference?

examples/jobs/sample-pytorchjob.yaml

The workload generated by this job should be the same, just replace the args with your examples.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-24T11:50:54Z

> @mbobrovskyi Could you paste the workload YAML here for reference?

You’re lucky – I still have it 🙂

```yaml
apiVersion: v1
items:
- apiVersion: kueue.x-k8s.io/v1beta2
  kind: Workload
  metadata:
    creationTimestamp: "2025-12-24T09:51:08Z"
    finalizers:
    - kueue.x-k8s.io/resource-in-use
    generation: 2
    labels:
      kueue.x-k8s.io/job-uid: 0a6b4c89-65cf-413d-8cf3-a334b66f48c6
    name: pytorchjob-pytorch-simple-dfbe0
    namespace: default
    ownerReferences:
    - apiVersion: kubeflow.org/v1
      blockOwnerDeletion: true
      controller: true
      kind: PyTorchJob
      name: pytorch-simple
      uid: 0a6b4c89-65cf-413d-8cf3-a334b66f48c6
    resourceVersion: "3642"
    uid: 8b213b35-6d1f-464e-9c5e-4315fa80899a
  spec:
    active: false
    podSets:
    - count: 1
      name: worker
      template:
        metadata: {}
        spec:
          containers:
          - args:
            - |-
              date
              for i in {1..100}; do
                echo "$i: hello"
                sleep 1
              done
            command:
            - /bin/bash
            - -c
            image: docker.io/kubeflowkatib/pytorch-mnist-cpu:v1beta1-21320b6
            imagePullPolicy: Always
            name: pytorch
            resources:
              limits:
                cpu: "1"
                memory: 2Gi
              requests:
                cpu: "1"
                memory: 2Gi
      topologyRequest:
        podIndexLabel: training.kubeflow.org/replica-index
    priority: 0
    queueName: user-queue
  status:
    accumulatedPastExecutionTimeSeconds: 93
    conditions:
    - lastTransitionTime: "2025-12-24T09:52:41Z"
      message: The workload is deactivated
      observedGeneration: 2
      reason: Pending
      status: "False"
      type: QuotaReserved
    - lastTransitionTime: "2025-12-24T09:52:41Z"
      message: The workload is deactivated
      observedGeneration: 2
      reason: Deactivated
      status: "True"
      type: Evicted
    - lastTransitionTime: "2025-12-24T09:52:41Z"
      message: The workload has no reservation
      observedGeneration: 2
      reason: NoReservation
      status: "False"
      type: Admitted
    - lastTransitionTime: "2025-12-24T09:52:41Z"
      message: The workload is deactivated
      observedGeneration: 2
      reason: Deactivated
      status: "False"
      type: Requeued
    schedulingStats:
      evictions:
      - count: 1
        reason: Deactivated
        underlyingCause: ""
kind: List
metadata:
  resourceVersion: ""
```

### Comment by [@izturn](https://github.com/izturn) — 2025-12-25T01:52:12Z

@mbobrovskyi  

mine: 

<img width="810" height="535" alt="Image" src="https://github.com/user-attachments/assets/1a756bab-5ea7-4ad0-b475-c8ee9f9c7ee4" />
yours: 

<img width="844" height="837" alt="Image" src="https://github.com/user-attachments/assets/42849494-0e0a-4584-89aa-07338c3033b1" />
I suspect there might be an issue here.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-25T04:53:58Z

Yeah, that’s the problem. Kueue evicted it, but for some reason it doesn’t set QuotaReserved=false and Admitted=false. Do you have logs? They would help a lot.

### Comment by [@izturn](https://github.com/izturn) — 2025-12-25T05:56:08Z

```
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.295407588Z","logger":"workload-reconciler","caller":"core/workload_controller.go:874","msg":"Workload update event","workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"queue":"default-queue","status":"admitted","clusterQueue":"default-queue"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.295528885Z","logger":"workload-reconciler","caller":"core/workload_controller.go:883","msg":"Workload will not be queued because the workload is not active","workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"queue":"default-queue","status":"admitted","clusterQueue":"default-queue"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.29554129Z","caller":"jobframework/reconciler.go:401","msg":"Reconciling Job","controller":"pytorchjob","controllerGroup":"kubeflow.org","controllerKind":"PyTorchJob","PyTorchJob":{"name":"pytorch-simple","namespace":"default"},"namespace":"default","name":"pytorch-simple","reconcileID":"d5736e7c-defe-456e-bf18-604f6f08d2ad","job":"default/pytorch-simple","gvk":"kubeflow.org/v1, Kind=PyTorchJob"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.295670394Z","caller":"core/workload_controller.go:173","msg":"Reconcile Workload","controller":"workload_controller","namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"b27a14ca-70c0-4ca8-9b4d-c8ff90283032"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.295726643Z","caller":"multikueue/workload.go:165","msg":"Reconcile Workload","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"7d3ab1b4-8949-4b63-a557-ad08f72965be"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.295798195Z","caller":"multikueue/workload.go:191","msg":"Skip Workload","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"7d3ab1b4-8949-4b63-a557-ad08f72965be","isDeleted":false}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.326435123Z","logger":"workload-reconciler","caller":"core/workload_controller.go:874","msg":"Workload update event","workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"queue":"default-queue","status":"admitted","clusterQueue":"default-queue"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.326479042Z","caller":"jobframework/reconciler.go:401","msg":"Reconciling Job","controller":"pytorchjob","controllerGroup":"kubeflow.org","controllerKind":"PyTorchJob","PyTorchJob":{"name":"pytorch-simple","namespace":"default"},"namespace":"default","name":"pytorch-simple","reconcileID":"2b96db7c-b80f-4d57-a809-ad8d85a9b46d","job":"default/pytorch-simple","gvk":"kubeflow.org/v1, Kind=PyTorchJob"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.32644496Z","caller":"multikueue/workload.go:165","msg":"Reconcile Workload","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"d8e1ebe3-9145-4e80-a0be-54d6295955e8"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.326516562Z","logger":"workload-reconciler","caller":"core/workload_controller.go:883","msg":"Workload will not be queued because the workload is not active","workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"queue":"default-queue","status":"admitted","clusterQueue":"default-queue"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.326572488Z","caller":"multikueue/workload.go:191","msg":"Skip Workload","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"d8e1ebe3-9145-4e80-a0be-54d6295955e8","isDeleted":false}
2025/12/25 05:48:52 http: TLS handshake error from 10.70.44.7:27940: EOF
{"level":"Level(-2)","ts":"2025-12-25T05:48:52.327019825Z","caller":"core/workload_controller.go:173","msg":"Reconcile Workload","controller":"workload_controller","namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"f709e167-3c56-48d8-9f14-ef69dbb945f8"}
{"level":"debug","ts":"2025-12-25T05:48:52.327095144Z","logger":"events","caller":"recorder/recorder.go:104","msg":"The workload is deactivated","type":"Normal","object":{"kind":"Workload","namespace":"default","name":"pytorchjob-pytorch-simple-a7194","uid":"90493afd-4186-4f6e-ace9-454d53b5299d","apiVersion":"kueue.x-k8s.io/v1beta2","resourceVersion":"1105281"},"reason":"EvictedDueToDeactivated"}
{"level":"info","ts":"2025-12-25T05:48:52.332449593Z","logger":"admission","caller":"jobframework/base_webhook.go:100","msg":"Validating update","webhookGroup":"kubeflow.org","webhookKind":"PyTorchJob","PyTorchJob":{"name":"pytorch-simple","namespace":"default"},"namespace":"default","name":"pytorch-simple","resource":{"group":"kubeflow.org","version":"v1","resource":"pytorchjobs"},"user":"system:serviceaccount:baize-system:kueue-controller-manager","requestID":"dc506e71-38da-4943-8930-25215fd9636d"}
{"level":"info","ts":"2025-12-25T05:48:52.335274853Z","caller":"log/warning_handler.go:64","msg":"unknown field \"spec.runPolicy.suspend\"","controller":"pytorchjob","controllerGroup":"kubeflow.org","controllerKind":"PyTorchJob","PyTorchJob":{"name":"pytorch-simple","namespace":"default"},"namespace":"default","name":"pytorch-simple","reconcileID":"2b96db7c-b80f-4d57-a809-ad8d85a9b46d","job":"default/pytorch-simple","gvk":"kubeflow.org/v1, Kind=PyTorchJob"}
{"level":"debug","ts":"2025-12-25T05:48:52.335925516Z","logger":"events","caller":"recorder/recorder.go:104","msg":"The workload is deactivated","type":"Normal","object":{"kind":"PyTorchJob","namespace":"default","name":"pytorch-simple","uid":"63b2f9d0-2b76-41a3-b181-df1e7fe5afd8","apiVersion":"kubeflow.org/v1","resourceVersion":"1104761"},"reason":"Stopped"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:53.296805869Z","caller":"core/localqueue_controller.go:153","msg":"Reconcile LocalQueue","controller":"localqueue_controller","namespace":"default","name":"default-queue","reconcileID":"e1ec9d2d-ad84-43b1-a5e6-a0e74b319ed8"}
{"level":"Level(-2)","ts":"2025-12-25T05:48:53.296818413Z","caller":"core/clusterqueue_controller.go:147","msg":"Reconcile ClusterQueue","controller":"clusterqueue_controller","namespace":"","name":"default-queue","reconcileID":"04559300-dec4-4a27-af13-27c85672b3a6"}
2025/12/25 05:48:53 http: TLS handshake error from 10.70.44.7:58481: EOF
2025/12/25 05:48:53 http: TLS handshake error from 10.70.44.7:8071: EOF
{"level":"Level(-2)","ts":"2025-12-25T05:48:53.309114314Z","logger":"localqueue-reconciler","caller":"core/localqueue_controller.go:240","msg":"Queue update event","localQueue":{"name":"default-queue","namespace":"default"}}
{"level":"Level(-2)","ts":"2025-12-25T05:48:53.309209406Z","caller":"core/localqueue_controller.go:153","msg":"Reconcile LocalQueue","controller":"localqueue_controller","namespace":"default","name":"default-queue","reconcileID":"185bf27b-edad-44a5-ab4e-dfb0b167058a"}
2025/12/25 05:48:53 http: TLS handshake error from 10.70.44.7:29064: EOF
{"level":"Level(-2)","ts":"2025-12-25T05:48:53.310947403Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:324","msg":"ClusterQueue update event","clusterQueue":{"name":"default-queue"}}
2025/12/25 05:48:53 http: TLS handshake error from 10.70.44.7:20936: EOF
{"level":"Level(-2)","ts":"2025-12-25T05:48:53.311113556Z","caller":"core/clusterqueue_controller.go:147","msg":"Reconcile ClusterQueue","controller":"clusterqueue_controller","namespace":"","name":"default-queue","reconcileID":"5aafad1c-1ee5-437e-a5d4-f45cb7eafb87"}
2025/12/25 05:48:53 http: TLS handshake error from 10.70.44.7:1193: EOF
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.707805009Z","caller":"jobframework/reconciler.go:401","msg":"Reconciling Job","controller":"pytorchjob","controllerGroup":"kubeflow.org","controllerKind":"PyTorchJob","PyTorchJob":{"name":"pytorch-simple","namespace":"default"},"namespace":"default","name":"pytorch-simple","reconcileID":"c1f3678d-1506-4d81-b504-942a5b3c8335","job":"default/pytorch-simple","gvk":"kubeflow.org/v1, Kind=PyTorchJob"}
{"level":"debug","ts":"2025-12-25T05:49:12.740297169Z","logger":"events","caller":"recorder/recorder.go:104","msg":"Workload 'default/pytorchjob-pytorch-simple-a7194' is declared finished","type":"Normal","object":{"kind":"PyTorchJob","namespace":"default","name":"pytorch-simple","uid":"63b2f9d0-2b76-41a3-b181-df1e7fe5afd8","apiVersion":"kubeflow.org/v1","resourceVersion":"1105430"},"reason":"FinishedWorkload"}
2025/12/25 05:49:12 http: TLS handshake error from 10.70.44.7:7618: EOF
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.741389654Z","caller":"multikueue/workload.go:165","msg":"Reconcile Workload","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"95668c08-c93b-49d5-a1d1-938674b26bfa"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.74146682Z","caller":"multikueue/workload.go:191","msg":"Skip Workload","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"95668c08-c93b-49d5-a1d1-938674b26bfa","isDeleted":false}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.741464206Z","logger":"workload-reconciler","caller":"core/workload_controller.go:874","msg":"Workload update event","workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"queue":"default-queue","status":"finished","prevStatus":"admitted","prevClusterQueue":"default-queue"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.741547521Z","caller":"jobframework/reconciler.go:401","msg":"Reconciling Job","controller":"pytorchjob","controllerGroup":"kubeflow.org","controllerKind":"PyTorchJob","PyTorchJob":{"name":"pytorch-simple","namespace":"default"},"namespace":"default","name":"pytorch-simple","reconcileID":"7929fe82-7a5c-4db0-a112-6de332c9a1eb","job":"default/pytorch-simple","gvk":"kubeflow.org/v1, Kind=PyTorchJob"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.741601094Z","logger":"workload-reconciler","caller":"core/workload_controller.go:883","msg":"Workload will not be queued because the workload is not active","workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"queue":"default-queue","status":"finished","prevStatus":"admitted","prevClusterQueue":"default-queue"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.741762075Z","caller":"core/workload_controller.go:173","msg":"Reconcile Workload","controller":"workload_controller","namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"56fb3507-a42c-45eb-8fec-3b5b2ab76618"}
{"level":"debug","ts":"2025-12-25T05:49:12.741787628Z","logger":"events","caller":"recorder/recorder.go:104","msg":"Workload 'default/pytorchjob-pytorch-simple-a7194' is declared finished","type":"Normal","object":{"kind":"PyTorchJob","namespace":"default","name":"pytorch-simple","uid":"63b2f9d0-2b76-41a3-b181-df1e7fe5afd8","apiVersion":"kubeflow.org/v1","resourceVersion":"1105430"},"reason":"FinishedWorkload"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.766230778Z","logger":"workload-reconciler","caller":"core/workload_controller.go:874","msg":"Workload update event","workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"queue":"default-queue","status":"finished"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.766259588Z","caller":"multikueue/workload.go:165","msg":"Reconcile Workload","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"3c4c3b8b-ad22-43d6-a3ce-9e94bd2cd439"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.766344888Z","logger":"workload-reconciler","caller":"core/workload_controller.go:883","msg":"Workload will not be queued because the workload is not active","workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"queue":"default-queue","status":"finished"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.766350297Z","caller":"multikueue/workload.go:191","msg":"Skip Workload","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"pytorchjob-pytorch-simple-a7194","namespace":"default"},"namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"3c4c3b8b-ad22-43d6-a3ce-9e94bd2cd439","isDeleted":false}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.766456361Z","caller":"core/workload_controller.go:173","msg":"Reconcile Workload","controller":"workload_controller","namespace":"default","name":"pytorchjob-pytorch-simple-a7194","reconcileID":"35645c35-46d4-471a-86fe-00c4d6162b54"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:12.767926815Z","caller":"jobframework/reconciler.go:401","msg":"Reconciling Job","controller":"pytorchjob","controllerGroup":"kubeflow.org","controllerKind":"PyTorchJob","PyTorchJob":{"name":"pytorch-simple","namespace":"default"},"namespace":"default","name":"pytorch-simple","reconcileID":"efccb34a-8eaf-4e5e-a3bd-22b62cf69d40","job":"default/pytorch-simple","gvk":"kubeflow.org/v1, Kind=PyTorchJob"}
{"level":"debug","ts":"2025-12-25T05:49:12.768084154Z","logger":"events","caller":"recorder/recorder.go:104","msg":"Workload 'default/pytorchjob-pytorch-simple-a7194' is declared finished","type":"Normal","object":{"kind":"PyTorchJob","namespace":"default","name":"pytorch-simple","uid":"63b2f9d0-2b76-41a3-b181-df1e7fe5afd8","apiVersion":"kubeflow.org/v1","resourceVersion":"1105430"},"reason":"FinishedWorkload"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:13.742514033Z","caller":"core/clusterqueue_controller.go:147","msg":"Reconcile ClusterQueue","controller":"clusterqueue_controller","namespace":"","name":"default-queue","reconcileID":"f8b93ece-b538-4bfd-b69b-bbecb332772f"}
{"level":"Level(-2)","ts":"2025-12-25T05:49:13.742514057Z","caller":"core/localqueue_controller.go:153","msg":"Reconcile LocalQueue","controller":"localqueue_controller","namespace":"default","name":"default-queue","reconcileID":"96f486a8-0595-468a-aff1-eb37d36a91f9"}
```
@mbobrovskyi retry with the log as above. thanks for your help

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-25T07:25:07Z

> {"level":"info","ts":"2025-12-25T05:48:52.335274853Z","caller":"log/warning_handler.go:64","msg":"unknown field \"spec.runPolicy.suspend\"","controller":"pytorchjob","controllerGroup":"kubeflow.org","controllerKind":"PyTorchJob","PyTorchJob":{"name":"pytorch-simple","namespace":"default"},"namespace":"default","name":"pytorch-simple","reconcileID":"2b96db7c-b80f-4d57-a809-ad8d85a9b46d","job":"default/pytorch-simple","gvk":"kubeflow.org/v1, Kind=PyTorchJob"}

Hmmm. This is interesting. Which version of Kubeflow do you have?

### Comment by [@izturn](https://github.com/izturn) — 2025-12-25T07:30:12Z

docker.io/kubeflow/training-operator:v1-5525468

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-25T07:35:06Z

What about this?

```
kubectl api-resources | grep PyTorchJob
```

### Comment by [@izturn](https://github.com/izturn) — 2025-12-25T07:38:53Z

[root@test ~]# kubectl api-resources | grep PyTorchJob
pytorchjobs                                             kubeflow.org/v1                     true         PyTorchJob

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-25T08:00:49Z

I didn't got why but it looks like you don't have `.spec.runPolicy.suspend` field on CRD.

Try to reinstall it using this:
kubectl apply --server-side -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=release-1.9"

### Comment by [@izturn](https://github.com/izturn) — 2025-12-25T08:26:09Z

@mbobrovskyi thx

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-25T10:09:42Z

/remove-kind bug

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-25T10:09:45Z

/kind support
