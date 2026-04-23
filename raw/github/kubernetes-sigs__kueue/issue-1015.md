# Issue #1015: Flaky test: Queue controller Should update status when workloads are created

**Summary**: Flaky test: Queue controller Should update status when workloads are created

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1015

**Last updated**: 2023-07-27T15:10:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-07-24T11:13:15Z
- **Updated**: 2023-07-27T15:10:12Z
- **Closed**: 2023-07-27T15:10:12Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The `Queue controller Should update status when workloads are created` is flaky:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1011/pull-kueue-test-integration-main/1683413143272820736

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-25T03:28:09Z

/assign @BinL233

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-07-25T03:28:11Z

@kerthcet: GitHub didn't allow me to assign the following users: BinL233.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1015#issuecomment-1649003158):

>/assign @BinL233 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@BinL233](https://github.com/BinL233) — 2023-07-25T11:21:10Z

By comparing failed logs and success logs, here is missing the deletion of resourceFlavor. There are only update events.
Here's the logs (line 185 - 189) you provided:
```
  2023-07-24T09:48:03.218261255Z	LEVEL(-2)	core/localqueue_controller.go:93	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-queue-v8c8m"}, "namespace": "core-queue-v8c8m", "name": "queue", "reconcileID": "1b034402-88e2-4411-bfc8-78b98648b3fc", "localQueue": {"name":"queue","namespace":"core-queue-v8c8m"}}
  2023-07-24T09:48:03.489100655Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:170	ResourceFlavor update event	{"resourceFlavor": {"name":"model-c"}}
  2023-07-24T09:48:03.489214447Z	LEVEL(-2)	core/resourceflavor_controller.go:78	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"model-c"}, "namespace": "", "name": "model-c", "reconcileID": "5e847aa0-9bf3-4fa4-b4b1-7dfa7240ae8b", "resourceFlavor": {"name":"model-c"}}
  2023-07-24T09:48:03.495016652Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:170	ResourceFlavor update event	{"resourceFlavor": {"name":"model-d"}}
  2023-07-24T09:48:03.498739021Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:135	LocalQueue delete event	{"localQueue": {"name":"queue","namespace":"core-queue-v8c8m"}}
```
Normally delete events should trig.

Maybe we can change the for loop to `gomega.Eventually` in line 69 of localqueue_controller_test.go. This should delete all resourceFlavors.

### Comment by [@BinL233](https://github.com/BinL233) — 2023-07-26T06:44:34Z

> By comparing failed logs and success logs, here is missing the deletion of resourceFlavor. There are only update events. Here's the logs (line 185 - 189) you provided:
> 
> ```
>   2023-07-24T09:48:03.218261255Z	LEVEL(-2)	core/localqueue_controller.go:93	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-queue-v8c8m"}, "namespace": "core-queue-v8c8m", "name": "queue", "reconcileID": "1b034402-88e2-4411-bfc8-78b98648b3fc", "localQueue": {"name":"queue","namespace":"core-queue-v8c8m"}}
>   2023-07-24T09:48:03.489100655Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:170	ResourceFlavor update event	{"resourceFlavor": {"name":"model-c"}}
>   2023-07-24T09:48:03.489214447Z	LEVEL(-2)	core/resourceflavor_controller.go:78	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"model-c"}, "namespace": "", "name": "model-c", "reconcileID": "5e847aa0-9bf3-4fa4-b4b1-7dfa7240ae8b", "resourceFlavor": {"name":"model-c"}}
>   2023-07-24T09:48:03.495016652Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:170	ResourceFlavor update event	{"resourceFlavor": {"name":"model-d"}}
>   2023-07-24T09:48:03.498739021Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:135	LocalQueue delete event	{"localQueue": {"name":"queue","namespace":"core-queue-v8c8m"}}
> ```
> 
> Normally delete events should trig.
> 
> Maybe we can change the for loop to `gomega.Eventually` in line 69 of localqueue_controller_test.go. This should delete all resourceFlavors.

I found ResourceFlavor delete events were trigged after `Queue controller Should update status when workloads are created` this Spec. It should trig before line 194 which is `STEP: Creating resourceFlavors @ 07/24/23 09:48:03.51`.

This is Line 191 - 202 of the logs:
```
------------------------------
Queue controller Should update status when workloads are created
/home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/core/localqueue_controller_test.go:150
  STEP: Creating resourceFlavors @ 07/24/23 09:48:03.51
  2023-07-24T09:48:03.510378609Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:118	LocalQueue create event	{"localQueue": {"name":"queue","namespace":"core-queue-n74rj"}}
  2023-07-24T09:48:03.510474408Z	LEVEL(-2)	core/localqueue_controller.go:93	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-queue-n74rj"}, "namespace": "core-queue-n74rj", "name": "queue", "reconcileID": "3ace6410-b7d8-4cae-965d-568eb6f24a65", "localQueue": {"name":"queue","namespace":"core-queue-n74rj"}}
  2023-07-24T09:48:03.514860075Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:148	Queue update event	{"localQueue": {"name":"queue","namespace":"core-queue-n74rj"}}
  2023-07-24T09:48:03.515083852Z	LEVEL(-2)	core/localqueue_controller.go:93	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-queue-n74rj"}, "namespace": "core-queue-n74rj", "name": "queue", "reconcileID": "a3d14cb4-cbd3-47ef-9dde-5cdb45824300", "localQueue": {"name":"queue","namespace":"core-queue-n74rj"}}
  2023-07-24T09:48:03.516644631Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:150	ResourceFlavor delete event	{"resourceFlavor": {"name":"model-c"}}
  2023-07-24T09:48:03.516689125Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:262	Got generic event	{"obj": {"name":"model-c"}, "kind": "/, Kind="}
  2023-07-24T09:48:03.5[200](https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1011/pull-kueue-test-integration-main/1683413143272820736#1:build-log.txt%3A200)75657Z	LEVEL(-2)	core/resourceflavor_controller.go:78	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"model-d"}, "namespace": "", "name": "model-d", "reconcileID": "1365d11c-cfd0-4371-b626-c0094042cfc4", "resourceFlavor": {"name":"model-d"}}
  [FAILED] in [It] - /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/core/localqueue_controller_test.go:153 @ 07/24/23 09:48:03.584
```
