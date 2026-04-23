# Issue #1527: kueue prevents non-kueue jobs from running

**Summary**: kueue prevents non-kueue jobs from running

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1527

**Last updated**: 2024-01-02T20:13:54Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@stevenBorisko](https://github.com/stevenBorisko)
- **Created**: 2023-12-28T18:13:27Z
- **Updated**: 2024-01-02T20:13:54Z
- **Closed**: 2024-01-02T20:12:16Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When I create a job without the localqueue annotation in the default namespace, the job gets suspended and never runs/completes (stays in pending).

**What you expected to happen**:
When I create a job without the localqueue annotation in the default namespace, the job runs immediately.

**How to reproduce it (as minimally and precisely as possible)**:
files uploaded (github won't let me upload yamls, so i appended `.txt` to them -- change them back with `for f in *.*.txt; do mv ${f} ${f%.*}; done`):
- [bug.yaml.txt](https://github.com/kubernetes-sigs/kueue/files/13788564/bug.yaml.txt): two jobs -- one that succeeds and one that does not
- [gets-admitted.txt](https://github.com/kubernetes-sigs/kueue/files/13788565/gets-admitted.txt): output of `kubectl -n bug describe jobs gets-admitted` (job from bug.yaml)
- [gets-suspended.txt](https://github.com/kubernetes-sigs/kueue/files/13788566/gets-suspended.txt): output of `kubectl describe jobs gets-suspended` (job from bug.yaml)
- [queue.yaml.txt](https://github.com/kubernetes-sigs/kueue/files/13788567/queue.yaml.txt): flavor, clusterqueue, and localqueue
- [repro.sh.txt](https://github.com/kubernetes-sigs/kueue/files/13788568/repro.sh.txt): steps to reproduce (create cluster, install kueue, create flavor/clusterqueues/localqueue, and submit/check jobs)

output summary (`gets-*.txt`): gets-admitted is a job that has the localqueue annotation and gets admitted while gets-suspended is a job that omits the bug namespace and localqueue annotation and never leaves pending.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
  - Client Version: v1.28.2
  - Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
  - Server Version: v1.27.3-gke.100
- Kueue version (use `git describe --tags --dirty --always`): v0.5.1
- Cloud provider or hardware configuration:
  - GKE on GCP
  - default node pool (3 e2-medium)
  - custom node pool (3 n2-standard-4)
- OS (e.g: `cat /etc/os-release`):
  - my machine: Debian GNU/Linux rodete
  - worker nodes: [gke-1273-gke100-cos-105-17412-101-24-c-pre](https://cloud.google.com/container-optimized-os/docs/release-notes/m105#cos-105-17412-101-24_)
- Kernel (e.g. `uname -a`):
  - my machine: 6.5.6-1rodete4-amd64
  - worker nodes: 5.15.109+
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-29T08:23:45Z

@stevenBorisko Can you share the `kueue-manager-config` ConfigMap resource deployed under the kueue-system namespace?

That behavior would be expected if `manageJobsWithoutQueueName` is `true`.

### Comment by [@stevenBorisko](https://github.com/stevenBorisko) — 2024-01-02T16:02:00Z

@tenzen-y it is identical to [this one](https://github.com/kubernetes-sigs/kueue/blob/v0.5.1/config/components/manager/controller_manager_config.yaml). I see the `manageJobsWithoutQueueName: true` line is commented -- I would assume that means true is the default value? If so, then nevermind -- like you said this is working as intended.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-02T18:53:10Z

> @tenzen-y it is identical to [this one](https://github.com/kubernetes-sigs/kueue/blob/v0.5.1/config/components/manager/controller_manager_config.yaml). I see the `manageJobsWithoutQueueName: true` line is commented -- I would assume that means true is the default value? If so, then nevermind -- like you said this is working as intended.

The `manageJobsWithoutQueueName` is false by default:

https://kueue.sigs.k8s.io/docs/reference/kueue-config.v1beta1/#Configuration

So, could you check if a workload resource was created against the job resource?

### Comment by [@stevenBorisko](https://github.com/stevenBorisko) — 2024-01-02T20:11:57Z

> > @tenzen-y it is identical to [this one](https://github.com/kubernetes-sigs/kueue/blob/v0.5.1/config/components/manager/controller_manager_config.yaml). I see the `manageJobsWithoutQueueName: true` line is commented -- I would assume that means true is the default value? If so, then nevermind -- like you said this is working as intended.
> 
> The `manageJobsWithoutQueueName` is false by default:
> 
> https://kueue.sigs.k8s.io/docs/reference/kueue-config.v1beta1/#Configuration
> 
> So, could you check if a workload resource was created against the job resource?

When I responded to the "share the kueue-manager-config configmap" question, I was experimenting around with some different ones I found online and I think I had forgot to delete/recreate the controller manager pod. I just destroyed my cluster and recreated/retried and now `manageJobsWithoutQueueName` is false and the `gets-suspended` job that wasn't working before now gets completed.

Sorry for the confusion, and thank you for helping out!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-02T20:13:53Z

> > > @tenzen-y it is identical to [this one](https://github.com/kubernetes-sigs/kueue/blob/v0.5.1/config/components/manager/controller_manager_config.yaml). I see the `manageJobsWithoutQueueName: true` line is commented -- I would assume that means true is the default value? If so, then nevermind -- like you said this is working as intended.
> > 
> > 
> > The `manageJobsWithoutQueueName` is false by default:
> > https://kueue.sigs.k8s.io/docs/reference/kueue-config.v1beta1/#Configuration
> > So, could you check if a workload resource was created against the job resource?
> 
> When I responded to the "share the kueue-manager-config configmap" question, I was experimenting around with some different ones I found online and I think I had forgot to delete/recreate the controller manager pod. I just destroyed my cluster and recreated/retried and now `manageJobsWithoutQueueName` is false and the `gets-suspended` job that wasn't working before now gets completed.
> 
> Sorry for the confusion, and thank you for helping out!

No problem :)
If you face any other problems, feel free to open new issues :)
