# Issue #7943: MultiKueue via ClusterProfile: add full e2e tests to confirm using a plugin for kind

**Summary**: MultiKueue via ClusterProfile: add full e2e tests to confirm using a plugin for kind

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7943

**Last updated**: 2026-01-16T10:52:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-27T09:48:49Z
- **Updated**: 2026-01-16T10:52:42Z
- **Closed**: 2026-01-16T10:52:42Z
- **Labels**: `priority/important-soon`, `kind/cleanup`, `area/multikueue`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 5

## Description

I would like to have a full e2e test which proves the integration and cluster connection via ClusterProfile works ok. For that we could have a simple plugin for kind which would load the credentials from a secret actually.

Related to https://github.com/kubernetes-sigs/kueue/issues/7942 and https://github.com/kubernetes-sigs/kueue/issues/7850

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T09:49:25Z

cc @mszadkow @hdp617

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-09T13:35:48Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-09T13:37:30Z

Note:
Create a simple plugin that copies kubeconfig from the secret to the clusterprofile.
Instead of using proprietary plugins to reduce the complexity of the tests.

### Comment by [@hdp617](https://github.com/hdp617) — 2025-12-09T16:39:29Z

Thanks for looking into this! If it's helpful, there's a [secret reader plugin](https://github.com/kubernetes-sigs/cluster-inventory-api/tree/main/cmd/secretreader-plugin) in the cluster-inventory-api repo I think could be used in the e2e tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:20:09Z

/area multikueue
/priority important-soon
