# Issue #7981: Flaky E2E Test: StatefulSet integration when StatefulSet created should admit group that fits

**Summary**: Flaky E2E Test: StatefulSet integration when StatefulSet created should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7981

**Last updated**: 2025-12-01T16:32:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-11-28T03:10:01Z
- **Updated**: 2025-12-01T16:32:29Z
- **Closed**: 2025-12-01T16:32:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

- End To End Suite: kindest/node:v1.33.4: [It] StatefulSet integration when StatefulSet created should admit group that fits

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:1065 with:
Expected
    <[]v1.Condition | len:0, cap:0>: nil
to have condition type Active and status True failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:1065 with:
Expected
    <[]v1.Condition | len:0, cap:0>: nil
to have condition type Active and status True
In [BeforeEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/statefulset_test.go:76 @ 11/28/25 02:18:06.778
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-33/1994225560498212864

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-28T03:10:16Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-28T07:49:04Z

Interesting, we have this error in the logs.

```
2025-11-28T02:17:58.249777571Z stderr F 2025-11-28T02:17:58.249579839Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "localqueue_controller", "namespace": "e2e-certs-ks4nq", "name": "main", "reconcileID": "5f750c24-6297-47b1-8b7e-88682523b322", "error": "Operation cannot be fulfilled on localqueues.kueue.x-k8s.io \"main\": StorageError: invalid object, Code: 4, Key: /registry/kueue.x-k8s.io/localqueues/e2e-certs-ks4nq/main, ResourceVersion: 0, AdditionalErrorMsg: Precondition failed: UID in precondition: 0ece462d-7ea0-41ba-94f3-b79fab42d5b3, UID in object meta: "}
2025-11-28T02:17:58.249792881Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
2025-11-28T02:17:58.249797041Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474
2025-11-28T02:17:58.249800541Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
2025-11-28T02:17:58.249804281Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421
2025-11-28T02:17:58.249807761Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1
2025-11-28T02:17:58.249811191Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296
2025-11-28T02:18:00.810698227Z stderr F 2025-11-28T02:18:00.810468856Z	LEVEL(-2)	core/localqueue_controller.go:153	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "e2e-certs-ks4nq", "name": "main", "reconcileID": "49fe694a-2bfa-4d53-aa72-8cbbf44b598b"}
2025-11-28T02:18:00.814591339Z stderr F 2025-11-28T02:18:00.814382748Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "localqueue_controller", "namespace": "e2e-certs-ks4nq", "name": "main", "reconcileID": "49fe694a-2bfa-4d53-aa72-8cbbf44b598b", "error": "Operation cannot be fulfilled on localqueues.kueue.x-k8s.io \"main\": StorageError: invalid object, Code: 4, Key: /registry/kueue.x-k8s.io/localqueues/e2e-certs-ks4nq/main, ResourceVersion: 0, AdditionalErrorMsg: Precondition failed: UID in precondition: 0ece462d-7ea0-41ba-94f3-b79fab42d5b3, UID in object meta: "}
```

This is probably an issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-28T07:55:32Z

Hm, I don't see how this is related. 

I observed in the past `ExpectLocalQueuesToBeActive` failing on other tests due to timeout in case leader election is still happening after restart (which may take 15s). I would check in the logs if we have any indication of leader election going on. If so it can help to bump timeout for the function to LongTimeout.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-28T13:07:33Z

/assign @sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T07:34:54Z

I analyzed the logs and I indeed think the fix should be in certs_test.go to make sure Kueue recovers from scaling up and down, see [comment](https://github.com/kubernetes-sigs/kueue/pull/8003#issuecomment-3594874477). I think just waiting for the LQ Reconcile as suggested in the [comment](https://github.com/kubernetes-sigs/kueue/pull/8003#issuecomment-3594878915) should help.
