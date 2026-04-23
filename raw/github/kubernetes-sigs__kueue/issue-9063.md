# Issue #9063: E2E_mode=dev should leave the new clusters in kubeconfig for Multikueue

**Summary**: E2E_mode=dev should leave the new clusters in kubeconfig for Multikueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9063

**Last updated**: 2026-02-10T11:32:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-09T14:59:11Z
- **Updated**: 2026-02-10T11:32:02Z
- **Closed**: 2026-02-10T11:32:02Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

 Make sure the newly created clusters are put into the "default" kubeconfig.

**Why is this needed**:

When I create clusters using `E2E_MODE=dev` make kind-image-build test-multikueue-e2e` then I would like to interact with the clusters after the testing. However, they are not put into the "main" kubeconfig.

This is also inconsistent with testing for single cluster, when the "kind" cluster is added to the main kubeconfig.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T14:59:21Z

cc @vladikkuzn @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-09T15:08:39Z

I think you need to use env variable like this:

KUBECONFIG=/Users/mykhailo_bobrovskyi/Projects/epam/kueue/bin/run-test-multikueue-e2e-1.35.0/kubeconfig-kind-manager:/Users/mykhailo_bobrovskyi/Projects/epam/kueue/bin/run-test-multikueue-e2e-1.35.0/kubeconfig-kind-worker1:/Users/mykhailo_bobrovskyi/Projects/epam/kueue/bin/run-test-multikueue-e2e-1.35.0/kubeconfig-kind-worker2

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-09T15:09:01Z

/cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T15:32:38Z

> I think you need to use env variable like this:

yeah, sure then it works, but it is not very convenient at all. For example requires bumping the KUBECONFIG after we bump k8s for testing Kueue.


I would prefer the clusters to be added to my main kubeconfig, as for the single cluster tests, unless there is a good reason not to do it for MultiKueue, but I cannot see it.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-10T11:03:16Z

/assign @mbobrovskyi
