# Issue #9439: MultiKueue: support RayService integration

**Summary**: MultiKueue: support RayService integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9439

**Last updated**: 2026-03-19T21:36:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-24T08:23:02Z
- **Updated**: 2026-03-19T21:36:32Z
- **Closed**: 2026-03-19T21:36:32Z
- **Labels**: `kind/feature`, `area/multikueue`
- **Assignees**: [@NarayanaSabari](https://github.com/NarayanaSabari)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add RayService support for MultiKueue.

This requires the pre-requisite at the KubeRay side: https://github.com/ray-project/kuberay/issues/4486

However, we probably start prototyping early using the main image, or release candidate of KubeRay.

**Why is this needed**:

To allow scheduling RayService objects via MultiKueue.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-24T08:23:13Z

cc @hiboyang

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2026-02-24T10:48:44Z

Hi, I'd like to work on this. Here's my understanding of the current state and proposed approach:

**Current state:**
- KubeRay side: `spec.managedBy` on RayService has been merged ([kuberay#4491](https://github.com/ray-project/kuberay/pull/4491)), release planned for March 15
- Kueue side: RayService as a top-level job was merged via [#9102](https://github.com/kubernetes-sigs/kueue/pull/9102) (controller, webhook, RBAC, E2E), but without MultiKueue support
- The vendored KubeRay API in Kueue doesn't yet have `ManagedBy` on `RayServiceSpec`

**Proposed implementation plan:**

1. **Bump the vendored KubeRay dependency** to pick up the `ManagedBy` field on `RayServiceSpec` (either from `main` or an RC once available)
2. **Implement `JobWithManagedBy` interface** on `RayService` in `rayservice_controller.go` - adding `CanDefaultManagedBy()`, `ManagedBy()`, `SetManagedBy()` methods, following the RayJob pattern
3. **Create `rayservice_multikueue_adapter.go`** implementing `MultiKueueAdapter` and `MultiKueueWatcher` - following the existing RayJob adapter pattern (`SyncJob`, `DeleteRemoteObject`, `IsJobManagedByKueue`, `GVK`, `GetEmptyList`, `WorkloadKeysFor`)
4. **Register the adapter** in `IntegrationCallbacks` in the `init()` function
5. **Add unit tests** in `rayservice_multikueue_adapter_test.go`
6. **Add MultiKueue E2E tests** for RayService

One thing to note: RayService is long-running (`Finished()` always returns `false`), so the adapter will continuously sync status rather than waiting for completion.

I plan to raise a PR for this. Let me know if there are any concerns or if I'm missing anything.

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2026-02-24T10:49:31Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-24T11:15:59Z

Thank you @NarayanaSabari ! This all sounds reasonable. 

To kick off the work early we need to figure out how to build Kueue using the main KubeRay as a depedency (or a release candidate there).

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2026-02-24T11:47:34Z

Thanks @mimowo! Good point on the dependency.

I see a few options for building with the `ManagedBy` field on `RayServiceSpec` before the KubeRay release:

1. **Use a Go pseudo-version pointing to KubeRay `master`** - e.g., `go get github.com/ray-project/kuberay/ray-operator@master` to get a pseudo-version like `v1.5.2-0.<timestamp>-<commit>`. This lets us build, test, and open a draft PR now, then swap to the proper release tag (v1.6.0 or an RC) before merging.

2. **Wait for a KubeRay RC** - the v1.6.0 release is planned for March 15, so an RC should be available before that. We could pin to it once available.

I think option 1 is the most practical path forward - I can open a draft PR with the pseudo-version dependency so we can iterate on the implementation, and we update to the stable KubeRay release before the final merge (Kueue release target is March 23, so timing should work).

I already have the implementation ready locally (adapter, controller changes, unit tests all passing). Happy to push the draft PR whenever you'd like. Let me know which approach you prefer!

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-24T11:51:42Z

Yeah, (1.) is quite good, it will work for getting the new code for sure, I'm not sure if they publish images for every commit build (TBD).

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2026-02-24T11:54:34Z

Good question. I checked the KubeRay CI - their `release-image-build` workflow only triggers on tags, so there are no per-commit images published to `quay.io/kuberay/operator`.

For the E2E tests, I think the approach would be:
1. **For unit tests and the draft PR** - the pseudo-version is sufficient, no operator image needed
2. **For E2E tests** - we can either build the KubeRay operator image locally from `master` (their Makefile supports `make docker-image`), or defer E2E tests until an RC image is published

Since the unit tests cover the MultiKueue adapter logic thoroughly, I'll open a draft PR with the pseudo-version + unit tests first, and we can add E2E tests once a KubeRay RC is available (or build from source if we want them sooner).

I'll get the draft PR up shortly!

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-24T17:20:51Z

Thanks @NarayanaSabari for working on this!

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-03-05T09:26:25Z

/area multikueue
