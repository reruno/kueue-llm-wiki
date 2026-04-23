# Issue #2205: APIService https issue for v0.6.2 visibility api

**Summary**: APIService https issue for v0.6.2 visibility api

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2205

**Last updated**: 2024-05-17T21:09:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2024-05-15T17:25:41Z
- **Updated**: 2024-05-17T21:09:43Z
- **Closed**: 2024-05-17T20:53:22Z
- **Labels**: `kind/bug`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 21

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
TLDR; looks like APIService is possibly ignoring `insecureSkipTLSVerify: true` field on APIService when enabling visibility api? 
Running Kueue on KIND (docker-upstream.apple.com/kindest/node:v1.25.16). 

`kubectl edit deployment -n kueue-system kueue-controller-manager`
I add:
```
- name: manager
   args: 
     - --feature-gates=MultiKueue=true
     - --feature-gates=LendingLimit=true
     - --feature-gates=VisibilityOnDemand=true
     - --feature-gates=QueueVisibility=true
     - --feature-gates=PartialAdmission=true
```

`kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.2/visibility-api.yaml`

```
kubectl get --raw "/apis/visibility.kueue.x-k8s.io/v1alpha1/clusterqueues/team-a/pendingworkloads?limit=1&offset=1"
Error from server (ServiceUnavailable): the server is currently unable to handle the request
```
⭐️**Note: server error ServiceUnavailable only appears after I apply the visibility api yaml serverside.**

```
kubectl get apiservice v1alpha1.visibility.kueue.x-k8s.io -o yaml
...
...
...
status:
  conditions:
  - lastTransitionTime: "2024-05-14T20:31:25Z"
    message: 'failing or missing response from https://10.96.172.213:443/apis/visibility.kueue.x-k8s.io/v1alpha1:
      Get "https://10.96.172.213:443/apis/visibility.kueue.x-k8s.io/v1alpha1": http:
      server gave HTTP response to HTTPS client'
    reason: FailedDiscoveryCheck
    status: "False"
    type: Available
```

**What you expected to happen**:
I expected to be able to look at workload position via the kubectl api visibility call

**Environment**:
- Kubernetes version (use `kubectl version`):
```Client Version: version.Info{Major:"1", Minor:"26", GitVersion:"v1.26.1", GitCommit:"8f94681cd294aa8cfd3407b8191f6c70214973a4", GitTreeState:"clean", BuildDate:"2023-01-18T15:51:24Z", GoVersion:"go1.19.5", Compiler:"gc", Platform:"darwin/amd64"}
Kustomize Version: v4.5.7
Server Version: version.Info{Major:"1", Minor:"25", GitVersion:"v1.25.16", GitCommit:"c5f43560a4f98f2af3743a59299fb79f07924373", GitTreeState:"clean", BuildDate:"2024-02-14T00:40:21Z", GoVersion:"go1.20.10", Compiler:"gc", Platform:"linux/amd64"}
```
- Kueue version (use `git describe --tags --dirty --always`):
v0.6.2

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-16T18:00:22Z

/assign @PBundyra

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-05-17T10:13:11Z

Could you please share output of `kubectl describe pod -n kueue-system` on `kueue-controller-manager`?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T15:08:06Z

Also, can you try changing the arguments to:

```
     - --feature-gates=MultiKueue=true,LendingLimit=true,VisibilityOnDemand=true,QueueVisibility=true,PartialAdmission=true
```

### Comment by [@amy](https://github.com/amy) — 2024-05-17T17:10:08Z

- Deleted old KIND cluster, created fresh KIND Kueue cluster
- Updated arguments to: https://github.com/kubernetes-sigs/kueue/issues/2205#issuecomment-2117810447
- Bounced  kueue controller manager pods
- serverside applied visibility api
- bounced kueue controller manager pods again
```
Amys-MacBook-Pro-2:kueue-experiments amychen$ kubectl describe apiservice v1alpha1.visibility.kueue.x-k8s.io
Name:         v1alpha1.visibility.kueue.x-k8s.io
Namespace:    
Labels:       <none>
Annotations:  <none>
API Version:  apiregistration.k8s.io/v1
Kind:         APIService
Metadata:
  Creation Timestamp:  2024-05-17T17:07:12Z
  Managed Fields:
    API Version:  apiregistration.k8s.io/v1
    Fields Type:  FieldsV1
    fieldsV1:
      f:spec:
        f:group:
        f:groupPriorityMinimum:
        f:insecureSkipTLSVerify:
        f:service:
          f:name:
          f:namespace:
        f:version:
        f:versionPriority:
    Manager:      kubectl
    Operation:    Apply
    Time:         2024-05-17T17:07:12Z
    API Version:  apiregistration.k8s.io/v1
    Fields Type:  FieldsV1
    fieldsV1:
      f:status:
        f:conditions:
          .:
          k:{"type":"Available"}:
            .:
            f:lastTransitionTime:
            f:message:
            f:reason:
            f:status:
            f:type:
    Manager:         kube-apiserver
    Operation:       Update
    Subresource:     status
    Time:            2024-05-17T17:07:13Z
  Resource Version:  1067
  UID:               171d577b-7c1d-47c9-b45a-aa52e89f5377
Spec:
  Group:                     visibility.kueue.x-k8s.io
  Group Priority Minimum:    100
  Insecure Skip TLS Verify:  true
  Service:
    Name:            kueue-visibility-server
    Namespace:       kueue-system
    Port:            443
  Version:           v1alpha1
  Version Priority:  100
Status:
  Conditions:
    Last Transition Time:  2024-05-17T17:07:13Z
    Message:               failing or missing response from https://10.96.111.146:443/apis/visibility.kueue.x-k8s.io/v1alpha1: Get "https://10.96.111.146:443/apis/visibility.kueue.x-k8s.io/v1alpha1": http: server gave HTTP response to HTTPS client
    Reason:                FailedDiscoveryCheck
    Status:                False
    Type:                  Available
Events:                    <none>
Amys-MacBook-Pro-2:kueue-experiments amychen$ kubectl describe pod -n kueue-system
Name:                 kueue-controller-manager-5b6f4b4c97-5ngkg
Namespace:            kueue-system
Priority:             500000
Priority Class Name:  p1
Service Account:      kueue-controller-manager
Node:                 test-kueue-worker/192.168.64.2
Start Time:           Fri, 17 May 2024 10:06:36 -0700
Labels:               control-plane=controller-manager
                      pod-template-hash=5b6f4b4c97
Annotations:          kubectl.kubernetes.io/default-container: manager
                      kubernetes.io/limit-ranger:
                        LimitRanger plugin set: cpu, memory request for container kube-rbac-proxy; cpu, memory limit for container kube-rbac-proxy
Status:               Running
IP:                   10.244.1.3
IPs:
  IP:           10.244.1.3
Controlled By:  ReplicaSet/kueue-controller-manager-5b6f4b4c97
Containers:
  manager:
    Container ID:  containerd://ee6437d6134ddec3b423e52af94e359cb96086aff0ad3a214255ca82ed0b173a
    Image:         registry.k8s.io/kueue/kueue:v0.6.2
    Image ID:      registry.k8s.io/kueue/kueue@sha256:ef1f07fa559eb396a93e67d682743bac602b512cf11d203e14b10bcfa2e89112
    Ports:         8082/TCP, 9443/TCP
    Host Ports:    0/TCP, 0/TCP
    Command:
      /manager
    Args:
      --config=/controller_manager_config.yaml
      --zap-log-level=2
    State:          Running
      Started:      Fri, 17 May 2024 10:06:39 -0700
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:        500m
      memory:     512Mi
    Liveness:     http-get http://:8081/healthz delay=15s timeout=1s period=20s #success=1 #failure=3
    Readiness:    http-get http://:8081/readyz delay=5s timeout=1s period=10s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /controller_manager_config.yaml from manager-config (rw,path="controller_manager_config.yaml")
      /tmp/k8s-webhook-server/serving-certs from cert (ro)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-dfhxh (ro)
  kube-rbac-proxy:
    Container ID:  containerd://a63c330b11eddcd163a5d50a56d273ec82f549c9074b6e31ab8e0ac996ac8bd9
    Image:         gcr.io/kubebuilder/kube-rbac-proxy:v0.8.0
    Image ID:      gcr.io/kubebuilder/kube-rbac-proxy@sha256:db06cc4c084dd0253134f156dddaaf53ef1c3fb3cc809e5d81711baa4029ea4c
    Port:          8443/TCP
    Host Port:     0/TCP
    Args:
      --secure-listen-address=0.0.0.0:8443
      --upstream=http://127.0.0.1:8080/
      --logtostderr=true
      --v=10
    State:          Running
      Started:      Fri, 17 May 2024 10:06:40 -0700
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     100m
      memory:  128Mi
    Requests:
      cpu:        100m
      memory:     128Mi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-dfhxh (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  cert:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kueue-webhook-server-cert
    Optional:    false
  manager-config:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      kueue-manager-config
    Optional:  false
  kube-api-access-dfhxh:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Guaranteed
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  95s   default-scheduler  Successfully assigned kueue-system/kueue-controller-manager-5b6f4b4c97-5ngkg to test-kueue-worker
  Normal  Pulling    94s   kubelet            Pulling image "registry.k8s.io/kueue/kueue:v0.6.2"
  Normal  Pulled     93s   kubelet            Successfully pulled image "registry.k8s.io/kueue/kueue:v0.6.2" in 1.336599868s (1.336603463s including waiting)
  Normal  Created    92s   kubelet            Created container manager
  Normal  Started    92s   kubelet            Started container manager
  Normal  Pulled     92s   kubelet            Container image "gcr.io/kubebuilder/kube-rbac-proxy:v0.8.0" already present on machine
  Normal  Created    91s   kubelet            Created container kube-rbac-proxy
  Normal  Started    91s   kubelet            Started container kube-rbac-proxy
```

```
Amys-MacBook-Pro-2:kueue-experiments amychen$ kubectl describe apiservice v1alpha1.visibility.kueue.x-k8s.io
Name:         v1alpha1.visibility.kueue.x-k8s.io
Namespace:    
Labels:       <none>
Annotations:  <none>
API Version:  apiregistration.k8s.io/v1
Kind:         APIService
Metadata:
  Creation Timestamp:  2024-05-17T17:07:12Z
  Managed Fields:
    API Version:  apiregistration.k8s.io/v1
    Fields Type:  FieldsV1
    fieldsV1:
      f:spec:
        f:group:
        f:groupPriorityMinimum:
        f:insecureSkipTLSVerify:
        f:service:
          f:name:
          f:namespace:
        f:version:
        f:versionPriority:
    Manager:      kubectl
    Operation:    Apply
    Time:         2024-05-17T17:07:12Z
    API Version:  apiregistration.k8s.io/v1
    Fields Type:  FieldsV1
    fieldsV1:
      f:status:
        f:conditions:
          .:
          k:{"type":"Available"}:
            .:
            f:lastTransitionTime:
            f:message:
            f:reason:
            f:status:
            f:type:
    Manager:         kube-apiserver
    Operation:       Update
    Subresource:     status
    Time:            2024-05-17T17:07:13Z
  Resource Version:  1067
  UID:               171d577b-7c1d-47c9-b45a-aa52e89f5377
Spec:
  Group:                     visibility.kueue.x-k8s.io
  Group Priority Minimum:    100
  Insecure Skip TLS Verify:  true
  Service:
    Name:            kueue-visibility-server
    Namespace:       kueue-system
    Port:            443
  Version:           v1alpha1
  Version Priority:  100
Status:
  Conditions:
    Last Transition Time:  2024-05-17T17:07:13Z
    Message:               failing or missing response from https://10.96.111.146:443/apis/visibility.kueue.x-k8s.io/v1alpha1: Get "https://10.96.111.146:443/apis/visibility.kueue.x-k8s.io/v1alpha1": http: server gave HTTP response to HTTPS client
    Reason:                FailedDiscoveryCheck
    Status:                False
    Type:                  Available
Events:                    <none>
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T18:31:30Z

@PBundyra this message is interesting `http:  server gave HTTP response to HTTPS client`

Shouldn't that be handled by the `kube-rbac-proxy` container?

@amy any Service configuration that differs from the manifests including in the release?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T18:41:20Z

Actually, can you share your KueueConfiguration? In particular, the `internalCertManagement`.
Or do you see any log lines from this file? https://github.com/kubernetes-sigs/kueue/blob/main/pkg/visibility/server.go#L49

### Comment by [@amy](https://github.com/amy) — 2024-05-17T18:59:20Z

```
kubectl get configmap -n kueue-system kueue-manager-config -o yaml
E0517 11:58:37.520554   99641 memcache.go:255] couldn't get resource list for visibility.kueue.x-k8s.io/v1alpha1: the server is currently unable to handle the request
E0517 11:58:37.544339   99641 memcache.go:106] couldn't get resource list for visibility.kueue.x-k8s.io/v1alpha1: the server is currently unable to handle the request
E0517 11:58:37.546758   99641 memcache.go:106] couldn't get resource list for visibility.kueue.x-k8s.io/v1alpha1: the server is currently unable to handle the request
E0517 11:58:37.549032   99641 memcache.go:106] couldn't get resource list for visibility.kueue.x-k8s.io/v1alpha1: the server is currently unable to handle the request
apiVersion: v1
data:
  controller_manager_config.yaml: |
    apiVersion: config.kueue.x-k8s.io/v1beta1
    kind: Configuration
    health:
      healthProbeBindAddress: :8081
    metrics:
      bindAddress: :8080
      ## Enable resource utilisation metrics for the ClusterQueue
      enableClusterQueueResources: true
    ## Enable pprof endpoints
    pprofBindAddress: :8082
    webhook:
      port: 9443
    leaderElection:
      leaderElect: true
      resourceName: kueue-manager.kueue.x-k8s.io
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
    ## This is required to optionally turn on "all or nothing" scheduling
    ## https://kueue.sigs.k8s.io/docs/tasks/manage/setup_sequential_admission/
    #waitForPodsReady:
    #  enable: true
    manageJobsWithoutQueueName: true
    internalCertManagement:
      enable: true
      webhookServiceName: kueue-webhook-service
      webhookSecretName: kueue-webhook-server-cert
    integrations:
      frameworks:
      ## Enable Job integration: https://kueue.sigs.k8s.io/docs/tasks/run/jobs/
      - "batch/job"
      ## Enable Pod integration (requires k8s 1.27): https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/
      #- "pod"
      #- "kubeflow.org/mpijob"
      #- "ray.io/rayjob"
      #- "ray.io/raycluster"
      #- "jobset.x-k8s.io/jobset"
      #- "kubeflow.org/mxjob"
      #- "kubeflow.org/paddlejob"
      #- "kubeflow.org/pytorchjob"
      #- "kubeflow.org/tfjob"
      #- "kubeflow.org/xgboostjob"
kind: ConfigMap
metadata:
  creationTimestamp: "2024-05-17T17:05:46Z"
  name: kueue-manager-config
  namespace: kueue-system
  resourceVersion: "12952"
  uid: 34e3aab5-8480-4e17-b45b-3b5a72addb68
```

### Comment by [@amy](https://github.com/amy) — 2024-05-17T19:05:53Z

I don't see logs within the kueue-controller related to the visibility api. Checking the kube api server I see this:
```
 response to HTTPS client
E0517 19:03:50.702309       1 available_controller.go:524] v1alpha1.visibility.kueue.x-k8s.io failed with: failing or missing response from https://10.96.111.146:443/apis/visibility.kueue.x-k8s.io/v1alpha1: Get "https://10.96.111.146:443/apis/visibility.kueue.x-k8s.io/v1alpha1": http: server gave HTTP response to HTTPS client
W0517 19:03:51.700060       1 handler_proxy.go:105] no RequestInfo found in the context
E0517 19:03:51.700296       1 controller.go:116] loading OpenAPI spec for "v1alpha1.visibility.kueue.x-k8s.io" failed with: failed to retrieve openAPI spec, http error: ResponseCode: 503, Body: service unavailable
, Header: map[Content-Type:[text/plain; charset=utf-8] X-Content-Type-Options:[nosniff]]
I0517 19:03:51.700336       1 controller.go:129] OpenAPI AggregationController: action for item v1alpha1.visibility.kueue.x-k8s.io: Rate Limited Requeue.
E0517 19:04:01.762297       1 available_controller.go:524] v1alpha1.visibility.kueue.x-k8s.io failed with: failing or missing response from https://10.96.111.146:443/apis/visibility.kueue.x-k8s.io/v1alpha1: Get "https://10.96.111.146:443/apis/visibility.kueue.x-k8s.io/v1alpha1": http: server gave HTTP response to HTTPS client
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T19:11:49Z

Uhm, looks like the similar situation as https://github.com/kubernetes-sigs/kueue/issues/1519

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T19:24:51Z

It looks like you didn't add back the feature-gates?

From https://github.com/kubernetes-sigs/kueue/issues/2205#issuecomment-2118032745

```
  manager:
    Container ID:  containerd://ee6437d6134ddec3b423e52af94e359cb96086aff0ad3a214255ca82ed0b173a
    Image:         registry.k8s.io/kueue/kueue:v0.6.2
    Image ID:      registry.k8s.io/kueue/kueue@sha256:ef1f07fa559eb396a93e67d682743bac602b512cf11d203e14b10bcfa2e89112
    Ports:         8082/TCP, 9443/TCP
    Host Ports:    0/TCP, 0/TCP
    Command:
      /manager
    Args:
      --config=/controller_manager_config.yaml
      --zap-log-level=2
    State:          Running
```

### Comment by [@amy](https://github.com/amy) — 2024-05-17T19:25:08Z

Weird, so it shows up in my deployment spec, but not the pod spec...

### Comment by [@amy](https://github.com/amy) — 2024-05-17T19:27:26Z

```
Amys-MacBook-Pro-2:kueue-experiments amychen$ kubectl describe deployment -n kueue-system
Name:                   kueue-controller-manager
Namespace:              kueue-system
CreationTimestamp:      Fri, 17 May 2024 10:05:47 -0700
Labels:                 control-plane=controller-manager
Annotations:            deployment.kubernetes.io/revision: 2
Selector:               control-plane=controller-manager
Replicas:               1 desired | 0 updated | 1 total | 1 available | 1 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:           control-plane=controller-manager
  Annotations:      kubectl.kubernetes.io/default-container: manager
  Service Account:  kueue-controller-manager
  Containers:
   manager:
    Image:       registry.k8s.io/kueue/kueue:v0.6.2
    Ports:       8082/TCP, 9443/TCP
    Host Ports:  0/TCP, 0/TCP
    Command:
      /manager
    Args:
      --feature-gates=MultiKueue=true,LendingLimit=true,VisibilityOnDemand=true,QueueVisibility=true,PartialAdmission=true
      --config=/controller_manager_config.yaml
      --zap-log-level=2
```

```
kubectl describe pod -n kueue-system
Name:                 kueue-controller-manager-5b6f4b4c97-9bl44
Namespace:            kueue-system
Priority:             500000
Priority Class Name:  p1
Service Account:      kueue-controller-manager
Node:                 test-kueue-worker/192.168.64.2
Start Time:           Fri, 17 May 2024 11:58:10 -0700
Labels:               control-plane=controller-manager
                      pod-template-hash=5b6f4b4c97
Annotations:          kubectl.kubernetes.io/default-container: manager
                      kubernetes.io/limit-ranger:
                        LimitRanger plugin set: cpu, memory request for container kube-rbac-proxy; cpu, memory limit for container kube-rbac-proxy
Status:               Running
IP:                   10.244.1.5
IPs:
  IP:           10.244.1.5
Controlled By:  ReplicaSet/kueue-controller-manager-5b6f4b4c97
Containers:
  manager:
    Container ID:  containerd://e7b593a55c4b31a5756e9b26b852730cc8e8243752dba78f4367b539a93ae269
    Image:         registry.k8s.io/kueue/kueue:v0.6.2
    Image ID:      registry.k8s.io/kueue/kueue@sha256:ef1f07fa559eb396a93e67d682743bac602b512cf11d203e14b10bcfa2e89112
    Ports:         8082/TCP, 9443/TCP
    Host Ports:    0/TCP, 0/TCP
    Command:
      /manager
    Args:
      --config=/controller_manager_config.yaml
      --zap-log-level=2
```

This is even after deleting the pod and waiting for deployment bring up. Weird...

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T19:28:18Z

can you try changing other parameters? Like the log-level?

### Comment by [@amy](https://github.com/amy) — 2024-05-17T19:29:45Z

yeah log level doesn't change either

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T19:31:19Z

Could you show the replicaset with the `kubectl get replicaset -n kueue-system`?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T19:33:03Z

This looks suspicious:
```
Replicas:               1 desired | 0 updated | 1 total | 1 available | 1 unavailable
StrategyType:           RollingUpdate
RollingUpdateStrategy:  25% max unavailable, 25% max surge
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T19:35:12Z

I guess that your updated replicaset failed to start pod somehow.

### Comment by [@amy](https://github.com/amy) — 2024-05-17T20:14:11Z

okay! Got the pod to update its args. Getting new error logs in the kueue controller:
```
I0517 20:12:46.090825       1 leaderelection.go:250] attempting to acquire leader lease kueue-system/kueue-manager.kueue.x-k8s.io...
{"level":"info","ts":"2024-05-17T20:12:46.192216512Z","logger":"cert-rotation","caller":"rotator/rotator.go:347","msg":"no cert refresh needed"}
{"level":"info","ts":"2024-05-17T20:12:46.192300248Z","logger":"cert-rotation","caller":"rotator/rotator.go:867","msg":"certs are ready in /tmp/k8s-webhook-server/serving-certs"}
{"level":"info","ts":"2024-05-17T20:12:46.261857114Z","caller":"controller/controller.go:220","msg":"Starting workers","controller":"cert-rotator","worker count":1}
{"level":"info","ts":"2024-05-17T20:12:46.263417658Z","logger":"cert-rotation","caller":"rotator/rotator.go:347","msg":"no cert refresh needed"}
{"level":"info","ts":"2024-05-17T20:12:46.264107092Z","logger":"cert-rotation","caller":"rotator/rotator.go:828","msg":"Ensuring CA cert","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration"}
{"level":"info","ts":"2024-05-17T20:12:46.274077578Z","logger":"cert-rotation","caller":"rotator/rotator.go:828","msg":"Ensuring CA cert","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration"}
{"level":"info","ts":"2024-05-17T20:12:46.284022151Z","logger":"cert-rotation","caller":"rotator/rotator.go:347","msg":"no cert refresh needed"}
{"level":"info","ts":"2024-05-17T20:12:46.284846815Z","logger":"cert-rotation","caller":"rotator/rotator.go:828","msg":"Ensuring CA cert","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration","name":"kueue-validating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration"}
{"level":"info","ts":"2024-05-17T20:12:46.294002625Z","logger":"cert-rotation","caller":"rotator/rotator.go:828","msg":"Ensuring CA cert","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration","name":"kueue-mutating-webhook-configuration","gvk":"admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration"}
I0517 20:12:46.493666       1 serving.go:374] Generated self-signed cert (/tmp/apiserver.crt, /tmp/apiserver.key)
{"level":"error","ts":"2024-05-17T20:12:46.493819819Z","logger":"visibility-server","caller":"visibility/server.go:52","msg":"Unable to apply VisibilityServerOptions","error":"failed to create listener: failed to listen on 0.0.0.0:8082: listen tcp 0.0.0.0:8082: bind: address already in use","stacktrace":"sigs.k8s.io/kueue/pkg/visibility.CreateAndStartVisibilityServer\n\t/workspace/pkg/visibility/server.go:52"}
F0517 20:12:46.493924       1 config.go:681] cannot derive external address port without listening on a secure port.
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T20:46:43Z

It looks like our default configuration recommends the same port for `pprofBindAddress: :8082` and the visibility API :)

Try putting the pprof in a different address?

### Comment by [@amy](https://github.com/amy) — 2024-05-17T20:53:22Z

it works! thanks for taking a look folks

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T21:09:41Z

thanks for opening the follow up issue!
