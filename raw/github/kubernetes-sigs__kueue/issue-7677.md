# Issue #7677: E2E Tests for Admission Fair Sharing

**Summary**: E2E Tests for Admission Fair Sharing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7677

**Last updated**: 2025-12-19T15:28:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-11-14T20:34:35Z
- **Updated**: 2025-12-19T15:28:34Z
- **Closed**: 2025-12-19T15:28:34Z
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 6

## Description

Forgive me if I missed it but I didn't see any e2e tests verifying Admission Fair Sharing.

It looks to be covered via integration tests.

Should we add e2e tests now that this feature is beta?

cc @PBundyra @mimowo

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-14T21:26:36Z

No objections.
/kind cleanup

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T09:26:41Z

I have no objections, but I'm not sure what we would gain since the mechanism is not using Pods so seems we can simulate it fully in integration tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T09:26:48Z

cc @PBundyra

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-18T20:22:55Z

> I have no objections, but I'm not sure what we would gain since the mechanism is not using Pods so seems we can simulate it fully in integration tests.

For Openshift Kueue, it would be great to be able to leverage these features on real clusters. 

We aim to provision kueue on real OCP clusters and then run the e2e against clusters. So having simpler e2e helps us validate that this feature works.

I do understand the challenge of replicating integration tests in e2e environments so I would be more interested in simple e2e for validating admission fair sharing.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-18T08:14:41Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:32:41Z

/priority important-soon
