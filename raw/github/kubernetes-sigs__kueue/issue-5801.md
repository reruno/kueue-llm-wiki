# Issue #5801: kueue.sigs.k8s.io Not updated as expected, what background am I missing?

**Summary**: kueue.sigs.k8s.io Not updated as expected, what background am I missing?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5801

**Last updated**: 2025-07-11T11:03:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@samzong](https://github.com/samzong)
- **Created**: 2025-06-30T06:49:51Z
- **Updated**: 2025-07-11T11:03:45Z
- **Closed**: 2025-07-11T11:03:44Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

https://kueue.sigs.k8s.io It was not updated as expected.

**What you expected to happen**:

In PR #5784 ，We have added internationalization capability to website,
But I found that https://kueue.sigs.k8s.io did not switch normally.

According to netlify.toml：

* For PR preview is `https://deploy-preview-$PR_NUMBER--kubernetes-sigs-kueue.netlify.app`。 
* For branch, it's should be https://$BRANCH--kubernetes-sigs-kueue.netlify.app

Here he is.

- https://deploy-preview-5784--kubernetes-sigs-kueue.netlify.app
- https://main--kubernetes-sigs-kueue.netlify.app

I checked the latest build log from this https://app.netlify.com/projects/kubernetes-sigs-kueue/deploys/68621a6807d2a40008225199

They are all updated, but kueue.sigs.k8s.io is still not updated,
so I guess this domain name points to another host and there will be another rule to trigger the update.

I want to know the reason here and whether I need to fix it.


**How to reproduce it (as minimally and precisely as possible)**:

after site docs change be merged, it's should displayed on the site.

## Discussion

### Comment by [@samzong](https://github.com/samzong) — 2025-06-30T06:50:33Z

@tenzen-y @mortent

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-30T07:02:29Z

@samzong https://kueue.sigs.k8s.io/ is updated based on the current state of the "website" branch. We have not yet  cherry-picked your PRs onto the "website" branch, because I supposed we do it when it is more advanced.

However, I'm ok to publish it incrementally as we move along with the translation go. Otherwise there will be many PRs to cherry-pick later

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-30T07:05:04Z

@samzong I tried auto-cherry-picking by robot, but it failed: https://github.com/kubernetes-sigs/kueue/pull/5784#issuecomment-3018032958.

Could you prepare the cherry-pick manually?

It should be convenient to use the `./hack/cherry_pick_pull.sh` script.

### Comment by [@samzong](https://github.com/samzong) — 2025-06-30T07:16:41Z

Okay, I like this cautious approach 👍, and my next focus is to improve the maturity of the Chinese translation.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-11T11:03:39Z

/close
I think this is clarified by now, and the website already has the translation: 

<img width="2522" height="643" alt="Image" src="https://github.com/user-attachments/assets/df1806b6-d5c5-4c57-9c87-5880616d3b7b" />

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-11T11:03:45Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5801#issuecomment-3061817000):

>/close
>I think this is clarified by now, and the website already has the translation: 
>
><img width="2522" height="643" alt="Image" src="https://github.com/user-attachments/assets/df1806b6-d5c5-4c57-9c87-5880616d3b7b" />


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
