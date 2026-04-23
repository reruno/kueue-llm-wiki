# Issue #1795: Address all the disabled warnings given by shell check

**Summary**: Address all the disabled warnings given by shell check

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1795

**Last updated**: 2024-08-05T16:36:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Vandit1604](https://github.com/Vandit1604)
- **Created**: 2024-03-04T17:04:56Z
- **Updated**: 2024-08-05T16:36:34Z
- **Closed**: 2024-08-05T16:36:32Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Vandit1604](https://github.com/Vandit1604)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
In https://github.com/kubernetes-sigs/kueue/pull/1552, We added shell check to the repository. Currently, we are ignoring a lot of shell check warnings.

```shell
# Currently disabled these errors will take care of them later
DISABLED_ERRORS="SC2002,SC3028,SC3054,SC3014,SC3040,SC3046,SC3030,SC3010,SC3037,SC3045,SC3006,SC3018,SC3016,SC3011,SC3044,SC3043,SC3060,SC3024,SC1091,SC2066,SC2086,SC2034,SC1083,SC1009,SC1073,SC1072,SC2155,SC2046"
```

This issue tracks the progress we make on addressing all the disabled errors/warnings given by shell check. See https://github.com/kubernetes-sigs/kueue/pull/1552 for more information.
 
**Why is this needed**:
The goals of Shell Check and addressing all the warnings are:

- To point out and clarify typical beginner's syntax issues that cause a shell to give cryptic error messages.

- To point out and clarify typical intermediate level semantic problems that cause a shell to behave strangely and counter-intuitively.

- To point out subtle caveats, corner cases and pitfalls that may cause an advanced user's otherwise working script to fail under future circumstances.

## Discussion

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-04T17:05:35Z

/assign

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-04T18:08:09Z

https://github.com/kubernetes-sigs/kueue/pull/1552#issuecomment-1976589359 

Leaving this here so I don't forget this.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-06T23:36:31Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-07T06:58:42Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-07T06:58:53Z

@Vandit1604 Still working on this?

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-06-07T11:07:05Z

Hi @tenzen-y 
Most of the disabled errors and warnings are already solved and taken care of, see https://github.com/kubernetes-sigs/kueue/pull/1840#discussion_r1542880280

Currently, we are ignoring these errors/warnings, see [shellcheckrc](https://github.com/kubernetes-sigs/kueue/blob/main/.shellcheckrc)

```shell
# Currently disabled these errors will take care of them later

# Not following: (error message here)
# https://github.com/koalaman/shellcheck/wiki/SC1091
disable=SC1091
# Since you double quoted this, it will not word split, and the loop will only run once
# https://github.com/koalaman/shellcheck/wiki/SC2066
disable=SC2066
# Double quote to prevent globbing and word splitting
# https://github.com/koalaman/shellcheck/wiki/SC2086
disable=SC2086
# foo appears unused. Verify it or export it
# https://github.com/koalaman/shellcheck/wiki/SC2034
disable=SC2034
# This {/} is literal. Check if ; is missing or quote the expression.
# https://github.com/koalaman/shellcheck/wiki/SC1083
disable=SC1083
# Declare and assign separately to avoid masking return values
# https://github.com/koalaman/shellcheck/wiki/SC2155
disable=SC2155
# Quote this to prevent word splitting
# https://github.com/koalaman/shellcheck/wiki/SC2046
disable=SC2046
```

I checked and disabled all of these and ran `make shell-lint` and there were no errors 🎆 
should I go ahead and remove the [configuration where we are disabling them](https://github.com/kubernetes-sigs/kueue/blob/main/.shellcheckrc#L9-L31) in shell check?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-12T12:12:39Z

> Hi @tenzen-y Most of the disabled errors and warnings are already solved and taken care of, see [#1840 (comment)](https://github.com/kubernetes-sigs/kueue/pull/1840#discussion_r1542880280)
> 
> Currently, we are ignoring these errors/warnings, see [shellcheckrc](https://github.com/kubernetes-sigs/kueue/blob/main/.shellcheckrc)
> 
> ```shell
> # Currently disabled these errors will take care of them later
> 
> # Not following: (error message here)
> # https://github.com/koalaman/shellcheck/wiki/SC1091
> disable=SC1091
> # Since you double quoted this, it will not word split, and the loop will only run once
> # https://github.com/koalaman/shellcheck/wiki/SC2066
> disable=SC2066
> # Double quote to prevent globbing and word splitting
> # https://github.com/koalaman/shellcheck/wiki/SC2086
> disable=SC2086
> # foo appears unused. Verify it or export it
> # https://github.com/koalaman/shellcheck/wiki/SC2034
> disable=SC2034
> # This {/} is literal. Check if ; is missing or quote the expression.
> # https://github.com/koalaman/shellcheck/wiki/SC1083
> disable=SC1083
> # Declare and assign separately to avoid masking return values
> # https://github.com/koalaman/shellcheck/wiki/SC2155
> disable=SC2155
> # Quote this to prevent word splitting
> # https://github.com/koalaman/shellcheck/wiki/SC2046
> disable=SC2046
> ```
> 
> I checked and disabled all of these and ran `make shell-lint` and there were no errors 🎆 should I go ahead and remove the [configuration where we are disabling them](https://github.com/kubernetes-sigs/kueue/blob/main/.shellcheckrc#L9-L31) in shell check?

Oh, thank you for investigating it!
Yeah, could you open PR to disable ignoring settings?

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-06-13T18:47:23Z

Sure [Done: #2410] @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-13T20:10:53Z

Uhm, I'm suspecting that the shellcheck doesn't work fine in this repository since I can see some lint errors once I manually perform the shellcheck against https://github.com/kubernetes-sigs/kueue/blob/main/hack/multikueue-e2e-test.sh in the https://www.shellcheck.net/.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-13T20:13:52Z

@Vandit1604 could you investigate the reason why shellcheck doesn't work fine?

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-06-15T16:23:33Z

@tenzen-y here, `scripts_to_check`  variable was holding only 1 file https://github.com/kubernetes-sigs/kueue/blob/main/hack/verify-shellcheck.sh#L24 because it was not an array and shell check was running only over it on single file. That's why it was not working.

I have pushed the changes in https://github.com/kubernetes-sigs/kueue/pull/2410 to fix it.

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-06-16T10:47:43Z

I have updated the PR to only solve shellcheck not working. Addressing all shellcheck disabled warnings will be done in another seperate PR.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-05T16:36:28Z

Resolved by https://github.com/kubernetes-sigs/kueue/pull/2763
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-05T16:36:32Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1795#issuecomment-2269476406):

>Resolved by https://github.com/kubernetes-sigs/kueue/pull/2763
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
