# Issue #9790: Temporarily restore the FlavorFungibilityImplicitPreferenceDefault feature gate to allow upgrades

**Summary**: Temporarily restore the FlavorFungibilityImplicitPreferenceDefault feature gate to allow upgrades

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9790

**Last updated**: 2026-03-12T07:05:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-10T16:25:37Z
- **Updated**: 2026-03-12T07:05:43Z
- **Closed**: 2026-03-12T07:05:43Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 4

## Description

**What would you like to be added**:

I would like to temporarily restore the  FlavorFungibilityImplicitPreferenceDefault feature gate to allow easier upgrade to 0.16 without changing in modelling.

**Why is this needed**:

To allow users an upgrade to 0.16 asap, and only later to drop the feature gate.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-10T16:26:25Z

/assign @vladikkuzn 
who worked on the feature gate and the preference field. 
cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-10T16:54:11Z

Note that using the `flavorFungability.preference` in 0.15 is tricky also due to the bug: https://github.com/kubernetes-sigs/kueue/pull/9464. So now the users need to essentially move to 0.16 and use `flavorFungability.preference` in one change. Clearly, stepwise upgrade is better experience - first keep feature gate and upgrade to 0.16.3, then use the field, then drop the feature gate.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-10T17:04:40Z

I synced with @mimowo offline, then we reached to agreement.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-10T17:09:34Z

The primary reason why I agreed this decision is that the preference field had very critical bugs for a while.

This means that this field behavior was unstable, and users probably not to introduce such unstable feature when they upgrade Kueue version because they want to minimize the risk at Kueue updates.
