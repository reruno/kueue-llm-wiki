# Issue #716: Support flux-operator

**Summary**: Support flux-operator

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/716

**Last updated**: 2023-05-11T05:41:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-04-24T14:10:31Z
- **Updated**: 2023-05-11T05:41:13Z
- **Closed**: 2023-05-10T13:05:00Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 26

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Support queuing of ephemeral and persistent mini-clusters from [flux-operator](https://flux-framework.org/flux-operator/).

It is possible that this works out-of-the-box, given that flux-operator uses the Job API to launch Pods.

If it works, we need to document any implications.
If it doesn't work, maybe we need to add a suspend flag and a translation controller.

**Why is this needed**:

To accommodate multiple HPC researchers in a kubernetes cluster

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-24T14:11:29Z

cc @vsoch

### Comment by [@trasc](https://github.com/trasc) — 2023-04-24T14:46:42Z

/assign

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-24T16:22:33Z

Will take a look at this! I haven't used kueue before, looking forward to trying it!

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-24T16:26:07Z

@trasc can I help with this, or in assigning yourself are you saying you will do it? I'd love to try it and learn about kueue, etc.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2023-04-24T16:30:51Z

++

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-24T16:52:09Z

@trasc, for context, @vsoch is one of the maintainers of flux-operator.
We discussed offline and she agreed to help with any questions you might have.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-24T17:06:18Z

@trasc happy to help with questions and test out what you do. Please ping me anytime you want to chat!

### Comment by [@trasc](https://github.com/trasc) — 2023-04-25T09:46:26Z

Sure @vsoch ,  Thanks.

### Comment by [@trasc](https://github.com/trasc) — 2023-04-25T15:29:28Z

The big picture looks good, in the sense  that to have a minicluster work scheduled by Kueue you just need to specify the localQueue name in the jobLabels spec.

So a set of miniclusters created with 

```yaml
apiVersion: flux-framework.org/v1alpha1
kind: MiniCluster
metadata:
  generateName: flux-sample-kueue-
spec:
  size: 1
  containers:
    - image: ghcr.io/flux-framework/flux-restful-api:latest
      command: echo hello world 
      resources:
        requests:
          cpu: 4
          memory: "200Mi"
  jobLabels:
    kueue.x-k8s.io/queue-name: user-queue
```
will run two at a time while using `config/samples/single-clusterqueue-setup.yaml`

However I see two more or less minor issues:

1.  the `...-cert-generator` pod is running outside of the minicluster job and cannot be scheduled by kueue.
2.  in some configurations (` size: 2`  in the above config) the minicluster job never ends, this will block the cluster queue resource quota.  

The resource requests can also be easily specified in minicluster spec.

cc: @alculquicondor @vsoch

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-25T16:18:25Z

Questions mostly for @vsoch 

> 1. the ...-cert-generator pod is running outside of the minicluster job and cannot be scheduled by kueue.

What is this pod for? Does it have to run per minicluster or could it be migrated to a shared controller for all mini-clusters.

If not, we have two options:
1. Add suspend field to MiniCluster and make the job a child job (like we do for MPIJob)
2. Start supporting [scheduling gates](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/) and have kueue control the gate for the cert-generator.

> 2. in some configurations ( size: 2 in the above config) the minicluster job never ends, this will block the cluster queue resource quota.

Either a bug or WAI? Does flux-operator add a sidecar container?

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-25T17:17:35Z

I’m interviewing someone will be able to comment on the next hour!

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-25T18:42:35Z

Answers!

> the ...-cert-generator pod is running outside of the minicluster job and cannot be scheduled by kueue.

This was a design problem I solved with creating a one-off single pod that runs before the minicluster is created. Basically, Flux requires a CURVE certificate to secure the tree-based overlay network. We typically use [keygen](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/man1/flux-keygen.html) to create that certificate that is shared by the cluster. Since flux has this command and flux will always be in the base container for the cluster, we use this one-off pod to generate it:

https://github.com/flux-framework/flux-operator/blob/e0e9e708d48c7d4fae19f86788debd8dc9d7cb8a/controllers/flux/templates/cert-generate.sh#L20-L22

and then we can give it to the subsequent cluster pods via a read-only ConfigMap. The original design I had would generate it on the fly (done by the broker) but then required a shared volume with RWX (read write many) and that wasn't a requirement I wanted to enforce for the cluster, because setting up storage kind of is terrible!  And not all workflows require storage (e.g., LAMMPS does not).

>  What is this pod for? Does it have to run per minicluster or could it be migrated to a shared controller for all mini-clusters.

It could definitely be done by some single, shared, controller - basically the operator needs to be able to retrieve a new certificate to put into a config map. One idea that comes to mind is a [CSI driver](https://github.com/converged-computing/oras-csi) I was working on. We could theoretically make a similar CSI driver that would just know how to generate and mount certificates. That might be (yet another) annoying dependency though. But perhaps it might work for kueue? Let me know if this might be of interest or if you have other design ideas for generating the certificate! It basically needs to be done once and then shared (the same one) across pods. I considered also interacting with Flux from the operator itself, but (at the time) getting Flux into Go and making that a requirement for the operator also seemed like a lot of overhead just for a certificate. But maybe that's not a crazy idea for something like a csi, and I was able to [recently](https://github.com/converged-computing/flux-go) get a basic binding working for flux in Go. So perhaps a CSI that uses Flux via Go to bind the certificate on demand would be cool (and useful outside of the context of flux too).

> Add suspend field to MiniCluster and make the job a child job (like we do for MPIJob)

This sounds interesting - so if the first "one-off" pod was actually a one-off job, and then the cluster a child of it, this design would work with kueue? What does it mean to have it be a child job?

> Start supporting [scheduling gates](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/) and have kueue control the gate for the cert-generator.

This sounds like it would be a bigger set of changes for kueue? I'm not familiar with scheduling gates but can read up on them.

> in some configurations ( size: 2 in the above config) the minicluster job never ends, this will block the cluster queue resource quota.
 
We haven't worked on / tested well the job termination behavior, primarily because our use cases are to bring up a persistent minicluster, or (in the case of the experiments for kubecon) we don't care, we just delete the minicluster CRD and make another one. This is an interesting point of discussion because we are using the same Job abstractions in totally different contexts. For kueue / MPIJob I suspect the Job object itself is the unit of operation. For the Flux Operator, we have an entire job orchestration / scheduler inside of the minicluster, and the Job itself is just a means to bring up the cluster. The status of the jobs come from Flux, not from the operator.

But that said, this likely (for the kueue use case) would be considered a bug that needs to be fixed, and we can chat about that here and I can work on it for you. For some context, the index 0 of the indexed job is the broker that is running the main job command, and when that finished, the index 0 pod will complete. The reason the others don't complete is because the implementation for a worker pod is very stupid - since we can't control the order of pods coming up, we have to ensure that they keep trying if they are up before the broker. So there [is a loop to do that](https://github.com/flux-framework/flux-operator/blob/e0e9e708d48c7d4fae19f86788debd8dc9d7cb8a/controllers/flux/templates/wait.sh#L345-L354). This was another early design problem for which I suggested some kind of better controlled logic / grouping for starting the pods in the indexed job (because the broker needs to be started first). If the jobs API could support this (or there is a better strategy for handling this) we would easily:

1. Start the broker first
2. Then start the worker pods, knowing they will find the broker to register to
3. When the broker exists, the worker pods will also exit, and all pods in the job complete.

Another idea - basically whenever the broker (index 0) pod is completed, the other pods are too. It doesn't really matter what they are doing. Is there a way to have the worker pods in the minicluster basically terminate / complete when they see index 0 is done? :thinking: 

So TLDR: with this current constraint and choice of design, this is expected behavior. I'd love to improve it if you want to chat about ideas - not sure if the TBA JobSet would be able to help?

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-25T18:57:02Z

@trasc if the use case of kueue is to submit many jobs (more high-throughput) you might be better off with one persistent minicluster and then using batch: https://flux-framework.org/flux-operator/getting_started/custom-resource-definition.html?h=batch#batch. That will give all the jobs to the flux scheduler within the same minicluster to the broker, and let Flux handle the scheduling across the pods (and no need to stress the kubernetes API with it).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-25T19:01:08Z

The use case of kueue is multi-tenancy: give order to multiple users sending jobs at the same time, more than what the cluster can accomodate. In the case of flux-operator, it would be multiple users creating mini-clusters at the same time.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-25T19:10:06Z

 > The use case of kueue is multi-tenancy: give order to multiple users sending jobs at the same time, more than what the cluster can accomodate. In the case of flux-operator, it would be multiple users creating mini-clusters at the same time.

Gotcha, so I think these are our options (given the current design, which is fairly flexible). All options will require figuring out a solution for the curve cert generation and having the workers complete, so I'll set those aside for now.

- Create **one new minicluster per job command**. This is how we ran the Kubecon experiments, bringing up the entire set of pods, running the command across the cluster, and then down. It doesn't take advantage of Flux as a scheduler, but moreso fits the model of some of the other job runners. It also seems inefficient to be doing all the work for just one command.
- Create **one new minicluster per _group_ of job commands**. If the single user has 100x a run of the same thing, it would make sense to give the entire group to flux to run - this is called a batch job - and the broker would terminate the same way (akin to one job) when they are all done. This would be much faster to not have to wait for pods to go up and down, and Flux can handle scheduling. kueue would need to add logic to handle the number of jobs allowed in the batch so one user cannot dominate the entire cluster.
- *Interactive* create one new persistent MiniCluster, up for as long as the single used needs it, for interactive submit. This can be done with an SDK, or via the RestFUL API. This makes sense if you want to be submitting jobs, but you aren't sure about how many and for how long.

We have different models for multi-tenancy (e.g., the RESTFul API server has an OAuth setup) but I think for this case, the minicluster ownership is the right level of permissions we should go for.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-25T19:37:40Z

That was a big message :) Let me try to respond to some questions. But otherwise, it might be useful for you to present in wg-batch the full architecture of the operator to gather some feedback. It might be too early for you, so maybe we can consider bringing back 2 different time slots for the meeting (we removed one because there was not enough demand for it).

> It could definitely be done by some single, shared, controller - basically the operator needs to be able to retrieve a new certificate to put into a config map. One idea that comes to mind is a [CSI driver](https://github.com/converged-computing/oras-csi) I was working on. We could theoretically make a similar CSI driver that would just know how to generate and mount certificates. That might be (yet another) annoying dependency though.

Probably the most common pattern would be to have the certificate generation as part of a controller, instead of launching a one-off pod (or job) for each mini-cluster.
However, the challenge we have here is that you might end up creating the ConfigMap much earlier than the time the Job actually starts (transitions from suspend=true to false). This might be fine at low scale, but it could bloat etcd at bigger scale.
In that case, a CSI driver could be an interesting solution, so that the cert is created only when the pods are created. But how to share the same key across pods? I'm not sure

> > Add suspend field to MiniCluster and make the job a child job (like we do for MPIJob)
> This sounds interesting - so if the first "one-off" pod was actually a one-off job, and then the cluster a child of it, this design would work with kueue? What does it mean to have it be a child job?

Let me elaborate. MPIJob creates a Job and a set of Pods. The MPIJob CRD has a `suspend` field, which kueue can control to decide when an MPIJob can start.
Additionally, Kueue supports managing the `suspend` field for the Job objects. We add an annotation to the Job that is a child of an MPIJob so that Kueue doesn't manage it.
In the case of flux-operator, if we add a `suspend` field to the MiniCluster, we would have to add the annotation to the Job it creates. If we do this, then you can keep the design you have for the cert-generator, but I still think that a cert-generator per MiniCluster is too much overhead.

> The reason the others don't complete is because the implementation for a worker pod is very stupid - since we can't control the order of pods coming up, we have to ensure that they keep trying if they are up before the broker. So there [is a loop to do that](https://github.com/flux-framework/flux-operator/blob/e0e9e708d48c7d4fae19f86788debd8dc9d7cb8a/controllers/flux/templates/wait.sh#L345-L354). This was another early design problem for which I suggested some kind of better controlled logic / grouping for starting the pods in the indexed job (because the broker needs to be started first). If the jobs API could support this

We have considered the possibility of adding some job completion policy, like complete if index 0 completes, or if x% of pods complete. But this hasn't been prioritized. I just opened an issue for tracking https://github.com/kubernetes/kubernetes/issues/117600

> not sure if the TBA JobSet would be able to help?

It won't, but as part of that effort we might enhance Job to support such semantics.

I think all modes of operating miniclusters are useful (one job per minicluster, batch of jobs and interactive). We should probably support all of them in kueue. However, from kueue's perspective, they are all the same: the Job should terminate.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-25T20:01:17Z

> That was a big message :) 

Sorry - I have lots of words! :laughing: 

> Let me try to respond to some questions. But otherwise, it might be useful for you to present in wg-batch the full architecture of the operator to gather some feedback. It might be too early for you, so maybe we can consider bringing back 2 different time slots for the meeting (we removed one because there was not enough demand for it).

This would be fantastic! I can be available almost any time later in the day.

> But how to share the same key across pods? I'm not sure

As a CSI, each pod would basically make a request for the same config map, likely namespaced to the job so there isn't any crossing of things.  They would all mount the same location provided by the driver, and [here is an example](https://converged-computing.github.io/oras-csi/#/usage?id=how-does-it-work) for what a request might look like (with different volume attributes for this hypothetical driver).

> In the case of flux-operator, if we add a suspend field to the MiniCluster, we would have to add the annotation to the Job it creates. If we do this, then you can keep the design you have for the cert-generator, but I still think that a cert-generator per MiniCluster is too much overhead.

I agree. And just to clarify, the Indexedjob _is_ the minicluster, it doesn't create another nested Kubernetes Job, a "job" running under the MiniCluster is a job that is submit to the flux scheduler, akin to a job submit in a high performance computing center. The certificate generator is [just a pod](https://github.com/flux-framework/flux-operator/blob/e0e9e708d48c7d4fae19f86788debd8dc9d7cb8a/controllers/flux/certs.go#L64-L80) and the operator [requires it to be generated](https://github.com/flux-framework/flux-operator/blob/e0e9e708d48c7d4fae19f86788debd8dc9d7cb8a/controllers/flux/minicluster.go#L299-L307) for the ConfigMap before the IndexedJob (the MiniCluster) is created.  There is no reason it couldn't be a job with some extra annotations / logic! I'll take a look at the MPI operator code and see if I can understand how it is using suspend (and if we could do similar with the Flux operator). 

> We have considered the possibility of adding some job completion policy, like complete if index 0 completes, or if x% of pods complete. But this hasn't been prioritized. I just opened an issue for tracking https://github.com/kubernetes/kubernetes/issues/117600

Excellent, thank you. This indeed would be perfect for our use case!

> I think all modes of operating miniclusters are useful (one job per minicluster, batch of jobs and interactive). We should probably support all of them in kueue. However, from kueue's perspective, they are all the same: the Job should terminate.

:+1: 

TLDR I'll explore the idea of a CSI driver that can handle the certificate generation (and possibly other flux assets too, that would make the startup more efficient!) and check out how the MPI operator handles suspect. And I'd love to come to a (later in the day) batch meeting - there are a few other design elements I'd love to get discussion / feedback around!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-25T20:05:36Z

> And just to clarify, the Indexedjob is the minicluster, it doesn't create another nested Kubernetes Job, a "job" running under the MiniCluster is a job that is submit to the flux scheduler, akin to a job submit in a high performance computing center. 

Right, that's what I understood. When I say "child" Job, I mean that the Job is a child of the MiniCluster resource.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-25T20:09:59Z

>  I'll take a look at the MPI operator code and see if I can understand how it is using suspend (and if we could do similar with the Flux operator).

Here is the integration code for MPIJob in Kueue.

However, it is our long term vision that we shouldn't need these integration layers for operators that just use one Job.

### Comment by [@trasc](https://github.com/trasc) — 2023-04-26T11:34:38Z

In my opinion, since the cert-generator should use a lot less resources than the actual job we could ignore it's existence for now from the kueue's point of view.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-26T17:13:55Z

> Here is the integration code for MPIJob in Kueue.

I didn't add a link :upside_down_face: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/mpijob/mpijob_controller.go

> In my opinion, since the cert-generator should use a lot less resources than the actual job we could ignore it's existence for now from the kueue's point of view.

I agree. However, it might still be valuable for flux-operator not have a ConfigMap laying around much earlier than the actual job start.

Back to the problem of job completion, it's also not kueue's concern whether the job finishes.

Maybe it's useful to add to the documentation that Kueue has limited support of flux-operator and document how to queue a MiniCluster https://github.com/kubernetes-sigs/kueue/issues/716#issuecomment-1522002509
@vsoch, do you agree? We could add a note in both websites: kueue and flux-operator

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-26T17:52:37Z

> @vsoch, do you agree? We could add a note in both websites: kueue and flux-operator

That would work for me, however I would like to work on improving some of the issues we chat previously about.

For a quick update, I was able to get certificate generation working yesterday in Go (using cgo) ([dummy example](https://github.com/converged-computing/flux-go/tree/main/docs#keygen-example)) and started prototyping the CSI, although I didn't finish it yet. It probably won't be good to require someone to always use the CSI, although (if I can put together a quick tutorial to install to a cluster) it could be potentially used with queue to nix needing to use the cert-generator pod, period.

> Maybe it's useful to add to the documentation that Kueue has limited support of flux-operator and document how to queue a MiniCluster https://github.com/kubernetes-sigs/kueue/issues/716#issuecomment-1522002509

I can probably help with that / give feedback when I try out the operator with kueue - I don't think I've used it before! But hmm I might have a long time ago with a Pi example from @ArangoGutierrez, I can't remember the details.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-26T18:02:34Z

@trasc can you take the documentation of the kueue side? 

Probably a new file in https://github.com/kubernetes-sigs/kueue/tree/main/site/content/en/docs/tasks

It might be useful to document the "known-limitations". @vsoch if you have issues in the flux-operator repo, we can link to them so users can follow the updates.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-04-26T18:08:57Z

They are referenced above, but for more clarify:
  
 - certificate generation issue: https://github.com/flux-framework/flux-operator/issues/150
 - pod termination: https://github.com/flux-framework/flux-operator/issues/151

should have time to work more on the first bullet today!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-10T15:38:54Z

@trasc can you mention Minicluster under `Batch user` tasks? https://kueue.sigs.k8s.io/docs/tasks/

### Comment by [@trasc](https://github.com/trasc) — 2023-05-11T05:41:13Z

> @trasc can you mention Minicluster under `Batch user` tasks? https://kueue.sigs.k8s.io/docs/tasks/

done
