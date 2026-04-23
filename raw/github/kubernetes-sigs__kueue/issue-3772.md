# Issue #3772: Stop using gcr.io images in Kueue for testing

**Summary**: Stop using gcr.io images in Kueue for testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3772

**Last updated**: 2025-02-20T10:58:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-09T11:59:11Z
- **Updated**: 2025-02-20T10:58:28Z
- **Closed**: 2025-02-20T10:58:28Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 21

## Description

**What would you like to be cleaned**:

Stop using the gcr.io images as https://github.com/kubernetes-sigs/kueue/blob/main/test/util/e2e.go#L28-L33.

**Why is this needed**:

The gcr.io image registry is deprecated and will be shut down in 2025: "After March 18, 2025, Container Registry will be shut down.", see: https://cloud.google.com/artifact-registry/docs/transition/transition-from-gcr.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-09T11:59:20Z

/assign @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-17T14:32:28Z

/unassign

Sorry, I don't have capacity to work on it for now.

### Comment by [@mabulgu](https://github.com/mabulgu) — 2024-12-17T20:20:23Z

Hi, I would love to work on this @mimowo . A few questions upfront tho:

- By "stop using" do you actually mean use another repo instead and replace the current `gcr.io/*` ones?
-  If "yes" to my above question, how much do we want to use the transition doc that you shared? Are we intending to move to `pkg.dev` as suggested in the doc or sth like quay.io or similar?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T06:36:38Z

> By "stop using" do you actually mean use another repo instead and replace the current gcr.io/* ones?

Ideally we use images in the `registry.k8s.io/kubernetes` repo ([browse](https://explore.ggcr.dev/?repo=registry.k8s.io%2Fkubernetes))

The options I see:
1. reach out to the owners of [perf-tests](https://github.com/kubernetes/perf-tests/tree/master/util-images/sleep) to publish the images to  `registry.k8s.io/kubernetes` 
2. reach out to the k8s-infra team to mirror the images to `registry.k8s.io/kubernetes`  
3. migrate to use some of the images which are already there, candidates are: [`kubernetes/pause`](https://explore.ggcr.dev/?repo=registry.k8s.io%2Fkubernetes%2Fpause), or busybox which is used by [k8s e2e tests](https://github.com/kubernetes/kubernetes/blob/4a0b0365efd6a4c072a1545f7beed3b6664497c2/test/e2e/framework/job/fixtures.go#L74) which has the sleep function

I know some folks in perf-tests, so let me try with (1.) first.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T06:39:20Z

cc @jprzychodzen

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T07:27:24Z

I believe the only reason to use the perf-image was to have something lean. 

However, since this means extra maintenance costs I'm good to move to another option like the busybox used by core k8s e2e tests. 

If you have capacity @mabulgu  then feel free to prototype moving to another image (and we can check if this impacts the e2e execution time substantially - I very much doubt so, because probably most of the time is consumed by the operators in kube and kueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T09:31:52Z

I'm currently leaning to migrate to use another image, preferably busybox which is used in k8s upstream: https://github.com/kubernetes/kubernetes/blob/4a0b0365efd6a4c072a1545f7beed3b6664497c2/test/e2e/framework/job/fixtures.go#L74.  The reason being to have a larger community base helping to maintain in case of issues. It solves this issue in particular.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T10:08:41Z

One thing which is bit non-standard in the sleep image and is used by our e2e tests is the ability to control the exit code, like here: https://github.com/kubernetes-sigs/kueue/blob/88d83ffc9b39ce125a60b242200eb5ed9863ea9b/test/e2e/singlecluster/e2e_test.go#L150. However, when me migrate to busybox we can replace that with a helper function encapsulating a script to return the desired exit code, like in upstream, [example](https://github.com/kubernetes/kubernetes/blob/master/test/e2e/framework/job/fixtures.go#L95-L153).

EDIT: and actually it enables us to make sure the SIGTERM trap is registered for sure as we do upstream in [here](https://github.com/kubernetes/kubernetes/pull/124396). The current approach while works most of the time is sometimes flaky, because it is not guaranteed the trap is [registered](https://github.com/kubernetes/perf-tests/blob/e65fb605afe9891223ed5382089fb04b95a06e31/util-images/sleep/main.go#L58)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-07T11:12:21Z

I'm leaning to use sleep from busybox as in k8s. WDYT @tenzen-y ?

@mabulgu do you have the capacity to work on this?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-08T21:12:44Z

I am leaning toward to registry.k8s.io/kubernetes/pause.
Do you have specific case where we want to verify the SIGTERM trap or more detailed container exit code?
Could we delegate the verifications to core Kube, and we focus only on the Kueue related behavior?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-09T08:35:19Z

> Do you have specific case where we want to verify the SIGTERM trap or more detailed container exit code?

We have currently 3 places which pass the `termination-code=1` so that the pod fails on deletion (see [here](https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue%20termination-code&type=code)). 

> Could we delegate the verifications to core Kube, and we focus only on the Kueue related behavior?

Yes, but I think the places which use custom exit code are meant to induce the pod to fail on deletion.
For example [here](https://github.com/kubernetes-sigs/kueue/blob/bf4657adc4e82b1458a8e0f78e0e21af15486d7b/test/e2e/singlecluster/pod_test.go#L209).

I guess we would either need to find another reliable way of failing the pods, but I'm not sure how to do it. We could also use `registry.k8s.io/kubernetes/pause` for all test cases, and just for the few which want non-zero exit code use busybox. It will be less work to start with. WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-17T04:25:55Z

> > Do you have specific case where we want to verify the SIGTERM trap or more detailed container exit code?
> 
> We have currently 3 places which pass the termination-code=1 so that the pod fails on deletion (see [here](https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue%20termination-code&type=code)).

IIUC, the kube-controller-manager uses the SIGTERM trap since the controllers have a mechanism and features based on the fine-grained exit code and finished container state.

But, in the Kueue side, the container terminal state does not matter since we want to just observe if Pod is finished except for exit code 0.

What is your motivation to handle a more fine-grained container terminal state on the Kueue side?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-17T13:23:40Z

I think we currently don't have any tests currently in Kueue which look at specific exit codes. However, we use non-zero exit codes to trigger pod failures on delete. This is meant to test specific scenarios for pod integration as the code depends on the pod failure / success, for example: https://github.com/kubernetes-sigs/kueue/blob/dc3d9bda112b786386a55c0b922094d1cd955f83/pkg/controller/jobs/pod/pod_controller.go#L724-L726. 

I don't think we currently have e2e depending on that for TAS, but there too the code for handling pod failures and successes differs in some places, as TAS manages pods.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-21T11:00:19Z

> I think we currently don't have any tests currently in Kueue which look at specific exit codes. However, we use non-zero exit codes to trigger pod failures on delete. This is meant to test specific scenarios for pod integration as the code depends on the pod failure / success, for example:
> 
> [kueue/pkg/controller/jobs/pod/pod_controller.go](https://github.com/kubernetes-sigs/kueue/blob/dc3d9bda112b786386a55c0b922094d1cd955f83/pkg/controller/jobs/pod/pod_controller.go#L724-L726)
> 
> Lines 724 to 726 in [dc3d9bd](/kubernetes-sigs/kueue/commit/dc3d9bda112b786386a55c0b922094d1cd955f83)
> 
>  if podInGroup.Status.Phase == corev1.PodFailed { 
>  	continue 
>  } 
> .
> I don't think we currently have e2e depending on that for TAS, but there too the code for handling pod failures and successes differs in some places, as TAS manages pods.

Uhm, I see. It seems that my understanding for `pause` was not correct. I assumed that the image can be execute shell command like `exit 1`. But as I checked the image in my local, the `pause` image does not have any shell. So, if we want to terminate the container with an arbitrary exit code, we need to use another image.

```shell
docker run --entrypoint "/bin/sh" -it registry.k8s.io/kubernetes/pause:3.10
docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: exec: "/bin/sh": stat /bin/sh: no such file or directory: unknown.
```

So, I would put +1 on `busybox`. Thank you for clarifications!

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-28T13:47:13Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-29T12:38:27Z

Ok, so I have changed the image to BusyBox v1.37.
Most of the cases are fine, I didn't tackle the `--termination code` yet, but I have checked how to do it, seems fairly easy.
However what I have observed in e2e tests is that time to delete pod has increased, thus sometimes 45 seconds is not enough.
From 3-4 seconds to 1 minute and 4 seconds... pretty significant.
Ofc it depends on number of pods to be deleted, but LWS tests are pretty consistent with this extended time of timeout.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T13:03:10Z

you might be missing a sigterm trap and then the delete requests wait for sigkill which is 30s later by default

### Comment by [@aojea](https://github.com/aojea) — 2025-01-30T20:55:30Z

agnhost image container all the necessary features for e2e, and if not we should add it, you can use it as pause image too

`kubectl exec test-agnhost -- /agnhost pause`

https://github.com/kubernetes/kubernetes/tree/master/test/images/agnhost#pause

handling sigterm

https://github.com/kubernetes/kubernetes/tree/master/test/images/agnhost#netexec

> 	CmdNetexec.Flags().IntVar(&delayShutdown, "delay-shutdown", 0, "Number of seconds to delay shutdown when receiving SIGTERM.")

https://github.com/kubernetes/kubernetes/blob/cec0492ddf39411aada4006a9f98fb22b6df9a7d/test/images/agnhost/netexec/netexec.go#L144

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-05T13:10:17Z

> agnhost image container all the necessary features for e2e, and if not we should add it, you can use it as pause image too
> 
> `kubectl exec test-agnhost -- /agnhost pause`
> 
> https://github.com/kubernetes/kubernetes/tree/master/test/images/agnhost#pause
> 
> handling sigterm
> 
> https://github.com/kubernetes/kubernetes/tree/master/test/images/agnhost#netexec
> 
> > CmdNetexec.Flags().IntVar(&delayShutdown, "delay-shutdown", 0, "Number of seconds to delay shutdown when receiving SIGTERM.")
> 
> https://github.com/kubernetes/kubernetes/blob/cec0492ddf39411aada4006a9f98fb22b6df9a7d/test/images/agnhost/netexec/netexec.go#L144

Oh, I did not know that. Thank you!
@mimowo I guess that we can avoid manual handling of SIGTERM once we introduce this image instead of busybox.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-05T13:16:48Z

> @mimowo I guess that we can avoid manual handling of SIGTERM once we introduce this image instead of busybox.

Indeed, I think we can use netexec /exit to exit the pod "on-demand", requesting "success" or "failure". Instead, of handling SIGTERM from within the container.

@mszadkow is already prototyping this approach https://github.com/kubernetes-sigs/kueue/pull/4145. There might be some gotchas here and there, for example we probably need to wait until the `/exit` endpoint is exposed. Seeing the pod "Running" will not be enough. Maybe seeing the pod "Ready" would, I'm not sure - it requires research.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-05T13:27:05Z

> [@mszadkow](https://github.com/mszadkow) is already prototyping this approach [#4145](https://github.com/kubernetes-sigs/kueue/pull/4145). There might be some gotchas here and there, for example we probably need to wait until the `/exit` endpoint is exposed. Seeing the pod "Running" will not be enough. Maybe seeing the pod "Ready" would, I'm not sure - it requires research.

Oh, that looks great progressing! @mszadkow @mimowo Thank you for moving this forward!
