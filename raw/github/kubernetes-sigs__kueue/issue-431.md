# Issue #431: [E2E Tests] - We should allow users to test the e2e code against existing clusters that aren't kind.

**Summary**: [E2E Tests] - We should allow users to test the e2e code against existing clusters that aren't kind.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/431

**Last updated**: 2022-11-28T14:28:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2022-11-22T15:37:49Z
- **Updated**: 2022-11-28T14:28:08Z
- **Closed**: 2022-11-28T14:28:08Z
- **Labels**: `kind/feature`
- **Assignees**: [@shubhbapna](https://github.com/shubhbapna)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Our e2e tests currently do the following:

1. Build Kind Cluster
2. Build a local image
3. Load that image to kind
4. Run our tests

It would be nice to allow users to use an existing cluster where the images are existing in a repo.  This could be useful for release testing on cloud vendors kubernetes clusters.  

**Why is this needed**:

Developers use a wide range of Kubernetes clusters for development and we should not assume that everyone wants to run on Kind.  

**Completion requirements**:

A developer can run the e2e tests on an existing cluster without assuming kind.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2022-11-22T15:39:04Z

/help
/good-first-issue

### Comment by [@shubhbapna](https://github.com/shubhbapna) — 2022-11-24T18:08:29Z

Hey @kannon92 would love to take a shot at this issue! Can I take it?

### Comment by [@kannon92](https://github.com/kannon92) — 2022-11-24T18:20:33Z

> Hey @kannon92 would love to take a shot at this issue! Can I take it?

Yep!

/assign @shubhbapna

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-24T18:22:33Z

/remove-help
/remove-good-first-issue

### Comment by [@shubhbapna](https://github.com/shubhbapna) — 2022-11-25T15:17:50Z

Are we assuming that the existing cluster will come pre-loaded with the image?
If not, do we have to build the image before we load it or they will simply provide us an image tag?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-25T15:34:32Z

You can assume that the existing cluster has access to the registry that `make image-local-push` pushes to.

### Comment by [@shubhbapna](https://github.com/shubhbapna) — 2022-11-25T16:22:53Z

Should I add another target or can I simply edit the existing target to behave like this:
```
# run using kind
make test-e2e

# run using existing cluster
make test-e2e USE_EXISTING_CLUSTER=true IMAGE_TAG=tag
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-25T16:39:31Z

Not having an extra target would be nice
