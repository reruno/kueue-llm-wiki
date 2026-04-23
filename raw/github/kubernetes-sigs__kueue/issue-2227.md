# Issue #2227: Jobsets having replicas = 0 for their replicatedJob are not handled in Kueue

**Summary**: Jobsets having replicas = 0 for their replicatedJob are not handled in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2227

**Last updated**: 2024-05-29T18:25:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@shrinandj](https://github.com/shrinandj)
- **Created**: 2024-05-17T21:02:20Z
- **Updated**: 2024-05-29T18:25:52Z
- **Closed**: 2024-05-29T11:04:22Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 12

## Description

**What happened**:
- Created a jobset with two replicatedJobs: the first one had a replica count of 1 and the other one had a replica count of 0.
- The jobset was created in a suspended state and had the required kueue labels/annotations
- The jobset was NOT unsuspended by Kueue and the 1 expected job did not start

**What you expected to happen**:
- Kueue should have unsuspended the jobset and started the job

**How to reproduce it (as minimally and precisely as possible)**:
- As mentioned above, create a jobset was two replicatedJobs: one with replicas > 0 and another with replicas = 0

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): `v1.28.8`
- Kueue version (use `git describe --tags --dirty --always`):`v0.6`
- Cloud provider or hardware configuration: `aws`
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

** Details **

Jobset CRD shows the default is 1 but it is not a minimum value of 1. So 0 is acceptable.
```
                    replicas:
                      default: 1
                      description: |-
                        Replicas is the number of jobs that will be created from this ReplicatedJob's template.
                        Jobs names will be in the format: <jobSet.name>-<spec.replicatedJob.name>-<job-index>
                      format: int32
                      type: integer
                    template:
```

Kueue's workload CRD shows that the podSet's count has a minimum value of 1:
```
                  properties:
                    count:
                      description: count is the number of pods for the spec.
                      format: int32
                      minimum: 1
                      type: integer
                    minCount:
                      description: |-
                        minCount is the minimum number of pods for the spec acceptable
                        if the workload supports partial admission.


                        If not provided, partial admission for the current PodSet is not
                        enabled.


                        Only one podSet within the workload can use this.


                        This is an alpha field and requires enabling PartialAdmission feature gate.
                      format: int32
                      minimum: 1
                      type: integer
```

Kueue's log show the following error:
```
{"level":"error","ts":"2024-05-17T20:59:35.924123528Z","caller":"controller/controller.go:329","msg":"Reconciler error","controller":"jobset","controllerGroup":"jobset.x-k8s.io","controllerKind":"JobSet","JobSet":{"name":"js-b8b2dc","namespace":"jobs-default"},"namespace":"jobs-default","name":"js-b8b2dc","reconcileID":"9fbf19e9-35a9-443a-a60d-78ef69dadaba","error":"Workload.kueue.x-k8s.io "jobset-js-b8b2dc-9431d" is invalid: spec.podSets[1].count: Invalid value: 0: spec.podSets[1].count in body should be greater than or equal to 1","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:329
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:266
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:227"}
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-18T03:31:40Z

@shrinandj Which version do you use JobSet?
If you use v0.5.0, please update the JobSet version to resolve JobSet regression.

https://github.com/kubernetes-sigs/kueue/issues/2096

### Comment by [@shrinandj](https://github.com/shrinandj) — 2024-05-19T16:24:39Z

Is that a different error where the `managed-by` label is being modified on suspension? In this case, there is a discrepancy in the expectations of `workload.podSet.count` which has to be > 0 and `jobset.replicatedJob.count` which can be 0.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-05-22T11:38:03Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-05-22T12:28:26Z

The source of issue was correctly identified, because exactly` jobset.replicatedJob` gets translated to `workload.podSet`. 
While former allows count 0 the latter does not.
Now this could be either corrected in `JobSet` or enhanced in `Kueue`.

Kueue option allows 2 solutions:

1. Fail the validation on JobSet creation (in JobSet webhook) if the replica count is 0. In result keep the JobSet suspended.
2. Ignore `replicatedJob` with count 0 and do not translate it to `podSet`. In result the remaining jobs (from the above example) will get scheduled.

@alculquicondor @tenzen-y wdyt?

@shrinandj seems that option 2 is your expected behaviour. May I ask what is the rationale behind `jobset.replicatedJob.count` equals 0 ?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T14:28:47Z

I guess we could do option 2.

However, it sounds surprising to me that jobset allows 0 replicas. @danielvegamyhre @kannon92 is this expected?

### Comment by [@kannon92](https://github.com/kannon92) — 2024-05-22T14:54:13Z

I think most workloads allow 0 replicas. I know that you can downscale deployments to 0.

When we implement elastic jobsets I think 0 should be a valid value.

### Comment by [@shrinandj](https://github.com/shrinandj) — 2024-05-22T15:16:52Z

> ... May I ask what is the rationale behind jobset.replicatedJob.count equals 0 ?

This is set dynamically and therefore could be 0.

The scenario where we ran into this is:
- The jobset is created with two replicatedJobs: `control` and `worker` (similar to the example of `driver` and `worker`).
- The `control` replicatedJob has replicas = 1 always. And `worker` has N - 1 where N is the total parallelism requested by the user. N itself can be based on some external system: E.g. N is the total number of files to process and each Job was supposed to process 1 file. If N == 1, the `worker` replicatedJob could have replicas = 0.

### Comment by [@shrinandj](https://github.com/shrinandj) — 2024-05-22T15:20:14Z

Option 2 works best IMO as well. Failing the workload will make that users will have to factor that in and change their upstream logic (or job submission processes if submitting manually) which just adds that much more complications.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-05-22T15:43:13Z

> > ... May I ask what is the rationale behind jobset.replicatedJob.count equals 0 ?
> 
> This is set dynamically and therefore could be 0.
> 
> The scenario where we ran into this is:
> 
> * The jobset is created with two replicatedJobs: `control` and `worker` (similar to the example of `driver` and `worker`).
> * The `control` replicatedJob has replicas = 1 always. And `worker` has N - 1 where N is the total parallelism requested by the user. N itself can be based on some external system: E.g. N is the total number of files to process and each Job was supposed to process 1 file. If N == 1, the `worker` replicatedJob could have replicas = 0.

Makes perfect sense, thanks!

### Comment by [@danielvegamyhre](https://github.com/danielvegamyhre) — 2024-05-22T16:15:16Z

> I guess we could do option 2.
> 
> However, it sounds surprising to me that jobset allows 0 replicas. @danielvegamyhre @kannon92 is this expected?

Yes I think we should allow 0 since we want to support [elastic JobSets](https://github.com/kubernetes-sigs/jobset/issues/463) which may scale replicas up/down (perhaps even to 0).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T17:46:22Z

In that case, we should change the validation of Workload to allow count=0 (as opposed to not adding it to the list of podsets).

And we need to make sure nothing else assumes like the value is not zero, like dividing by count (I think we have a few of these).

/assign @trasc

### Comment by [@shrinandj](https://github.com/shrinandj) — 2024-05-29T18:25:50Z

Thanks a lot for doing this! 🙏
