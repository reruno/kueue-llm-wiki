# Issue #5418: Doc: Revisit Adopters category

**Summary**: Doc: Revisit Adopters category

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5418

**Last updated**: 2025-11-01T07:44:12Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-05-30T06:09:53Z
- **Updated**: 2025-11-01T07:44:12Z
- **Closed**: 2025-11-01T07:44:11Z
- **Labels**: `lifecycle/rotten`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 15

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We want to revist the adapter categories, `End User` and `Provider` in https://kueue.sigs.k8s.io/docs/adopters/.

**Why is this needed**:

As we discussed in https://github.com/kubernetes-sigs/kueue/pull/5285#discussion_r2095519344, we want to re-categorize the adapters since we do not have any description against each definition (End user / Provider).

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T06:10:12Z

/kind documentation
/remove-kind cleanup

cc @mimowo @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T06:24:23Z

Yes, the column in the current form is confusing, because we don't have any description indicating the meaning. I suggest to remove the column and maybe re add in the future if we have a clear definition.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-30T10:55:33Z

/retitle Doc: Revisit Adaptors category

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-30T10:56:01Z

I'm also in favor of deleting `Type` column

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T11:09:01Z

I would like to keep the type column, but we should add https://www.cncf.io/enduser/#:~:text=End%20User%20Definition,Consultancies%20and%20systems%20integrators to describe what is end users.

The end users' usage indicates that Kueue is actually leveraged in their production, which has obviously advantage users who evaluate and consider whether or not they should introduce Kueue to their env.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T11:23:33Z

> I would like to keep the type column, but we should add https://www.cncf.io/enduser/#:~:text=End%20User%20Definition,Consultancies%20and%20systems%20integrators to describe what is end users.

To be fair even this definition isn't very clear in some cases, say if you are not a lawyer, say to determine "Consultancies and systems integrators.". 

I think we will not be in a position to argue if someone opens a PR and claims some company type. So I'm concerned we may run into unnecessary debates and disagreements on PRs about their positioning. Also, disclosing the positioning could be discouraging to some adopters (I imagine).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T11:28:29Z

> The end users' usage indicates that Kueue is actually leveraged in their production, which has obviously advantage users who evaluate and consider whether or not they should introduce Kueue to their env.

I agree this could have been useful at the beginning, but I believe Kueue, at this point, is established as used at production by end user companies. So, at this point in time, I don't see this adding much value, most of the companies in this column are "End user" anyway already.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-30T11:56:51Z

> /retitle Doc: Revisit Adaptors category

/retitle Doc: Revisit Adopters category

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T15:44:18Z

> > I would like to keep the type column, but we should add https://www.cncf.io/enduser/#:~:text=End%20User%20Definition,Consultancies%20and%20systems%20integrators to describe what is end users.
> 
> To be fair even this definition isn't very clear in some cases, say if you are not a lawyer, say to determine "Consultancies and systems integrators.".
> 
> I think we will not be in a position to argue if someone opens a PR and claims some company type. So I'm concerned we may run into unnecessary debates and disagreements on PRs about their positioning. Also, disclosing the positioning could be discouraging to some adopters (I imagine).

I don't say that Kueue maintainers should decide whether or not the adopter company is acually an end user. We always can respect their decision. If they think their company is end user, they can put it on our documentation.

> > The end users' usage indicates that Kueue is actually leveraged in their production, which has obviously advantage users who evaluate and consider whether or not they should introduce Kueue to their env.
> 
> I agree this could have been useful at the beginning, but I believe Kueue, at this point, is established as used at production by end user companies. So, at this point in time, I don't see this adding much value, most of the companies in this column are "End user" anyway already.

I know your team has many end-user companies as customers. However, that is not public information. Additionally, the public information will be gone once we remove the `Type` column. The newcomer will struggle to obtain information.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T15:52:34Z

I'm totally ok to try to make this term as unambiguous as possible. Feel free to submit proposal PR. 

We can test that first, and only re-evaluate the decision if we encounter that some users are still confused.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T05:58:12Z

> I'm totally ok to try to make this term as unambiguous as possible. Feel free to submit proposal PR.
> 
> We can test that first, and only re-evaluate the decision if we encounter that some users are still confused.

SGTM, I will try to open a PR for improving.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-02T06:42:34Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-02T07:19:18Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-01T07:44:06Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-01T07:44:11Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5418#issuecomment-3475906082):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
