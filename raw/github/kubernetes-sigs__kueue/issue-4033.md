# Issue #4033: Flaky Test: Topology Aware Scheduling when Negative scenarios for ClusterQueue configuration should mark TAS ClusterQueue as inactive if used in cohort

**Summary**: Flaky Test: Topology Aware Scheduling when Negative scenarios for ClusterQueue configuration should mark TAS ClusterQueue as inactive if used in cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4033

**Last updated**: 2025-01-29T14:48:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-01-22T07:58:37Z
- **Updated**: 2025-01-29T14:48:11Z
- **Closed**: 2025-01-29T14:48:08Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failure on "TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Negative scenarios for ClusterQueue configuration should mark TAS ClusterQueue as inactive if used in cohort"

```shell
{Timed out after 5.000s.
Expected object to be comparable, diff:   []v1.Condition{
  	{
  		... // 2 ignored and 2 identical fields
  		Reason: "NotSupportedWithTopologyAwareScheduling",
  		Message: strings.Join({
  			"Can't admit new workloads: TAS is not supported for cohorts",
- 			`, there is no Topology "default" for TAS flavor "tas-flavor"`,
  			".",
  		}, ""),
  	},
  }
 failed [FAILED] Timed out after 5.000s.
Expected object to be comparable, diff:   []v1.Condition{
  	{
  		... // 2 ignored and 2 identical fields
  		Reason: "NotSupportedWithTopologyAwareScheduling",
  		Message: strings.Join({
  			"Can't admit new workloads: TAS is not supported for cohorts",
- 			`, there is no Topology "default" for TAS flavor "tas-flavor"`,
  			".",
  		}, ""),
  	},
  }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/tas/tas_test.go:112 @ 01/22/25 04:30:36.473
}
```

**What you expected to happen**:

Succeeded

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-9/1881918244332244992

<img width="1350" alt="Image" src="https://github.com/user-attachments/assets/741d43ed-aba9-4d22-8e2a-df2cedac1636" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-22T07:58:48Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-22T13:25:05Z

/assign 
Let me check, it seems like a race condition with processing the topology ADDED event and creating the message. 

I think we can just relax the assert and only check the reason "NotSupportedWithTopologyAwareScheduling". The message is tested at the unit tests level.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T09:17:28Z

I looked at this a bit more and tried to repro locally by running the test in a loop, however it didn't fail after over 1000 repeats under stress. So, I believe the best path forward is to improve logging as proposed in https://github.com/kubernetes-sigs/kueue/pull/4068.

As discussed in https://github.com/kubernetes-sigs/kueue/issues/4033#issuecomment-2607244843 the tests are a little bit too strong, and I wouldn't mind just asserting on the reason. OTOH, it may be an indication the propagation of events is racy.

It is possible that occasionally, on a loaded CI machine, the 5s timeout is not enough for the events to propagate. So, I would like to propose extending the integration tests timeout to 10s. This is the timeout also used in JobSet [link](https://github.com/kubernetes-sigs/jobset/blob/ec942521899668e414d1775da8a2acffbd1b1d17/test/integration/controller/jobset_controller_test.go#L45). When the test succeeds the timeout does not matter anyway, when it fails waiting 5s would not make much of a difference IMO. WDYT @tenzen-y @PBundyra @mbobrovskyi ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T09:18:19Z

cc @mszadkow any opinion on extending the timeout for integration tests to 10s?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-01-29T09:32:40Z

I'm fine with extending the timeout. Too strict timeout could indeed be a reason for failure, and if it isn't we'll get a clear signal that we should proceed with debugging. We can change it back to 5s if it still flakes afterwards

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T09:47:55Z

> We can change it back to 5s if it still flakes afterwards

Yes, but if we don't get the signal quickly (which I believe will be the case given how rare flake it is), then it could get risky for other tests added in the meanwhile. 

Alternatively, I could introduce a new timeout const list MediumTimeout=15s, and use in the test only, then it would get easier to revert to 5s, wdyt?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-29T11:48:47Z

I agree with your theory @mimowo about events propagation, let's increase the time.
However if it will get flaky again we need more insight

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T14:48:04Z

/close 
I suggest to close for now and we re-open if the issue re-occurs after https://github.com/kubernetes-sigs/kueue/pull/4092, with https://github.com/kubernetes-sigs/kueue/pull/4068 hopefully providing more info.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-29T14:48:09Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4033#issuecomment-2621861949):

>/close 
>I suggest to close for now and we re-open if the issue re-occurs after https://github.com/kubernetes-sigs/kueue/pull/4092, with https://github.com/kubernetes-sigs/kueue/pull/4068 hopefully providing more info.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
