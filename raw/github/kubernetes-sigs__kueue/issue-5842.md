# Issue #5842: Localization: support Chinese for Kueue website

**Summary**: Localization: support Chinese for Kueue website

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5842

**Last updated**: 2025-10-06T16:14:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-02T10:23:30Z
- **Updated**: 2025-10-06T16:14:44Z
- **Closed**: 2025-10-06T16:14:43Z
- **Labels**: `kind/documentation`, `area/localization`, `language/zh`
- **Assignees**: _none_
- **Comments**: 22

## Description

An issue to track the recent effort to translate the Kueue documentation into Chinese.

Most relevant PRs so far:
- https://github.com/kubernetes-sigs/kueue/pull/5784

Cherry-pick of the PRs so far:
- https://github.com/kubernetes-sigs/kueue/pull/5825

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-02T10:25:14Z

/kind localization
cc @samzong @my-git9 @windsonsea 
I open the issue to track the progress, feel free to reference PRs as "Part of" in the description so that we can track them easier.
cc @tenzen-y

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-02T10:25:18Z

@mimowo: The label(s) `kind/localization` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5842#issuecomment-3027313941):

>/kind localization
>cc @samzong @my-git9 @windsonsea 
>I open the issue to track the progress, feel free to reference PRs as "Part of" in the description so that we can track them easier.
>cc @tenzen-y 
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-02T10:26:26Z

/label localization

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-02T10:26:30Z

@mimowo: The label(s) `/label localization` cannot be applied. These labels are supported: `api-review, tide/merge-method-merge, tide/merge-method-rebase, tide/merge-method-squash, team/katacoda, refactor, ci-short, ci-extended, ci-full`. Is this label configured under `labels -> additional_labels` or `labels -> restricted_labels` in `plugin.yaml`?

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5842#issuecomment-3027317466):

>/label localization


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-02T10:29:25Z

/kind localization

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-02T10:30:00Z

@tenzen-y I'm proposing to add the localization kind to track the PRs, wdyt?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-02T10:37:33Z

@mimowo I would like to use the same labels with k/website.

- [area/localization](https://github.com/kubernetes/website/labels/area%2Flocalization)
- [language/zh](https://github.com/kubernetes/website/labels/language%2Fzh)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-02T10:44:55Z

The localizations issue / PR must have `kind/documentation`, `area/localization`, and `language/xxx`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-02T10:45:06Z

> [@mimowo](https://github.com/mimowo) I would like to use the same labels with k/website.

+1, sg

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-02T10:45:31Z

/kind documentation
/area localization
/language zh

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-02T10:45:35Z

@mimowo: The label(s) `area/localization, language/zh` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5842#issuecomment-3027372517):

>/kind documentation
>/area localization
>/language zh


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-02T10:50:23Z

/area localization
/language zh

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-02T10:51:51Z

/remove-kind localization

### Comment by [@samzong](https://github.com/samzong) — 2025-07-02T16:29:44Z

I agree that following k/website is a very good practice, which also helps to set a good example for other SIGs.

And most contributors start with k/website, so it is a natural transition for them rather than a new learning cost.

And show we add a worflow Automatically add language labels? like PR Title start with lang-code ?

### Comment by [@windsonsea](https://github.com/windsonsea) — 2025-07-03T00:29:14Z

Cool, adding labels (`area/localization`, `language/zh`) is a normal way to track.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-01T10:01:57Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T10:07:00Z

/remove-lifecycle

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T10:07:21Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T11:04:18Z

@samzong @my-git9 @windsonsea @ls-2018 
Thank you for the effort!

It looks like most of the pages are translated by now, so I'm wondering if it is time to close the issue and move to "maintenance" mode for the translation, wdyt?

### Comment by [@samzong](https://github.com/samzong) — 2025-10-06T16:10:50Z

@mimowo Agree👍, maintenance mode sounds perfect.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-06T16:14:37Z

Thank you @samzong , sgtm, I'm closing the issue then as most of the work looks done.

Still, whenever you folks find some pages missing translation or out-of-sync, then feel free to contribute. 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-06T16:14:44Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5842#issuecomment-3372566041):

>Thank you @samzong , sgtm, I'm closing the issue then as most of the work looks done.
>
>Still, whenever you folks find some pages missing translation or out-of-sync, then feel free to contribute. 
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
