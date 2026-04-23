# Issue #4495: Flaky test: TopologyAwareScheduling for AppWrapper when Creating an AppWrapper Should place pods

**Summary**: Flaky test: TopologyAwareScheduling for AppWrapper when Creating an AppWrapper Should place pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4495

**Last updated**: 2025-03-05T20:37:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-05T08:26:24Z
- **Updated**: 2025-03-05T20:37:11Z
- **Closed**: 2025-03-05T20:15:47Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@dgrove-oss](https://github.com/dgrove-oss), [@mimowo](https://github.com/mimowo)
- **Comments**: 17

## Description

/kind flake 

**What happened**:

The test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4493/pull-kueue-test-e2e-tas-main/1897195533643026432

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

run ci

**Anything else we need to know?**:

```
End To End TAS Suite: kindest/node:v1.31.1: [It] TopologyAwareScheduling for AppWrapper when Creating an AppWrapper Should place pods expand_less	47s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/appwrapper_test.go:129 with:
Expected
    <[]v1.Pod | len:5, cap:8>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "job-0-2tk5q",
                GenerateName: "job-0-",
                Namespace: "e2e-tas-aw-dnz4h",
                SelfLink: "",
                UID: "7e5b1126-3a4b-4310-9637-41e061a0de48",
                ResourceVersion: "5578",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-05T08:20:44Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "job-name": "job-0",
                    "kueue.x-k8s.io/podset": "appwrapper-0",
                    "kueue.x-k8s.io/tas": "true",
                    "workload.codeflare.dev/appwrapper": "appwrapper",
                    "batch.kubernetes.io/controller-uid": "0e203b4a-8c6d-4507-8e61-0f991d37493e",
                    "batch.kubernetes.io/job-name": "job-0",
                    "controller-uid": "0e203b4a-8c6d-4507-8e61-0f991d37493e",
                },
                Annotations: {
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-rack",
                    "kueue.x-k8s.io/workload": "appwrapper-appwrapper-5f337",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "job-0",
                        UID: "0e203b4a-8c6d-4507-8e61-0f991d37493e",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-05T08:20:44Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:batch.kubernetes.io/controller-uid\":{},\"f:batch.kubernetes.io/job-name\":{},\"f:controller-uid\":{},\"f:job-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:workload.codeflare.dev/appwrapper\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0e203b4a-8c6d-4507-8e61-0f991d37493e\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{},\"f:example.com/gpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{},\"f:example.com/gpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-05T08:20:45Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:spec\":{\"f:nodeSelector\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time:...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 4 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/appwrapper_test.go:129 with:
Expected
    <[]v1.Pod | len:5, cap:8>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "job-0-2tk5q",
                GenerateName: "job-0-",
                Namespace: "e2e-tas-aw-dnz4h",
                SelfLink: "",
                UID: "7e5b1126-3a4b-4310-9637-41e061a0de48",
                ResourceVersion: "5578",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-03-05T08:20:44Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "job-name": "job-0",
                    "kueue.x-k8s.io/podset": "appwrapper-0",
                    "kueue.x-k8s.io/tas": "true",
                    "workload.codeflare.dev/appwrapper": "appwrapper",
                    "batch.kubernetes.io/controller-uid": "0e203b4a-8c6d-4507-8e61-0f991d37493e",
                    "batch.kubernetes.io/job-name": "job-0",
                    "controller-uid": "0e203b4a-8c6d-4507-8e61-0f991d37493e",
                },
                Annotations: {
                    "kueue.x-k8s.io/podset-preferred-topology": "cloud.provider.com/topology-rack",
                    "kueue.x-k8s.io/workload": "appwrapper-appwrapper-5f337",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "job-0",
                        UID: "0e203b4a-8c6d-4507-8e61-0f991d37493e",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-05T08:20:44Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/podset-preferred-topology\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:batch.kubernetes.io/controller-uid\":{},\"f:batch.kubernetes.io/job-name\":{},\"f:controller-uid\":{},\"f:job-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/tas\":{},\"f:workload.codeflare.dev/appwrapper\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0e203b4a-8c6d-4507-8e61-0f991d37493e\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{},\"f:example.com/gpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{},\"f:example.com/gpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-03-05T08:20:45Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:spec\":{\"f:nodeSelector\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time:...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 4
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/appwrapper_test.go:130 @ 03/05/25 08:21:29.909
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T08:26:48Z

cc @dgrove-oss  @nasedil @mbobrovskyi

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-05T14:49:43Z

interesting... the pod list has an extra element (length 5).  Wonder how that happened. It must have had length 4 just above (line 120) to have gotten to the test at line 129 that failed with a persistent length of 5.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T15:26:37Z

Actually, looking the kube-controller-manager logs: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4493/pull-kueue-test-e2e-tas-main/1897195533643026432/artifacts/run-test-tas-e2e-1.31.1/kind-control-plane/pods/kube-system_kube-controller-manager-kind-control-plane_dda87b33b5146c881a881b2a944d8a25/kube-controller-manager/0.log we see indeed 5 pods were created:
```
> cat test.log | grep e2e-tas-aw-dnz4h/job-0 | grep Create
2025-03-05T08:20:44.740465757Z stderr F I0305 08:20:44.740247       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-tas-aw-dnz4h/job-0" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="SuccessfulCreate" message="Created pod: job-0-w69nw"
2025-03-05T08:20:44.751351856Z stderr F I0305 08:20:44.751203       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-tas-aw-dnz4h/job-0" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="SuccessfulCreate" message="Created pod: job-0-2tk5q"
2025-03-05T08:20:44.753437166Z stderr F I0305 08:20:44.753249       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-tas-aw-dnz4h/job-0" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="SuccessfulCreate" message="Created pod: job-0-pvmf9"
2025-03-05T08:20:44.761712587Z stderr F I0305 08:20:44.761607       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-tas-aw-dnz4h/job-0" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="SuccessfulCreate" message="Created pod: job-0-5sx9c"
2025-03-05T08:20:58.009740771Z stderr F I0305 08:20:58.009648       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-tas-aw-dnz4h/job-0" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="SuccessfulCreate" message="Created pod: job-0-7fxns"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T15:29:27Z

Interestingly:
- the last pod was created 14s later than the first 4
- there is a potentially related bug in k/k https://github.com/kubernetes/kubernetes/issues/130103 which could result in Job controller racing and creating more pods than needed, however in this case Job controller would have planty of time before creating the 5th

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T15:31:08Z

I suppose we could chase it down based on the pod names and looking into kubelet logs. Maybe one of the pods failed for a weird reason and was replaced. In that case we could just filter only "Running" pods in the function.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-05T16:23:41Z

I don't often get to the level of looking at [kubelet logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4493/pull-kueue-test-e2e-tas-main/1897195533643026432/artifacts/run-test-tas-e2e-1.31.1/kind-worker/kubelet.log), but it seems like the pod `job-0-pvmf9` did fail.

```
Mar 05 08:21:25 kind-worker kubelet[251]: I0305 08:21:25.575391     251 status_manager.go:881] "Status for pod updated successfully" pod="e2e-tas-aw-dnz4h/job-0-pvmf9" statusVersion=2 status={"phase":"Pending","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-05T08:21:25Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-05T08:21:22Z"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-05T08:21:22Z","reason":"PodFailed"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-05T08:21:22Z","reason":"PodFailed"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-05T08:21:22Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.3.12","podIPs":[{"ip":"10.244.3.12"}],"startTime":"2025-03-05T08:21:22Z","containerStatuses":[{"name":"c","state":{"terminated":{"exitCode":1,"reason":"Error","startedAt":"2025-03-05T08:21:24Z","finishedAt":"2025-03-05T08:21:25Z","containerID":"containerd://078cc68cbd959c37217c7aef36cfb6a0d7886003b2f8635f4121dca09f1e0bbc"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-05@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://078cc68cbd959c37217c7aef36cfb6a0d7886003b2f8635f4121dca09f1e0bbc","started":false,"volumeMounts":
```

Although those timestamps of `8:21:25` are after the `8:20:58` of the job-controller-logs...a bit off.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T16:27:34Z

But this is interesting because the Pod was still pending so it didn't event had a chance to start( it transitioned directly Pending - Failed). Wondering if maybe it was deleted by some actor. Does Appswrapper under some circumstances delete pods directly?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T16:31:01Z

But this is interesting because the Pod was still pending so it didn't event had a chce to start. Wondering if maybe it was deleted by some actor. Does Appswrapper under some circumstances delete pods directly?

Edit actually the log line tyou posted is 1min later so at this point maybe it was deleted just by the test code.

I think likely the reason to create the 5th pod was indeed that one of the pods was deleted, but this particular one seems was killed after the 5th pod was created.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-05T16:33:57Z

> But this is interesting because the Pod was still pending so it didn't event had a chance to start( it transitioned directly Pending - Failed). Wondering if maybe it was deleted by some actor. Does Appswrapper under some circumstances delete pods directly?

Yes.  This is part of the fault tolerance AppWrapper does.  It monitors the pods created by the jobs it is wrapping and if they haven't been scheduled within a "reasonable" time, it interprets that as a job failure, deletes the wrapped resource, waits a bit, and then tries again (recreates the wrapped resource).   The default threshold for pods to be scheduled is 60 seconds, since we are normally expecting that if Kueue admits an AppWrapper then the Pods should be scheduled by Kubernetes relatively quickly.   It can be set to a higher value via an annotation on the appwrapper.   Let me go look at the AppWrapper logs and see if I can see evidence of this happening.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-05T16:45:48Z

That doesn't appear to be happening.
```
(base) dgrove@Dave's IBM Mac appwrapper % grep e2e-tas-aw-dnz4h ~/Desktop/log.txt 
2025-03-05T08:20:44.625607661Z stderr F 2025-03-05T08:20:44.625365558Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Applying defaults	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "kubernetes-admin", "requestID": "cb8b4346-35a6-4216-82c0-a50f8f3a08c8", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper"}}
2025-03-05T08:20:44.639443543Z stderr F 2025-03-05T08:20:44.63922572Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Validating create	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "kubernetes-admin", "requestID": "88ea40d9-3364-47fa-82f8-e3d4fbf1d37c", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper"}}
2025-03-05T08:20:44.65432483Z stderr F 2025-03-05T08:20:44.654120567Z	INFO	logr@v1.4.2/logr.go:280	Suspended	{"controller": "AppWrapper", "controllerGroup": "workload.codeflare.dev", "controllerKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "reconcileID": "9a9d1ea2-177e-476a-a89d-e24f92abd5c2", "phase": "Suspended"}
2025-03-05T08:20:44.682691394Z stderr F 2025-03-05T08:20:44.68246515Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Validating update	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "868264c9-02d6-41e5-be3d-30ae3a33b860", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper"}}
2025-03-05T08:20:44.690725541Z stderr F 2025-03-05T08:20:44.690527888Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Validating update	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "system:serviceaccount:appwrapper-system:appwrapper-controller-manager", "requestID": "3c9b9d79-b4e4-4f5d-b921-df5a03b4c601", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper"}}
2025-03-05T08:20:44.694559437Z stderr F 2025-03-05T08:20:44.694356754Z	INFO	logr@v1.4.2/logr.go:280	Finalizer Added	{"controller": "AppWrapper", "controllerGroup": "workload.codeflare.dev", "controllerKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "reconcileID": "45b20924-5c6e-4d17-ab1d-a0ca40bc943f"}
2025-03-05T08:20:44.702838268Z stderr F 2025-03-05T08:20:44.702615594Z	INFO	logr@v1.4.2/logr.go:280	Resuming	{"controller": "AppWrapper", "controllerGroup": "workload.codeflare.dev", "controllerKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "reconcileID": "45b20924-5c6e-4d17-ab1d-a0ca40bc943f", "phase": "Resuming"}
2025-03-05T08:20:44.711691727Z stderr F 2025-03-05T08:20:44.711496664Z	INFO	logr@v1.4.2/logr.go:280	Resuming	{"controller": "AppWrapper", "controllerGroup": "workload.codeflare.dev", "controllerKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "reconcileID": "c0c3d39f-538f-4bfc-beb6-274578fe6abf", "phase": "Resuming"}
2025-03-05T08:20:44.711988152Z stderr F 2025-03-05T08:20:44.711842649Z	INFO	logr@v1.4.2/logr.go:280	After injection	{"controller": "AppWrapper", "controllerGroup": "workload.codeflare.dev", "controllerKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "reconcileID": "5fb791ee-b5e0-4038-8d7d-225633486b8b", "obj": {"apiVersion": "batch/v1", "kind": "Job", "namespace": "e2e-tas-aw-dnz4h", "name": "job-0"}}
2025-03-05T08:20:44.748163559Z stderr F 2025-03-05T08:20:44.747950746Z	INFO	logr@v1.4.2/logr.go:280	Running	{"controller": "AppWrapper", "controllerGroup": "workload.codeflare.dev", "controllerKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "reconcileID": "5fb791ee-b5e0-4038-8d7d-225633486b8b", "phase": "Running"}
2025-03-05T08:20:44.758977477Z stderr F 2025-03-05T08:20:44.758782845Z	INFO	logr@v1.4.2/logr.go:280	Running	{"controller": "AppWrapper", "controllerGroup": "workload.codeflare.dev", "controllerKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "reconcileID": "1e551734-c8c0-49e0-8670-468eaa83d828", "phase": "Running"}
2025-03-05T08:21:34.989769177Z stderr F 2025-03-05T08:21:34.989562124Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Validating update	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "system:serviceaccount:appwrapper-system:appwrapper-controller-manager", "requestID": "c14934ca-0fcb-49bf-a5c9-2aebb4d929b9", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper"}}
2025-03-05T08:21:34.996033368Z stderr F 2025-03-05T08:21:34.995825955Z	INFO	logr@v1.4.2/logr.go:280	Finalizer Deleted	{"controller": "AppWrapper", "controllerGroup": "workload.codeflare.dev", "controllerKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"e2e-tas-aw-dnz4h"}, "namespace": "e2e-tas-aw-dnz4h", "name": "appwrapper", "reconcileID": "0f46103a-5cb9-48bf-8705-560453700e35"}
```

We would have emitted a log message with `phase` being `Suspending`.  The AppWrapper is in the `Running` phase until it is externally deleted.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T18:11:39Z

Ok, I see in kubelet logs on [kind-worker4](https://gcsweb.k8s.io/gcs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4493/pull-kueue-test-e2e-tas-main/1897195533643026432/artifacts/run-test-tas-e2e-1.31.1/kind-worker4/kubelet.log) that `e2e-tas-aw-dnz4h/job-0-2tk5q` failed, and it was running for a while:
08:20:47: (we have: phase: Running)
```
Mar 05 08:20:47 kind-worker4 kubelet[251]: I0305 08:20:47.823823     251 status_manager.go:872] "Patch status for pod" pod="e2e-tas-aw-dnz4h/job-0-2tk5q" podUID="7e5b1126-3a4b-4310-9637-41e061a0de48" patch="{\"metadata\":{\"uid\":\"7e5b1126-3a4b-4310-9637-41e061a0de48\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-05T08:20:47Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-05T08:20:47Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-05T08:20:47Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-05@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-05T08:20:47Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-wd5sl\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Running\",\"podIP\":\"10.244.9.4\",\"podIPs\":[{\"ip\":\"10.244.9.4\"}]}}"
```
then 05 08:20:50 (we have phase Failed)
```
Mar 05 08:20:50 kind-worker4 kubelet[251]: I0305 08:20:50.833389     251 status_manager.go:872] "Patch status for pod" pod="e2e-tas-aw-dnz4h/job-0-2tk5q" podUID="7e5b1126-3a4b-4310-9637-41e061a0de48" patch="{\"metadata\":{\"uid\":\"7e5b1126-3a4b-4310-9637-41e061a0de48\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-05T08:20:50Z\",\"reason\":\"PodFailed\",\"status\":\"False\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-05T08:20:50Z\",\"reason\":\"PodFailed\",\"status\":\"False\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-05@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"terminated\":{\"containerID\":\"containerd://8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003\",\"exitCode\":1,\"finishedAt\":\"2025-03-05T08:20:48Z\",\"reason\":\"Error\",\"startedAt\":\"2025-03-05T08:20:47Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-wd5sl\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}]}}"
```
So, this is why the Pod was replaced by the Job controller. 

Also, I looked at the [apiserver](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4493/pull-kueue-test-e2e-tas-main/1897195533643026432/artifacts/run-test-tas-e2e-1.31.1/kind-control-plane/pods/kube-system_kube-apiserver-kind-control-plane_7a0b404ba4be154f06e448d4823ad91f/kube-apiserver/0.log) logs, but there the first DELETE request was much later:

```
2025-03-05T08:21:29.984070766Z stderr F I0305 08:21:29.983705       1 httplog.go:134] "HTTP" verb="DELETE" URI="/api/v1/namespaces/e2e-tas-aw-dnz4h/pods/job-0-5sx9c" latency="9.367417ms" userAgent="kube-controller-manager/v1.31.1 (linux/amd64) kubernetes/948afe5/system:serviceaccount:kube-system:generic-garbage-collector" audit-ID="2940ed40-58bd-4ded-9e35-135479223a9d" srcIP="172.18.0.7:55792" apf_pl="workload-high" apf_fs="kube-system-service-accounts" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="9.146854ms" resp=200
```
so, indeed it was not deleted. The options I see:
1. some very rare one off failure on node (say containerd or kubelet failed)
2. some bug in the new agnhost image which makes it occasionally fail
3. some actor sent the request /exit 1 to agnhost for this pod (we have WaitForActivePodsAndTerminate which does exactly that but it is never called from TAS suite)

So, my thinking is  1. or 2., but in any case it seems we could just make the test a little more robust by only including Running pods.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T18:39:35Z

A bit closer look at kubelet logs we see "ContainerDied":

```
Mar 05 08:20:50 kind-worker4 kubelet[251]: I0305 08:20:50.817858     251 kubelet.go:2439] "SyncLoop (PLEG): event for pod" pod="e2e-tas-aw-dnz4h/job-0-2tk5q" event={"ID":"7e5b1126-3a4b-4310-9637-41e061a0de48","Type":"ContainerDied","Data":"8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003"}
```
and in containerd for the containerd logs we have:

```
Mar 05 08:20:46 kind-worker4 containerd[111]: time="2025-03-05T08:20:46.895858068Z" level=info msg="CreateContainer within sandbox \"ba940fd855209b88f186482477936602ceaa7934e8fb9e06547431245577c824\" for &ContainerMetadata{Name:c,Attempt:0,} returns container id \"8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003\""
Mar 05 08:20:46 kind-worker4 containerd[111]: time="2025-03-05T08:20:46.899075784Z" level=info msg="StartContainer for \"8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003\""
Mar 05 08:20:47 kind-worker4 containerd[111]: time="2025-03-05T08:20:47.740297059Z" level=info msg="StartContainer for \"8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003\" returns successfully"
Mar 05 08:20:50 kind-worker4 containerd[111]: time="2025-03-05T08:20:50.178097410Z" level=info msg="shim disconnected" id=8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003 namespace=k8s.io
Mar 05 08:20:50 kind-worker4 containerd[111]: time="2025-03-05T08:20:50.178169251Z" level=warning msg="cleaning up after shim disconnected" id=8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003 namespace=k8s.io
Mar 05 08:20:51 kind-worker4 containerd[111]: time="2025-03-05T08:20:51.820209660Z" level=info msg="Container to stop \"8beba762608ec152577132272e271c0508aa0fc09bc8b0dd238610b2a0ddf003\" must be in running or unknown state, current state \"CONTAINER_EXITED\"
```
seeing CONTAINER_EXITED, and we know exit code is 1, so this is unlikely OOM (it would rather be 137). So, it seems some sort of a crash of the agnhost.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T18:42:25Z

haha, ok got it looking at the container logs: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4493/pull-kueue-test-e2e-tas-main/1897195533643026432/artifacts/run-test-tas-e2e-1.31.1/kind-worker4/pods/e2e-tas-aw-dnz4h_job-0-2tk5q_7e5b1126-3a4b-4310-9637-41e061a0de48/c/0.log
```
2025-03-05T08:20:48.123301648Z stderr F Error: unknown command "60s" for "app" 
```
We need to use the `Image(util.E2eTestAgnHostImage, util.BehaviorWaitForDeletion).` instead.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-05T18:45:00Z

Bad merge/rebase 🤦‍♂   I think the PR adding this test was closely overlapping with the PR to switch testing images.  We got the image switch, but missed changing the argument.   Nice investigation!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-05T19:32:18Z

@dgrove-oss @mimowo As I checked entire Kueue E2E, this case is only place using incorrect command in `Image()`.
Could you open fix PR?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-05T19:44:23Z

I will do one.  Thanks to @mimowo for finding the bug!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-05T20:37:08Z

/assign @mimowo @dgrove-oss
