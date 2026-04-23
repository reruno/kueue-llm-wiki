# Issue #3526: Support log retrieval on MultiKueue

**Summary**: Support log retrieval on MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3526

**Last updated**: 2026-04-20T08:05:58Z

---

## Metadata

- **State**: open
- **Author**: [@rochaporto](https://github.com/rochaporto)
- **Created**: 2024-11-13T14:35:13Z
- **Updated**: 2026-04-20T08:05:58Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 26

## Description

**What would you like to be added**:

We would like to be able to retrieve logs from MultiKueue workloads, directly from the master cluster.

**Why is this needed**:

Multiple tools running on top of Kubernetes rely on the log retrieval API to give live feedback to users.

Examples include:
* The GitLab CI Kubernetes executor (https://docs.gitlab.com/runner/executors/kubernetes/) relies on the logs functionality to provide CI job logs to the users
* The Kubeflow jobs also integrate with log retrieval to display live feedback to users in the different dashboards ()

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@Horiodino](https://github.com/Horiodino) — 2024-11-25T18:15:47Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-26T03:18:25Z

Note that this needs for KEP, first.

### Comment by [@rochaporto](https://github.com/rochaporto) — 2024-11-26T08:10:55Z

> Note that this needs for KEP, first.

Should i help with this? Happy to join a meeting and discuss the use case in more detail if needed.

### Comment by [@Horiodino](https://github.com/Horiodino) — 2024-11-26T11:59:50Z

Hii ,Please let me know if there's an opportunity for me to assist or join any discussions related to this enhancement.

### Comment by [@asaiacai](https://github.com/asaiacai) — 2024-12-03T22:33:59Z

likewise, i am interested in this feature/enhancement.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-04T19:29:20Z

My first key question is the interface where we expose Worker clusters logs in the Management cluster. `kubectl logs`? dedicated Web console? or cli tools?

### Comment by [@Horiodino](https://github.com/Horiodino) — 2024-12-04T20:21:17Z

i believe we should expose a centralized API endpoint in the management cluster . This would allow tools like GitLab CI or Kubeflow to integrate easily without requiring direct access to worker clusters. Additionally, this approach would make it reliable and flexible for others to add a web console or CLI tools for log retrieval and interaction as needed. What you think !

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-04T20:41:15Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-04T20:47:17Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-02T20:52:04Z

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

### Comment by [@rochaporto](https://github.com/rochaporto) — 2025-06-03T06:59:28Z

/remove-lifecycle stale

This is still required, we can look into helping out with the implementation as well.

### Comment by [@tskillian](https://github.com/tskillian) — 2025-07-24T21:19:13Z

Looking beyond just logs - my company couldn't use multikueue because we also needed exec, attach, and metrics to be visible for each pod in the kubernetes cluster. What we did is combined usage of kueue with [virtual kubelet](https://virtual-kubelet.io/) and it's been working great so far - we're sharing thousands of GPU devices across clutster boundaries and virtual kubelet is such a good "drop in" replacement that most people don't even realize anything has changed for them.

I think using virtual kubelet in this matter would be a more "kubernetes" based approach - everything works just as if your pods were running on your cluster.

### Comment by [@rochaporto](https://github.com/rochaporto) — 2025-08-06T12:04:41Z

> Looking beyond just logs - my company couldn't use multikueue because we also needed exec, attach, and metrics to be visible for each pod in the kubernetes cluster. What we did is combined usage of kueue with [virtual kubelet](https://virtual-kubelet.io/) and it's been working great so far - we're sharing thousands of GPU devices across clutster boundaries and virtual kubelet is such a good "drop in" replacement that most people don't even realize anything has changed for them.
> 
> I think using virtual kubelet in this matter would be a more "kubernetes" based approach - everything works just as if your pods were running on your cluster.

Do you have more details on this setup? This was part of the initial discussion, to have a virtual kubelet like implementation that would expose logs/exec.

### Comment by [@donggrame](https://github.com/donggrame) — 2025-09-10T06:38:11Z

@tskillian Would you mind sharing the setup in detail?

### Comment by [@tskillian](https://github.com/tskillian) — 2025-09-10T14:20:23Z

Sure - happy to share more details on our setup.

At a high level, we have virtual kubelets (VK) running as an addon in manager clusters, where each VK represents a resource flavor that exists a worker cluster.

Kueue is responsible for scheduling pods to these VKs. Once a workload is admitted into a specific resource flavor by kueue, the corresponding pod(s) is scheduled onto the VK node. From there, our VK provider creates a corresponding "remote" pod in   the worker cluster and continuously syncs pod status back to the manager cluster.

Operationally, the VK provider serves as a proxy layer. For example:
- When Kubernetes queries logs, metrics, or issues an exec request, the VK just forwards those calls to the appropriate kubelet in the worker cluster.
- This means teams can continue using standard tooling (e.g., kubectl logs, kubectl exec, HPA, etc.) as if the workloads were running on the manager cluster, even though they’re actually running on the worker cluster.

This setup lets us cleanly separate concerns:
- Kueue handles queueing, fairness, and quota enforcement across all compute.
- Virtual Kubelets abstract away the multi-cluster execution.
- Teams don’t need to know which cluster their Pods are running on, it "just works".

We’ve been able to share over 10,000 GPUs across clusters with this setup, greatly increasing our utilization while still ensuring critical workloads get the compute they need before others.

Happy to share more details if it'd be helpful.

### Comment by [@donggrame](https://github.com/donggrame) — 2025-09-11T04:40:31Z

@tskillian 
Thanks for your input. It is already very helpful. I tried to replicate the environment and it just works as you said.

I also wonder if you use TAS (Topology Aware Scheduling) feature in Kueue. VK seems to aggregate all the nodes in a cluster into a single virtual kubelet which means Kueue has no information whatsoever about underlining topology of the VK cluster. Are you happened to have any workarounds, like creating VK for each node?

### Comment by [@tskillian](https://github.com/tskillian) — 2025-09-12T15:33:54Z

We basically collapse specific node pools into a single VK and do not currently use TAS, but you could have a VK per "physical" node too if you wanted so you could use TAS - just depends on how the VK provider is implemented.

You may also be able to "reverse" the direction here, where workloads are replicated to the worker cluster for TAS first and then after those pods are created there, corresponding pods are created/scheduled to the VK on the manager cluster to enable metrics/logs/etc..

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-11T15:34:35Z

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

### Comment by [@rochaporto](https://github.com/rochaporto) — 2025-12-11T15:41:07Z

We're still interested in this feature and can commit some resources to get it implemented.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:28:22Z

/area multikueue
/priority important-soon

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:28:35Z

cc @mwielgus

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:28:40Z

cc @mwysokin

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-18T09:03:18Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-18T09:21:01Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T10:15:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T08:05:56Z

/remove-lifecycle stale
