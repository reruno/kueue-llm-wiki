# Issue #1477: Release artifacts are not signed

**Summary**: Release artifacts are not signed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1477

**Last updated**: 2024-03-26T20:38:44Z

---

## Metadata

- **State**: open
- **Author**: [@psschwei](https://github.com/psschwei)
- **Created**: 2023-12-16T22:46:51Z
- **Updated**: 2024-03-26T20:38:44Z
- **Closed**: —
- **Labels**: `kind/feature`, `sig/release`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

`#SecuritySlam`

**What would you like to be added**:

The project cryptographically signs release artifacts.

**Why is this needed**:

Signing artifacts would boost the security of the project. And since the CLOMonitor security score flags the project for not signing its artifacts, signing them would also make the score better.

**Completion requirements**:

These are the details from [CLOMonitor](https://clomonitor.io/projects/cncf/kueue#kueue_security) around this task:

```
Signed-Releases OpenSSF Scorecard check

Score: 0 (check passes with score >= 1)

Reason: 0 out of 5 artifacts are signed or have provenance

Details:

Warn: release artifact v0.5.1 does not have provenance: https://api.github.com/repos/kubernetes-sigs/kueue/releases/131789880
Warn: release artifact v0.5.1 not signed: https://api.github.com/repos/kubernetes-sigs/kueue/releases/131789880
Warn: release artifact v0.5.0 does not have provenance: https://api.github.com/repos/kubernetes-sigs/kueue/releases/126674662
Warn: release artifact v0.5.0 not signed: https://api.github.com/repos/kubernetes-sigs/kueue/releases/126674662
Warn: release artifact v0.4.2 does not have provenance: https://api.github.com/repos/kubernetes-sigs/kueue/releases/124678930
Warn: release artifact v0.4.2 not signed: https://api.github.com/repos/kubernetes-sigs/kueue/releases/124678930
Warn: release artifact v0.4.1 does not have provenance: https://api.github.com/repos/kubernetes-sigs/kueue/releases/117224650
Warn: release artifact v0.4.1 not signed: https://api.github.com/repos/kubernetes-sigs/kueue/releases/117224650
Warn: release artifact v0.4.0 does not have provenance: https://api.github.com/repos/kubernetes-sigs/kueue/releases/111415075
Warn: release artifact v0.4.0 not signed: https://api.github.com/repos/kubernetes-sigs/kueue/releases/111415075

Please see the [check documentation](https://github.com/ossf/scorecard/blob/e1d3abc7fd2bdfe8819ac19b5c82815ea20890e6/docs/checks.md#signed-releases) in the ossf/scorecard repository for more details
```

## Discussion

### Comment by [@psschwei](https://github.com/psschwei) — 2023-12-16T22:49:31Z

/sig release

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2023-12-18T09:55:44Z

/retitle Release artifacts are not signed

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2023-12-18T09:56:39Z

This is a result report of the `#securitySlam` 
cc @alculquicondor @tenzen-y

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T15:29:40Z

Are there instructions on how to sign them?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T15:31:10Z

Found it https://wiki.debian.org/Creating%20signed%20GitHub%20releases

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-17T15:38:59Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-26T20:38:42Z

/lifecycle frozen
