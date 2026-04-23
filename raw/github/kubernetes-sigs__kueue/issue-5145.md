# Issue #5145: Helm E2E Tests

**Summary**: Helm E2E Tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5145

**Last updated**: 2026-03-11T07:43:36Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-04-30T15:29:16Z
- **Updated**: 2026-03-11T07:43:36Z
- **Closed**: —
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 20

## Description

As Kueue has both kustomize/Helm, we should consider having e2e tests that make sure Helm creates a functional Kueue installation.

I think we should deploy helm (rather than kustomize) and then run the e2e suite.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-30T15:29:28Z

/help
/good-first-issue

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T05:55:22Z

I don't think that we should add E2E only for Helm.
What we want to verify is whether or not the generated manifests are correct. The helm manifests generation does not related to actual Kueue behavior.

So, instead of this one, we want to add generated manifests verifications by https://github.com/helm-unittest/helm-unittest

### Comment by [@SD-13](https://github.com/SD-13) — 2025-05-01T07:40:55Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T07:45:56Z

This is not yet accepted.
/remove-assign

/remove-help

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T07:46:24Z

/unassign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T07:46:33Z

/unassign @SD-13

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-01T16:22:41Z

> I don't think that we should add E2E only for Helm. What we want to verify is whether or not the generated manifests are correct. The helm manifests generation does not related to actual Kueue behavior.
> 
> So, instead of this one, we want to add generated manifests verifications by https://github.com/helm-unittest/helm-unittest

I guess I don't have much confidence that helm unit tests would actually report a failure in kueue installation.

It would just verify that helm is valid.

For JobSet, I would like to add https://github.com/kubernetes-sigs/jobset/issues/899. We also have helm-unittests but we still would like to catch failures in deploying of JobSet and anything that would cause our e2e tests to fail.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T18:59:34Z

The root cause of the installation issue for Helm is not tied to the actual cluster. The problem is that unintended manifests are generated, isn't it?

Adding non-essential E2E testings lead longer CI time. Instead of that, we should focus on essential verification something like whether or not we can obtain expected manifests from Helm when we enable some flag (parameter).

> For JobSet, I would like to add https://github.com/kubernetes-sigs/jobset/issues/899. We also have helm-unittests but we still would like to catch failures in deploying of JobSet and anything that would cause our e2e tests to fail.

I'm not JobSet owner, so I don't argue JobSet should not have E2E testings for Helm.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-05T06:50:29Z

Bugs which surface in runtime, but not when generating manifests aren't common, but they are possible. I think this is one example: https://github.com/kubernetes-sigs/kueue/pull/4903. So, I see some value in e2e testing helms.

> Adding non-essential E2E testings lead longer CI time.

Well, if we introduced a dedicated CI job like e2e-helm, it would not extend the CI time for developer perspective.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T15:12:32Z

> Bugs which surface in runtime, but not when generating manifests aren't common, but they are possible. I think this is one example: [#4903](https://github.com/kubernetes-sigs/kueue/pull/4903). So, I see some value in e2e testing helms.
> 
> > Adding non-essential E2E testings lead longer CI time.
> 
> Well, if we introduced a dedicated CI job like e2e-helm, it would not extend the CI time for developer perspective.

As I can check #4903, that looks like manifests errors, that is not related Kueue behavior. Shouldn't we determine what is expected to be generated from Helm instead of real cluster testing?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T06:56:59Z

> As I can check [#4903](https://github.com/kubernetes-sigs/kueue/pull/4903), that looks like manifests errors, that is not related Kueue behavior. Shouldn't we determine what is expected to be generated from Helm instead of real cluster testing?

Maybe we could, but this requires some dedicated rules which can only be discovered after the bug (these would be rules to prevent future regressions). With e2e tests we could find such bugs during development. 

We have a similar case here actually: https://github.com/kubernetes-sigs/kueue/issues/5186, where the generates template has correct syntax, but does not work well.

I would actually be leaning to have e2e tests seeing the other bug.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T10:36:33Z

> > As I can check [#4903](https://github.com/kubernetes-sigs/kueue/pull/4903), that looks like manifests errors, that is not related Kueue behavior. Shouldn't we determine what is expected to be generated from Helm instead of real cluster testing?
> 
> Maybe we could, but this requires some dedicated rules which can only be discovered after the bug (these would be rules to prevent future regressions). With e2e tests we could find such bugs during development.
> 
> We have a similar case here actually: [#5186](https://github.com/kubernetes-sigs/kueue/issues/5186), where the generates template has correct syntax, but does not work well.
> 
> I would actually be leaning to have e2e tests seeing the other bug.

I think that the pointed problem is caused by generated CRD files which is not related Helm.
Adding tests against the generated CRD files would be better instead of Helm dedicated tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T10:58:52Z

This issue was only present for the helm manifests, take a look at the diff for the fix pr

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-07T11:24:51Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T07:00:28Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T07:03:25Z

Recently we had this issue: https://github.com/kubernetes-sigs/kueue/issues/6797

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-11T07:33:34Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T07:38:06Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-11T07:38:30Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-11T07:43:36Z

/remove-lifecycle stale
