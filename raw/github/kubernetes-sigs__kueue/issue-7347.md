# Issue #7347: Add helm chart to deploy resources required by TAS

**Summary**: Add helm chart to deploy resources required by TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7347

**Last updated**: 2025-11-24T16:56:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Edwinhr716](https://github.com/Edwinhr716)
- **Created**: 2025-10-23T02:28:34Z
- **Updated**: 2025-11-24T16:56:46Z
- **Closed**: 2025-11-24T16:56:46Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

@mwysokin created a GKE specific extension of the helm chart for automating the deployment of the resources required by TAS called AutoKueue here: https://github.com/mwysokin/kueue/tree/autokueue. I propose we make AutoKueue cloud agnostic and add it to the upstream repo. 

AutoKueue adds a helm hook which deploys a topology object, creates a resource flavor, a cluster queue, and a local queue. For the upstream version, we can automate the creation of everything except the local queue. The user will create the local queue in their chosen namespace. We can add a new flag called `autoKueue` which will enable the hook. AutoKueue will have the following flags:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| autoKueue.tasLevels | list | `[{name: cloud.provider.com/topology-block}]` | Defines the TAS levels |
| autoKueue.nodeLabel | object | `{cloud.provider.com/node-group: "tas-group"}` | Sets the Resource flavor node label | 


**Why is this needed**:
TAS is a very useful feature for other controllers such as JobSet and LWS. However, often users don't need the extra features of Kueue, and just want to use TAS. Abstracting away most of the TAS set up makes it easier to use. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

cc @ahg-g

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-12T16:41:25Z

There is a related issue https://github.com/kubernetes-sigs/kueue/issues/7610.

This one is focusing on creating localqueues based on ClusterQueue namespace selector. Would this satisfy your use case?

> For the upstream version, we can automate the creation of everything except the local queue. The user will create the local queue in their chosen namespace
