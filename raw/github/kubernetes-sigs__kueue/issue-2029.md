# Issue #2029: Kubernetes 1.30: kueue controller fails to remove scheduling gates

**Summary**: Kubernetes 1.30: kueue controller fails to remove scheduling gates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2029

**Last updated**: 2024-04-24T15:47:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@bh-tt](https://github.com/bh-tt)
- **Created**: 2024-04-22T10:46:19Z
- **Updated**: 2024-04-24T15:47:33Z
- **Closed**: 2024-04-23T11:31:10Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 16

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
We have a Pod with the kueue.x-k8s.io/queue-name label to be managed by Kueue. Kueue correctly picks up the Pod, adds the scheduling gate, the managed label and the finalizer. The workload resource admits the Pod, but then the schedulingGate is never removed. As a result the Pod remains pending forever.
**What you expected to happen**:
I expected Kueue to remove the scheduling gate so the Pod can start.
**How to reproduce it (as minimally and precisely as possible)**:
Not completely sure, but it appears to be related to upgrading tot k8s 1.30 (as on our other clusters with 1.29.3 the same kueue versions and config works fine). I'll try to get a reproducer setup.

I do have a stacktrace:
```
manager {"level":"error","ts":"2024-04-22T09:46:14.590383907Z","caller":"jobframework/reconciler.go:388","msg":"Unsuspending job","controller":"v1_pod","namespace":"dat","name":"tijdenworkflow-javacronworkflow-1713738780-usfeest-3331214905",
"reconcileID":"34a7014a-b891-4e3e-a91d-5d02b5348318","job":"dat/tijdenworkflow-javacronworkflow-1713738780-usfeest-3331214905","gvk":"/v1, Kind=Pod","error":"Pod \"tijdenworkflow-javacronworkflow-1713738780-usfeest-3331214905\" is invalid: spec: Forbidden: pod updates may not change fields other than `spec.containers[*].image`,`spec.initContainers[*].image`,`spec.activeDeadlineSeconds`,`spec.tolerations` (only additions to existing tolerations),`spec.terminationGracePeriodSecon
ds` (allow it to be set to 1 if it was previously negative)\n  core.PodSpec{\n  \tVolumes:        {{Name: \"workload-socket\", VolumeSource: {EmptyDir: &{}}}, {Name: \"credential-socket\", VolumeSource: {EmptyDir: &{}}}, {Name: \"workloa    
d-certs\", VolumeSource: {EmptyDir: &{}}}, {Name: \"istio-envoy\", VolumeSource: {EmptyDir: &{Medium: \"Memory\"}}}, ...},\n  \tInitContainers: {{Name: \"istio-validation\", Image: \"docker.io/istio/proxyv2:1.21.1\", Args: {\"istio-iptable  
s\", \"-p\", \"15001\", \"-z\", ...}, Resources: {Limits: {s\"cpu\": {i: {...}, s: \"500m\", Format: \"DecimalSI\"}, s\"memory\": {i: {...}, Format: \"BinarySI\"}}, Requests: {s\"cpu\": {i: {...}, s: \"20m\", Format: \"DecimalSI\"}, s\"ephem
eral-storage\": {i: {...}, Format: \"BinarySI\"}, s\"memory\": {i: {...}, Format: \"BinarySI\"}}}, ...}, {Name: \"istio-proxy\", Image: \"docker.io/istio/proxyv2:1.21.1\", Args: {\"proxy\", \"sidecar\", \"--domain\", \"$(POD_NAMESPACE).svc.c
luster.local\", ...}, Ports: {{Name: \"http-envoy-prom\", ContainerPort: 15090, Protocol: \"TCP\"}}, ...}, {Name: \"init\", Image: \"docker.io/bitnami/argo-workflow-exec:3.5.5-debian-12-r4\", Command: {\"argoexec\", \"init\", \"--loglevel\",
 \"info\", ...}, Env: {{Name: \"ARGO_POD_NAME\", ValueFrom: &{FieldRef: &{APIVersion: \"v1\", FieldPath: \"metadata.name\"}}}, {Name: \"ARGO_POD_UID\", ValueFrom: &{FieldRef: &{APIVersion: \"v1\", FieldPath: \"metadata.uid\"}}}, {Name: \"GOD
EBUG\", Value: \"x509ignoreCN=0\"}, {Name: \"ARGO_WORKFLOW_NAME\", Value: \"tijdenworkflow-javacronworkflow-1713738780\"}, ...}, ...}},\n  \tContainers: []core.Container{\n  \t\t{Name: \"wait\", Image: \"docker.io/bitnami/argo-workflow-e    
xec:3.5.5-debian-12-r4\", Command: {\"argoexec\", \"wait\", \"--loglevel\", \"info\", ...}, Env: {{Name: \"ARGO_POD_NAME\", ValueFrom: &{FieldRef: &{APIVersion: \"v1\", FieldPath: \"metadata.name\"}}}, {Name: \"ARGO_POD_UID\", ValueFrom: &{F
ieldRef: &{APIVersion: \"v1\", FieldPath: \"metadata.uid\"}}}, {Name: \"GODEBUG\", Value: \"x509ignoreCN=0\"}, {Name: \"ARGO_WORKFLOW_NAME\", Value: \"tijdenworkflow-javacronworkflow-1713738780\"}, ...}, ...},\n  \t\t{\n  \t\t\t... // 18    
 identical fields\n  \t\t\tTerminationMessagePolicy: \"File\",\n  \t\t\tImagePullPolicy:          \"Always\",\n  \t\t\tSecurityContext: &core.SecurityContext{\n  \t\t\t\t... // 9 identical fields\n  \t\t\t\tProcMount:       nil,\n�          
� \t\t\t\tSeccompProfile:  &{Type: \"RuntimeDefault\"},\n- \t\t\t\tAppArmorProfile: &core.AppArmorProfile{Type: \"RuntimeDefault\"},\n+ \t\t\t\tAppArmorProfile: nil,\n  \t\t\t},\n  \t\t\tStdin:     false,\n  \t\t\tStdinOnce: false,\         
n  \t\t\tTTY:       false,\n  \t\t},\n  \t},\n  \tEphemeralContainers: nil,\n  \tRestartPolicy:       \"Never\",\n  \t... // 28 identical fields\n  }\n","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconcile              
r).ReconcileGenericJob\n\t/workspace/pkg/controller/jobframework/reconciler.go:388\nsigs.k8s.io/kueue/pkg/controller/jobs/pod.(*Reconciler).Reconcile\n\t/workspace/pkg/controller/jobs/pod/pod_controller.go:108\nsigs.k8s.io/controller-runtime
/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pk
g/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/intern
al/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:227"}
```
**Anything else we need to know?**:
For now we have disabled the pod framework controller. The batch/job controller seems unaffected, likely because (I think) it does not use scheduling gates.
**Environment**:
- Kubernetes version (use `kubectl version`): v1.30.0
- Kueue version (use `git describe --tags --dirty --always`): v0.6.2
- Cloud provider or hardware configuration: selfhosted kubeadm cluster
- OS (e.g: `cat /etc/os-release`): '"Debian GNU/Linux 12 (bookworm)"'
- Kernel (e.g. `uname -a`): 'Linux <hostname>6.1.0-20-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.85-1 (2024-04-11) x86_64 GNU/Linux'
- Install tools: helm
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-04-22T15:40:35Z

When I have seen issues like that, it seems to be related to a misbehaving webhook.

```
"reconcileID":"34a7014a-b891-4e3e-a91d-5d02b5348318","job":"dat/tijdenworkflow-javacronworkflow-1713738780-usfeest-3331214905","gvk":"/v1, Kind=Pod","error":"Pod \"tijdenworkflow-javacronworkflow-1713738780-usfeest-3331214905\" is invalid: spec: Forbidden: pod updates may not change fields other than `spec.containers[*].image`,`spec.initContainers[*].image`,`spec.activeDeadlineSeconds`,`spec.tolerations` (only additions to existing tolerations),`spec.terminationGracePeriodSecon
```

Why this would impact 1.30 and not 1.29 is a really interesting question.

### Comment by [@bh-tt](https://github.com/bh-tt) — 2024-04-23T07:31:49Z

Well the following deployment does *not* reproduce it, the pods start normally on a 1.30 cluster. I'll continue to look for a reproducer, likely the issue has something to do with either istio injecting a sidecar into the Pod, or something about the argo workflows template.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-bh
  namespace: it
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/instance: test-bh
      app.kubernetes.io/name: test-bh
  template:
    metadata:
      labels:
        app.kubernetes.io/instance: test-bh
        app.kubernetes.io/name: test-bh
        sidecar.istio.io/inject: "false"
        kueue.x-k8s.io/queue-name: default
    spec:
      containers:
      - image: image-registry:443/it/images/diag
        imagePullPolicy: IfNotPresent
        name: slapd
        args:
          - sleep
          - "300"
```

### Comment by [@bh-tt](https://github.com/bh-tt) — 2024-04-23T07:32:40Z

It's not istio either, adding that to the pod starts fine.

### Comment by [@bh-tt](https://github.com/bh-tt) — 2024-04-23T11:29:00Z

Alright I have a reproducer:
Kueue chart v0.6.2, values:
```
      enableCertManager: false
      enablePrometheus: true
      controllerManager:
        manager:
          image:
            tag: *kueue_version
        containerSecurityContext:
          capabilities:
            drop:
              - ALL
          privileged: false
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
        podSecurityContext:
          seccompProfile:
            type: RuntimeDefault
        replicas: 1
      managerConfig:
        controllerManagerConfigYaml: "{{ kueue_controller_config | ansible.builtin.to_nice_yaml(indent=2) }}"
```

Contents of the kueue-manager-config Configmap:
```
apiVersion: v1                                                                                                                                                                                                                                   
data:                                                                                                                                                                                                                                            
  controller_manager_config.yaml: |                                                                                                                                                                                                              
    apiVersion: config.kueue.x-k8s.io/v1beta1                                                                                                                                                                                                    
    clientConnection:                                                                                                                                                                                                                            
      burst: 100                                                                                                                                                                                                                                 
      qps: 50                                                                                                                                                                                                                                    
    controller:                                                                                                                                                                                                                                  
      groupKindConcurrency:                                                                                                                                                                                                                      
        ClusterQueue.kueue.x-k8s.io: 1                                                                                                                                                                                                           
        Job.batch: 5                                                                                                                                                                                                                             
        LocalQueue.kueue.x-k8s.io: 1                                                                                                                                                                                                             
        ResourceFlavor.kueue.x-k8s.io: 1                                                                                                                                                                                                         
        Workload.kueue.x-k8s.io: 1                                                                                                                                                                                                               
    health:                                                                                                                                                                                                                                      
      healthProbeBindAddress: :8081                                                                                                                                                                                                              
    integrations:                                                                                                                                                                                                                                
      frameworks:                                                                                                                                                                                                                                
      - batch/job                                                                                                                                                                                                                                
      - pod                                                                                                                                                                                                                                      
    kind: Configuration                                                                                                                                                                                                                          
    leaderElection:                                                                                                                                                                                                                              
      leaderElect: false                                                                                                                                                                                                                         
      resourceName: c1f6bfd2.kueue.x-k8s.io                                                                                                                                                                                                      
    metrics:                                                                                                                                                                                                                                     
      bindAddress: :8080                                                                                                                                                                                                                         
    podOptions:                                                                                                                                                                                                                                  
      namespaceSelector:                                                                                                                                                                                                                         
        matchExpressions:                                                                                                                                                                                                                        
        - key: kubernetes.io/metadata.name                                                                                                                                                                                                       
          operator: NotIn                                                                                                                                                                                                                        
          values:                                                                                                                                                                                                                                
          - kube-system                                                                                                                                                                                                                          
          - kueue-system                                                                                                                                                                                                                         
      podSelector:                                                                                                                                                                                                                               
        matchExpressions:                                                                                                                                                                                                                        
        - key: kueue.x-k8s.io/queue-name                                                                                                                                                                                                         
          operator: Exists                                                                                                                                                                                                                       
    webhook:                                                                                                                                                                                                                                     
      port: 9443                                                                                                                                                                                                                                 
kind: ConfigMap                                                                                                                                                                                                                                  
metadata:                                                                                                                                                                                                                                        
  annotations:                                                                                                                                                                                                                                   
    meta.helm.sh/release-name: kueue                                                                                                                                                                                                             
    meta.helm.sh/release-namespace: kueue-system                                                                                                                                                                                                 
  creationTimestamp: "2023-05-09T07:35:57Z"                                                                                                                                                                                                      
  labels:                                                                                                                                                                                                                                        
    app.kubernetes.io/managed-by: Helm                                                                                                                                                                                                           
  name: kueue-manager-config                                                                                                                                                                                                                     
  namespace: kueue-system                                                                                                                                                                                                                        
  resourceVersion: "340960284"                                                                                                                                                                                                                   
  uid: 6cd0c12a-5d2e-402c-9509-5e4ae12f0f37
```


Reproducer Pod (remove the metadata.annotations.' container.apparmor.security.beta.kubernetes.io/main' field to make it work) :
```
apiVersion: v1
kind: Pod
metadata:
  annotations:
    container.apparmor.security.beta.kubernetes.io/main: runtime/default
  labels:
    kueue.x-k8s.io/queue-name: default
    sidecar.istio.io/inject: "false"
  name: kueue-reproducer
  namespace: it
spec:
  containers:
  - image: debian:bookworm
    name: main
```

Likely cause is that the apparmor annotation graduated to Stable in 1.30 and perhaps some logic exists in the apiserver to automatically add that to the container security context? The stacktrace in the initial comment is still the same, and I see a value in it related to AppArmorProfile I think.

I'm not sure kueue can actually fix this, I'll try if kueue admits the pods nicely if I set the apparmorprofile in the securitycontext.

### Comment by [@bh-tt](https://github.com/bh-tt) — 2024-04-23T11:31:10Z

Setting the value in the container securityContext works, I'll close this as it requires a minor change to manifests to fix it.
```
apiVersion: v1
kind: Pod
metadata:
  labels:
    kueue.x-k8s.io/queue-name: default
    sidecar.istio.io/inject: "false"
  name: test-kueue-reproducer
  namespace: it
spec:
  containers:
  - image: debian:bookworm
    name: main
    securityContext:
      appArmorProfile:
        type: RuntimeDefault
```

### Comment by [@kannon92](https://github.com/kannon92) — 2024-04-23T15:05:17Z

@alculquicondor or @tenzen-y  anything you think we'd want in the repo for this research?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-23T16:38:03Z

I guess the apiserver is rejecting the change?

You should have seen some error logs in the Kueue manager for the pod reconciler.

### Comment by [@bh-tt](https://github.com/bh-tt) — 2024-04-24T06:11:09Z

Yes, that's the stacktrace I posted in the initial comment.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-24T06:41:48Z

We don't support the K8s v1.30 yet, but mentioning this restriction might be worth it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-24T14:46:13Z

I think you should open an issue on kubernetes/kubernetes. The apiserver shouldn't be trying to change a Pod if it cannot be changed.

I left a comment, but @bh-tt better follow up with a dedicated bug https://github.com/kubernetes/kubernetes/pull/123435#issuecomment-2075125351

### Comment by [@liggitt](https://github.com/liggitt) — 2024-04-24T15:00:29Z

How is kueue removing the scheduling gates? Is it doing a read into a typed pod object, then a simple update back? If so, it is likely dropping the new apparmor field and is the thing the apiserver sees as trying to mutate the pod on update.

Clients doing updates of Pod objects should either stay perfectly up to date with their API definitions so they never drop fields, or should use a patch to modify just the field they want to touch and nothing else.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-24T15:29:20Z

The OP is using `v0.6.2`, which uses 1.28 libraries.

`v0.7.x` will use 1.29 libraries, so I think it shouldn't run into this problem. But yes, it will be more resilient to use patch/apply for scheduling gates removal.

Opened https://github.com/kubernetes-sigs/kueue/issues/2056

### Comment by [@liggitt](https://github.com/liggitt) — 2024-04-24T15:41:16Z

> `v0.7.x` will use 1.29 libraries, so I think it shouldn't run into this problem

1.29 or 1.30? the fields were added in 1.30

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-24T15:44:36Z

> > `v0.7.x` will use 1.29 libraries, so I think it shouldn't run into this problem
> 
> 1.29 or 1.30? the fields were added in 1.30

It could upgrade to 1.30 until a new kueue release, but we have some blockers to upgrade to 1.30: https://github.com/kubernetes-sigs/kueue/issues/2004

So maybe we should keep using v1.29.

### Comment by [@liggitt](https://github.com/liggitt) — 2024-04-24T15:45:44Z

using 1.29 libs would be ok if https://github.com/kubernetes-sigs/kueue/issues/2056 is fixed

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-24T15:47:32Z

> using 1.29 libs would be ok if #2056 is fixed

Thank you for letting me know!
