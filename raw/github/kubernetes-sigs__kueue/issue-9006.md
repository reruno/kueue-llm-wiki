# Issue #9006: periodic-kueue-test-e2e-k8s-main-was  is failing

**Summary**: periodic-kueue-test-e2e-k8s-main-was  is failing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9006

**Last updated**: 2026-02-06T10:32:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-05T14:41:20Z
- **Updated**: 2026-02-06T10:32:34Z
- **Closed**: 2026-02-06T10:32:34Z
- **Labels**: `kind/bug`, `kind/failing-test`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
periodic-kueue-test-e2e-k8s-main-was is failing 
**What you expected to happen**:
not failing 
**How to reproduce it (as minimally and precisely as possible)**:
https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-e2e-k8s-main-was
**Anything else we need to know?**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-k8s-main-was/2019369300455854080


```
Loading image 'us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.17.0-devel-71-g7210ffd8e' to cluster 'kind'
  Loading image to node: kind-worker
Error response from daemon: reference does not exist
ctr: unrecognized image format
Failed to load image 'us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.17.0-devel-71-g7210ffd8e' to node 'kind-worker'
Switched to context "kind-kind".
Exporting logs for cluster "kind" to:
/logs/artifacts/run-test-e2e-k8s-main-was
No resources found in kueue-system namespace.
No resources found in default namespace.
Switched to context "kind-kind".
Deleting cluster "kind" ...
Deleted nodes: ["kind-worker" "kind-worker2" "kind-control-plane"]
make: *** [Makefile-test.mk:307: run-test-e2e-k8s-main-was] Error 1
+ EXIT_VALUE=2
+ set +o xtrace
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-05T14:41:29Z

/kind failing-test

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-05T14:42:34Z

cc @IrvingMg ptal

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-05T15:31:54Z

/assign
