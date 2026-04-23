# Issue #757: The suspend=true added to the job by the default job webhook has not taken effect.

**Summary**: The suspend=true added to the job by the default job webhook has not taken effect.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/757

**Last updated**: 2023-05-11T15:35:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@fjding](https://github.com/fjding)
- **Created**: 2023-05-09T13:05:16Z
- **Updated**: 2023-05-11T15:35:04Z
- **Closed**: 2023-05-11T15:35:04Z
- **Labels**: `kind/bug`
- **Assignees**: [@fjding](https://github.com/fjding)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When I create a job that contains one pod, occasionally the following situation will occur. Two pods will be created at the same time. The status of one pod is Terminating, and the status of the other pod is Pending. I think the Terminating pod should not be created
![image](https://github.com/kubernetes-sigs/kueue/assets/21192363/a97bdc58-798d-4d3f-a777-307a93f0a8d1)
**What you expected to happen**:
I think the suspend=true added to the job by the default job webhook has not taken effect.
![image](https://github.com/kubernetes-sigs/kueue/assets/21192363/19d58291-7391-4f17-b9b7-e10707cda99c)

The address of the job object is different from the address of &Job{*job}. I added a test case for testing, and it is true, so the suspend=true added here will not take effect.

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-09T13:21:47Z

Seems like there are two things going on:

1) suspend field is not set for webhook.

2) https://github.com/kubernetes/enhancements/issues/3939 - Is a KEP to fix the terminating/pending issue

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-09T13:22:16Z

Would either of you mind sending a fix for 1?

This needs to be backported.

### Comment by [@fjding](https://github.com/fjding) — 2023-05-09T14:16:18Z

> Would either of you mind sending a fix for 1?
> 
> This needs to be backported.

Ok， I am glad to do it

### Comment by [@fjding](https://github.com/fjding) — 2023-05-09T14:18:51Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-10T12:16:21Z

@alculquicondor I think this bug is critical. Should we create a patch release?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-10T15:30:37Z

I think so. Let's get the PR merged and cherry-picked.
