# Issue #4266: kueue-controller-manager failed to list *v1beta1.Workload

**Summary**: kueue-controller-manager failed to list *v1beta1.Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4266

**Last updated**: 2025-02-18T07:07:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kalki7](https://github.com/kalki7)
- **Created**: 2025-02-16T13:52:56Z
- **Updated**: 2025-02-18T07:07:57Z
- **Closed**: 2025-02-18T06:52:13Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 9

## Description


**What happened**: After running a few hundred thousand jobs using kueue, hosted on a GKE Cluster, the kueue-controller-manager started throwing this error 

```""Unhandled Error" err="sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: Failed to watch *v1beta1.Workload: failed to list *v1beta1.Workload: the server was unable to return a response in the time allotted, but may still be processing the request (get workloads.kueue.x-k8s.io)" logger="UnhandledError""```

Upon trying to list all the workloads, I got the following error

```Error from server: rpc error: code = ResourceExhausted desc = grpc: trying to send message larger than max (2240131343 vs. 2147483647)```

I presume that this is because of the limit set by the GKE Cluster. But even after iterating through the workloads in batches and deleting them off, and restarting kueue, the kueue-controller-manager (manager container) is still in an unready status with the aforementioned error.


**What you expected to happen**: Schedule the jobs as per usual

**How to reproduce it (as minimally and precisely as possible)**: Run over 250K jobs

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
`Client Version: v1.30.6-dispatcher
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.30.8-gke.1261000`
- Kueue version (use `git describe --tags --dirty --always`): v0.10.0
- Cloud provider or hardware configuration: GCP Managed Kubernetes Engine - GKE
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-16T19:19:33Z

Are you using multikueue?

And how many jobs are actually still active?

If you are running batch jobs, I wonder if using ttlAfterFinished would help?

### Comment by [@kalki7](https://github.com/kalki7) — 2025-02-17T03:35:31Z

We're not using multikueue, at the moment there are no jobs active, purged them all. The ttlAfterFinished was set to 3s. 

When we list jobs, we get `None` but when we list workloads we see a whole lot of data. To delete this, we require kueue-controller-manager. But since there's the rpc limit of 2gb, the health check fails.

I think we've caused a deadlock situation.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-17T07:58:46Z

IIUC Kueue was able to operate until restart because it is using the List and Watch pattern - it listed when there was few workloads, then it just kept observing the new. After restart it was not able to list them all again as the volume of data exceeded 2gb.

So, IIUC at this point is not just an issue with Kueue. You may check if `kubectl get workload` but I suspect it may not work as the data already exceeds 2gb. 

To recover I think you can try (but I haven't myself):
1. list the workloads in chunks and delete them one-by-one, `kubectl get wl --chunk-size=1000` and probably pipe with kubectl delete command, similarly as done [here](https://github.com/kubernetes/kubectl/issues/866#issuecomment-638432674). I believe this does not require kube-controller-manager as the kubectl commands should directly talk to API server. You can also add filtering to not touch some of the still important workloads.
2. use DeleteCollection command which has limits, like we do [here](https://github.com/kubernetes/kubernetes/blob/87fcae2bc765e4f752bcf7dfbd0c57f75ec751a3/test/integration/job/job_test.go#L3584)

In the longer run, we are planning to add a feature to Kueue for GCing finished workloads https://github.com/kubernetes-sigs/kueue/pull/2686. Take a look if this is what would help you to prevent such situations in the long run. cc @mwysokin

### Comment by [@kalki7](https://github.com/kalki7) — 2025-02-17T12:10:16Z

Hey @mimowo, yes I've tried the chunking, which works but the kubectl delete is what isn't working as expected.

I've tried deleting one workload to begin with, the command returns deleted, even proxying with kubectl and using the delete apis returns successful 200 status. But the workload is still present there. Even tried --force

I've tried deleting it in every possible way (that I know of), but they're not getting deleted. Hence, I presumed that we'd require the kueue-controller-manager to delete them.

Kindly advise if there might be something I'm missing or if I'm off track entirely.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-17T12:47:09Z

Ah, this might be because the workloads have finalizers. If this is the case you need to send a patch per workload to delete.

You can probably adjust the commands here: https://stackoverflow.com/questions/52819428/remove-kubernetes-service-catalog-finalizer-with-cli

### Comment by [@kalki7](https://github.com/kalki7) — 2025-02-18T05:41:11Z

Thanks @mimowo, here's a small script that clears out the finalisers and deletes the workloads as well in batches

```
set -x

for j in $(kubectl get wl --chunk-size=1000 -o custom-columns=:.metadata.name)
do
    kubectl patch workload $j -p '{"metadata":{"finalizers":null}}' --type=merge
    kubectl delete workload $j
done
```

The GCing by kueue internally would be great for a situation like this in the future. Additionally I would like your thoughts on a kueue limit feature, where apart from nominalQuota, something like a maximumQuota, once hit, kueue-controller-manager just stops accepting new workloads like rate limiting the requests.

For example, a queue has pods nominalQuota as 10, but a maximumQuota of 100, after 100 jobs have been submitted, the kueue api just doesn't accept jobs.

This is coming from the perspective of it making rate limiting to the cluster easier from the point of kueue. Do share your thoughts on the same!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-18T06:03:05Z

> Additionally I would like your thoughts on a kueue limit feature, where apart from nominalQuota, something like a maximumQuota, once hit, kueue-controller-manager just stops accepting new workloads like rate limiting the requests.
> 
> For example, a queue has pods nominalQuota as 10, but a maximumQuota of 100, after 100 jobs have been submitted, the kueue api just doesn't accept jobs.
> 
> This is coming from the perspective of it making rate limiting to the cluster easier from the point of kueue. Do share your thoughts on the same!

Thank you for the new feature requests. If we can limit the number of Workload API resources by `maximumQuota`, it could avoid your situation. However, I guess that it is challenging since we leverage the Workload API for advanced scheduling (requeue, fairsharing, and so on...) and preemptions.

### Comment by [@kalki7](https://github.com/kalki7) — 2025-02-18T06:52:13Z

Yes, and I'm not sure about the urgency of this especially from a kueue perspective.

But either way, I shall create an enhancement request to follow up. Thanks all !!!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-18T07:07:04Z

> Thanks @mimowo, here's a small script that clears out the finalisers and deletes the workloads as well in batches

Awesome that it worked, and thank you for sharing the script - I'm taking a note of it :) 

> Additionally I would like your thoughts on a kueue limit feature, where apart from nominalQuota, something like a maximumQuota, once hit, kueue-controller-manager just stops accepting new workloads like rate limiting the requests.

TBH it feels outside of scope for Kueue, but feel free to propose it as an issue, I'm open to considering it. The questions which pop to my head, and might be helpful when proposing the enhancement:
1. what is the main motivation - is it to prevent the accumulated workloads from killing the system? Then, I believe the new feature (https://github.com/kubernetes-sigs/kueue/pull/2686) should help. Unless, you would have >200k workloads "active" which cannot be GCed.
2. "If we can limit the number of Workload API resources by maximumQuota" -  it seems like the cap on the workloads should be in different units. Quota is expressed in the resource units (CPU, mem, GPU), while the maximalQuota would be just a number without units? 
3. would the limit be on the number of "active" workloads (admitted and pending), or just pending. Should the cap on the number of workloads be also per CQ or global?
