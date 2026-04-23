# Issue #590: Kueue deletes workloads for jobs with limits, but no requests

**Summary**: Kueue deletes workloads for jobs with limits, but no requests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/590

**Last updated**: 2023-03-17T21:27:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-02-21T14:47:14Z
- **Updated**: 2023-03-17T21:27:18Z
- **Closed**: 2023-03-17T21:27:18Z
- **Labels**: `kind/bug`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
**What happened**:

Kueue creates and deletes in a loop (the cycle is <1s) a workload for a job with limits, but without requests.

**What you expected to happen**:

Kueue does not delete the workloads and allows the jobs to complete.

**How to reproduce it (as minimally and precisely as possible)**:

0. Setup Kueue with the `main` local queue
1. Create a job from the yaml
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-longrun-only-limits
  annotations:
    kueue.x-k8s.io/queue-name: main
spec:
  suspend: true
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: job-longrun
        image: centos:7
        resources:
          limits:
            cpu: 100m
            memory: "200Mi"
        command: ["bash"]
        args: ["-c", 'sleep 120 && echo "Hello world"']
        imagePullPolicy: IfNotPresent
  backoffLimit: 0
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): master (before 1.27)
- Kueue version (use `git describe --tags --dirty --always`): master (before 0.3.0)
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-21T16:42:24Z

This was introduced in https://github.com/kubernetes-sigs/kueue/pull/317.

We need to fix by changing the logic that matches a Workload and a Job. This logic should be included in the job integration library, maybe at the podtemplate level. cc @kerthcet 

We should also have an integration test.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-27T02:50:50Z

/assign
Let me fix this at first.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-27T10:43:09Z

I'd like to default the container again then process deepEqual. See https://github.com/kubernetes-sigs/kueue/pull/597
