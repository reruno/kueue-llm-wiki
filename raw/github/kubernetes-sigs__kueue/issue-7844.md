# Issue #7844: [flaky e2e starup] "manager" in "kueue-controller-manager-59598f4b99-pc2h5" has restarted 1 times

**Summary**: [flaky e2e starup] "manager" in "kueue-controller-manager-59598f4b99-pc2h5" has restarted 1 times

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7844

**Last updated**: 2025-11-26T10:04:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-24T11:14:26Z
- **Updated**: 2025-11-26T10:04:38Z
- **Closed**: 2025-11-26T10:04:38Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 10

## Description

/kind flake 

**What happened**:

failure on unrelated branch:  https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7827/pull-kueue-test-e2e-main-1-34/1992908904400424960

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:

ci 
**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.34.0: [BeforeSuite] expand_less	34s
{Told to stop trying after 0.007s.
"manager" in "kueue-controller-manager-59598f4b99-pc2h5" has restarted 1 times failed [FAILED] Told to stop trying after 0.007s.
"manager" in "kueue-controller-manager-59598f4b99-pc2h5" has restarted 1 times
In [BeforeSuite] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/suite_test.go:73 @ 11/24/25 11:02:48.53
}
```
and I found the logs:

```
{"AdmissionFairSharing":true,"ConfigurableResourceTransformations":true,"DynamicResourceAllocation":false,"ElasticJobsViaWorkloadSlices":false,"FailureRecoveryPolicy":false,"FlavorFungibility":true,"FlavorFungibilityImplicitPreferenceDefault":false,"HierarchicalCohorts":true,"LendingLimit":true,"LocalQueueDefaulting":true,"LocalQueueMetrics":true,"ManagedJobsNamespaceSelectorAlwaysRespected":true,"MultiKueue":true,"MultiKueueAdaptersForCustomJobs":true,"MultiKueueAllowInsecureKubeconfigs":false,"MultiKueueBatchJobWithManagedBy":true,"MultiKueueClusterProfile":false,"ObjectRetentionPolicies":true,"PartialAdmission":true,"PrioritySortingWithinCohort":true,"PropagateBatchJobLabelsToWorkload":true,"ReclaimablePods":true,"SanitizePodSets":true,"TASBalancedPlacement":false,"TASFailedNodeReplacement":true,"TASFailedNodeReplacementFailFast":true,"TASProfileLeastFreeCapacity":false,"TASProfileMixed":true,"TASReplaceNodeOnPodTermination":true,"TopologyAwareScheduling":true,"VisibilityOnDemand":true,"WorkloadRequestUseMergePatch":false}}
2025-11-24T11:01:07.900702194Z stderr F 2025-11-24T11:01:07.900446511Z	LEVEL(-2)	setup	kueue/main.go:206	K8S Client	{"qps": 50, "burst": 100}
2025-11-24T11:01:07.984863254Z stderr F 2025-11-24T11:01:07.973859483Z	ERROR	setup	kueue/main.go:310	Skipping admission check controller setup: Provisioning Requests not supported (Possible cause: missing or unsupported cluster-autoscaler)	{"error": "no matches for kind \"ProvisioningRequest\" in version \"autoscaling.x-k8s.io/v1\""}
2025-11-24T11:01:07.984933095Z stderr F main.setupIndexes
2025-11-24T11:01:07.984938865Z stderr F 	/workspace/cmd/kueue/main.go:310
2025-11-24T11:01:07.984943295Z stderr F main.main
2025-11-24T11:01:07.984947545Z stderr F 	/workspace/cmd/kueue/main.go:251
2025-11-24T11:01:07.985049507Z stderr F runtime.main
2025-11-24T11:01:07.985056697Z stderr F 	/usr/local/go/src/runtime/proc.go:285
2025-11-24T11:01:07.990253588Z stderr F 2025-11-24T11:01:07.989909494Z	INFO	setup	kueue/main.go:453	Probe endpoints are configured on healthz and readyz
2025-11-24T11:01:07.990631542Z stderr F 2025-11-24T11:01:07.99045343Z	INFO	setup	cert/cert.go:90	Waiting for certificate generation to complete
2025-11-24T11:01:07.990963446Z stderr F 2025-11-24T11:01:07.990746704Z	INFO	setup	kueue/main.go:295	Starting manager
2025-11-24T11:01:07.991855927Z stderr F 2025-11-24T11:01:07.991582444Z	INFO	controller-runtime.metrics	server/server.go:208	Starting metrics server
```
which looks related

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T11:18:30Z

cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-24T11:24:02Z

Do we have prow logs?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T11:38:40Z

Yes, will update the description also
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7827/pull-kueue-test-e2e-main-1-34/1992908904400424960

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T16:09:43Z

fyi, this failure was before merging https://github.com/kubernetes-sigs/kueue/pull/7772

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-25T06:59:10Z

One more failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7845/pull-kueue-test-e2e-multikueue-main/1993207895721775104.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-11-25T09:26:16Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-11-25T09:29:24Z

On my first try, I was able to reproduce this error locally. Let's see if it’s just as easy to reproduce in subsequent attempts. In any case, I’ll start looking into it.

```bash
/Users/Irving_Mondragon/Documents/git/kueue/test/e2e/singlecluster/suite_test.go:59
  STEP: Waiting for availability of deployment: "kueue-system/kueue-controller-manager" @ 11/25/25 10:25:25.244
  "level"=0 "msg"="Deployment is available in the cluster" "deployment"={"name"="kueue-controller-manager" "namespace"="kueue-system"} "waitingTime"="1m1.936154916s"
  STEP: Checking no restarts for the controller: "kueue-system/kueue-controller-manager" @ 11/25/25 10:26:27.184
  [FAILED] in [BeforeSuite] - /Users/Irving_Mondragon/Documents/git/kueue/test/e2e/singlecluster/suite_test.go:73 @ 11/25/25 10:26:27.196
[BeforeSuite] [FAILED] [61.951 seconds]
[BeforeSuite] 
/Users/Irving_Mondragon/Documents/git/kueue/test/e2e/singlecluster/suite_test.go:59

  [FAILED] Told to stop trying after 0.012s.
  "manager" in "kueue-controller-manager-b8789887d-gvnsj" has restarted 1 times
  In [BeforeSuite] at: /Users/Irving_Mondragon/Documents/git/kueue/test/e2e/singlecluster/suite_test.go:73 @ 11/25/25 10:26:27.196
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T12:53:43Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7859/pull-kueue-test-e2e-main-1-33/1993296869014376448

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T17:46:17Z

I have an idea, if you are able to repro the problem, but the investigation if hard due to lost logs after container restart, then I think we can just change the `restartPolicy: Never` in https://github.com/kubernetes-sigs/kueue/blob/main/config/components/manager/manager.yaml
Then when the issue happens, then instead of restarting the container the whole pod is recreated. As a result we should get the Kueue logs recorded in artifacts for investigation.

Ah, but then the test may just pass rather than fail, as the container will not restart - the whole pod would be recreated (but I'm not sure).

Alternative is to inspect the exit containers on Kind using probably `docker exec -it kind-worker crictl -a` (iirc -a includes exit containers)

EDIT: trying a quick check: https://github.com/kubernetes-sigs/kueue/pull/7892

EDIT2: it will not work: https://github.com/kubernetes-sigs/kueue/pull/7892#issuecomment-3576899682

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-26T07:23:36Z

Ok, I think I know what is going on - livenessProbe kills the Pod after ~1min. 

Our configuration of the liveness prove is:
```yaml
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 8081
              scheme: HTTP
            initialDelaySeconds: 15
            periodSeconds: 20
            successThreshold: 1
            timeoutSeconds: 1
```
so iiuc  `initialDelaySeconds + periodSeconds` * `failureThreshold` gives around 55s of runtime, but probably there are some extra delays which make it around 1min.

In kubelet logs we see: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7859/pull-kueue-test-e2e-main-1-33/1993296869014376448/artifacts/run-test-e2e-singlecluster-1.33.4/kind-worker2/kubelet.log
```
Nov 25 12:43:55 kind-worker2 kubelet[230]: I1125 12:43:55.649262     230 kuberuntime_manager.go:1107] "Message for Container of pod" containerName="manager" containerStatusID={"Type":"containerd","ID":"eb41fdf666294105b7e9d89a58636eb24b98fd279116b94b0db26c9e979b1dc6"} pod="kueue-system/kueue-controller-manager-c674868fd-5mrvp" containerMessage="Container manager failed liveness probe, will be restarted"
```
and we see exactly 3 logs matching `"Probe failed" probeType="Liveness"`

Also, here we have both containers preserved: https://gcsweb.k8s.io/gcs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7859/pull-kueue-test-e2e-main-1-33/1993296869014376448/artifacts/run-test-e2e-singlecluster-1.33.4/kind-worker2/pods/kueue-system_kueue-controller-manager-c674868fd-5mrvp_dd1677d1-d00b-459c-8345-9db1c657f911/manager/ and we see that the new one was started 59s.

Solution ideas:

1. I think this issue is now more common as we introduced the bootstrap manager, because it does not register the health probe (checked by the liveness probe). So I think registering the health check in the bootstrap container should help. There will only be a small blip between the managers, but it will not fail the probe 3 times in a row.

2. use startupProbe which seems to be designed for similar cases of long startup, but I think this is a change to yaml which isn't really necessary. I think when the bootstrap manager is working the container is healthy, it is just not fully operational yet, but this is another probe - the readiness probe.

So I think (1.) is better.
