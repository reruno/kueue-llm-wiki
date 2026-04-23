# Issue #2213: Plain Pod gets deleted once admitted via ProvisioningRequest (DWS)

**Summary**: Plain Pod gets deleted once admitted via ProvisioningRequest (DWS)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2213

**Last updated**: 2024-05-22T18:23:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-16T18:12:06Z
- **Updated**: 2024-05-22T18:23:00Z
- **Closed**: 2024-05-22T18:23:00Z
- **Labels**: `kind/bug`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 7

## Description

**What happened**:

After a ProvisioningRequest using `provisioningClassName: queued-provisioning.gke.io` was provisioned, Kueue ungated the Pod and added the node selectors and annotations.

Then, it assumed that the Workload no longer matched the Pod, thus triggering the eviction process:

```
2024-05-16T17:46:26.776057524Z {"caller":"jobframework/reconciler.go:385", "controller":"v1_pod", "gvk":"/v1, Kind=Pod", "job":"kueue-dws/dws-pod", "level":"Level(-2)", "msg":"Job admitted, unsuspending", "name":"dws-pod", "namespace":"kueue-dws", "reconcileID":"b519d6ea-8dd9-4340-8990-c4da4a67ecd5", "ts":"2024-05-16T17:46:26.775893243Z"}
2024-05-16T17:46:26.777898261Z {"Workload":{…}, "caller":"core/workload_controller.go:150", "controller":"workload", "controllerGroup":"kueue.x-k8s.io", "controllerKind":"Workload", "level":"Level(-2)", "msg":"Reconciling Workload", "name":"pod-dws-pod-4e884", "namespace":"kueue-dws", "reconcileID":"b010ca53-2b15-4d19-87c7-51a044425dfe", "ts":"2024-05-16T17:46:26.777789892Z", "workload":{…}}
2024-05-16T17:46:27.056640239Z {"caller":"jobframework/reconciler.go:263", "controller":"v1_pod", "gvk":"/v1, Kind=Pod", "job":"kueue-dws/dws-pod", "level":"Level(-2)", "msg":"Reconciling Job", "name":"dws-pod", "namespace":"kueue-dws", "reconcileID":"c355b605-29b7-42f2-95bb-6ef81876ec1a", "ts":"2024-05-16T17:46:27.056497343Z"}
2024-05-16T17:46:27.056962616Z {"caller":"jobframework/reconciler.go:521", "controller":"v1_pod", "gvk":"/v1, Kind=Pod", "job":"kueue-dws/dws-pod", "level":"Level(-2)", "msg":"job with no matching workload, suspending", "name":"dws-pod", "namespace":"kueue-dws", "reconcileID":"c355b605-29b7-42f2-95bb-6ef81876ec1a", "ts":"2024-05-16T17:46:27.056832747Z"}
```

**What you expected to happen**:

The pod to run.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a cluster and configure DWS using https://cloud.google.com/kubernetes-engine/docs/how-to/provisioningrequest
2. Create a plain Pod, for example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dws-pod
  labels:
    kueue.x-k8s.io/queue-name: dws-local-queue
spec:
      nodeSelector:
        cloud.google.com/gke-accelerator: "nvidia-l4"
      tolerations:
      - key: "nvidia.com/gpu"
        operator: "Exists"
        effect: "NoSchedule"
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["120s"]
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
            nvidia.com/gpu: "1"
          limits:
            cpu: "500m"
            memory: "512Mi"
            nvidia.com/gpu: "1"
      restartPolicy: Never
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): `v1.29.4-gke.1447000`
- Kueue version (use `git describe --tags --dirty --always`): `v0.6.2`
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-16T18:12:16Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-16T19:35:20Z

cc @mimowo

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T14:10:10Z

This seems to be specific to `queued-provisioning.gke.io`.

This is the final form of the Pod when it's deleted:

```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    cluster-autoscaler.kubernetes.io/consume-provisioning-request: pod-dws-pod-4e884-dws-prov-1
    cluster-autoscaler.kubernetes.io/safe-to-evict: "false"
  creationTimestamp: "2024-05-17T14:02:54Z"
  deletionGracePeriodSeconds: 0
  deletionTimestamp: "2024-05-17T14:06:40Z"
  finalizers:
  - acondor.dev/hold
  labels:
    kueue.x-k8s.io/managed: "true"
    kueue.x-k8s.io/queue-name: dws-jobs
  name: dws-pod
  namespace: kueue-dws
  resourceVersion: "1713714"
  uid: 8f1ec3b1-1865-4bee-b9c6-db8cde6b22bf
spec:
  containers:
  - args:
    - 120s
    image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
    imagePullPolicy: IfNotPresent
    name: dummy-job
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
        nvidia.com/gpu: "1"
      requests:
        cpu: 500m
        memory: 512Mi
        nvidia.com/gpu: "1"
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-trz5v
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeSelector:
    autoscaling.gke.io/provisioning-request: gke-kueue-dws-pod-dws-pod-4e884-dw-e6800c22a9239747
    cloud.google.com/gke-accelerator: nvidia-l4
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Never
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoSchedule
    key: nvidia.com/gpu
    operator: Exists
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  - effect: NoSchedule
    key: cloud.google.com/gke-queued
    operator: Equal
    value: "true"
  volumes:
  - name: kube-api-access-trz5v
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          expirationSeconds: 3607
          path: token
      - configMap:
          items:
          - key: ca.crt
            path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
          - fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
            path: namespace
status:
  conditions:
  - lastProbeTime: null
    lastTransitionTime: null
    message: '0/9 nodes are available: 9 node(s) didn''t match Pod''s node affinity/selector.
      preemption: 0/9 nodes are available: 9 Preemption is not helpful for scheduling.'
    reason: Unschedulable
    status: "False"
    type: PodScheduled
  - lastProbeTime: null
    lastTransitionTime: "2024-05-17T14:06:40Z"
    message: No matching Workload; restoring pod templates according to existent Workload
    reason: StoppedByKueue
    status: "True"
    type: TerminationTarget
  phase: Failed
  qosClass: Guaranteed
```

And this is the Workload:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  creationTimestamp: "2024-05-17T14:02:54Z"
  deletionGracePeriodSeconds: 0
  deletionTimestamp: "2024-05-17T14:06:40Z"
  finalizers:
  - acondor.dev/hold
  generation: 2
  labels:
    kueue.x-k8s.io/job-uid: 8f1ec3b1-1865-4bee-b9c6-db8cde6b22bf
  name: pod-dws-pod-4e884
  namespace: kueue-dws
  ownerReferences:
  - apiVersion: v1
    blockOwnerDeletion: true
    controller: true
    kind: Pod
    name: dws-pod
    uid: 8f1ec3b1-1865-4bee-b9c6-db8cde6b22bf
  resourceVersion: "1713462"
  uid: bd0f33c2-9630-492e-a517-a7dbdf77c943
spec:
  active: true
  podSets:
  - count: 1
    name: main
    template:
      metadata: {}
      spec:
        containers:
        - args:
          - 120s
          image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
          imagePullPolicy: IfNotPresent
          name: dummy-job
          resources:
            limits:
              cpu: 500m
              memory: 512Mi
              nvidia.com/gpu: "1"
            requests:
              cpu: 500m
              memory: 512Mi
              nvidia.com/gpu: "1"
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
          volumeMounts:
          - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
            name: kube-api-access-trz5v
            readOnly: true
        dnsPolicy: ClusterFirst
        enableServiceLinks: true
        nodeSelector:
          cloud.google.com/gke-accelerator: nvidia-l4
        preemptionPolicy: PreemptLowerPriority
        priority: 0
        restartPolicy: Never
        schedulerName: default-scheduler
        schedulingGates:
        - name: kueue.x-k8s.io/admission
        securityContext: {}
        serviceAccount: default
        serviceAccountName: default
        terminationGracePeriodSeconds: 30
        tolerations:
        - effect: NoSchedule
          key: nvidia.com/gpu
          operator: Exists
        - effect: NoExecute
          key: node.kubernetes.io/not-ready
          operator: Exists
          tolerationSeconds: 300
        - effect: NoExecute
          key: node.kubernetes.io/unreachable
          operator: Exists
          tolerationSeconds: 300
        volumes:
        - name: kube-api-access-trz5v
          projected:
            defaultMode: 420
            sources:
            - serviceAccountToken:
                expirationSeconds: 3607
                path: token
            - configMap:
                items:
                - key: ca.crt
                  path: ca.crt
                name: kube-root-ca.crt
            - downwardAPI:
                items:
                - fieldRef:
                    apiVersion: v1
                    fieldPath: metadata.namespace
                  path: namespace
  priority: 0
  priorityClassSource: ""
  queueName: dws-jobs
status:
  admission:
    clusterQueue: dws-cluster-queue
    podSetAssignments:
    - count: 1
      flavors:
        cpu: default-flavor
        memory: default-flavor
        nvidia.com/gpu: default-flavor
      name: main
      resourceUsage:
        cpu: 500m
        memory: 512Mi
        nvidia.com/gpu: "1"
  admissionChecks:
  - lastTransitionTime: "2024-05-17T14:02:55Z"
    message: ""
    name: dws-prov
    podSetUpdates:
    - annotations:
        cluster-autoscaler.kubernetes.io/consume-provisioning-request: pod-dws-pod-4e884-dws-prov-1
      name: main
    state: Ready
  conditions:
  - lastTransitionTime: "2024-05-17T14:02:55Z"
    message: Quota reserved in ClusterQueue dws-cluster-queue
    reason: QuotaReserved
    status: "True"
    type: QuotaReserved
  - lastTransitionTime: "2024-05-17T14:06:40Z"
    message: The workload is admitted
    reason: Admitted
    status: "True"
    type: Admitted
```

And ProvisioningRequest:

```yaml
apiVersion: autoscaling.x-k8s.io/v1beta1
kind: ProvisioningRequest
metadata:
  creationTimestamp: "2024-05-17T14:02:55Z"
  finalizers:
  - acondor.dev/hold
  generation: 1
  name: pod-dws-pod-4e884-dws-prov-1
  namespace: kueue-dws
  ownerReferences:
  - apiVersion: kueue.x-k8s.io/v1beta1
    blockOwnerDeletion: true
    controller: true
    kind: Workload
    name: pod-dws-pod-4e884
    uid: bd0f33c2-9630-492e-a517-a7dbdf77c943
  resourceVersion: "1713452"
  uid: db6b3133-1680-4956-8a2a-84e3c1084c93
spec:
  podSets:
  - count: 1
    podTemplateRef:
      name: ppt-pod-dws-pod-4e884-dws-prov-1-main
  provisioningClassName: queued-provisioning.gke.io
status:
  conditions:
  - lastTransitionTime: "2024-05-17T14:03:18Z"
    message: Provisioning Request was successfully queued.
    observedGeneration: 1
    reason: SuccessfullyQueued
    status: "True"
    type: Accepted
  - lastTransitionTime: "2024-05-17T14:06:40Z"
    message: Provisioning Request was successfully provisioned.
    observedGeneration: 1
    reason: Provisioned
    status: "True"
    type: Provisioned
  - lastTransitionTime: "2024-05-17T14:03:01Z"
    message: Provisioning Request hasn't failed.
    observedGeneration: 1
    reason: NotFailed
    status: "False"
    type: Failed
  provisioningClassDetails:
    AcceleratorType: nvidia-l4
    NodeGroupName: gke-dev-g2-standard-8-1-c78cf7da-grp
    NodePoolName: g2-standard-8-1
    ResizeRequestName: gke-kueue-dws-pod-dws-pod-4e884-dw-e6800c22a9239747
    SelectedZone: us-central1-a
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T15:14:42Z

I confirmed with a customer that `v0.5.x` is unaffected.

### Comment by [@trasc](https://github.com/trasc) — 2024-05-17T16:35:26Z

> I confirmed with a customer that `v0.5.x` is unaffected. 

The tolerations are not part of the equivalency check in v0.5.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T19:50:57Z

IIRC, this changed with a combination of #1223 and https://github.com/kubernetes-sigs/kueue/pull/1304

Because this is a regression, let's do a hotfix by ignoring changes to tolerations and nodeSelectors when the workload is admitted.

For a long term solution, I would like the ProvisioningRequest status to tell us what is going to change.

Another alternative that @trasc proposed offline was to add some configuration to the pod integration to ignore certain tolerations and nodeSelectors. But this adds configuration overhead to users, for something that the system should figure out.

### Comment by [@trasc](https://github.com/trasc) — 2024-05-20T07:52:18Z

/assign @vladikkuzn
