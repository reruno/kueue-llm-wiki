# Issue #70: Make the GPU a prime citizen in kueue

**Summary**: Make the GPU a prime citizen in kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/70

**Last updated**: 2022-02-25T15:00:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@zvonkok](https://github.com/zvonkok)
- **Created**: 2022-02-25T09:55:13Z
- **Updated**: 2022-02-25T15:00:26Z
- **Closed**: 2022-02-25T14:59:53Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 3

## Description

Hello fellow HPC and batch enthusiasts, I have read your public doc with much interest and I have seen that the GPU is mentioned a couple of times. To make kueue and GPUs a success story I think we need to align the requirements that kueue needs for scheduling with our k8s stack which should expose the right information that you need to make the right scheduling decisions. 

There are dedicated GPUs, MIG slices, vGPU either time shared or MIG backed, those are all features that need to be taken into consideration. Going further if we're doing multi-node with MPI and such, we need to think also about network topologies and node interconnects. You may rather use nodes that have GPUDirect enabled than nodes that have "only" a GPU with a slow ethernet connection. 

I am one of the tech-leads for accelerator enablement on Kubernetes at NVIDIA and I am happy to help to move this forward.

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-25T11:11:22Z

Thanks. We are glad that you are interested in this project.  I'm also doing some work on managing and scheduling accelerator (like GPU/MIG/vGPU/NPU) in Kubernetes. These are very import in Batch System. I'm looking forward to working together in the future to move Kueue forward.

> Going further if we're doing multi-node with MPI and such, we need to think also about network topologies and node interconnects.

Kueue is currently not node-aware. I'm not sure it's possible to do some things like topologies and node interconnects. This feels more like the work to do in the scheduler. Can you share more details of your idea? Thanks

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-25T14:59:42Z

Correct, this feature request fits more in kube-scheduler and kubelet.

The perfect venue to discuss these ideas is the wg-batch https://github.com/kubernetes/community/tree/master/wg-batch

Hopefully we will set up a meeting today.

In the meantime, better open an issue in github.com/kubernetes/kubernetes

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-02-25T14:59:53Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/70#issuecomment-1050927588):

>Correct, this discussion fits more in kube-scheduler and kubelet.
>
>The perfect venue to discuss these ideas is the wg-batch https://github.com/kubernetes/community/tree/master/wg-batch
>
>Hopefully we will set up a meeting today.
>
>In the meantime, better open an issue in github.com/kubernetes/kubernetes
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
