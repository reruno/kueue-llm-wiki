# Issue #7156: TAS integration with Kubeflow Trainer v2

**Summary**: TAS integration with Kubeflow Trainer v2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7156

**Last updated**: 2025-10-24T08:51:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-03T12:25:10Z
- **Updated**: 2025-10-24T08:51:37Z
- **Closed**: 2025-10-24T08:51:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 3

## Description

**What would you like to be added**:

Support TAS running for Kubeflow Trainer v2. Currently it does not work as reported here: https://github.com/kubernetes-sigs/kueue/issues/6865#issuecomment-3327164428

This is currently waiting on https://github.com/kubeflow/trainer/issues/2784 with the pending PR https://github.com/kubeflow/trainer/pull/2785

Once the PR lands in Trainer we need to adjust Kueue.

**Why is this needed**:

We have users interested in the integration. Both Kubeflow Trainer v2 and TAS as major recent investments so it would be great to make them compatible.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T12:25:49Z

cc @izturn @kaisoz @andreyvelich @tenzen-y @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T10:32:53Z

I see this is merged https://github.com/kubeflow/trainer/pull/2785. So, basically, the integration should work when we have Trainer 2.1.0 released. In order to make sure there are no blockers I would appreciate to have already some PoC PR using the main branch on the Kubeflow Trainer v2.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-10-09T11:23:18Z

/assign

I can take care of this one 😊
