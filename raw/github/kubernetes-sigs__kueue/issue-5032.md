# Issue #5032: v1beta2: Delete .enable field from FairSharing API in config

**Summary**: v1beta2: Delete .enable field from FairSharing API in config

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5032

**Last updated**: 2025-11-13T17:07:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-04-17T09:05:24Z
- **Updated**: 2025-11-13T17:07:41Z
- **Closed**: 2025-11-13T17:07:41Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
- Remove `.enable` field from the FairSharing config API

**Why is this needed**:
With changes introduced by https://github.com/kubernetes-sigs/kueue/pull/4252 we have two modes of FairSharing. One of them is defined by `.preemptionStrategies`, and the second one by `.admissionFairSharing` field. Hence, the `.enable` field is redundant and allows user defining invalid states e.g. when `enabled=true` but both `preemptionStrategies` and `admissionFairSharing` are empty

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-17T09:06:17Z

Is we agree on this change, I'll add it to v1beta2 wishlist
cc @mimowo @tenzen-y @gabesaba @mwielgus

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-04-17T09:14:53Z

I support this change. It will make the API more intuitive for users, and harder to misconfigure.

We may want to add to the v1beta2 wishlist:

A dedicated field for PreemptionFairSharing (perhaps with a better name), and one for AdmissionFairSharing, so it is crystal clear that preemptionStrategies is applying to this preemption mode. It will also allow those modes to be cleanly extended/modified as needed in the future

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-17T09:40:21Z

sounds reasonable, the reason we introduced the "enable" field in knobs for some features was to enable administrators to enable / disable a feature without losing the configuration. This seemed like a reasonable use-case, but I'm not sure if this is "best practice" or commonly used strategy in other projects. 

If we decide on that I would suggest to apply the same approach to other configuration aspects, such as WaitForPodsReady too, for consistency and clear approach. I'm personally ok either way.

cc @tenzen-y @dgrove-oss wdyt?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-18T13:07:09Z

+1 on this. I do think we should maybe not delete a field from a beta API though. I would be happy with deprecation for a release and then a removal. 

We could also remove it when we promote the config apis to v1?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-03T13:56:34Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T08:16:03Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-02T09:02:05Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-03T08:19:51Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-03T08:20:31Z

Oh, we forgot to add it to v1beta2 wishlist. Let me add it still as a nice to have here: https://github.com/kubernetes-sigs/kueue/issues/7113

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-03T08:20:45Z

/retitle v1beta2: Delete .enable field from FairSharing API in config

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-03T08:24:57Z

I'm not totally sure if we want to drop the "enable" field, maybe just adding validation to prevent this: "Hence, the .enable field is redundant and allows user defining invalid states e.g. when enabled=true but both preemptionStrategies and admissionFairSharing are empty" - basically validate against "enable=true" and empty preemptionStrategies, wdyt @PBundyra ?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-11-04T12:52:14Z

I still think having `.enable` field in the API is a bad design

>  the reason we introduced the "enable" field in knobs for some features was to enable administrators to enable / disable a feature without losing the configuration

I don't think we should be hinted by such a motivation. An admin is able to copy and save the old configuration and it's fairly easy. If there's no technical setback of improving this API, and it's mainly about ease of use for an admin (switching the field vs saving old configuration) then I wouldn't treat it as a blocker

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T13:02:45Z

I'm ok with that, but then should we also adjust waitaforapodsaready and inetrnalCertManagement, seems desired to have consistent API.

 cc @mwysokin as it may potentially also impact upgrades

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-07T14:52:14Z

/assign
