# Issue #8440: [LWS] E2E tests for Rollout Strategy

**Summary**: [LWS] E2E tests for Rollout Strategy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8440

**Last updated**: 2026-04-09T17:09:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@anahas-redhat](https://github.com/anahas-redhat)
- **Created**: 2026-01-05T20:00:42Z
- **Updated**: 2026-04-09T17:09:09Z
- **Closed**: 2026-04-09T17:09:08Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**: I'd like to ask if E2E tests for Rollout Update can be added for LeaderWorkerSet.
I'm asking this because, by checking LeaderWorkerSet test suite - test/e2e/singlecluster/leaderworkerset_test.go - I was not able to find tests related to that.

**Why is this needed**: It's being described as a feature/concept of LWS [here](https://lws.sigs.k8s.io/docs/concepts/rollout-strategy/). I have manually checked this with [Kueue Operator ](https://github.com/openshift/kueue-operator)and, it seems to be working fine. 

Thank you.
cc @kannon92

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-05T20:13:59Z

How do you expect this feature to interact with Kueue?

### Comment by [@anahas-redhat](https://github.com/anahas-redhat) — 2026-01-05T20:26:45Z

My expectation was, when updating an LWS template in a Kueue-managed namespace, Kueue must smoothly handle the maxSurge replicas created during the rollout. Despite the sequential update (due to MaxUnavailable feature gate), the process of spinning up new pods/replicas and terminating old ones should be transparent. This includes Kueue successfully applying its labels and managing the pod lifecycle without interrupting the LWS update flow.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-05T20:34:28Z

I don't have an issue with adding a e2e test for this. Just know that MaxUnavailable may not be set on the kind clusters we run these e2e on.

### Comment by [@anahas-redhat](https://github.com/anahas-redhat) — 2026-01-05T22:06:59Z

@kannon92 yes, I was not planning to use MaxUnavailable even if we were testing only on OCP, because it's a Feature Gate (not available by default). 
So, that's why I mentioned the updates would be sequencial for now.

However, do you think this test adds some kind of value? If not, we can leave it for now.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:32:20Z

I'm ok with adding the tests, but I'm wondering what is not covered by this existing test: https://github.com/kubernetes-sigs/kueue/blob/72d70ff68a0cfb2cbe2a99d468e82215efcaaf82/test/e2e/singlecluster/leaderworkerset_test.go#L616-L625 which triggers replica replacements due to update of the image.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-08T22:34:12Z

@mimowo 

I think the idea is that LWS has a field called rolloutStrategy and the ask is to include a e2e test in kueue to reflect the interaction of this feature with Kueue.

The existing tests you mention do not change rolloutStrategy for LWS.

Now I don't necessary know if Kueue has to care about this.

@Edwinhr716 @kerthcet @ardaguclu 


workload reference:
```
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: leaderworkerset-rollout
spec:
  rolloutStrategy:
    type: RollingUpdate
    rollingUpdateConfiguration:
      maxUnavailable: 2
      maxSurge: 2
  replicas: 4
  leaderWorkerTemplate:
    size: 4
    workerTemplate:
      spec:
        containers:
        - name: nginx
          image: nginxinc/nginx-unprivileged:1.27
          resources:
            limits:
              cpu: "100m"
            requests:
              cpu: "50m"
          ports:
          - containerPort: 8080
   ```

### Comment by [@Edwinhr716](https://github.com/Edwinhr716) — 2026-01-09T03:49:53Z

FYI maxUnavailable is enabled by default on clusters 1.35+ since it was graduated to Beta

### Comment by [@anahas-redhat](https://github.com/anahas-redhat) — 2026-01-09T14:35:10Z

@Edwinhr716  as of now, there are no OCP versions that support Kubernetes 1.35+. Since our goal is to validate this against OCP versions supported by Kueue as well, we wouldn't be able to count with this feature gate enabled in this moment.

Do you think this is a problem? Or, can we go ahead and try to implement this test?s?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-09T14:38:12Z

For upstream our e2e tests are based on Kind so I don't think there is any reason to consider OCP here.

I'm not actually sure if we have 1.35 yet running in Kueue CI.

### Comment by [@anahas-redhat](https://github.com/anahas-redhat) — 2026-01-09T15:37:09Z

Thanks for the response, Kevin.

I’m raising this because, for the Kueue Operator downstream, we execute tests on OCP. I know that OCP is not really a concern for upstream but, the MaxUnavailableStatefulSet feature gate creates a compatibility gap for our CI.

Specifically:

- MaxUnavailableStatefulSet is introduced in Kubernetes 1.35.
- OCP 4.21 will likely be based on Kubernetes 1.34, meaning this feature won't be available in our current downstream environments.
- If we automate E2E tests relying on this gate, they will pass in Kind (upstream) but fail in OCP (downstream).

What would be the recommendation in this case? I was thinking of not using this feature gate for now. The downside is that we won't be able to execute updates in parallel, but it ensures the suite remains portable. 
Alternatively, we could hold these specific test cases until OCP catches up to 1.35.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-09T16:24:23Z

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

### Comment by [@anahas-redhat](https://github.com/anahas-redhat) — 2026-04-09T17:09:02Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-09T17:09:09Z

@anahas-redhat: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8440#issuecomment-4216075642):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
