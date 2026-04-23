# Issue #6889: [flaky e2e tests] due to: error: timed out waiting for the condition on deployments/kubeflow-trainer-controller-manager

**Summary**: [flaky e2e tests] due to: error: timed out waiting for the condition on deployments/kubeflow-trainer-controller-manager

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6889

**Last updated**: 2025-09-18T10:48:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-17T11:37:06Z
- **Updated**: 2025-09-18T10:48:05Z
- **Closed**: 2025-09-18T10:01:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

failures on unreleated branches, eg https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6876/pull-kueue-test-e2e-main-1-33/1968272284959379456

**What you expected to happen**:
no failures
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
secret/kubeflow-trainer-webhook-cert serverside-applied
service/kubeflow-trainer-controller-manager serverside-applied
deployment.apps/kubeflow-trainer-controller-manager serverside-applied
validatingwebhookconfiguration.admissionregistration.k8s.io/validator.trainer.kubeflow.org serverside-applied
error: timed out waiting for the condition on deployments/kubeflow-trainer-controller-manager
Switched to context "kind-kind".
Exporting logs for cluster "kind" to:
/logs/artifacts/run-test-e2e-singlecluster-1.33.4
No resources found in kueue-system namespace.
No resources found in default namespace.
Deleting cluster "kind" ...
Deleted nodes: ["kind-control-plane" "kind-worker" "kind-worker2"]
make: *** [Makefile-test.mk:135: run-test-e2e-singlecluster-1.33.4] Error 1
+ EXIT_VALUE=2
+ set +o xtrace
Cleaning up after docker in docker.
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T11:37:14Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T11:38:17Z

cc @kaisoz @mbobrovskyi this "error: timed out waiting for the condition on deployments/kubeflow-trainer-controller-manager" suggests some timeout when starting the controller. I'm wondering if bumping the timeout could help.

Also, we may need to revisit the resources on the infra, maybe we need to increase 10 to 12 CPU?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T11:40:04Z

This seems related to the recently merged https://github.com/kubernetes-sigs/kueue/pull/6597. 

It does not seem to fail very often, so probably no reason to revert, but it would be good to prioritize fixing, as it may be affecting all branches before the release

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T11:42:14Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6876/pull-kueue-test-e2e-multikueue-main/1968272285160706048

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-17T12:21:47Z

/assign

I have a hunch, let me have a look

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-17T13:31:26Z

Is this related to [https://github.com/kubernetes-sigs/kueue/issues/6879?](https://github.com/kubernetes-sigs/kueue/issues/6879?%E2%80%9D)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T10:48:05Z

> Is this related to [https://github.com/kubernetes-sigs/kueue/issues/6879?](https://github.com/kubernetes-sigs/kueue/issues/6879?%E2%80%9D)

I think these were duplicates, closed the other too after https://github.com/kubernetes-sigs/kueue/pull/6909
