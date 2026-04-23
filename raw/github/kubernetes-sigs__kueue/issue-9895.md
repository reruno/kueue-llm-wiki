# Issue #9895: Introduce less verbose ginkgo formatter

**Summary**: Introduce less verbose ginkgo formatter

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9895

**Last updated**: 2026-03-16T17:25:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-16T12:26:25Z
- **Updated**: 2026-03-16T17:25:41Z
- **Closed**: 2026-03-16T17:25:41Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@reruno](https://github.com/reruno)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to register less verbose ginkgo formatter, at least for types known to Kueue.

**Why is this needed**:

We observe a lot of lines which are useless, and take space, see discussion in https://github.com/kubernetes-sigs/kueue/pull/9890#issuecomment-4066997129

Example from the discussion:
```
EphemeralContainers: nil,
RestartPolicy: "Never",
TerminationGracePeriodSeconds: nil,
ActiveDeadlineSeconds: nil,
DNSPolicy: "",
NodeSelector: nil,
ServiceAccountName: "",
DeprecatedServiceAccount: "",
AutomountServiceAccountToken: nil,
NodeName: "",
HostNetwork: false,
HostPID: false,
HostIPC: false,
ShareProcessNamespace: nil,
SecurityContext: nil,
ImagePullSecrets: nil,
Hostname: "",
Subdomain: "",
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T12:26:48Z

cc @mbobrovskyi @reruno

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-16T16:56:41Z

/assign @reruno

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-16T16:56:46Z

@mbobrovskyi: GitHub didn't allow me to assign the following users: reruno.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9895#issuecomment-4069163812):

>/assign @reruno 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@reruno](https://github.com/reruno) — 2026-03-16T17:02:54Z

/assign
