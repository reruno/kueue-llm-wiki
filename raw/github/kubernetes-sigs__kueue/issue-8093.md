# Issue #8093: Easy to use running e2e test for developers

**Summary**: Easy to use running e2e test for developers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8093

**Last updated**: 2026-01-19T13:47:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-05T13:01:39Z
- **Updated**: 2026-01-19T13:47:17Z
- **Closed**: 2026-01-19T13:47:16Z
- **Labels**: `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

As a developer I would like a mode which allows me to easily run e2e tests in a loop. 

This is inspired by the PR: https://github.com/kubernetes-sigs/kueue/pull/7657 which is going in the right direction, but instead of introducing so many env. variables I want something simple and intuitive to work with.

I think we generally have two main modes of operation:
1. CI - create the cluster, delete the cluster, run tests
2. dev mode - create the cluster or reuse if exists from prev run, rebuild Kueue, run tests, don't delete cluster

So, I'm thinking about something like 
`E2E_DEV_MODE=true` variable which will do:
1.  create the cluster or reuse if exists from prev run
2. don't delete cluster
3. install all the dependencies like JobSet, appWrapper only if not done yet
4. rebuild Kueue only
5. run tests 

Once this is done I don't think we need variables like `CREATE_CLUSTER` or `DELETE_CLUSTER` or `E2E_TEST_ONLY_EVN`. They are cumbersome to learn and use, and we actually have just 2 modes currently.

Let me know if you have more use cases.

The alternative would be `E2E_MODE` with CI/DEV options for now.

**Why is this needed**:

As a developer I want the cluster to stay around for (1.) manual investigation after tests, (2) quick re-run.

Currently this is cumbersome because the test goal deletes the cluster.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-05T13:04:24Z

> 2. don't delete cluster

We need to think about how to clean this up. For singlecluster it’s easy – just execute `kind delete cluster`. But what about multikueue?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-05T13:11:38Z

/cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T13:20:46Z

> We need to think about how to clean this up. For singlecluster it’s easy – just execute kind delete cluster. But what about multikueue?

We can introduce `E2E_SKIP_CLUSTER_CLEANUP=true` for MultiKueue, but I would still keep the clusters around in the developer mode by default

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-05T16:21:14Z

cc @MaysaMacedo 

I know you were running into some challenges with working with the e2e tests. Curious on your thoughts?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-08T08:09:33Z

> k about how to clean this up. For singlecluster it’s easy – just execute `kind delete cluster`. But what about multikueue?

Do you refer to cleaning up the clusters before another run or removing them out later?
Because ` kind delete cluster` removes it, while we want them to stay

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:46:55Z

I think this option would work really well for developing MultiKueue where we want to often use the test setup to priovision the clusters. This has been also raised in:
https://github.com/kubernetes-sigs/kueue/issues/6036 and https://github.com/kubernetes-sigs/kueue/issues/6033

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:19:30Z

/area multikueue
/priority important-soon

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-06T13:18:40Z

/assign
