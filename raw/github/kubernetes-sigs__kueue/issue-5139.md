# Issue #5139: [Dashboard] Kueue-Viz showing Unknown Status for Workloads

**Summary**: [Dashboard] Kueue-Viz showing Unknown Status for Workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5139

**Last updated**: 2025-05-23T16:52:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-04-28T20:03:09Z
- **Updated**: 2025-05-23T16:52:37Z
- **Closed**: 2025-05-23T16:52:37Z
- **Labels**: `kind/bug`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I ran the default examples with KueueViz and the panel for workloads display status unknown for the workloads.

![Image](https://github.com/user-attachments/assets/38de9400-45b0-4b51-a327-3888ed5db780)


**What you expected to happen**:
Workloads should say their status (admitted)
**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:
I used the modified default values
```yaml
# Default values for kueue.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.
nameOverride: ""
fullnameOverride: ""
# Enable each function, like kustomize https://github.com/kubernetes-sigs/kueue/blob/main/config/default/kustomization.yaml
enablePrometheus: false
# Enable x509 automated certificate management using cert-manager (cert-manager.io)
enableCertManager: false
# Customize controllerManager
controllerManager:
  #featureGates:
  #  - name: PartialAdmission
  #    enabled: true
  manager:
    image:
      repository: registry.k8s.io/kueue/kueue
      # This should be set to 'IfNotPresent' for released version      
      pullPolicy: Always
      tag: v0.11.4
    podAnnotations: {}
    resources:
      limits:
        cpu: "2"
        memory: 512Mi
      requests:
        cpu: 500m
        memory: 512Mi
    podSecurityContext:
      runAsNonRoot: true
      seccompProfile:
        type: RuntimeDefault
    containerSecurityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
          - ALL
  replicas: 1
  imagePullSecrets: []
  readinessProbe:
    initialDelaySeconds: 5
    periodSeconds: 10
    timeoutSeconds: 1
    failureThreshold: 3
    successThreshold: 1
  livenessProbe:
    initialDelaySeconds: 15
    periodSeconds: 20
    timeoutSeconds: 1
    failureThreshold: 3
    successThreshold: 1
  topologySpreadConstraints: []
  podDisruptionBudget:
    enabled: false
    minAvailable: 1
kubernetesClusterDomain: cluster.local
# controller_manager_config.yaml. controllerManager utilizes this yaml via manager-config Configmap.
managerConfig:
  controllerManagerConfigYaml: |-
    apiVersion: config.kueue.x-k8s.io/v1beta1
    kind: Configuration
    health:
      healthProbeBindAddress: :8081
    metrics:
      bindAddress: :8443
    # enableClusterQueueResources: true
    webhook:
      port: 9443
    leaderElection:
      leaderElect: true
      resourceName: c1f6bfd2.kueue.x-k8s.io
    controller:
      groupKindConcurrency:
        Job.batch: 5
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    clientConnection:
      qps: 50
      burst: 100
    #pprofBindAddress: :8083
    #waitForPodsReady:
    #  enable: false
    #  timeout: 5m
    #  recoveryTimeout: 3m
    #  blockAdmission: false
    #  requeuingStrategy:
    #    timestamp: Eviction
    #    backoffLimitCount: null # null indicates infinite requeuing
    #    backoffBaseSeconds: 60
    #    backoffMaxSeconds: 3600
    #manageJobsWithoutQueueName: true
    #managedJobsNamespaceSelector:
    #  matchExpressions:
    #    - key: kubernetes.io/metadata.name
    #      operator: NotIn
    #      values: [ kube-system, kueue-system ]
    #internalCertManagement:
    #  enable: false
    #  webhookServiceName: ""
    #  webhookSecretName: ""
    integrations:
      frameworks:
      - "batch/job"
      - "kubeflow.org/mpijob"
      - "ray.io/rayjob"
      - "ray.io/raycluster"
      - "jobset.x-k8s.io/jobset"
      - "kubeflow.org/paddlejob"
      - "kubeflow.org/pytorchjob"
      - "kubeflow.org/tfjob"
      - "kubeflow.org/xgboostjob"
      - "workload.codeflare.dev/appwrapper"
      - "pod"
      - "deployment"
      - "statefulset"
      - "leaderworkerset.x-k8s.io/leaderworkerset"
    #  externalFrameworks:
    #  - "Foo.v1.example.com"
    #fairSharing:
    #  enable: true
    #  preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
    #resources:
    #  excludeResourcePrefixes: []
    # transformations:
    # - input: nvidia.com/mig-4g.5gb
    #   strategy: Replace | Retain
    #   outputs:
    #     example.com/accelerator-memory: 5Gi
    #     example.com/accelerator-gpc: 4
# ports definition for metricsService and webhookService.
metricsService:
  ports:
    - name: https
      port: 8443
      protocol: TCP
      targetPort: 8443
  type: ClusterIP
  annotations: {}
webhookService:
  ipDualStack:
    enabled: false
    ipFamilies: ["IPv6", "IPv4"]
    ipFamilyPolicy: "PreferDualStack"
  ports:
    - port: 443
      protocol: TCP
      targetPort: 9443
  type: ClusterIP
# kueueviz dashboard
enableKueueViz: true
kueueViz:
  backend:
    image: "us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueueviz-backend:main"
  frontend:
    image: "us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueueviz-frontend:main"
metrics:
  prometheusNamespace: monitoring
  serviceMonitor:
    tlsConfig:
      insecureSkipVerify: true
```

I am seeing the following errors in the backend deployment:

```
2025/04/28 19:51:33 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:34276: writev: broken pipe"
2025/04/28 19:54:34 ERROR Error writing message:  error="write tcp 127.0.0.1:8080->127.0.0.1:34304: write: broken pipe"
[GIN] 2025/04/28 - 19:54:34 | 200 |         4m10s |       127.0.0.1 | GET      "/ws/local-queues"
[GIN] 2025/04/28 - 19:56:10 | 200 | 35.005333329s |       127.0.0.1 | GET      "/ws/local-queues"
2025/04/28 19:56:10 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:36880: writev: broken pipe"
2025/04/28 19:56:10 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:52574: writev: broken pipe"
[GIN] 2025/04/28 - 19:56:10 | 200 | 55.006875094s |       127.0.0.1 | GET      "/ws/workloads"
[GIN] 2025/04/28 - 19:56:11 | 200 | 30.022514012s |       127.0.0.1 | GET      "/ws/workloads"
2025/04/28 19:56:11 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:52642: writev: broken pipe"
2025/04/28 19:56:11 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:37232: writev: broken pipe"
[GIN] 2025/04/28 - 19:56:11 | 200 |         2m45s |       127.0.0.1 | GET      "/ws/workloads/dashboard"
2025/04/28 19:56:12 ERROR Error writing message:  error="write tcp 127.0.0.1:8080->127.0.0.1:52560: write: broken pipe"
[GIN] 2025/04/28 - 19:56:12 | 200 | 35.005865591s |       127.0.0.1 | GET      "/ws/cluster-queues"
[GIN] 2025/04/28 - 19:56:13 | 200 | 10.014959205s |       127.0.0.1 | GET      "/ws/workloads"
2025/04/28 19:56:13 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:48794: writev: broken pipe"
2025/04/28 19:56:13 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:36694: writev: broken pipe"
[GIN] 2025/04/28 - 19:56:13 | 200 | 45.561918762s |       127.0.0.1 | GET      "/ws/workloads/dashboard"
2025/04/28 19:56:14 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:36830: writev: broken pipe"
[GIN] 2025/04/28 - 19:56:14 | 200 | 40.227859772s |       127.0.0.1 | GET      "/ws/workloads"
[GIN] 2025/04/28 - 19:58:30 | 200 |         1m10s |       127.0.0.1 | GET      "/ws/workloads/dashboard"
2025/04/28 19:58:30 ERROR Error writing message:  error="writev tcp 127.0.0.1:8080->127.0.0.1:59646: writev: broken pipe"
```

**Environment**:
- Kubernetes version (use `kubectl version`): kind (1.32)
- Kueue version (use `git describe --tags --dirty --always`):kehannon@kehannon-thinkpadp1gen4i:~/Work/kueue$ git describe --tags --dirty --always
v0.12.0-devel-170-ge3ba696fa-dirty

- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-29T03:01:11Z

/kind dashboard

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-09T15:54:22Z

cc @akram @mimowo

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-20T18:41:13Z

I did a test and I still see this problem for 0.12 rc.

@akram any ideas on cause?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-23T16:15:19Z

I think I figured out the issue.

```
                    <TableCell>{workload.status?.state || "Unknown"}</TableCell>
```
I don't see anything around state in the workload API so I think this column could just be dropped from the front end.
