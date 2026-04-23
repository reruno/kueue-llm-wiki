# Issue #8911: [Flaky MultiKueue E2E] MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster [no image]

**Summary**: [Flaky MultiKueue E2E] MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster [no image]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8911

**Last updated**: 2026-02-13T08:52:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-30T12:43:46Z
- **Updated**: 2026-02-13T08:52:02Z
- **Closed**: 2026-02-13T08:52:02Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 18

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

End To End MultiKueue Suite: kindest/node:v1.34.3: [It] MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster 

```
{Timed out after 300.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/e2e.go:250 with:
Expected
    <string>: ReplicaSetUpdated
to equal
    <string>: NewReplicaSetAvailable failed [FAILED] Timed out after 300.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/e2e.go:250 with:
Expected
    <string>: ReplicaSetUpdated
to equal
    <string>: NewReplicaSetAvailable
In [BeforeAll] at: /home/prow/go/src/kubernetes-sigs/kueue/test/util/e2e.go:626 @ 01/30/26 11:33:40.885
}
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/2017192467891228672

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T14:45:55Z

I analyzed the logs a bit, first [kube scheduler logs](https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/2017192467891228672/artifacts/run-test-multikueue-e2e-1.34.3/kind-manager-control-plane/pods/kube-system_kube-scheduler-kind-manager-control-plane_3f477774c95bba5be6157bdcc9dadb3d/kube-scheduler/0.log) indicate the new Kueue replica was `kueue-controller-manager-8494d6795b-8vqfm`:

```
2026-01-30T11:28:40.04180459Z stderr F I0130 11:28:40.041115       1 eventhandlers.go:135] "Add event for unscheduled pod" pod="kueue-system/kueue-controller-manager-6665b5bd7c-cvczl"
2026-01-30T11:28:40.04182933Z stderr F I0130 11:28:40.041207       1 schedule_one.go:100] "Attempting to schedule pod" pod="kueue-system/kueue-controller-manager-6665b5bd7c-cvczl"
2026-01-30T11:28:40.04185292Z stderr F I0130 11:28:40.041504       1 default_binder.go:70] "Attempting to bind pod to node" pod="kueue-system/kueue-controller-manager-6665b5bd7c-cvczl" node="kind-manager-worker"
2026-01-30T11:28:40.046296387Z stderr F I0130 11:28:40.046113       1 eventhandlers.go:219] "Delete event for unscheduled pod" pod="kueue-system/kueue-controller-manager-6665b5bd7c-cvczl"
2026-01-30T11:28:40.046341957Z stderr F I0130 11:28:40.046113       1 eventhandlers.go:260] "Add event for scheduled pod" pod="kueue-system/kueue-controller-manager-6665b5bd7c-cvczl"
2026-01-30T11:28:40.049151627Z stderr F I0130 11:28:40.048900       1 schedule_one.go:346] "Successfully bound pod to node" pod="kueue-system/kueue-controller-manager-6665b5bd7c-cvczl" node="kind-manager-worker" evaluatedNodes=2 feasibleNodes=1
2026-01-30T11:28:40.397138634Z stderr F I0130 11:28:40.396937       1 httplog.go:134] "HTTP" verb="GET" URI="/readyz" latency="108.641µs" userAgent="kube-probe/1.34" audit-ID="" srcIP="127.0.0.1:44550" resp=200
2026-01-30T11:28:40.949574591Z stderr F I0130 11:28:40.949442       1 eventhandlers.go:135] "Add event for unscheduled pod" pod="kueue-system/kueue-controller-manager-8494d6795b-8vqfm"
2026-01-30T11:28:40.949607991Z stderr F I0130 11:28:40.949534       1 schedule_one.go:100] "Attempting to schedule pod" pod="kueue-system/kueue-controller-manager-8494d6795b-8vqfm"
2026-01-30T11:28:40.950135317Z stderr F I0130 11:28:40.949953       1 default_binder.go:70] "Attempting to bind pod to node" pod="kueue-system/kueue-controller-manager-8494d6795b-8vqfm" node="kind-manager-worker"
2026-01-30T11:28:40.954721095Z stderr F I0130 11:28:40.954482       1 schedule_one.go:346] "Successfully bound pod to node" pod="kueue-system/kueue-controller-manager-8494d6795b-8vqfm" node="kind-manager-worker" evaluatedNodes=2 feasibleNodes=1
2026-01-30T11:28:40.954760585Z stderr F I0130 11:28:40.954603       1 eventhandlers.go:219] "Delete event for unscheduled pod" pod="kueue-system/kueue-controller-manager-8494d6795b-8vqfm"
2026-01-30T11:28:40.954775716Z stderr F I0130 11:28:40.954641       1 eventhandlers.go:260] "Add event for scheduled pod" pod="kueue-system/kueue-controller-manager-8494d6795b-8vqfm"
```

but when I check the kubelet logs it reveals the replica never started:

```
Jan 30 11:28:54 kind-manager-worker kubelet[222]: E0130 11:28:54.293617     222 log.go:32] "PullImage from image service failed" err="rpc error: code = NotFound desc = failed to pull and unpack image \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": failed to resolve reference \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1: not found" image="us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1"
Jan 30 11:28:54 kind-manager-worker kubelet[222]: E0130 11:28:54.293688     222 kuberuntime_image.go:43] "Failed to pull image" err="rpc error: code = NotFound desc = failed to pull and unpack image \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": failed to resolve reference \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1: not found" image="us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1"
Jan 30 11:28:54 kind-manager-worker kubelet[222]: E0130 11:28:54.293808     222 kuberuntime_manager.go:1449] "Unhandled Error" err="init container secretreader-plugin-init start failed in pod kueue-controller-manager-8494d6795b-8vqfm_kueue-system(c8c87ab9-e13d-4ae4-8578-8092cce568ab): ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": failed to resolve reference \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1: not found" logger="UnhandledError"
Jan 30 11:28:54 kind-manager-worker kubelet[222]: E0130 11:28:54.293852     222 pod_workers.go:1324] "Error syncing pod, skipping" err="failed to \"StartContainer\" for \"secretreader-plugin-init\" with ErrImagePull: \"rpc error: code = NotFound desc = failed to pull and unpack image \\\"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\\\": failed to resolve reference \\\"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\\\": us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1: not found\"" pod="kueue-system/kueue-controller-manager-8494d6795b-8vqfm" podUID="c8c87ab9-e13d-4ae4-8578-8092cce568ab"
Jan 30 11:28:54 kind-manager-worker kubelet[222]: I0130 11:28:54.293920     222 event.go:389] "Event occurred" object="kueue-system/kueue-controller-manager-8494d6795b-8vqfm" fieldPath="spec.initContainers{secretreader-plugin-init}" kind="Pod" apiVersion="v1" type="Warning" reason="Failed" message="Failed to pull image \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": rpc error: code = NotFound desc = failed to pull and unpack image \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": failed to resolve reference \"us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1\": us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1: not found"
Jan 30 11:28:54 kind-manager-worker kubelet[222]: I0130 11:28:54.293976     222 event.go:389] "Event occurred" object="kueue-system/kueue-controller-manager-8494d6795b-8vqfm" fieldPath="spec.initContainers{secretreader-plugin-init}" kind="Pod" apiVersion="v1" type="Warning" reason="Failed" message="Error: ErrImagePull"
```
these images indicate there was a problem with the image, so I think we have two points:
1. I really think it would be useful to wait for the deployment ready before restarting Kueue, this could already early indicate the problems with the container image, making investigation easier. I was raising this before, see [here](https://github.com/kubernetes-sigs/kueue/issues/8850#issuecomment-3809859533) 
2. in any case, the question why the image `us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1` wasn't there (but I don't know why, maybe we didn't built it somehow?)

cc @mszadkow @mbobrovskyi any ideas here?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T14:47:38Z

/assign @mszadkow 
tentatively who already have all the context for building the plugin image
cc @kshalot who may also have some ideas here

### Comment by [@kshalot](https://github.com/kshalot) — 2026-01-30T16:45:09Z

> 2. in any case, the question why the image `us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1` wasn't there (but I don't know why, maybe we didn't built it somehow?)

If it wasn't built in the first place this wouldn't be working from the get go I guess.

@mimowo is there some "garbage collection" of the images in the staging registry? For example, I see that the kueue images only go as far as 03.11.2025, the kueueviz ones are from 26.10.2025. The Cluster Profile feature was developed around November, maybe the image was added there around that time, it became stale and was automatically removed?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:50:30Z

Thanks for looking into this. Surely we have GC of images in staging registry, after 90 days. However, I think this image is built on every CI build, and is not stored in the registry. You can see all images here:
http://us-central1-docker.pkg.dev/k8s-staging-images/kueue

<img width="1102" height="439" alt="Image" src="https://github.com/user-attachments/assets/dd3c59a2-d1c6-4256-8be0-67aa5b39336b" />

So, I think one of the two (a) somehow this image wasn't built on the CI run, (b) it was built on the CI run but not loaded to the Kind worker.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-30T16:50:44Z

Image was built:
```
#9 exporting layers 0.2s done
#9 writing image sha256:280009a357844ba21fa01241c598cb1977c5ae070469aee5bea2bc3394a04ef2 done
#9 naming to us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1 done
#9 DONE 0.2s
```
Image was loaded but only to workers, but we need it on manager:
```
Loading image 'us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1' to cluster 'kind-worker1'
  Loading image to node: kind-worker1-worker
Loading image 'us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin:0.0.1' to cluster 'kind-worker2'
  Loading image to node: kind-worker2-worker
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:52:54Z

Oh, interesting, could it be a race condition that we upload the image to all currently existing clusters, and the "manager" cluster wasn't provisioned at that time yet? This could explain the "flaky" nature.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-02T07:52:43Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2017955730673373184

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-02T15:14:15Z

Ok, actually the last failure was differenet:

```
  "level"=0 "msg"="Kueue configuration updated" "took"="25.551143234s"
  [38;5;9m[FAILED][0m in [BeforeEach] - /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1514 [38;5;243m@ 02/01/26 14:01:51.547[0m
  [1mSTEP:[0m reverting the configuration [38;5;243m@ 02/01/26 14:01:51.554[0m
  Exporting logs for cluster "kind-manager" to:
  /logs/artifacts/run-test-multikueue-e2e-1.34.0
  "level"=0 "msg"="Deployment status condition before the restart" "type"="Progressing" "status"="True" "reason"="NewReplicaSetAvailable"
  [1mSTEP:[0m Waiting for availability of deployment: "kueue-system/kueue-controller-manager" [38;5;243m@ 02/01/26 14:02:16.583[0m
  "level"=0 "msg"="Deployment is available in the cluster" "deployment"={"name"="kueue-controller-manager" "namespace"="kueue-system"} "waitingTime"="3.503811ms"
  [1mSTEP:[0m Waiting for deployment to have only available replicas: "kueue-system/kueue-controller-manager" [38;5;243m@ 02/01/26 14:02:16.587[0m
  "level"=0 "msg"="Deployment has only available replicas in the cluster" "deployment"={"name"="kueue-controller-manager" "namespace"="kueue-system"} "waitingTime"="3.618004ms"
  [1mSTEP:[0m Waiting for leader election lease "kueue-system/c1f6bfd2.kueue.x-k8s.io" [38;5;243m@ 02/01/26 14:02:16.59[0m
[38;5;9m• [FAILED] [54.942 seconds][0m
[0mMultiKueue [38;5;9m[1mwhen Connection via ClusterProfile no plugins [BeforeEach] [0muses ClusterProfile as way to connect worker cluster[0m
  [38;5;9m[BeforeEach][0m [38;5;243m/home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1512[0m
  [38;5;243m[It] /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1522[0m

  [38;5;9m[FAILED] Expected success, but got an error:
      <*errors.StatusError | 0xc0009855e0>: 
      conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
      {
          ErrStatus: {
              TypeMeta: {Kind: "", APIVersion: ""},
              ListMeta: {
                  SelfLink: "",
                  ResourceVersion: "",
                  Continue: "",
                  RemainingItemCount: nil,
              },
              Status: "Failure",
              Message: "conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
              Reason: "",
              Details: nil,
              Code: 500,
          },
      }[0m
  [38;5;9mIn [1m[BeforeEach][0m[38;5;9m at: [1m/home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1514[0m [38;5;243m@ 02/01/26 14:01:51.547[0m
```
let me create a separete ticket, because I think the root cause is different here, because the image was clearly loaded to all kind workers.

EDIT: extracted this failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2017955730673373184
to the issue: https://github.com/kubernetes-sigs/kueue/issues/8937

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-02T15:16:18Z

/retitle [Flaky MultiKueue E2E] MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster [no image]

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-02-09T12:52:56Z

Seems that none of the base images were loaded onto `kind-manager` cluster.
First one to loaded was `appwrapper` - agnhost, kueue, secretereader-plugin were skipped.
```
Switched to context "kind-kind-manager".
Switched to context "kind-kind-worker1".
Switched to context "kind-kind-worker2".
Loading image 'quay.io/ibm/appwrapper:v1.1.2' to cluster 'kind-manager'
  Loading image to node: kind-manager-worker
Loading image 'registry.k8s.io/e2e-test-images/agnhost:2.52' to cluster 'kind-worker1'
  Loading image to node: kind-worker1-worker
Loading image 'registry.k8s.io/e2e-test-images/agnhost:2.52' to cluster 'kind-worker2'
  Loading image to node: kind-worker2-worker
```

We don't actually wait for all of the nodes to be ready, we wait for 1 minute for control-plane node.
We log node and pod information, but we do not check their readiness or return an error if they are not ready.
`"$ARTIFACTS/$1-nodes.log"` for each cluster reports, control-plane `Ready` but worker `NotReady`.

Also none of the checks in `cluster_create` actually prevents to go further if something is lagging behind.
We could add something like: `wait_for_kind_cluster_ready` before leaving `cluster_create`.

Wdyt? @mimowo @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T13:08:40Z

> We don't actually wait for all of the nodes to be ready, we wait for 1 minute for control-plane node.

Indeed, this seems like source of the problem. Instead we should wait for "all clusters" to be provisioned, say for 5min.

> Also none of the checks in cluster_create actually prevents to go further if something is lagging behind.
We could add something like: wait_for_kind_cluster_ready before leaving cluster_create.

This sounds reasonable. We should wait for the clusters to be provisioned before starting to load images, because otherwise we may skip some (as it happened). The only thing to be careful about is performance, to avoid sequential cluster_create -> cluster_create -> wait. Ideally we would trigger cluster creation in parallel, then wait for them all. Unless parallel cluster creation is not supported by Kind (I don't know).

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-02-09T18:16:48Z

Also @mbobrovskyi has good point, why only one test failed and not the others.

I suspect that like @mimowo showed in `http://us-central1-docker.pkg.dev/k8s-staging-images/kueue` 
the only missing image in the registry is `secretreader-plugin`.
Only `secretreader-plugin` is loaded locally and if we skipped `cluster_kind_load` step the other images can be loaded from registry, but not this one - the same for agnhost.

Maybe let's push the image to the registry too?
wdyt @mimowo @mbobrovskyi ?

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-09T18:53:22Z

I feel that being able to pull the image from a registry introduces a bit of unpredictability to the process. Also I don't think the image is in the registry for presubmits in PRs, which run e2e tests as well.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T18:54:54Z

> Maybe let's push the image to the registry too?

Maybe, but I wouldn't couple it to this bugfix. 

Waiting for the provisioning of Kind clusters before loading or building images is something we should do regardless of where the images are taken from (pulled or built).

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-09T19:15:28Z

To be honest it's very strange:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/2017192467891228672#1:build-log.txt%3A1263-1266

We are loading only to worker nodes. But couple lines before we are loading agnhost for manager as well:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/2017192467891228672#1:build-log.txt%3A1215-1220

I think the problem with this line:

https://github.com/kubernetes-sigs/kueue/blob/d6d2f92e1814371d498a9b71c847995f6b4bdbcc/hack/e2e-common.sh#L428

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-09T19:48:38Z

> We are loading only to worker nodes. But couple lines before we are loading agnhost for manager as well:
> https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/2017192467891228672#1:build-log.txt%3A1215-1220

In the link you sent it's not the agnhost image being loaded to manager but the jobset one, they just aligned perfectly.

None of those were loaded to the manager:
* registry.k8s.io/e2e-test-images/agnhost:2.52
* registry.k8s.io/e2e-test-images/agnhost:2.62
* us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue
* us-central1-docker.pkg.dev/k8s-staging-images/kueue/secretreader-plugin

which suggests this https://github.com/kubernetes-sigs/kueue/pull/9067 is a potential fix, no?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-09T20:00:36Z

> In the link you sent it's not the agnhost image being loaded to manager but the jobset one, they just aligned perfectly.

Ah you right. Thanks for catching.

> which suggests this https://github.com/kubernetes-sigs/kueue/pull/9067 is a potential fix, no?

Unfortunately, no. https://github.com/kubernetes-sigs/kueue/pull/9067 only removes a redundant wrapper, and I don’t think that’s the source of the problem.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-09T20:02:48Z

> Also none of the checks in cluster_create actually prevents to go further if something is lagging behind.
We could add something like: wait_for_kind_cluster_ready before leaving cluster_create.

In that case, @mszadkow, I think you’re right – we need to wait for the nodes. This should probably help:

```bash
kubectl wait --for=condition=Ready node \  
--selector='!node-role.kubernetes.io/control-plane' \  
--timeout=300s
```
