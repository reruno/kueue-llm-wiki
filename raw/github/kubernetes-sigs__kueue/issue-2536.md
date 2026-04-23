# Issue #2536: Automatic Workload Creation

**Summary**: Automatic Workload Creation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2536

**Last updated**: 2024-07-08T07:38:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@m-mamdouhi](https://github.com/m-mamdouhi)
- **Created**: 2024-07-04T14:32:25Z
- **Updated**: 2024-07-08T07:38:29Z
- **Closed**: 2024-07-05T09:49:06Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 6

## Description

is there a way for kueue to make workloads for kubeflow jobs? I know for batch job kueue automatically creates the workload but how to do it with other jobs is not clarified in the documentation. just adding the label to the manifest doesn't seem to be creating the workload automatically then creating the job.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-07-04T22:43:35Z

Hi we have a couple of guides relating  to kubeflow jobs [here](https://kueue.sigs.k8s.io/docs/tasks/run/kubeflow/), please make sure you follow the [administer cluster quotas](https://kueue.sigs.k8s.io/docs/tasks/manage/administer_cluster_quotas/) guide before creating the kubefflow jobs.

### Comment by [@m-mamdouhi](https://github.com/m-mamdouhi) — 2024-07-05T07:39:11Z

I have done all the steps of the guide several times, but the problem is that for any job that isn't a Batch/v1 job the workload doesn't get created. 
I looked into the controller_manager_config.yaml as well and the name is already added ( I want to deploy kubeflow and xgboost). Is there a step besides the guide that I have to do? 
because it works perfectly well with Batch jobs just not any other job.
any help would be very much appreciated

### Comment by [@trasc](https://github.com/trasc) — 2024-07-05T09:02:47Z

Can you check the logs of the kueue's controller manager?

### Comment by [@m-mamdouhi](https://github.com/m-mamdouhi) — 2024-07-05T09:48:52Z

I found the issue to be a misconfiguration on my part in the helm installation using crossplane. 
I managed to fix it.  Thanks @trasc for responding and trying to help me out!

### Comment by [@pgn-dev](https://github.com/pgn-dev) — 2024-07-06T06:15:01Z

@m-mamdouhi would you mind sharing what was the misconfiguration?

### Comment by [@m-mamdouhi](https://github.com/m-mamdouhi) — 2024-07-08T07:38:11Z

@pgn-dev it was one (or both) of these two things not sure which:
1. the naming of the cluster to be created by crossplane was too long so the workloads weren't being created.
2. I had not correctly added the name of a custom workload configuration to the external integration framework
