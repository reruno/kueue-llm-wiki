# Issue #8227: MultiKueueCluster unable to connect to a cluster

**Summary**: MultiKueueCluster unable to connect to a cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8227

**Last updated**: 2025-12-17T21:00:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Smuger](https://github.com/Smuger)
- **Created**: 2025-12-12T22:10:57Z
- **Updated**: 2025-12-17T21:00:45Z
- **Closed**: 2025-12-17T21:00:45Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 17

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I'm trying to connect Manage and Worker clusters in GKE in one fleet

**kueue-controller-manager logs** 
```json
{
    "level":"error",
    "ts":"2025-12-12T21:22:18.614915841Z",
    "caller":"controller/controller.go:474",
    "msg":"Reconciler error",
    "controller":"multikueuecluster",
    "controllerGroup":"kueue.x-k8s.io",
    "controllerKind":"MultiKueueCluster",
    "MultiKueueCluster":
    {
        "name":"n-r-training-cluster-us-w4"
    },
    "namespace":"",
    "name":"n-r-training-cluster-us-w4",
    "reconcileID":"XXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    "error":"panic: runtime error: invalid memory address or nil pointer dereference [recovered]",
    "stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"
}
```

```
k get clusterprofile -A
---
kueue-system              n-r-training-cluster-us-e4-us-east4   68m
kueue-system              n-r-training-cluster-us-w4-us-west4   68m
```
**ClusterProfile**
```yaml
Name:         n-r-training-cluster-us-w4-us-west4
Namespace:    kueue-system
Labels:       goog-terraform-provisioned=true
              kueue=worker-cluster
              x-k8s.io/cluster-manager=gke-fleet
Annotations:  fleet.gke.io/clusterName: projects/XXXXXXXXXXX/locations/us-west4/clusters/n-r-training-cluster-us-w4
              fleet.gke.io/membershipName: projects/XXXXXXXXXXX/locations/us-west4/memberships/n-r-training-cluster-us-w4
              fleet.gke.io/metricsEndpoint: https://monitoring.googleapis.com/v1/projects/XXXXXXX/location/global/prometheus
              gateway.gke.io/endpoint:
                https://us-west4-connectgateway.googleapis.com/v1/projects/XXXXXXXXXX/locations/us-west4/gkeMemberships/n-r-training-cluster-us-w4
API Version:  multicluster.x-k8s.io/v1alpha1
Kind:         ClusterProfile
Metadata:
  Creation Timestamp:  2025-12-12T20:42:25Z
  Generation:          1
  Resource Version:    XXXXXXXXXXXXXXXX
  UID:                 XXXXX-XXXXX-XXXX-XXXX-XXXXXXXXXX
Spec:
  Cluster Manager:
    Name:        gke-fleet
  Display Name:  n-r-training-cluster-us-w4(us-west4)
Status:
  Access Providers:
    Cluster:
      Server:  https://us-west4-connectgateway.googleapis.com/v1/projects/XXXXXXXX/locations/us-west4/gkeMemberships/n-r-training-cluster-us-w4
    Name:      google
  Conditions:
    Last Transition Time:  2025-12-12T20:42:25Z
    Message:               
    Reason:                Joined
    Status:                True
    Type:                  Joined
  Version:
    Kubernetes:  v1.34.1-gke.3355000
Events:          <none>
```

**MultiKueueCluster**
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: MultiKueueCluster
metadata:
  name: n-r-training-cluster-us-w4
spec:
  clusterSource:
    clusterProfileRef:
      name: n-r-training-cluster-us-w4-us-west4
```
**MultiKueueConfig**
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: MultiKueueConfig
metadata:
 name: multikueue-dws
spec:
 clusters: # Worker clusters
   - n-r-training-cluster-us-w4
```

**What you expected to happen**:

I was expecting MultiKueueCluster to connect using **clusterprofile**

**How to reproduce it (as minimally and precisely as possible)**:
1. Create 2 GKE clusters
2. Join them into one fleet
3. Set these resource_labels for one of the clusters
```
fleet-clusterinventory-management-cluster = "true"
fleet-clusterinventory-namespace = "kueue-system"
```
4. Enable master_global_access_config for both
5. Install Kueue with MultiKueueClusterProfile flag enabled

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): **v1.34.1-gke.3355000**
- Kueue version (use `git describe --tags --dirty --always`): **v0.15.0**
- Cloud provider or hardware configuration: **Google Cloud**
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T06:57:24Z

cc @hdp617 @mszadkow  ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T06:59:33Z

`panic: runtime error: invalid memory address or nil pointer dereference [recovered]` seeing this you are probably missing also configuration in the Kueue's configMap. @hdp617 has some example how to do it for GKE. The null pointer exception itself is solved here: https://github.com/kubernetes-sigs/kueue/pull/8071.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-15T10:40:30Z

Yes @mimowo is right, the issue you are seeing is due to lack of CredentialProvider configuration in MK config.

### Comment by [@Smuger](https://github.com/Smuger) — 2025-12-15T15:38:33Z

Thanks @mimowo and @mszadkow for your help

I'm sorry, I don't have much experience in GKE fleet / ClusterProfile and I couldn't find a good example in https://github.com/hdp617

My changes:
- Updated kueue to 0.15.1
- Fixed my configmap so now it looks like this:
```yaml
controllerManager:
  featureGates:
    - name: MultiKueueClusterProfile
      enabled: true
managerConfig:
  controllerManagerConfigYaml: |-
    multiKueue:
      clusterProfile:
        credentialsProviders:
        - name: google
          execConfig:
            apiVersion: client.authentication.k8s.io/v1beta1
            command: /plugins/gcp-auth-plugin
            interactiveMode: Never
```
- I've patched kueue-controller-manager deploy with:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kueue-controller-manager
  namespace: kueue-system
spec:
  template:
    spec:
      initContainers:
      - name: add-auth-plugin
        image: us-central1-docker.pkg.dev/XXXXXXXXXXX/gcp-auth-plugin/gcp-auth-plugin:latest
        command: ["cp"]
        args: 
        - "/gcp-auth-plugin"
        - "/plugins/gcp-auth-plugin"
        volumeMounts:
        - name: clusterprofile-plugins
          mountPath: "/plugins/"
      containers:
      - name: manager
        volumeMounts:
        - name: clusterprofile-plugins
          mountPath: "/plugins/"
      volumes:
      - name: clusterprofile-plugins
        emptyDir: {}
```
I've got the gcp-auth-plugin from [Googel Doc](https://github.com/GoogleCloudPlatform/gke-fleet-management/tree/main/gcp-auth-plugin) and send it to my Artifact Registry 

which solved some problems but I'm still seeing:

```bash
k get MultiKueueCluster -A

NAME                         CONNECTED   AGE
n-r-training-cluster-us-w4   False       6m13s
```

```json
{
    "level":"error",
    "ts":"2025-12-15T14:23:34.804143967Z",
    "caller":"multikueue/multikueuecluster.go:406",
    "msg":"failed to set kubeConfig in the remote client",
    "controller":"multikueuecluster",
    "controllerGroup":"kueue.x-k8s.io",
    "controllerKind":"MultiKueueCluster",
    "MultiKueueCluster":
    {
      "name":"n-r-training-cluster-us-w4"
    },
    "namespace":"",
    "name":"n-r-training-cluster-us-w4",
    "reconcileID":"XXXXXXXXXXXXXXXXX",
    "error":"failed to get server groups: unknown",
    "stacktrace":"sigs.k8s.io/kueue/pkg/controller/admissionchecks/multikueue.(*clustersReconciler).setRemoteClientConfig\n\t/workspace/pkg/controller/admissionchecks/multikueue/multikueuecluster.go:406\nsigs.k8s.io/kueue/pkg/controller/admissionchecks/multikueue.(*clustersReconciler).Reconcile\n\t/workspace/pkg/controller/admissionchecks/multikueue/multikueuecluster.go:446\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"
    }
```

when I run `/plugins/gcp-auth-plugin` via exec -it I get a token 

```json
{
"kind":"ExecCredential",
"apiVersion":"client.authentication.k8s.io/v1beta1",
"spec":{
  "interactive":false
},
"status":{
  "expirationTimestamp":"2025-12-15T16:06:30Z",
  "token":"XXX"
  }
}
```

I'm aware that this is a Kueue repo and not a GKE support channel, so if this is out of scope please do let me know and I'll to try to debug it further on my own

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T15:50:11Z

I don't know at this moment where is the problem. 

Your setup in Kueue looks quite reasonable. 

I'm pretty sure @hdp617 will have some insights as he configured it working e2e in the past with GKE.

In any case it is ok to seek help both in Kueue repo as well as in GKE support for issues where it is unclear which layer is at fault.

### Comment by [@hdp617](https://github.com/hdp617) — 2025-12-15T17:24:14Z

@Smuger I see that the plugin works locally but fails in the MultiKueue environement. This suggests that the manager cluster lacks the permissions to use Workload Identity to authenticate to the worker clusters.

Could you try adding the following IAM [policy bindings](https://github.com/GoogleCloudPlatform/gke-fleet-management/tree/feat/multikueue-clusterprofile/multikueue-clusterprofile#add-iam-policy-bindings)?

### Comment by [@Smuger](https://github.com/Smuger) — 2025-12-15T18:35:54Z

Hi @hdp617 
Thanks for your response

Just to add some context:
-  I'm using private clusters. Both clusters can reach each other
- This is my first time setting up a fleet so there is a high chance I forgot something simple 

I have:

1. **Workload Identity enabled** on every cluster and I used it for other services already
<img width="510" height="343" alt="Image" src="https://github.com/user-attachments/assets/80254f81-3779-4334-a43d-ab51dabf1bf9" />

2. **IAM Binding** set for the **kueue-controller-manager k8s service account in kueue-system namespace**
<img width="1243" height="75" alt="Image" src="https://github.com/user-attachments/assets/548a0ae8-49cb-4fc2-848f-99af5f70af87" />

3. Both clusters are private but I can access each others endpoints from pods running in them

4. **multikueuecluster** for cluster n-r-training-cluster-us-w4 is still `False` and still getting 
```
failed to get server groups: unknown
```
in kueue-controller-manager

### Comment by [@hdp617](https://github.com/hdp617) — 2025-12-15T19:16:26Z

@Smuger Thanks for your patience when we're polishing the documentation for this feature!

It's unclear to me what the problem is as your setup looks good to me. A few questions:
* How did you add your worker clusters to the Fleet?
* What is the worker cluster's workload pool? You can check it with `gcloud container clusters describe n-r-training-cluster-us-w4 --location europe-west4 --format="value(workloadIdentityConfig.workloadPool)"`. If it's not `<PROJECT_ID>.svc.id.goog`, it might be using the legacy identity pool. You can adjust the IAM policy bindings with the correct identity pool.

### Comment by [@Smuger](https://github.com/Smuger) — 2025-12-15T20:26:07Z

@hdp617 

Clusters are in **different regions** but still in the **same project** and **same VPC**

n-r-training-cluster-us-e4 - **Hub**
n-r-training-cluster-us-w4 - **Worker**

**Fleet**
<img width="1714" height="501" alt="Image" src="https://github.com/user-attachments/assets/472bca42-a776-4513-862d-3517079a7125" />

- I'm setting this up via Terraform. Both clusters joined the same fleet like this:

```terraform
resource "google_container_cluster" "private_no_auto_cluster" {

  fleet {
      project = <project-name>
  }

  workload_identity_config {
      workload_pool = <project-name>.svc.id.goog
  }
  
  resource_labels = {
      fleet-clusterinventory-management-cluster = "true"
      fleet-clusterinventory-namespace = "kueue-system"
  }

  service_external_ips_config {
      enabled = false
  }

  default_snat_status {
      disabled = false
  }

  private_cluster_config {
      enable_private_endpoint = true
      enable_private_nodes    = true
      master_ipv4_cidr_block  = "172.16.0.128/28"
    
      master_global_access_config {
        enabled = true
      }
  }
}
```
- Workload pool looks new project-name.svc.id.goog
```
gcloud container clusters describe n-r-training-cluster-us-e4 --location us-east4 --format="value(workloadIdentityConfig.workloadPool)"

<project-name>.svc.id.goog
```

### Comment by [@hdp617](https://github.com/hdp617) — 2025-12-15T21:15:37Z

Thanks for sharing! I'll try to reproduce it and get back to you. In the mean time, I used [this](https://github.com/GoogleCloudPlatform/gke-fleet-management/blob/feat/multikueue-clusterprofile/multikueue-clusterprofile/1-infrastructure/main.tf) GKE cluster setup when testing MultiKueue with ClusterProfile and Fleet if it's helpful.

### Comment by [@kshalot](https://github.com/kshalot) — 2025-12-17T15:20:24Z

Hey @Smuger!

One thing that might be missing in your setup is that the Connect Gateway API is disabled. I think it's an easy one to miss. I just tested it and I'm getting the exact same issue when the API is not enabled.

Can you check whether that's the case?

cc @hdp617

### Comment by [@hdp617](https://github.com/hdp617) — 2025-12-17T15:31:37Z

> Hey [@Smuger](https://github.com/Smuger)!
> 
> One thing that might be missing in your setup is that the Connect Gateway API is disabled. I think it's an easy one to miss. I just tested it and I'm getting the exact same issue when the API is not enabled.
> 
> Can you check whether that's the case?
> 
> cc [@hdp617[<img alt="" width="15" height="15" src="chrome-extension://dlebflppeeemcdpidccbiblndppbmjmh/ospo-chrome-ext-logo.png">](https://teams.googleplex.com/huypham@google.com)](https://github.com/hdp617)

Ah, it makes sense. I have `disable_on_destroy = false` for GCP APIs so that's why I haven't been able to reproduce this.

### Comment by [@Smuger](https://github.com/Smuger) — 2025-12-17T15:51:42Z

Thanks for the suggestion @kshalot 

My **Connect Gateway API** are enabled on both clusters but this does suggest some other network problem 

<img width="642" height="458" alt="Image" src="https://github.com/user-attachments/assets/83892865-6c44-494b-be6f-43d8e18dcd3a" />

<img width="625" height="462" alt="Image" src="https://github.com/user-attachments/assets/fbcdc7a1-24e9-4935-b828-976c2ebe5400" />

Here is some more config that's on both of them:

<img width="509" height="719" alt="Image" src="https://github.com/user-attachments/assets/4be1cc08-7759-4e8e-8fb9-b8caa0c94d3b" />

cc @hdp617

### Comment by [@kshalot](https://github.com/kshalot) — 2025-12-17T15:59:44Z

I'm pretty sure those are different things - I'm talking about the **Connect Gateway API** (note the "Connect" part), which is part of the GKE Fleet management.

The "Gateway API" in cluster details is the data plane gateway API (I think this? https://gateway-api.sigs.k8s.io/).

So just to confirm - is the Connect Gateway API enabled in GCP? For clarity, here are the docs on how to enable this - https://docs.cloud.google.com/endpoints/docs/openapi/enable-api.

### Comment by [@Smuger](https://github.com/Smuger) — 2025-12-17T16:12:02Z

@kshalot 

crap, sorry I totaly missunderstood you

You are right! my **[connectgateway.googleapis.com](https://console.cloud.google.com/apis/library/connectgateway.googleapis.com)** was disabled

<img width="496" height="293" alt="Image" src="https://github.com/user-attachments/assets/1fce07e5-11f1-4a60-9a48-4d3425ae8519" />

I'm applying the change right now

### Comment by [@Smuger](https://github.com/Smuger) — 2025-12-17T16:21:14Z

I can confirm that disabled [http://connectgateway.googleapis.com/](https://console.cloud.google.com/apis/library/connectgateway.googleapis.com) was the problem

```bash
k get MultiKueueCluster

NAME                         CONNECTED   AGE
n-r-training-cluster-us-w4   True        45h
```

Thank you so much @hdp617 and @kshalot for your help! I really appreciate it

Sorry for bothering you with such a silly mistake

### Comment by [@hdp617](https://github.com/hdp617) — 2025-12-17T16:29:26Z

Thanks for confirming. And this is not a silly mistake at all. I'll make sure this is documented in our docs and examples.
