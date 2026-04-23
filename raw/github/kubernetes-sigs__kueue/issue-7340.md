# Issue #7340: Make sure all e2e tests use valid images

**Summary**: Make sure all e2e tests use valid images

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7340

**Last updated**: 2025-11-06T22:52:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-22T07:53:52Z
- **Updated**: 2025-11-06T22:52:53Z
- **Closed**: 2025-11-06T22:52:53Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description


**What happened**:

Some e2e tests, eg metrics_test.go test/e2e/singlecluster/metrics_test.go are using images which cannot be pull. All such occurences should be replaced with the valid Agnhost image.

**What you expected to happen**:

No such lines in the logs: 
```
Oct 21 20:10:48 kind-worker kubelet[221]: E1021 20:10:48.335028     221 log.go:32] "PullImage from image service failed" err="rpc error: code = Unknown desc = failed to pull and unpack image \"docker.io/library/pause:latest\": failed to resolve reference \"docker.io/library/pause:latest\": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed" image="pause:latest"
Oct 21 20:10:48 kind-worker kubelet[221]: E1021 20:10:48.335118     221 kuberuntime_image.go:43] "Failed to pull image" err="failed to pull and unpack image \"docker.io/library/pause:latest\": failed to resolve reference \"docker.io/library/pause:latest\": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed" image="pause:latest"

```

**How to reproduce it (as minimally and precisely as possible)**:

CI: https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-34/1980723728153055232/artifacts/run-test-e2e-singlecluster-1.34.0/kind-worker/kubelet.log

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-22T07:54:45Z

cc @mykysha @mbobrovskyi

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-05T13:51:45Z

/assign
