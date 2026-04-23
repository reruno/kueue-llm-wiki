# Issue #8838: TAS ignores resources excluded via excludeResourcePrefixes for placement calculations

**Summary**: TAS ignores resources excluded via excludeResourcePrefixes for placement calculations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8838

**Last updated**: 2026-02-04T20:12:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2026-01-27T21:43:05Z
- **Updated**: 2026-02-04T20:12:35Z
- **Closed**: 2026-02-04T20:12:35Z
- **Labels**: `kind/bug`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
 TAS uses filtered pod requests from `excludeResourcePrefixes` when calculating how many pods can fit on each node. This causes TAS to           
 potentially over-schedule pods on nodes that don't have sufficient excluded resources.                                                                                      
 
The root cause is in `pkg/workload/workload.go` where `totalRequestsFromPodSets()` filters pod requests using `dropExcludedResources()`. The filtered request is stored in `PodSetResources.Requests` and later used by TAS in `pkg/scheduler/flavorassigner/tas_flavorassigner.go` via `SinglePodRequests()`.                                         
                                                                                                                                                                             
 TAS should use the original, unfiltered pod spec requests to accurately determine how many pods can fit on each node based on all resources the pods actually need, regardless of whether those resources are excluded from quota calculations.

**What you expected to happen**:
TAS should consider all pod resource requests for placement calculations, including resources excluded via `excludeResourcePrefixes`. The purpose of `excludeResourcePrefixes` is to exclude resources from quota accounting, not from physical placement calculations.

**How to reproduce it (as minimally and precisely as possible)**:
**Kueue:** v0.16.0                                                                                                                                                          
 **Kind cluster manifest:** Standard 2-worker cluster                                                                                                                        
                                                                                                                                                                             
 ### Manifests:                                                                                                                                                              
 <details>                                                                                                                                                                 
   <summary>kind-config.yaml</summary>                                                                                                                                       
                                                                                                                                                                             
   ```yaml                                                                                                                                                                   
   kind: Cluster                                                                                                                                                             
   apiVersion: kind.x-k8s.io/v1alpha4                                                                                                                                        
   nodes:                                                                                                                                                                    
   - role: control-plane                                                                                                                                                     
   - role: worker                                                                                                                                                            
   - role: worker                                                                                                                                                            
   ```                                                                                                                                                                       
   </details>                                                                                                                                                                
                                                                                                                                                                             
   <details>                                                                                                                                                                 
   <summary>kueue-config.yaml </summary>                                                                                             
                                                                                                                                                                             
   ```yaml                                                                                                                                                                   
   apiVersion: v1                                                                                                                                                            
   kind: ConfigMap                                                                                                                                                           
   metadata:                                                                                                                                                                 
     name: kueue-manager-config                                                                                                                                              
     namespace: kueue-system                                                                                                                                                 
   data:                                                                                                                                                                     
     controller_manager_config.yaml: |                                                                                                                                       
       apiVersion: config.kueue.x-k8s.io/v1beta2                                                                                                                             
       kind: Configuration                                                                                                                                                   
       health:                                                                                                                                                               
         healthProbeBindAddress: :8081                                                                                                                                       
       metrics:                                                                                                                                                              
         bindAddress: :8443                                                                                                                                                  
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
           Cohort.kueue.x-k8s.io: 1                                                                                                                                          
           ClusterQueue.kueue.x-k8s.io: 1                                                                                                                                    
           ResourceFlavor.kueue.x-k8s.io: 1                                                                                                                                  
       clientConnection:                                                                                                                                                     
         qps: 50                                                                                                                                                             
         burst: 100                                                                                                                                                          
       integrations:                                                                                                                                                         
         frameworks:                                                                                                                                                         
           - "batch/job"                                                                                                                                                     
           - "pod"                                                                                                                                                           
       resources:                                                                                                                                                            
         excludeResourcePrefixes:                                                                                                                                            
           - "example.com/"                                                                                                                                                  
   ```                                                                                                                                                                       
   </details>                                                                                                                                                                
                                                                                                                                                                             
   <details>                                                                                                                                                                 
   <summary>topology.yaml</summary>                                                                                                                                          
                                                                                                                                                                             
   ```yaml                                                                                                                                                                   
   apiVersion: kueue.x-k8s.io/v1beta2                                                                                                                                        
   kind: Topology                                                                                                                                                            
   metadata:                                                                                                                                                                 
     name: default-topology                                                                                                                                                  
   spec:                                                                                                                                                                     
     levels:                                                                                                                                                                 
       - nodeLabel: kubernetes.io/hostname                                                                                                                                   
   ```                                                                                                                                                                       
   </details>                                                                                                                                                                
                                                                                                                                                                             
   <details>                                                                                                                                                                 
   <summary>resource-flavor.yaml</summary>                                                                                                                                   
                                                                                                                                                                             
   ```yaml                                                                                                                                                                   
   apiVersion: kueue.x-k8s.io/v1beta2                                                                                                                                        
   kind: ResourceFlavor                                                                                                                                                      
   metadata:                                                                                                                                                                 
     name: tas-flavor                                                                                                                                                        
   spec:                                                                                                                                                                     
     nodeLabels:                                                                                                                                                             
       node-role.kubernetes.io/worker: ""                                                                                                                                    
     topologyName: default-topology                                                                                                                                          
   ```                                                                                                                                                                       
   </details>                                                                                                                                                                
                                                                                                                                                                             
   <details>                                                                                                                                                                 
   <summary>cluster-queue.yaml</summary>                                                                                                                                     
                                                                                                                                                                             
   ```yaml                                                                                                                                                                   
   apiVersion: kueue.x-k8s.io/v1beta2                                                                                                                                        
   kind: ClusterQueue                                                                                                                                                        
   metadata:                                                                                                                                                                 
     name: test-cq                                                                                                                                                           
   spec:                                                                                                                                                                     
     namespaceSelector: {}                                                                                                                                                   
     resourceGroups:                                                                                                                                                         
       - coveredResources: ["cpu"]                                                                                                                                           
         flavors:                                                                                                                                                            
           - name: tas-flavor                                                                                                                                                
             resources:                                                                                                                                                      
               - name: cpu                                                                                                                                                   
                 nominalQuota: 8                                                                                                                                             
   ```                                                                                                                                                                       
   </details>                                                                                                                                                                
                                                                                                                                                                             
   <details>                                                                                                                                                                 
   <summary>local-queue.yaml</summary>                                                                                                                                       
                                                                                                                                                                             
   ```yaml                                                                                                                                                                   
   apiVersion: kueue.x-k8s.io/v1beta2                                                                                                                                        
   kind: LocalQueue                                                                                                                                                          
   metadata:                                                                                                                                                                 
     name: test-lq                                                                                                                                                           
     namespace: default                                                                                                                                                      
   spec:                                                                                                                                                                     
     clusterQueue: test-cq                                                                                                                                                   
   ```                                                                                                                                                                       
   </details>                                                                                                                                                                
                                                                                                                                                                             
   <details>                                                                                                                                                                 
   <summary>test-workload.yaml</summary>                                                                                                                                     
                                                                                                                                                                             
   ```yaml                                                                                                                                                                   
   apiVersion: kueue.x-k8s.io/v1beta2                                                                                                                                        
   kind: Workload                                                                                                                                                            
   metadata:                                                                                                                                                                 
     name: test-wl                                                                                                                                                           
     namespace: default                                                                                                                                                      
   spec:                                                                                                                                                                     
     queueName: test-lq                                                                                                                                                      
     podSets:                                                                                                                                                                
       - name: main                                                                                                                                                          
         count: 4                                                                                                                                                            
         topologyRequest:                                                                                                                                                    
           preferred: kubernetes.io/hostname                                                                                                                                 
         template:                                                                                                                                                           
           spec:                                                                                                                                                             
             restartPolicy: Never                                                                                                                                            
             containers:                                                                                                                                                     
               - name: test                                                                                                                                                  
                 image: busybox                                                                                                                                              
                 command: ["sleep", "3600"]                                                                                                                                  
                 resources:                                                                                                                                                  
                   requests:                                                                                                                                                 
                     cpu: "100m"                                                                                                                                             
                     example.com/test-resource: "1"
   ```                                                                                                                                                                       
   </details> 
                                                                        
   ### Steps to reproduce:                                                                                                                                                   
                                                                                                                                                                             
   1. Create Kind cluster with 2 worker nodes                                                                                                                                
   2. Label worker nodes with `node-role.kubernetes.io/worker=""`                                                                                                            
   3. Patch each worker node with extended resource: `example.com/test-resource: 2`                                                                                          
      ```bash                                                                                                                                                                
      kubectl proxy &                                                                                                                                                        
      curl -X PATCH -H "Content-Type: application/json-patch+json" \                                                                                                         
        --data '[{"op": "add", "path": "/status/capacity/example.com~1test-resource", "value": "2"},                                                                         
                 {"op": "add", "path": "/status/allocatable/example.com~1test-resource", "value": "2"}]' \                                                                   
        "http://localhost:8001/api/v1/nodes/<node-name>/status"                                                                                                              
      ```                                                                                                                                                                    
   4. Install Kueue v0.16.0                                                                                                                                                  
   5. Apply the kueue-config.yaml
   6. Restart Kueue controller to pick up config                                                                                                                             
   7. Apply the Kueue resources                                                                                        
   8. Apply the test workload                                                                                     
   9. Check workload status: 
   ```sh
   kubectl get workload test-wl -o jsonpath='{.status.admission.podSetAssignments[0].topologyAssignment}' | jq .
   ```                                 
                                                                                                                                                                             
   ### Expected result:                                                                                                                                                      
                                                                                                                                                                             
   With 2 nodes each having `example.com/test-resource: 2`, and 4 pods each needing 1, TAS should assign:                                                                    
   - 2 pods to worker1                                                                                                                                                       
   - 2 pods to worker2                                                                                                                                                       
                                                                                                                                                                             
   ### Actual result:                                                                                                                                                        
                                                                                                                                                                             
   TAS assigns all 4 pods to a single node:                                                                                                                                  
                                                                                                                                                                             
   ```json                                                                                                                                                                   
   {                                                                                                                                                                         
     "levels": ["kubernetes.io/hostname"],                                                                                                                                   
     "slices": [{                                                                                                                                                            
       "domainCount": 1,                                                                                                                                                     
       "podCounts": {"universal": 4},                                                                                                                                        
       "valuesPerLevel": [{"universal": "tas-exclude-test-worker2"}]                                                                                                         
     }]                                                                                                                                                                      
   }                                                                                                                                                                         
   ```                                                                                                                                                                       
                                                                                                                                                                             
   This happens because TAS only sees the filtered requests (CPU only) and ignores `example.com/test-resource`.                                                              
                                                                                                                                                                             
   ## Anything else we need to know?:                                                                                                                                       
The bug was likely introduced unintentionally when `excludeResourcePrefixes` was added (PR #2267) without a KEP. TAS came later (PR #3256) and inherited the filtered requests without explicit design consideration for this interaction. 

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-27T21:43:14Z

/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-27T21:43:22Z

cc @MaysaMacedo

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2026-01-28T01:43:32Z

@sohankunkerkar thanks for the investigation!
so if I get this right, given `excludeResourcePrefixes` is meant to control resources for quota management and admission process that means it shouldn't have impacted TAS because TAS is meant for placement of resource, right?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-28T04:29:44Z

Yes, you are right. `excludeResourcePrefixes` is documented for `quota management and admission process` but it controls what resources count against `ClusterQueue` budget. TAS handles physical placement based on actual node capacity. These should be independent, but the current code path causes them to overlap incorrectly: `totalRequestsFromPodSets()` calls `dropExcludedResources()` before storing requests, and TAS uses `SinglePodRequests()` which returns these filtered requests. So TAS ignores excluded resources when calculating how many pods fit per node.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T12:51:42Z

Yes, I agree with the issue. TAS should consider resources excluded by `excludeResourcePrefixes`, because this is for quota management. TAS wants to be as close as possible to kube-scheduler, just with more sophisticated algorithms for AI workloads. Ultimately, we would like to delegate scheduling to kube-scheduler when the kube-scheduler has WAS and TAS built-in. So, TAS in Kueue will produce more accurate scheduling if it takes into account resources excluded by `excludeResourcePrefixes`

cc @tenzen-y @gabesaba in case you have some opinion here too

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-28T13:32:27Z

> Yes, I agree with the issue. TAS should consider resources excluded by `excludeResourcePrefixes`, because this is for quota management. TAS wants to be as close as possible to kube-scheduler, just with more sophisticated algorithms for AI workloads. Ultimately, we would like to delegate scheduling to kube-scheduler when the kube-scheduler has WAS and TAS built-in. So, TAS in Kueue will produce more accurate scheduling if it takes into account resources excluded by `excludeResourcePrefixes`
> 
> cc [@tenzen-y](https://github.com/tenzen-y) [@gabesaba](https://github.com/gabesaba) in case you have some opinion here too

+1

See related discussion here https://github.com/kubernetes-sigs/kueue/pull/8396#discussion_r2713424680 (thanks @sohankunkerkar for making the connection)
