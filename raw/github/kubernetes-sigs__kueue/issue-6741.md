# Issue #6741: [flaky test]  LeaderWorkerSet integration when LeaderWorkerSet created should allow to update the PodTemplate in LeaderWorkerSet

**Summary**: [flaky test]  LeaderWorkerSet integration when LeaderWorkerSet created should allow to update the PodTemplate in LeaderWorkerSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6741

**Last updated**: 2025-10-01T06:58:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-08T08:44:25Z
- **Updated**: 2025-10-01T06:58:27Z
- **Closed**: 2025-10-01T06:58:27Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

/kind flake 


**What happened**:

failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-12-1-32/1964230525405106176

on nightly build

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:633 with:
Expected
    <[]v1.Pod | len:4, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0",
                GenerateName: "lws-",
                Namespace: "lws-e2e-hg5gr",
                SelfLink: "",
                UID: "533b8817-f5a6-4792-a492-3db66a3fd758",
                ResourceVersion: "6249",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-09-06T07:47:48Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "apps.kubernetes.io/pod-index": "0",
                    "controller-revision-hash": "lws-cc779d4f",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-fd0f7",
                    "kueue.x-k8s.io/podset": "leader",
                    "kueue.x-k8s.io/queue-name": "lws-lq",
                    "leaderworkerset.sigs.k8s.io/group-key": "ec750e5ee4a474d50948dae1d5d155cdb29f951a",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-fd0f7",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "5bbd7574c4",
                    "statefulset.kubernetes.io/pod-name": "lws-0",
                },
                Annotations: {
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "leader",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-fd0f7",
                    "leaderworkerset.sigs.k8s.io/size": "3",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "941e87ef-999e-42c7-8e04-4cab7f5fbbd3",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: [
                    "kueue.x-k8s.io/managed",
                ],
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-09-06T07:47:48Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"941e87ef-999e-42c7-8e04-4cab7f5fbbd3\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomain\":{},\"f:terminationGracePeriodSeconds\":{}}}",
           ...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 6 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:633 with:
Expected
    <[]v1.Pod | len:4, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0",
                GenerateName: "lws-",
                Namespace: "lws-e2e-hg5gr",
                SelfLink: "",
                UID: "533b8817-f5a6-4792-a492-3db66a3fd758",
                ResourceVersion: "6249",
                Generation: 0,
                CreationTimestamp: {
                    Time: 2025-09-06T07:47:48Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "apps.kubernetes.io/pod-index": "0",
                    "controller-revision-hash": "lws-cc779d4f",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-fd0f7",
                    "kueue.x-k8s.io/podset": "leader",
                    "kueue.x-k8s.io/queue-name": "lws-lq",
                    "leaderworkerset.sigs.k8s.io/group-key": "ec750e5ee4a474d50948dae1d5d155cdb29f951a",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-fd0f7",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "5bbd7574c4",
                    "statefulset.kubernetes.io/pod-name": "lws-0",
                },
                Annotations: {
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "leader",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-fd0f7",
                    "leaderworkerset.sigs.k8s.io/size": "3",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "941e87ef-999e-42c7-8e04-4cab7f5fbbd3",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: [
                    "kueue.x-k8s.io/managed",
                ],
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2025-09-06T07:47:48Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"941e87ef-999e-42c7-8e04-4cab7f5fbbd3\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomain\":{},\"f:terminationGracePeriodSeconds\":{}}}",
           ...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 6
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:637 @ 09/06/25 07:48:28.305
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T08:02:35Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-13-1-32/1970899986707124224

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-09-30T08:07:12Z

I ran over 100 executions with each of Kueue 0.12 and 0.13 on Kubernetes 1.32, reducing cluster resources to 4 CPUs and 8 GiB memory, but haven’t been able to reproduce the issue locally so far. 

Could this be related to an infrastructure issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T08:12:30Z

Maybe this is because the machines were loaded. Can you check the logs to see if the LWS was scaled eventually (maybe after the timeout?). In that case we could update the timeout I think. 6 pods in LWS is much as for e2e tests.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-09-30T16:56:19Z

Based on the logs for Kueue v0.12, it looks like the Pods were eventually created. Here's a summary of the timeline:

**TIMEOUT at 07:48:28.305**

Before the timeout, we can see multiple logs showing Pod creation and recreation after updating the template. The logs include entries like:
```
2025-09-06T07:47:41.046978217Z stderr F 2025-09-06T07:47:41Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "c51f9ab7-74e5-472e-9cfe-acb9c7a8935b"}
2025-09-06T07:47:41.068079051Z stderr F 2025-09-06T07:47:41Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "dc5c6cc9-bc8d-4266-a6f8-0bd41b11d1cc"}
2025-09-06T07:47:41.070205351Z stderr F 2025-09-06T07:47:41Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-2","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-2", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "b3e6ea84-9b39-48f8-aa16-6eda19c05703"}
2025-09-06T07:47:41.071872298Z stderr F 2025-09-06T07:47:41Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "342399bf-5907-4561-ad6b-aad1b72cda02"}
2025-09-06T07:47:41.096066262Z stderr F 2025-09-06T07:47:41Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-2","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-2", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "3de1c009-2c85-456e-9a3a-c82a7e6a8a98"}
2025-09-06T07:47:41.188357169Z stderr F 2025-09-06T07:47:41Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "7e8d3de1-eb47-4abf-b635-9725cb0033e5"}
2025-09-06T07:47:47.533030587Z stderr F 2025-09-06T07:47:47Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1-2","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1-2", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "7d345bcf-8b87-4303-a413-aa714217c770"}
2025-09-06T07:47:47.54987249Z stderr F 2025-09-06T07:47:47Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1-2","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1-2", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "b573234d-f94b-4bc0-b4b5-f2079ac214a2"}
2025-09-06T07:47:47.56733822Z stderr F 2025-09-06T07:47:47Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "fb14b408-24f2-4150-9c67-3ed36d53567a"}
2025-09-06T07:47:47.607673491Z stderr F 2025-09-06T07:47:47Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1-2","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1-2", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "1ef94557-3ff7-4629-8738-ba3f7205e842"}
2025-09-06T07:47:48.097498004Z stderr F 2025-09-06T07:47:48Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "844585ad-1ec3-4a45-a253-5c032672139b"}
2025-09-06T07:47:48.426301194Z stderr F 2025-09-06T07:47:48Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "08d74a29-c71c-466c-9ef1-eccaba1acd3d"}
2025-09-06T07:47:48.45568016Z stderr F 2025-09-06T07:47:48Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "a656ba3e-02a1-4373-b6c1-a4dc197a49d3"}
2025-09-06T07:47:48.475432582Z stderr F 2025-09-06T07:47:48Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "73029c20-0cf3-4dcc-9aa9-e077e1fc11eb"}
2025-09-06T07:47:48.478549212Z stderr F 2025-09-06T07:47:48Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "2f522cb2-3676-4086-b037-5b0e36052eae"}
...
2025-09-06T07:47:48.850773794Z stderr F 2025-09-06T07:47:48Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "8e7983c0-5b64-48e6-a4c1-f13930e00615"}
2025-09-06T07:47:48.921029316Z stderr F 2025-09-06T07:47:48Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-2","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-2", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "58627448-6870-4294-bdc4-f1872d7f8816"}
2025-09-06T07:47:49.041656376Z stderr F 2025-09-06T07:47:49Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "a3dee753-f4a1-4a97-b527-b42448b9c93e"}
...
2025-09-06T07:48:09.11829124Z stderr F 2025-09-06T07:48:09Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "c81721c9-3c81-4525-8158-b053a74c2ae8"}
```

However, until `2025-09-06T07:48:09` (just before the timeout), the logs show activity for only 5 of the 6 expected Pods:
`lws-0`, `lws-0-2`, `lws-1-1`, `lws-1-2`, and `lws-0-1`. The missing Pod at this point is `lws-1`.


There are also several repeated log entries for `lws-0-1` before the timeout, which suggests that this Pod might still have been in the process of being recreated at that time. This could explain why the error message shows only 4 out of 6 Pods as ready when the timeout occurred.
```
2025-09-06T07:48:09.11829124Z stderr F 2025-09-06T07:48:09Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:statefulset-controller", "requestID": "c81721c9-3c81-4525-8158-b053a74c2ae8"}
```


Later, **after the timeout**, the missing Pod (`lws-1`) does appear in the logs:
```
2025-09-06T07:48:28.455341258Z stderr F 2025-09-06T07:48:28Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-0","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-0", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "kubernetes-admin", "requestID": "14d45865-8105-468d-b4ec-9fdfa4834f11"}
2025-09-06T07:48:28.468730088Z stderr F 2025-09-06T07:48:28Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "kubernetes-admin", "requestID": "151256ce-9e97-4767-96b6-64082ce9a567"}
2025-09-06T07:48:28.488910034Z stderr F 2025-09-06T07:48:28Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1-1","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1-1", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "kubernetes-admin", "requestID": "61aad54d-36ed-4c3b-a9f7-366774915c50"}
2025-09-06T07:48:28.507956948Z stderr F 2025-09-06T07:48:28Z	LEVEL(-2)	admission	Defaulting Pod	{"webhookGroup": "", "webhookKind": "Pod", "Pod": {"name":"lws-1-2","namespace":"lws-e2e-hg5gr"}, "namespace": "lws-e2e-hg5gr", "name": "lws-1-2", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "kubernetes-admin", "requestID": "f277509a-07c0-41a0-a557-5dd34fbc6df6"}
```

This suggests that the issue might be related to timing, possibly due to an overloaded machine or some other infrastructure issue, where some Pods were still in the process of being recreated or initialized when the timeout was reached.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T17:06:30Z

Thank you, in that case I suggest to just bump the timeout.
