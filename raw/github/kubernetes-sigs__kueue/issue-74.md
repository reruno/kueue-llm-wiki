# Issue #74: Support Argo/Tekton workflows

**Summary**: Support Argo/Tekton workflows

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/74

**Last updated**: 2026-03-24T19:59:26Z

---

## Metadata

- **State**: open
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-25T21:09:20Z
- **Updated**: 2026-03-24T19:59:26Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`, `size/L`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 68

## Description

This is lower priority than https://github.com/kubernetes-sigs/kueue/issues/65, but it would be good to have an integration with a workflow framework.

Argo supports the suspend flag, the tricky part is that suspend is for the whole workflow, meaning a QueuedWorkload would need to represent the resources of the whole workflow all at once. 

Ideally Argo should create jobs per sequential step, and then resource reservation happens one step at a time.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-25T21:30:01Z

FYI @terrytangyuan

Also, extracted from a comment in https://bit.ly/kueue-apis (can't find the person's github)

> A compromise might be a way of submitting a job, but have it "paused" so that the workflow manager can unpause it after its deps have been met, but the job still can wait in line in the queue so it doesn't add a lot of wall clock time. The scheduler would ignore any paused jobs until they are unpaused?

The idea is to allow for a dependent job to jump to the head of the queue when the dependencies are met.

### Comment by [@kfox1111](https://github.com/kfox1111) — 2022-02-25T22:09:26Z

Yes, but it essentially only jumps to the head of the line if it already was at the head of the line.

### Comment by [@terrytangyuan](https://github.com/terrytangyuan) — 2022-03-01T17:56:37Z

I guess I'll have to read through the design doc for queue APIs in order to understand the use case better here. Any thoughts on what the integration looks like and how the two interoperate with each other?

### Comment by [@kfox1111](https://github.com/kfox1111) — 2022-03-02T19:32:20Z

Consider there to be two components. a queue, and a scheduler.
The queue is where jobs wait in line. A scheduler picks entries to work on at the head of the line.

Sometimes in the real world, its a family waiting in line. One member goes off to use the bathroom. If they are not back by the time its their turn, they usually say, "let the next folks go, we're not ready yet". The scheduler in this case just ignores that entry and goes to the next entry in the queue. The option to allow jobs to be "not ready yet, don't schedule me, but still queue me" could be interesting to various workflow managers.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-06-15T15:19:10Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-16T02:01:42Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-04T16:16:10Z

Would a similar integration like Argo and Volcano work in this case?

https://github.com/volcano-sh/volcano/blob/master/example/integrations/argo/20-job-DAG.yaml

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-06T14:49:29Z

Not really. That seems to be creating a different job for each step of the workflow. Then, each job enters the queues only after the previous step has finished. This can already be accomplished with Kueue and batch/v1.Job.

We would like to enhance the experience roughly as described here: https://github.com/kubernetes-sigs/kueue/issues/74#issuecomment-1051285404

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-12-05T15:15:59Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-12-06T01:54:03Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-03-06T02:24:46Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-06T02:26:07Z

/remove-lifecycle stale

### Comment by [@lbernick](https://github.com/lbernick) — 2023-04-12T13:18:49Z

Hi, I am trying to figure out if I could use Kueue for queueing Tekton PipelineRuns (more info on tekton at [tekton.dev/docs](http://tekton.dev/docs)). From reading [bit.ly/kueue-apis](http://bit.ly/kueue-apis), it seems like Kueue is going to have separate controllers that create Workload objects for different types of workloads (although I'm not sure if that's the case yet).

Would it be reasonable to write a separate controller that creates Workload objects for pending PipelineRuns, and starts the PipelineRuns when the workload is admitted by the queue? I'm not sure if this is possible because it seems like kueue somehow mutates the workloads' node affinity directly, and the relationship between PipelineRuns and pod specs doesn't work in quite the same way as between Jobs and pod specs.

I'm also curious if it's possible to create a queue that is just based on count of running objects rather than their compute resource requirements.

More details on what I'm trying to do: https://github.com/tektoncd/community/blob/main/teps/0132-queueing-concurrent-runs.md

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T16:04:13Z

> it seems like Kueue is going to have separate controllers that create Workload objects for different types of workloads (although I'm not sure if that's the case yet).

These controllers can live in the Kueue repo, the tekton repo or a new repo altogether.
We currently have a controller for kubeflow MPIJob in the kueue repo. If the Tekton community is open to have this integration, we can discuss where is the best place to put it.

> Would it be reasonable to write a separate controller that creates Workload objects for pending PipelineRuns, and starts the PipelineRuns when the workload is admitted by the queue? 

Depends on what you want. When talking about workflows, there are two possibilities: (a) queue the entire workflow or (b) queue the steps.

> I'm not sure if this is possible because it seems like kueue somehow mutates the workloads' node affinity directly, and the relationship between PipelineRuns and pod specs doesn't work in quite the same way as between Jobs and pod specs.

Injecting node affinities is the mechanism to support fungibility (example: this job can run on ARM or x86, let kueue decide to run it where there is still quota). If this is not something that matters to you, you can not create flavors.

> I'm also curious if it's possible to create a queue that is just based on count of running objects rather than their compute resource requirements.

Kueue is a quota-based system. Currently it uses pod resource requests and we plan to add number of pods #485.
What kind of object would make sense to count in Tekton? I would expect that there should be resource requests somewhere.

I'll comment more when I finish reading the doc above. Thanks for sharing :)

cc @kerthcet

### Comment by [@lbernick](https://github.com/lbernick) — 2023-04-12T17:01:05Z

Thanks for your response!

> These controllers can live in the Kueue repo, the tekton repo or a new repo altogether. We currently have a controller for kubeflow MPIJob in the kueue repo. If the Tekton community is open to have this integration, we can discuss where is the best place to put it.

Still in the early exploration phase, but looking forward to discussing more what would work!

> Kueue is a quota-based system. Currently it uses pod resource requests and we plan to add number of pods #485. What kind of object would make sense to count in Tekton? I would expect that there should be resource requests somewhere.

Tekton uses PipelineRuns, which are DAGs of TaskRuns, and each TaskRun corresponds to a pod. One of our use cases is basically just to avoid overwhelming a kube cluster, in which case queueing based on resource requirements would be useful. However, there are some wrinkles with how we handle resource requirements, since we have containers running sequentially in a pod rather than in parallel, so the default k8s assumption that pod resource requirements are the sum of container resource requirements doesn't apply. For this reason, queueing based on TaskRun or PipelineRun count may be simpler for us. Since TaskRuns correspond to pods, queueing based on pod count would solve the TaskRun use case at least. 

We also have some use cases that would probably need to be met in Tekton with a wrapper API (e.g. "I want to have only 5 PipelineRuns at a time of X Pipeline that communicates with a rate-limited service"; "I want to have only one deployment PipelineRun running at a time", etc). If we could use Kueue to create a queue of at most X TaskRuns, we'd be in good shape to design something in Tekton meeting these needs.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T17:20:11Z

> Since TaskRuns correspond to pods, queueing based on pod count would solve the TaskRun use case at least.

Yes, the pod count would help. But I would encourage users to also add pod requests. This is particularly important for HPC workflows. You might want dedicated CPUs and accelerators.

I agree that it wouldn't make sense to queue at a lower level than TaskRuns.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-27T18:39:36Z

You are welcome to add a topic to our WG Batch meetings if you want to show your design proposals for queuing workflows.

https://docs.google.com/document/d/1XOeUN-K0aKmJJNq7H07r74n-mGgSFyiEDQ3ecwsGhec/edit

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-04-28T03:31:25Z

One feedback for this is we have Tekton+ArgoCD as our CICD pipelines, for cost effectiveness, we deploy tekton together with other application services(non-productive), what will happen is we will run into insufficient resources when there're a lot of CI runs. So we have to isolate them.  Queueing is important for tekton as well I think.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-04-28T04:01:36Z

We have waitForPodsReady which will wait until the previous job has enough pods running, I think we can expand this to like pendingForTargetQuantity, for job, it will still return the pod number, but for tekton, it will wait for target number of pipelineRuns/taskRuns, but we need to implement the suspend in pipelineRun/taskRun. 

I think resource management is great for tekton, but if no, we can also make it out by watching the pipelineRun/taskRun amount. But this needs a refactor to kueue for now resources are required. Just for brainstorming.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-04-28T04:04:10Z

Another concern is about preemption, I think it will be dangerous for tekton in some cases. Like deploying applications.

### Comment by [@terrytangyuan](https://github.com/terrytangyuan) — 2023-12-15T01:16:45Z

@alculquicondor @ahg-g I added https://github.com/argoproj/argo-workflows/issues/12363 to track and hopefully would attract more contributors to work on this.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T08:15:08Z

@terrytangyuan FYI: we're working on https://github.com/kubernetes/kubernetes/issues/121681 for workflow support.

### Comment by [@sam-leitch-oxb](https://github.com/sam-leitch-oxb) — 2024-01-03T11:30:58Z

It is possible to use pod-level integration using the [Plain Pods](https://kueue.sigs.k8s.io/docs/tasks/run_plain_pods/) approach.

We use this config snippet (from [kueue-manager-config](https://kueue.sigs.k8s.io/docs/installation/#install-a-custom-configured-released-version)) to integrate Argo Workflows into Kueue:

```
          integrations:
            frameworks:
            - "pod"
            podOptions:
              # You can change namespaceSelector to define in which
              # namespaces kueue will manage the pods.
              namespaceSelector:
                matchExpressions:
                - key: kubernetes.io/metadata.name
                  operator: NotIn
                  values: [ kube-system, kueue-system ]
              # Kueue uses podSelector to manage pods with particular
              # labels. The default podSelector will match all the pods.
              podSelector:
                matchExpressions:
                - key: workflows.argoproj.io/completed
                  operator: In
                  values: [ "false", "False", "no" ]
```

This configuration adds a scheduling gate to each Argo Workflows pod and will only release it once there is quota available.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-03T11:41:56Z

> It is possible to use pod-level integration using the [Plain Pods](https://kueue.sigs.k8s.io/docs/tasks/run_plain_pods/) approach.
> 
> We use this config snippet (from [kueue-manager-config](https://kueue.sigs.k8s.io/docs/installation/#install-a-custom-configured-released-version)) to integrate Argo Workflows into Kueue:
> 
> ```
>           integrations:
>             frameworks:
>             - "pod"
>             podOptions:
>               # You can change namespaceSelector to define in which
>               # namespaces kueue will manage the pods.
>               namespaceSelector:
>                 matchExpressions:
>                 - key: kubernetes.io/metadata.name
>                   operator: NotIn
>                   values: [ kube-system, kueue-system ]
>               # Kueue uses podSelector to manage pods with particular
>               # labels. The default podSelector will match all the pods.
>               podSelector:
>                 matchExpressions:
>                 - key: workflows.argoproj.io/completed
>                   operator: In
>                   values: [ "false", "False", "no" ]
> ```
> 
> This configuration adds a scheduling gate to each Argo Workflows pod and will only release it once there is quota available.

Thanks for putting an example here :)

Yes, that's right. The plain pod integration could potentially support the ArgoWorkflow. 
However, the plain pod integration doesn't support all kueue features, such as partial admission. So the native ArgoWorkflkow support would be worth it.

Regarding the features not supported in the plain pod integration, please see for more details: https://github.com/kubernetes-sigs/kueue/tree/main/keps/976-plain-pods#non-goals

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-03T16:51:04Z

Oh that's cool. How do you set up the queue-name in the Pods?

I'm not familiar with Argo. Does it have support for pods working in parallel or pods that all need to start together?

Another thing to note is that behavior you are getting is that Pods are created when their dependencies complete. Meaning that, in a busy cluster, a workflow might be spending too much time waiting in the queue for each step. Is this acceptable?

It's probably acceptable for some users. Would you be willing to write a tutorial for the kueue website?

### Comment by [@sam-leitch-oxb](https://github.com/sam-leitch-oxb) — 2024-01-03T22:21:04Z

> Oh that's cool. How do you set up the queue-name in the Pods?

You can use either spec.template[].metadata or spec.podMetadata to define a queue.

> I'm not familiar with Argo. Does it have support for pods working in parallel or pods that all need to start together?

Argo supports parallel execution of pods, and those pods are only created when each "node" of the workflow is ready to run.
This type of integration simply prevents each pod from executing until they pass Kueue's admission checks.

> Another thing to note is that behavior you are getting is that Pods are created when their dependencies complete. Meaning that, in a busy cluster, a workflow might be spending too much time waiting in the queue for each step. Is this acceptable?

I'm still waiting to see how well it works. I don't expect the wait time between nodes to be a problem, but a backlog of partially complete workflows may become problematic.

Most of the use cases revolve around ETL nodes followed by process nodes and vice-versa. Depending on how the queues are configured, I could end up with too many partially complete workflows that take up ephemeral resources.

> It's probably acceptable for some users. Would you be willing to write a tutorial for the kueue website?

Sure.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-02T22:40:06Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-03T07:00:07Z

/remove-lifecycle stale

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-04-25T07:10:11Z

Is there any progress for supporting argo/tekon workflows?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-25T13:52:10Z

I don't think anyone has followed through with it. Would you like to propose something?
I think we might require changes in both projects, but at least the Argo community is in favor of doing something: https://github.com/argoproj/argo-workflows/issues/12363

### Comment by [@kannon92](https://github.com/kannon92) — 2024-04-25T14:05:12Z

@alculquicondor I'm confused. Isn't it possible to support argo-workflows indirectly through pod integration?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-25T16:03:29Z

It is indeed possible. But a tighter integration, with atomic admission, would be beneficial.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-04-26T01:53:57Z

If the user want to run the step which contains multi pods only when all pods can run, we may need some methods to know which pods should be in the same workload. So only pod integration may not enough.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-06-03T02:45:56Z

cc @Zhuzhenghao Discussion about integrating Kueue with tekton.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-01T03:26:27Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-01T03:47:02Z

 /remove-lifecycle stale

### Comment by [@terrytangyuan](https://github.com/terrytangyuan) — 2024-09-01T03:48:54Z

https://github.com/argoproj/argo-workflows/issues/12363 has 22 upvotes. We just need someone to drive this.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-09-02T01:37:54Z

@terrytangyuan Hi, is there any conclusion about what exactly to suspend (the entire workflow or the layer)?

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-09-02T01:47:42Z

We developed two different ways to help the queuing of workflows in our environment.
1. Users can define the max resources on the entire workflow. During the execution of workflow, the total resources can not exceed the admission.
2. Integrate a controller to convert a workflow to insert a suspend template before each layer. And create a workload for each suspend layer.

And the plain pods suspend is also an available method.
I can write a simple KEP to tell the advantages and disadvantages for each method and track the discussion.
@alculquicondor @tenzen-y Hi, is there anyone working on this?

### Comment by [@lukasmrtvy](https://github.com/lukasmrtvy) — 2024-09-02T09:47:06Z

@KunWuLuan is the mentioned controller opensourced?  Thanks :)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-03T06:36:43Z

> We developed two different ways to help the queuing of workflows in our environment.
> 
> 1. Users can define the max resources on the entire workflow. During the execution of workflow, the total resources can not exceed the admission.
> 2. Integrate a controller to convert a workflow to insert a suspend template before each layer. And create a workload for each suspend layer.
> 
> And the plain pods suspend is also an available method. I can write a simple KEP to tell the advantages and disadvantages for each method and track the discussion. @alculquicondor @tenzen-y Hi, is there anyone working on this?


@KunWuLuan Thank you for tackling this issue.
1. Does this indicate a new API object or field? or Reusing existing API objects or fields?
2. Does this indicate a part of Job integration controller implemented `GenericJob` interface similar to batch/v1 Job and other Jobs.

As a first step, it would be a great improvement if you could provide documents and examples for Plain Pod Integration + ArgoWorkflows.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-09-03T09:54:19Z

What's the layer means here? One step?

If so, I think maybe it's possible to create all workloads for all the steps(parallel steps as one workload) and suspend them all. Once a workload finishes, allow the next one, I think the controller knows the dependence.

However, how can we distinguish with the injected `suspend` vs used configured `suspend`.

I think the approach 1) can be a simple start. Anyway, glad to see the KEP.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-03T15:52:25Z

Note that someone started a PR to document how to use the plain pods integration with argo https://github.com/kubernetes-sigs/kueue/pull/1545, but they abandoned it.

Regardless, I would be interested in a more robust support at the layer level. See this comment for my high level proposal https://github.com/argoproj/argo-workflows/issues/12363#issuecomment-1870421459

### Comment by [@kfox1111](https://github.com/kfox1111) — 2024-09-03T17:07:30Z

plain pod.... could that work with gitlab runner jobs too? the lack of scheduling there has been a pain.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-09-06T03:34:50Z

> @KunWuLuan is the mentioned controller opensourced? Thanks :)

The controller is not opensourced yet.

> Does this indicate a new API object or field? or Reusing existing API objects or fields?

Yes, we introduced a specific key in workflow's annotations like 
```
 annotations:
   min-resources: |
     cpu: 5
     memory: 5G
```

> Does this indicate a part of Job integration controller implemented GenericJob interface similar to batch/v1 Job and other Jobs.

Yes we deployed a Job integration controller which contains a controller to create CR like workload and a controller to inject suspend template to original workflow.

> As a first step, it would be a great improvement if you could provide documents and examples for Plain Pod Integration + ArgoWorkflows.

On problem, working on it. : )

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-06T12:09:46Z

> Yes we deployed a Job integration controller which contains a controller to create CR like workload and a controller to inject suspend template to original workflow.

That seems useful, but annotations are not a sustainable API. Argo folks were in favor of doing a proper integration, so we can probably change their API to accommodate the needs of the integration.

But again, something at the layer level is probably better.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-06T14:58:19Z

> > Yes we deployed a Job integration controller which contains a controller to create CR like workload and a controller to inject suspend template to original workflow.
> 
> That seems useful, but annotations are not a sustainable API. Argo folks were in favor of doing a proper integration, so we can probably change their API to accommodate the needs of the integration.
> 
> But again, something at the layer level is probably better.

I think that we want to support the creation of Workload at the layer level as well, and we want to push all Workload sequentially. This layer-level approach allows us to prevent wasting resources for the entire workflow.
 
But, I think that we can evaluate the layer-level approach during the KEP (https://github.com/kubernetes-sigs/kueue/pull/2976).

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-09-10T08:53:15Z

@alculquicondor @tenzen-y 
Introduced a KEP to discuss the advantages and constraints of three different granularity levels for supporting workflows , and three approaches for supported workflows at the layer level are also proposed.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-09-10T09:07:07Z

@terrytangyuan If you have time, please also have a look, thanks very much.

### Comment by [@terrytangyuan](https://github.com/terrytangyuan) — 2024-09-10T16:21:11Z

Awesome! I'll share the proposal around the Argo Workflows community as well.

### Comment by [@terrytangyuan](https://github.com/terrytangyuan) — 2024-09-10T16:23:32Z

Can someone remove "Tekton" from the title of this issue?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-10T17:25:01Z

Ideally, the mechanism should be extensible to Tekton and any other workflow manager. But certainly, we can start with just Argo.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-09-11T09:46:29Z

> Ideally, the mechanism should be extensible to Tekton and any other workflow manager. But certainly, we can start with just Argo.

+1 this should be aligned with other workflow tools as well, from kueue side.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-09-11T12:01:53Z

> Ideally, the mechanism should be extensible to Tekton and any other workflow manager. But certainly, we can start with just Argo.

I understand. In that case, this component should aim to minimize its dependencies on modifications to other workflow managers.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-11T17:45:24Z

Not necessarily. But it should aim at modification that could be feasible in other projects. Just like we did the `suspend` field for Job that could be replicated in projects such as kubeflow and kuberay.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-10-11T18:26:25Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-10-12T08:40:14Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-10T09:03:07Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-17T04:32:17Z

/remove-lifecycle rotten

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-29T15:46:53Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-29T16:19:47Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-29T18:10:06Z

/remove-lifecycle stale

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-05-29T07:09:14Z

For Tekton we ([Konflux](https://konflux-ci.dev/)) developed an external framework for supporting PipelineRuns - https://github.com/konflux-ci/tekton-kueue

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-29T14:08:11Z

> https://github.com/konflux-ci/tekton-kueue

Thank you for letting us know. That would be really helpful to understand what is needed for us.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-27T14:52:28Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-26T15:34:54Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-26T15:36:21Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-24T19:59:23Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/
