# Issue #4215: workload.codeflare.dev/appwrapper unsupported value

**Summary**: workload.codeflare.dev/appwrapper unsupported value

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4215

**Last updated**: 2025-02-24T07:21:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2025-02-10T20:31:55Z
- **Updated**: 2025-02-24T07:21:00Z
- **Closed**: 2025-02-24T07:20:58Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description


**What happened**:

I failed to install kueue using helm.
I followed the instructions on the readme and the controller didn't start with the following error:

`{"level":"error","ts":"2025-02-10T20:20:50.432349454Z","logger":"setup","caller":"kueue/main.go:120","msg":"Unable to load the configuration","error":"integrations.frameworks[9]: Unsupported value: \"workload.codeflare.dev/appwrapper\": supported values: \"batch/job\", \"deployment\", \"jobset.x-k8s.io/jobset\", \"kubeflow.org/mpijob\", \"kubeflow.org/mxjob\", \"kubeflow.org/paddlejob\", \"kubeflow.org/pytorchjob\", \"kubeflow.org/tfjob\", \"kubeflow.org/xgboostjob\", \"pod\", \"ray.io/raycluster\", \"ray.io/rayjob\", \"statefulset\"","errorCauses":[{"error":"integrations.frameworks[9]: Unsupported value: \"workload.codeflare.dev/appwrapper\": supported values: \"batch/job\", \"deployment\", \"jobset.x-k8s.io/jobset\", \"kubeflow.org/mpijob\", \"kubeflow.org/mxjob\", \"kubeflow.org/paddlejob\", \"kubeflow.org/pytorchjob\", \"kubeflow.org/tfjob\", \"kubeflow.org/xgboostjob\", \"pod\", \"ray.io/raycluster\", \"ray.io/rayjob\", \"statefulset\""}],"stacktrace":"main.main\n\t/workspace/cmd/kueue/main.go:120\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:272"}
`

**What you expected to happen**:

Installation to complete successfully.

**How to reproduce it (as minimally and precisely as possible)**:

Install using helm by following the kueue readme.

**Anything else we need to know?**:

After commenting out the "workload.codeflare.dev/appwrapper" line from the values file the installation completed successfully.

**Environment**:
- Kubernetes version (use `kubectl version`):

Server Version: version.Info{Major:"1", Minor:"31", GitVersion:"v1.31.2", GitCommit:"5864a4677267e6adeae276ad85882a8714d69d9d", GitTreeState:"clean", BuildDate:"2024-11-08T19:38:46Z", GoVersion:"go1.22.8", Compiler:"gc", Platform:"linux/amd64"}


- Kueue version (use `git describe --tags --dirty --always`):
v0.11.0-devel-148-g3755065c-dirty

- Cloud provider or hardware configuration:
kind cluster

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T07:30:12Z

> I followed the instructions on the readme ...

Do you mean the installation instructions? 

Note that appwrapper is not released yet, so 0.10.1 version of Kueue does not have it. It will be released in 0.11.0 for the first time. If you want to test it you need to install a staging version (either by manifest or helm).

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-02-11T08:35:47Z

| Do you mean the installation instructions? 

yes - https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/README.md

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T08:39:59Z

I see, try something like 
`helm install kueue oci://us-central1-docker.pkg.dev/k8s-staging-images/charts/kueue --version="v20250211-v0.11.0-devel-156-g21af73b2" --create-namespace --namespace=kueue-system` (latest main build).

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-23T20:08:24Z

And if you are using the main's branch for the values. You will need to remove appwrapper from the supported frameworks.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-24T07:20:54Z

/close
We already have e2e tests on the main branch: https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/singlecluster/appwrapper_test.go.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-24T07:20:58Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4215#issuecomment-2677603667):

>/close
>We already have e2e tests on the main branch: https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/singlecluster/appwrapper_test.go. 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
