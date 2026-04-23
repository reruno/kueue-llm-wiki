# Issue #4142: [Flaky test] Provisioning when A workload is using a provision admission check Should not set AdmissionCheck status to Rejected...

**Summary**: [Flaky test] Provisioning when A workload is using a provision admission check Should not set AdmissionCheck status to Rejected...

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4142

**Last updated**: 2025-12-08T09:41:36Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-02-04T08:30:16Z
- **Updated**: 2025-12-08T09:41:36Z
- **Closed**: 2025-12-08T09:41:36Z
- **Labels**: `kind/bug`, `kind/flake`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:

Provisioning admission check suite: [It] Provisioning when A workload is using a provision admission check Should not set AdmissionCheck status to Rejected, deactivate Workload, emit an event, and bump metrics when workload is Finished, and the ProvisioningRequest's condition is set to CapacityRevoked

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:626 with:
Expected
    <[]v1beta1.AdmissionCheckState | len:1, cap:1>: [
        {
            Name: "ac-prov",
            State: "Rejected",
            LastTransitionTime: {
                Time: 2025-02-03T16:08:02Z,
            },
            Message: "",
            PodSetUpdates: [
                {
                    Name: "ps1",
                    Labels: nil,
                    Annotations: {
                        "autoscaling.x-k8s.io/consume-provisioning-request": "wl-ac-prov-1",
                        "autoscaling.x-k8s.io/provisioning-class-name": "provisioning-class",
                        "cluster-autoscaler.kubernetes.io/consume-provisioning-request": "wl-ac-prov-1",
                        "cluster-autoscaler.kubernetes.io/provisioning-class-name": "provisioning-class",
                    },
                    NodeSelector: nil,
                    Tolerations: nil,
                },
                {
                    Name: "ps2",
                    Labels: nil,
                    Annotations: {
                        "cluster-autoscaler.kubernetes.io/provisioning-class-name": "provisioning-class",
                        "autoscaling.x-k8s.io/consume-provisioning-request": "wl-ac-prov-1",
                        "autoscaling.x-k8s.io/provisioning-class-name": "provisioning-class",
                        "cluster-autoscaler.kubernetes.io/consume-provisioning-request": "wl-ac-prov-1",
                    },
                    NodeSelector: nil,
                    Tolerations: nil,
                },
            ],
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000e44030>: {
        Expected: <v1beta1.AdmissionCheckState>{
            Name: "ac-prov",
            State: "Ready",
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Message: "",
            PodSetUpdates: nil,
        },
        Options: [
            <*cmp.pathFilter | 0xc000b383a8>{
                core: {},
                fnc: 0x79d560,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    } failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:626 with:
Expected
    <[]v1beta1.AdmissionCheckState | len:1, cap:1>: [
        {
            Name: "ac-prov",
            State: "Rejected",
            LastTransitionTime: {
                Time: 2025-02-03T16:08:02Z,
            },
            Message: "",
            PodSetUpdates: [
                {
                    Name: "ps1",
                    Labels: nil,
                    Annotations: {
                        "autoscaling.x-k8s.io/consume-provisioning-request": "wl-ac-prov-1",
                        "autoscaling.x-k8s.io/provisioning-class-name": "provisioning-class",
                        "cluster-autoscaler.kubernetes.io/consume-provisioning-request": "wl-ac-prov-1",
                        "cluster-autoscaler.kubernetes.io/provisioning-class-name": "provisioning-class",
                    },
                    NodeSelector: nil,
                    Tolerations: nil,
                },
                {
                    Name: "ps2",
                    Labels: nil,
                    Annotations: {
                        "cluster-autoscaler.kubernetes.io/provisioning-class-name": "provisioning-class",
                        "autoscaling.x-k8s.io/consume-provisioning-request": "wl-ac-prov-1",
                        "autoscaling.x-k8s.io/provisioning-class-name": "provisioning-class",
                        "cluster-autoscaler.kubernetes.io/consume-provisioning-request": "wl-ac-prov-1",
                    },
                    NodeSelector: nil,
                    Tolerations: nil,
                },
            ],
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000e44030>: {
        Expected: <v1beta1.AdmissionCheckState>{
            Name: "ac-prov",
            State: "Ready",
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Message: "",
            PodSetUpdates: nil,
        },
        Options: [
            <*cmp.pathFilter | 0xc000b383a8>{
                core: {},
                fnc: 0x79d560,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:636 @ 02/03/25 16:08:13.817
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4081/pull-kueue-test-integration-main/1886445469324808192

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T07:20:34Z

Recent occurence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4591/pull-kueue-test-integration-main/1900260147398184960

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-12T08:13:16Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-11T08:43:22Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-09T09:08:25Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-08T09:11:05Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-08T09:41:31Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-08T09:41:36Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4142#issuecomment-3625961926):

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
