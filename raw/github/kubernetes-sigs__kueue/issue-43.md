# Issue #43: Consider a diff image for testing/samples

**Summary**: Consider a diff image for testing/samples

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/43

**Last updated**: 2022-02-22T17:15:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Created**: 2022-02-21T22:15:50Z
- **Updated**: 2022-02-22T17:15:17Z
- **Closed**: 2022-02-22T17:15:17Z
- **Labels**: `kind/test`
- **Assignees**: _none_
- **Comments**: 6

## Description

I am running into 
```bash
  Warning  Failed     11s   kubelet            Failed to pull image "perl": rpc error: code = Unknown desc = reading manifest latest in docker.io/library/perl: toomanyrequests: You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limit
```
we might want to consider an image out of a diff registry to avoid this unfortunate error 

/kind test

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-02-21T22:15:51Z

@ArangoGutierrez: The label(s) `kind/testing` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/43):

>I am running into 
>```bash
>  Warning  Failed     11s   kubelet            Failed to pull image "perl": rpc error: code = Unknown desc = reading manifest latest in docker.io/library/perl: toomanyrequests: You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limit
>```
>we might want to consider an image out of a diff registry to avoid this unfortunate error 
>
>/kind testing


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-21T22:16:34Z

/kind test

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-21T22:23:06Z

I have this one :

- `quay.io/eduardoarango/pi:ubi8`

This is the repo -> https://github.com/ArangoGutierrez/Pi

```bash
[eduardo@fedora kueue]$ kubectl logs sample-job--1-24kpr

 1000 trials, pi is 3.120000 
```
The *sample-job.yaml* looks like

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  annotations:
    kueue.x-k8s.io/queue-name: main
spec:
  parallelism: 3
  completions: 30
  suspend: true
  template:
    spec:
      containers:
      - name: pi
        image: quay.io/eduardoarango/pi:ubi8
        command: ["pi",  "1000"]
        resources:
          requests:
            cpu: 1
            memory: "200Mi"
          limits:
            cpu: 1
            memory: "200Mi"
      restartPolicy: Never
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T15:12:34Z

Use `gcr.io/k8s-staging-perf-tests/sleep:latest`

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-22T15:39:51Z

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  annotations:
    kueue.x-k8s.io/queue-name: main
spec:
  parallelism: 3
  completions: 3
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:latest
        command: ["sleep",  "30"]
        resources:
          requests:
            cpu: 1
            memory: "200Mi"
          limits:
            cpu: 1
            memory: "200Mi"
      restartPolicy: Never
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T16:32:54Z

lgtm
