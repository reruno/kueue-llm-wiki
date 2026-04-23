# Issue #3174: Make LossLessDefaulter selective to only prevent dropping fields outside of schema

**Summary**: Make LossLessDefaulter selective to only prevent dropping fields outside of schema

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3174

**Last updated**: 2024-11-07T09:01:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-01T17:14:34Z
- **Updated**: 2024-11-07T09:01:28Z
- **Closed**: 2024-11-07T09:01:25Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 6

## Description

**What would you like to be added**:

Investigate making the LossLessDefaulter in Kueue to only prevent dropping fields outside of schema. 
This is a follow up from the discussion: https://github.com/kubernetes-sigs/kueue/pull/3132#discussion_r1782255326

And follow up to the issue: https://github.com/kubernetes-sigs/kueue/issues/2878


**Why is this needed**:

* Long term we may want to remove some fields in Kueue webhooks, and it would be hard with the current LossLessDefaulter
* Making LossLessDefaulter selective could possibly let us promote it as an opt-in defaulter in controller-runtime, allowing for:
  - reduced maintenance cost by moving from Kueue to controller-runtime
  - allow sharing the solution with other projects so that they don't need to reinvent the wheel

**Completion requirements**:

Investigate if this is feasible. and what is the implementation complexity, prototype.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-01T17:15:00Z

/assign @tenzen-y 
per comment https://github.com/kubernetes-sigs/kueue/pull/3132#discussion_r1783163941
/cc @alculquicondor

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-01T17:23:48Z

Sorry. I did not want to indicate taking this issue.
/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-02T06:20:02Z

Sorry, I misread your message which was clear. Thanks for clarifying!
Anyway, the issue is open for contributions.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-03T05:57:05Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T09:01:21Z

/close
we don't need this in Kueue as there is fix in controller-runtime to be released, issue to track using the fix: https://github.com/kubernetes-sigs/kueue/issues/3469

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-07T09:01:26Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3174#issuecomment-2461674176):

>/close
>we don't need this in Kueue as there is fix in controller-runtime to be released, issue to track using the fix: https://github.com/kubernetes-sigs/kueue/issues/3469


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
