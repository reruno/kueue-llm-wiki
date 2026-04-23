# Issue #580: Leader election is not supported

**Summary**: Leader election is not supported

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/580

**Last updated**: 2023-03-03T13:40:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@fjding](https://github.com/fjding)
- **Created**: 2023-02-17T06:18:16Z
- **Updated**: 2023-03-03T13:40:59Z
- **Closed**: 2023-03-03T13:40:59Z
- **Labels**: `kind/bug`
- **Assignees**: [@fjding](https://github.com/fjding)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
![image](https://user-images.githubusercontent.com/21192363/219564224-8c1f9672-fcea-4fb9-9263-24ae8b502855.png)
I find the workload-scheduler start before leader election operation, it means only support deploy one instance?

**What you expected to happen**:

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-17T13:37:18Z

That's a good point, we should only start the scheduler once the leader was chosen.

I think the best way to implement  this is to make the scheduler controller an instance of `ctrl.Runnable` and add it to the manager through `mgr.Add()`, instead of starting a go routine explicitly.

And we should probably add an E2E test with leader election.

Do you mind taking any of these tasks?

### Comment by [@fjding](https://github.com/fjding) — 2023-02-17T13:51:43Z

OK, I am very happy to participate in this project and do some tasks, please assign it to me.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-17T14:14:48Z

Just type `/assign` in a comment

### Comment by [@fjding](https://github.com/fjding) — 2023-02-17T14:17:20Z

/assign

### Comment by [@fjding](https://github.com/fjding) — 2023-02-21T12:30:10Z

Hi，I have tried changing the scheduler to support 2 instance(the master and slave).  but it caused a lot of problems，such as when a job is created,  the workload will be created by two instances at the same time in  job-controller，and the  secondary  webhook server cannot be started, etc.
so I think if we want to make kueue support 2 instance, systematic design is required, but this may not be the most important at this stage。

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-21T16:37:41Z

Did you enable leader election through the component config? https://kueue.sigs.k8s.io/docs/installation/#install-a-custom-configured-released-version
IIUC, this should prevent two controllers that run through the manager to process objects.

Please make sure to use inclusive language when communicating in a CNCF project https://inclusivenaming.org/word-lists/tier-1/_master-slave/

### Comment by [@fjding](https://github.com/fjding) — 2023-02-22T03:06:05Z

> Did you enable leader election through the component config? https://kueue.sigs.k8s.io/docs/installation/#install-a-custom-configured-released-version IIUC, this should prevent two controllers that run through the manager to process objects.
> 
> Please make sure to use inclusive language when communicating in a CNCF project https://inclusivenaming.org/word-lists/tier-1/_master-slave/
I'm very sorry for my poor wording, I'll refer to the installation docs to support the Primary and Secondary instance

### Comment by [@fjding](https://github.com/fjding) — 2023-02-22T07:56:53Z

Hi, There is a difficult problem for which I don't have a good solution. When starting two instances, the webhook service thinks that both pods are ready and will distribute request traffic. but the secondary instance webhook server will not start in kueue-controller-manager, when  creating a clusterqueue, if the request traffic is forwarded to the secondary instance, the creation will fail

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-22T13:40:10Z

That's interesting. The service wouldn't direct traffic to a Pod unless the readiness check passes. This is defined here: https://github.com/kubernetes-sigs/kueue/blob/5bc814176b292e3f1a98175062a224e6a54ff0a4/config/components/manager/manager.yaml#L45

Are you saying that the manager doesn't start the webhooks when not leader, but reports as ready? I think the correct solution should be to start the webhooks regardless of leader status, as they are stateless.

### Comment by [@fjding](https://github.com/fjding) — 2023-02-27T07:48:08Z

> That's interesting. The service wouldn't direct traffic to a Pod unless the readiness check passes. This is defined here:
> 
> https://github.com/kubernetes-sigs/kueue/blob/5bc814176b292e3f1a98175062a224e6a54ff0a4/config/components/manager/manager.yaml#L45
> 
> Are you saying that the manager doesn't start the webhooks when not leader, but reports as ready? I think the correct solution should be to start the webhooks regardless of leader status, as they are stateless.

I have this problem in the release-0.2 branch test, but I found that the latest main branch, cert-controller has been upgraded from 0.3 to 0.6, and the webhook server can be started in two instance

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-27T13:34:23Z

In that case, we should just make sure only one kueue scheduler runs, right?

### Comment by [@fjding](https://github.com/fjding) — 2023-02-28T02:28:53Z

> In that case, we should just make sure only one kueue scheduler runs, right?

Yes
