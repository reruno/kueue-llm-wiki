# Issue #9094: v1beta2 migration script - support large scale

**Summary**: v1beta2 migration script - support large scale

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9094

**Last updated**: 2026-02-10T14:28:03Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-10T13:10:31Z
- **Updated**: 2026-02-10T14:28:03Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We have an issue using the mitigation script at large scale. https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/hack/migrate-to-v1beta2.sh

The error we were getting:
```
Migrating workloads.kueue.x-k8s.io...
Error from server: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=Workload failed: Post "[https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s](https://kueue-webhook-service.kueue-system.svc/convert?timeout=30s)": EOF
```

We were successful to migrate by splitting running the script namespace-by-namespace.

We may also need to do paging better, but maybe namespace-by-namespace is enough.

**Why is this needed**:

To support migrating to v1beta2 for large evironments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T13:10:52Z

@mwielgus @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T13:27:46Z

/cc @mbobrovskyi 
tentatively, who is already familiar with that. We will sync on the next version of the script. Our patched version namespace-by-namespace must be cleaned up

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T13:27:56Z

/assign @mbobrovskyi

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-10T13:39:09Z

I can share my production cluster migration step in the following:

1. Update Kueue Controller Manager with `kustomize build "$KUEUE_V016_MANIFESTS_DIR" | kubectl apply --server-side --force-conflicts -f -`
2. Wait for all kueue-controller-managers ready (All replicas must be ready)
3. Execute `./migrate-to-v1beta2.sh`

I'm not sure if this is the expected approach. 
But, as I check your migration error (`Error from server: conversion webhook for kueue.x-k8s.io/v1beta1, Kind=Workload failed: Post "[https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s](https://kueue-webhook-service.kueue-system.svc/convert?timeout=30s)": EOF`), 2 possible errors are considered: (1 one of the kueue replicas is unavailable, or (2 a lack of replicas. In case of a large cluster, they should increase manager replicas as much as possible in advance because the concurrent webhook execution should be delegated to multiple kueue managers.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-10T13:42:27Z

> I can share my production cluster migration step in the following:

If it is not a secret how many workloads do you have?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-10T13:50:26Z

I think we need to add pagination to our script to allow batch updates instead of fetching all objects.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-10T14:03:33Z

> > I can share my production cluster migration step in the following:
> 
> If it is not a secret how many workloads do you have?

I shared my env in another space, then @mbobrovskyi confirmed that the error facing the env is far from my case.
So, I believe that batch processing would be worth it.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2026-02-10T14:28:03Z

The underlying problem is that conversion webhook needs to process the whole batch in 150 seconds. If the processing takes more, the list is dropped. How much Kueue can process and send back within these 150 seconds depends on the network and node performance but with workloads counted in XX k it definitely fails.
