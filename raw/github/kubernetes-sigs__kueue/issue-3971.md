# Issue #3971: Improved Helm chart versioning practices

**Summary**: Improved Helm chart versioning practices

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3971

**Last updated**: 2025-02-19T11:10:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rptaylor](https://github.com/rptaylor)
- **Created**: 2025-01-14T22:35:37Z
- **Updated**: 2025-02-19T11:10:31Z
- **Closed**: 2025-02-19T11:10:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Improve helm chart versioning to follow best practices.  The CI that is used to produce Helm charts appears to overwrite the chart version with the appVersion, meaning that the two are always the same.

**Why is this needed**:

See discussion:   https://github.com/kubernetes-sigs/kueue/pull/3925#discussion_r1905262367

The comment https://github.com/kubernetes-sigs/kueue/pull/3925#discussion_r1915546412  illustrates some issues that could be improved.

Going forward I would suggest using both chart version and appVersion, and they should necessarily diverge over time: let the chart version be incremented on any/every chart update (including a new kueue version, i.e. appVersion), while the appVersion should only change when the default value of the kueue version changes.  There is a reason that two kinds of versions exist and it is best practice to use both as intended.

Aside from that, personally I found it a bit counterintuitive/confusing when trying to install the kueue chart - it seemed odd that I needed to use the appVersion when retrieving the OCI chart, when normally the chart version is used (which appeared to be 0.1.0 based on https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/Chart.yaml  but evidently that is not the case; afterwards I realized the chart version must be set equal to the appVersion when CI publishes the chart).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-15T13:03:18Z

Thank you for opening the issue, the chart versioning in Kueue is confusing indeed. 

In particular, the `version` field seems to be totally ignored even though the comment suggests to update it based on the semantic versioning. Instead, the values is ignored and set to `appVersion`- I'm yet not clear which code specifically does the overwrite, but it looks like that. do you know @tenzen-y ?

However, I'm not yet clear about the practical issues from the user perspective. We never update the helm charts for a specific version, so v0.10.0 will always be the same chart. Bugfixes are released in point releases. The published charts for the daily builds of the charts also don't conflict as the version is very specific, eg. `v20241112-v0.10.0-devel-31-g43b73747`. 

So, it might be we should just update the comment to indicate the "version" field is set by the CI process (and best if we also indicate where and which step for transparency).

### Comment by [@rptaylor](https://github.com/rptaylor) — 2025-01-15T19:41:31Z

Okay thanks for clarifying and elaborating. Based on further discussion in https://github.com/kubernetes-sigs/kueue/pull/3925#discussion_r1915546412 it is again not as bad as I first thought.  ><

If version and appVersion are both used to separately represent the chart and app version, it would allow the chart and kueue release process to be decoupled; new charts could be released more rapidly than the release cycle of the kueue code/image. The daily chart builds could be another way to address that though. It would be useful to have some notes/docs about how/where to find the daily builds, possibly also in Chart.yaml as a helpful pointer. With OCI charts, unlike a helm repo, AFAICT you can't browse available chart versions.
Anyway thanks!

### Comment by [@zargor](https://github.com/zargor) — 2025-01-24T10:22:10Z

It is still misleading having chart version `0.1.0` and app version `v0.10.1`, while actually those versions are identical, both are `v0.10.1`

Also would be great to release new chart deprecating rbac proxy. As noticed there is already a commit covering that.
https://github.com/kubernetes-sigs/kueue/commit/81b90cd9286e9960afaea6a8a5aaedbf320d9650

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-24T11:05:33Z

i agree the field comment is misleading and I would welcome a PR to improve it, or just drop the version field entirely. im not sure we have any user facing issue due at the moment.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-19T08:27:38Z

I have accidentally encountered the CI line which sets both `version` and `appVersion` as the same when preparing the helm package for release: [here](https://github.com/kubernetes-sigs/kueue/blob/main/Makefile#L274C18-L274C63) and in [here](https://github.com/kubernetes-sigs/kueue/blob/2587f1538b4bbe2a80c407c110404b6320dc0072/hack/push-chart.sh#L51).

So, I think the only remaining thing is to improve the comment for the "version" field in `charts/kueue/Chart.yaml`. I will open a PR

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-19T08:35:49Z

PTAL: https://github.com/kubernetes-sigs/kueue/pull/4308
