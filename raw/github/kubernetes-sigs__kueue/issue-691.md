# Issue #691: Make integration config more flexible.

**Summary**: Make integration config more flexible.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/691

**Last updated**: 2023-04-27T20:04:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-04-12T06:14:16Z
- **Updated**: 2023-04-27T20:04:17Z
- **Closed**: 2023-04-27T20:04:17Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently, restringing the available jobs integration is done in a herdcoded linear flow.

https://github.com/kubernetes-sigs/kueue/blob/dc1bed47e1abf36303f58cf42e9a1fe94ad998ac/main.go#L183-L223

Before this starts growing too much, maybe we can replace with a loop.

We can have some RegisterIntegration method that is called from the init() function of each integration's package.

Then the main goes over all the registered integrations, checks if they are enabled before calling the constructor. Otherwise it creates the noop webhook.

**Why is this needed**:

Simplifies the addition of new integration and keep the code cleaner. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-04-12T14:56:57Z

/assign
