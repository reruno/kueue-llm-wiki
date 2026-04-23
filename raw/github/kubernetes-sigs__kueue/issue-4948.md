# Issue #4948: Flaky Test: Provisioning when A workload is using a provision admission check Should ignore the change if Workload is Admitted and the ProvisioningRequest's condition is set to BookingExpired

**Summary**: Flaky Test: Provisioning when A workload is using a provision admission check Should ignore the change if Workload is Admitted and the ProvisioningRequest's condition is set to BookingExpired

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4948

**Last updated**: 2025-05-07T15:09:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-04-14T06:11:41Z
- **Updated**: 2025-05-07T15:09:16Z
- **Closed**: 2025-05-07T15:09:16Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failed `Provisioning admission check suite: [It] Provisioning when A workload is using a provision admission check Should ignore the change if Workload is Admitted and the ProvisioningRequest's condition is set to BookingExpired [slow]` on the periodic release-0.10 CI Job.

```shell
{Failed after 0.387s.
The function passed to Consistently failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:690 with:
Expected
    <[]v1beta1.AdmissionCheckState | len:1, cap:4>: [
        {
            Name: "ac-prov",
            State: "Rejected",
            LastTransitionTime: {
                Time: 2025-04-14T01:44:32Z,
            },
            Message: "",
            PodSetUpdates: [
                {
                    Name: "ps1",
                    Labels: nil,
                    Annotations: {
                        "autoscaling.x-k8s.io/consume-provisioning-request": "wl-ac-prov-1",
                        "autoscaling.x-k8s.io/provisioning-class-name": "provisioning-class",
                        "cluster-autoscaler.kubernetes.io/consume-provisioning-request": "wl-ac-prov-1",
                        "cluster-autoscaler.kubernetes.io/provisioning-class-name": "provisioning-class",
                    },
                    NodeSelector: nil,
                    Tolerations: nil,
                },
                {
                    Name: "ps2",
                    Labels: nil,
                    Annotations: {
                        "autoscaling.x-k8s.io/consume-provisioning-request": "wl-ac-prov-1",
                        "autoscaling.x-k8s.io/provisioning-class-name": "provisioning-class",
                        "cluster-autoscaler.kubernetes.io/consume-provisioning-request": "wl-ac-prov-1",
                        "cluster-autoscaler.kubernetes.io/provisioning-class-name": "provisioning-class",
                    },
                    NodeSelector: nil,
                    Tolerations: nil,
                },
            ],
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000b6af60>: {
        Expected: <v1beta1.AdmissionCheckState>{
            Name: "ac-prov",
            State: "Ready",
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Message: "",
            PodSetUpdates: nil,
        },
        Options: [
            <*cmp.pathFilter | 0xc0005963d8>{
                core: {},
                fnc: 0x79dbc0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    } failed [FAILED] Failed after 0.387s.
The function passed to Consistently failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:690 with:
Expected
    <[]v1beta1.AdmissionCheckState | len:1, cap:4>: [
        {
            Name: "ac-prov",
            State: "Rejected",
            LastTransitionTime: {
                Time: 2025-04-14T01:44:32Z,
            },
            Message: "",
            PodSetUpdates: [
                {
                    Name: "ps1",
                    Labels: nil,
                    Annotations: {
                        "autoscaling.x-k8s.io/consume-provisioning-request": "wl-ac-prov-1",
                        "autoscaling.x-k8s.io/provisioning-class-name": "provisioning-class",
                        "cluster-autoscaler.kubernetes.io/consume-provisioning-request": "wl-ac-prov-1",
                        "cluster-autoscaler.kubernetes.io/provisioning-class-name": "provisioning-class",
                    },
                    NodeSelector: nil,
                    Tolerations: nil,
                },
                {
                    Name: "ps2",
                    Labels: nil,
                    Annotations: {
                        "autoscaling.x-k8s.io/consume-provisioning-request": "wl-ac-prov-1",
                        "autoscaling.x-k8s.io/provisioning-class-name": "provisioning-class",
                        "cluster-autoscaler.kubernetes.io/consume-provisioning-request": "wl-ac-prov-1",
                        "cluster-autoscaler.kubernetes.io/provisioning-class-name": "provisioning-class",
                    },
                    NodeSelector: nil,
                    Tolerations: nil,
                },
            ],
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000b6af60>: {
        Expected: <v1beta1.AdmissionCheckState>{
            Name: "ac-prov",
            State: "Ready",
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Message: "",
            PodSetUpdates: nil,
        },
        Options: [
            <*cmp.pathFilter | 0xc0005963d8>{
                core: {},
                fnc: 0x79dbc0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:697 @ 04/14/25 01:44:34.401
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:

- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-10/1910870358446051328
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-10/1911595141114630144

<img width="1198" alt="Image" src="https://github.com/user-attachments/assets/ed515681-7810-41ee-978c-2899816ae6a8" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T06:11:48Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-14T06:24:26Z

cc @PBundyra do you know if this is just a test failure, or indication of some prod code issues?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T06:24:29Z

This also happened at release-0.11 branch as well: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-11/1911037713113419776

<img width="1145" alt="Image" src="https://github.com/user-attachments/assets/ed3e238a-11d2-4277-8058-ab2f43faaa7c" />

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-14T06:39:25Z

Interestingly, it used to be stable - no failures between March 7 (for another reason) and Apr 12. OTOH I don't see a PR which could be attributed to the recent failures. So it seems like an old issue, but very rare.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-14T06:56:56Z

I looked at the code of the test and it seems there is a flake possible indeed:
```golang
ginkgo.By("Setting the provisioning request as Provisioned", func() {
	gomega.Eventually(func(g gomega.Gomega) {
		g.Expect(k8sClient.Get(ctx, provReqKey, &createdRequest)).To(gomega.Succeed())
		apimeta.SetStatusCondition(&createdRequest.Status.Conditions, metav1.Condition{ // 1
			Type:   autoscaling.Provisioned,
				Status: metav1.ConditionTrue,
				Reason: autoscaling.Provisioned,
			})
		g.Expect(k8sClient.Status().Update(ctx, &createdRequest)).Should(gomega.Succeed())
	}, util.Timeout, util.Interval).Should(gomega.Succeed())
})

ginkgo.By("Checking if the workload is Admitted", func() {
	util.SyncAdmittedConditionForWorkloads(ctx, k8sClient, &updatedWl)
	util.ExpectWorkloadsToBeAdmitted(ctx, k8sClient, &updatedWl)  // 2
})

ginkgo.By("Setting the provisioning request as BookingExpired", func() {
	gomega.Eventually(func(g gomega.Gomega) {
		g.Expect(k8sClient.Get(ctx, provReqKey, &createdRequest)).Should(gomega.Succeed()) // 3
		apimeta.SetStatusCondition(&createdRequest.Status.Conditions, metav1.Condition{
			Type:   autoscaling.BookingExpired,
			Status: metav1.ConditionTrue,
			Reason: autoscaling.BookingExpired,
		})
		g.Expect(k8sClient.Status().Update(ctx, &createdRequest)).Should(gomega.Succeed())
	}, util.Timeout, util.Interval).Should(gomega.Succeed())
})
```
It is possible that the code at `//3` didn't yet see the new `autoscaling.Provisioned` condition. Then, it added `autoscaling.BookingExpired`, but as a consequence the `Provisioned` condition was removed. Typically, the `Get` at 3 already sees the new condition, but this is not guaranteed by how events are distributed in k8s. If this is the case, then a relatively simple fix would be to add a check, just after line 3, that the `Provisioned` is present already.

EDIT: otoh, it does not seem confirmed by logs for the namespace `provisioning-zx4nd` (in that case we would see provisioned: false after provisioned: true) :

```
 "level"=0 "msg"="Created namespace: provisioning-zx4nd"
  2025-04-12T12:49:56.321496622Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:140	LocalQueue create event	{"localQueue": {"name":"queue","namespace":"provisioning-zx4nd"}}
  2025-04-12T12:49:56.321882677Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "provisioning-zx4nd", "name": "queue", "reconcileID": "df75c565-07bf-4339-a58b-4ab8208205dd"}
  2025-04-12T12:49:56.403299264Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:173	Queue update event	{"localQueue": {"name":"queue","namespace":"provisioning-zx4nd"}}
  2025-04-12T12:49:56.403768631Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "provisioning-zx4nd", "name": "queue", "reconcileID": "778f28fc-c6fc-49af-8dd9-0a91e6ec53e1"}
  2025-04-12T12:49:56.625207953Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:601	Workload create event	{"workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "queue": "queue", "status": "pending"}
  2025-04-12T12:49:56.625912233Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "404a3b2e-3a93-46a7-b681-7380ee19ffcd"}
  2025-04-12T12:49:56.62640344Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "234116eb-6979-45dd-8a97-88ef14067128"}
  2025-04-12T12:49:56.626630573Z	LEVEL(-3)	core/workload_controller.go:414	The workload needs admission checks updates	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "234116eb-6979-45dd-8a97-88ef14067128", "clusterQueue": {"name":"cluster-queue"}, "admissionChecks": {"ac-prov":{}}}
  2025-04-12T12:49:56.723313783Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "queue": "queue", "status": "pending"}
  2025-04-12T12:49:56.723965493Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "bcbb9b07-028b-42bd-b200-e27e5f29a29e"}
  2025-04-12T12:49:56.724663102Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "4a1fd8f8-a398-4d0c-bbee-721dba2a6625"}
  2025-04-12T12:49:57.318626168Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "queue": "queue", "status": "quotaReserved", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
  2025-04-12T12:49:57.31950158Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "30959c51-bd34-4d39-acc7-c572ee8b857b"}
  2025-04-12T12:49:57.320255511Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "92e134ce-bc59-4ffc-b00a-684f02ac3233"}
  2025-04-12T12:49:57.320564525Z	LEVEL(-3)	provisioning/controller.go:276	Creating ProvisioningRequest	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "92e134ce-bc59-4ffc-b00a-684f02ac3233", "requestName": "wl-ac-prov-1", "attempt": 1}
  2025-04-12T12:49:57.598787181Z	DEBUG	events	recorder/recorder.go:104	Created ProvisioningRequest: "wl-ac-prov-1"	{"type": "Normal", "object": {"kind":"Workload","namespace":"provisioning-zx4nd","name":"wl","uid":"9e448fdc-17f8-44b8-b6ef-a8c847ebb7c0","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"539"}, "reason": "ProvisioningRequestCreated"}
  2025-04-12T12:49:57.619212486Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "e006dc2a-3b10-47f8-b815-e6219efd9c3c"}
  2025-04-12T12:49:57.62025868Z	LEVEL(-3)	provisioning/controller.go:560	Synchronizing admission check state based on provisioning request	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "e006dc2a-3b10-47f8-b815-e6219efd9c3c", "wl": {"name":"wl","namespace":"provisioning-zx4nd"}, "check": "ac-prov", "prName": "wl-ac-prov-1", "failed": false, "provisioned": false, "accepted": false, "bookingExpired": false, "capacityRevoked": false}
  2025-04-12T12:49:57.691756499Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "provisioning-zx4nd", "name": "queue", "reconcileID": "be6761fc-6442-48b2-8f4f-1947eb9cc08f"}
  2025-04-12T12:49:57.820178373Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:173	Queue update event	{"localQueue": {"name":"queue","namespace":"provisioning-zx4nd"}}
  2025-04-12T12:49:57.821164887Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "provisioning-zx4nd", "name": "queue", "reconcileID": "600375d5-1710-474f-b440-a057f7ace9a4"}
  2025-04-12T12:49:57.912044306Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "17bdd4af-fe23-45fc-bfed-d284a413a89d"}
  2025-04-12T12:49:57.912597964Z	LEVEL(-3)	provisioning/controller.go:560	Synchronizing admission check state based on provisioning request	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "17bdd4af-fe23-45fc-bfed-d284a413a89d", "wl": {"name":"wl","namespace":"provisioning-zx4nd"}, "check": "ac-prov", "prName": "wl-ac-prov-1", "failed": false, "provisioned": true, "accepted": false, "bookingExpired": false, "capacityRevoked": false}
  2025-04-12T12:49:58.123200134Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "queue": "queue", "status": "quotaReserved", "clusterQueue": "cluster-queue"}
  2025-04-12T12:49:58.124147288Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "6ea24a1c-3262-4e51-bcf1-7a96bdef6352"}
  2025-04-12T12:49:58.126649843Z	LEVEL(-2)	provisioning/controller.go:245	Skip syncing of the ProvReq for admission check which is Ready	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "17bdd4af-fe23-45fc-bfed-d284a413a89d", "workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "admissionCheck": "ac-prov"}
  2025-04-12T12:49:58.127116619Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "52a54198-d5a7-4afc-ac81-663729d3727f"}
  2025-04-12T12:49:58.127569806Z	LEVEL(-3)	provisioning/controller.go:560	Synchronizing admission check state based on provisioning request	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "52a54198-d5a7-4afc-ac81-663729d3727f", "wl": {"name":"wl","namespace":"provisioning-zx4nd"}, "check": "ac-prov", "prName": "wl-ac-prov-1", "failed": false, "provisioned": true, "accepted": false, "bookingExpired": false, "capacityRevoked": false}
  2025-04-12T12:49:58.127708797Z	LEVEL(-2)	provisioning/controller.go:245	Skip syncing of the ProvReq for admission check which is Ready	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "52a54198-d5a7-4afc-ac81-663729d3727f", "workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "admissionCheck": "ac-prov"}
  2025-04-12T12:49:58.626601405Z	DEBUG	events	recorder/recorder.go:104	Admitted by ClusterQueue cluster-queue, wait time since reservation was 2s	{"type": "Normal", "object": {"kind":"Workload","namespace":"provisioning-zx4nd","name":"wl","uid":"9e448fdc-17f8-44b8-b6ef-a8c847ebb7c0","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"549"}, "reason": "Admitted"}
  2025-04-12T12:49:58.726566921Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "2d72c285-c71c-45a6-ab2d-49ac22883e1e"}
  2025-04-12T12:49:58.727076619Z	LEVEL(-3)	provisioning/controller.go:560	Synchronizing admission check state based on provisioning request	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "2d72c285-c71c-45a6-ab2d-49ac22883e1e", "wl": {"name":"wl","namespace":"provisioning-zx4nd"}, "check": "ac-prov", "prName": "wl-ac-prov-1", "failed": false, "provisioned": true, "accepted": false, "bookingExpired": true, "capacityRevoked": false}
  2025-04-12T12:49:58.803281982Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "queue": "queue", "status": "admitted", "prevStatus": "quotaReserved", "clusterQueue": "cluster-queue"}
  2025-04-12T12:49:58.804170105Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "31dfe103-f870-4a2e-a870-96594dd2473a"}
  2025-04-12T12:49:58.991328189Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "queue": "queue", "status": "admitted", "clusterQueue": "cluster-queue"}
  2025-04-12T12:49:58.992677248Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "220a9260-4eb1-4b3e-84d6-a1849b96b722"}
  2025-04-12T12:49:58.992971692Z	LEVEL(-3)	core/workload_controller.go:382	Workload is evicted due to admission checks	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "220a9260-4eb1-4b3e-84d6-a1849b96b722"}
  2025-04-12T12:49:59.012716958Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "9a3af549-806d-44a9-b4d0-4f1a520169f3"}
  2025-04-12T12:49:59.014611225Z	LEVEL(-3)	provisioning/controller.go:560	Synchronizing admission check state based on provisioning request	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "9a3af549-806d-44a9-b4d0-4f1a520169f3", "wl": {"name":"wl","namespace":"provisioning-zx4nd"}, "check": "ac-prov", "prName": "wl-ac-prov-1", "failed": false, "provisioned": true, "accepted": false, "bookingExpired": true, "capacityRevoked": false}
  2025-04-12T12:49:59.124438278Z	LEVEL(-3)	core/workload_controller.go:392	Workload is evicted due to rejected admission checks	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "220a9260-4eb1-4b3e-84d6-a1849b96b722", "workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "rejectedChecks": ["ac-prov"]}
  2025-04-12T12:49:59.125069707Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "provisioning-zx4nd", "name": "queue", "reconcileID": "cda19e40-542c-4144-8755-659408d14419"}
  2025-04-12T12:49:59.190826136Z	DEBUG	events	recorder/recorder.go:104	Deactivating workload because AdmissionCheck for ac-prov was Rejected: 	{"type": "Warning", "object": {"kind":"Workload","namespace":"provisioning-zx4nd","name":"wl","uid":"9e448fdc-17f8-44b8-b6ef-a8c847ebb7c0","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"553"}, "reason": "AdmissionCheckRejected"}
  2025-04-12T12:49:59.20911448Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "queue": "queue", "status": "admitted", "clusterQueue": "cluster-queue"}
  2025-04-12T12:49:59.209870861Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "fa597243-c494-4ea0-99d2-dfcb62ad5d33"}
  2025-04-12T12:49:59.211464203Z	LEVEL(-2)	provisioning/controller.go:125	Reconcile Workload	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "a5ffd60c-0f9d-41f0-b2d2-7ac97b5a12ad"}
  2025-04-12T12:49:59.212044711Z	LEVEL(-3)	provisioning/controller.go:560	Synchronizing admission check state based on provisioning request	{"controller": "provisioning_workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "a5ffd60c-0f9d-41f0-b2d2-7ac97b5a12ad", "wl": {"name":"wl","namespace":"provisioning-zx4nd"}, "check": "ac-prov", "prName": "wl-ac-prov-1", "failed": false, "provisioned": true, "accepted": false, "bookingExpired": true, "capacityRevoked": false}
  2025-04-12T12:49:59.21836141Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:173	Queue update event	{"localQueue": {"name":"queue","namespace":"provisioning-zx4nd"}}
  2025-04-12T12:49:59.218767625Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "provisioning-zx4nd", "name": "queue", "reconcileID": "eed44d15-7bd3-4801-856b-e4b58fd70b6b"}
  2025-04-12T12:49:59.31932702Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:165	LocalQueue delete event	{"localQueue": {"name":"queue","namespace":"provisioning-zx4nd"}}
  2025-04-12T12:49:59.496230401Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:631	Workload delete event	{"workload": {"name":"wl","namespace":"provisioning-zx4nd"}, "queue": "queue", "status": "admitted"}
  2025-04-12T12:49:59.721504347Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "workload_controller", "namespace": "provisioning-zx4nd", "name": "wl", "reconcileID": "fa597243-c494-4ea0-99d2-dfcb62ad5d33", "error": "Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"wl\": StorageError: invalid object, Code: 4, Key: /registry/kueue.x-k8s.io/workloads/provisioning-zx4nd/wl, ResourceVersion: 0, AdditionalErrorMsg: Precondition failed: UID in precondition: 9e448fdc-17f8-44b8-b6ef-a8c847ebb7c0, UID in object meta: "}
```
So, based on the logs it seems the provisionining controller stepped into https://github.com/kubernetes-sigs/kueue/blob/6345f5d42dde10a86b364f23ed94c793552bb518/pkg/controller/admissionchecks/provisioning/controller.go#L614

This is possible, because the Admitted condition is set by another controller (workload_controller), and there might be a delay before the provisioning controller knows about the Admitted. 

Since BookingExpired in practice is added after 10min I don't think this is a practical problem, but we should think how to plumb it in tests too.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-14T09:45:37Z

> This is possible, because the Admitted condition is set by another controller (workload_controller), and there might be a delay before the provisioning controller knows about the Admitted.

Yes, I suspect this is the cause

> Since BookingExpired in practice is added after 10min I don't think this is a practical problem, but we should think how to plumb it in tests too.

Agree, not sure about the solution yet though, besides some hardcoded delay in tests to give the provisioning controller some time

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-14T12:23:46Z

Yeah, just waiting for 100ms or so  (since Admitted.LastTransitionTime) might be the pragmatic solution.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T18:35:24Z

This failure happend again at release-0.11 branch periodic job: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-11/1919736208716468224

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-07T09:08:47Z

Seems like we never coded the solution we agreed on, will do it today

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-07T09:13:04Z

PTAL: https://github.com/kubernetes-sigs/kueue/pull/5183
