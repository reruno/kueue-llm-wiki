# Issue #499: custom workload

**Summary**: custom workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/499

**Last updated**: 2023-01-11T13:23:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@talcoh2x](https://github.com/talcoh2x)
- **Created**: 2022-12-30T15:11:05Z
- **Updated**: 2023-01-11T13:23:35Z
- **Closed**: 2023-01-11T13:23:34Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 6

## Description

Hi, we are looking for exactly such solution for managing and utilize large scale cluster with "batch" workload.
As i understand (and correct me if I'm wrong ) kueue still not fully integrated with kubeflow(training operator)/MpiJob.
what I'm try to understand first is:
- if there is support of kueue  with kubeflow(training operator)/MpiJob 
- if not, what can we do from our side (not from kubeflow(training operator)/MpiJob ) to make it work. to make kueue work with those 
CRD.
- we have resources name habana.ai/<xx> . as I saw you have supports for any compute resource name right ?
- we have the option to configure "kueue" in some way to control on the priority of the queue or the order inside the queue ?

we are working with PodGroup so what really interesting us is "queue  control" step before the workload get into the scheduler ( I think that exactly what your doing here). my concern is how to do the integration with other CRD and how can I "extend" our reqirments into kueue.
for example in k8 scheduler we extended preFilter/Filter and score with plugins that related to our clusters requirement wondering how it will work here

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-03T13:22:37Z

Hello,
There is currently no support for kubeflow jobs.
The first step to support them is to add a [suspend field similar to Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/#suspending-a-job). If you are interested in working on this, the kubeflow community is already receptive to the idea https://github.com/kubeflow/training-operator/issues/1519
You can do the same in MPIJob v2 https://github.com/kubeflow/mpi-operator/ (FWIIW, I'm a reviewer in this project).

For your own resources, you would have to do the same: add a suspend field.

Then, you write small controllers that translate the logic from your CRD (or kubeflow's) into a Workload object, similar to our job-controller https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/workload/job/job_controller.go
This controller doesn't have to be part of the kueue repo. It could be it's own binary. But we will accept controllers in the main repo for widely use APIs such as kubeflow #65
This is an advantage of Kueue in comparison to the approach of having plugins: There is no need to recompile kueue to add support for more objects, just add these small controller in the cluster.

Kueue supports priority. In the case of batch/Job, priority comes from the priority set in the pod template. You can define priority for your CRDs as you wish (adding a field, an annotation or simply using the pod priority too).

### Comment by [@talcoh2x](https://github.com/talcoh2x) — 2023-01-10T16:18:47Z

Hi thanks for your inputs! 
i have one more question, do we have an option to extend kueue in a similar way to k8s scheduler e.g: "filter", "pre-filter" ...
for example - 
to prioritize PODGroup with minMember > 5
or
to prioritize POD with LABEL X/Y ... 
?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-10T18:19:51Z

This was suggested in #10, but there is no progress. We probably should gather more feedback before committing to such thing.

In your examples, could you add priorities to the job templates in a webhook or something like that?

### Comment by [@talcoh2x](https://github.com/talcoh2x) — 2023-01-11T07:12:39Z

Yes, we set different priority (we have around 3 4 different priority) for different use cases, that will work i believe. I just checking how we can "extend" and modify the queue as we want without to changed the code only by adding as "extender"/"plugin".
it will give us the flexibility we need. 

I'll continue follow https://github.com/kubernetes-sigs/kueue/issues/10

thank you! hope also we will join to the effort here

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-11T13:23:31Z

Let's close this issue and continue discussions in the already opened issues.

Feel free to open more if you have other feedback.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-01-11T13:23:35Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/499#issuecomment-1378747323):

>Let's close this issue and continue discussions in the already opened issues.
>
>Feel free to open more if you have other feedback.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
