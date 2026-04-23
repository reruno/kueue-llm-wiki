# Issue #4378: MultiKueue when Creating a multikueue admission check Should run an appwrapper containing a job on worker if admitted

**Summary**: MultiKueue when Creating a multikueue admission check Should run an appwrapper containing a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4378

**Last updated**: 2025-03-19T08:15:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-02-24T14:44:57Z
- **Updated**: 2025-03-19T08:15:35Z
- **Closed**: 2025-03-19T08:15:33Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
This e2e multikueue test flaked:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4301/pull-kueue-test-e2e-multikueue-main/1894013562272092160

**What you expected to happen**:
I expected test to succeed

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T14:48:31Z

/kind flake

This might be same flake with https://github.com/kubernetes-sigs/kueue/issues/4376
But those have different error messages.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T14:49:44Z

/retitle MultiKueue when Creating a multikueue admission check Should run an appwrapper containing a job on worker if admitted

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T14:49:53Z

cc: @dgrove-oss

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-25T22:29:10Z

In both cases, the appwrapper controller on worker1 (where the job is expected to run),  has an odd problem shown below during startup when it is trying to load a config map to get the operator configuration.
```
2025-02-24T12:42:12.42429078Z stderr F 2025-02-24T12:42:12.423929135Z	INFO	setup	log/deleg.go:127	Build info	{"version": "v1.0.4", "date": "2025-02-12 14:01"}
2025-02-24T12:42:12.425600879Z stderr F 2025-02-24T12:42:12.425383746Z	ERROR	setup	log/deleg.go:142	unable to initialise configuration	{"error": "failed to get API group resources: unable to retrieve the complete list of server APIs: v1: Get \"https://10.96.0.1:443/api/v1\": dial tcp 10.96.0.1:443: connect: network is unreachable"}
2025-02-24T12:42:12.425614359Z stderr F sigs.k8s.io/controller-runtime/pkg/log.(*delegatingLogSink).Error
2025-02-24T12:42:12.425619789Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.19.3/pkg/log/deleg.go:142
2025-02-24T12:42:12.425624829Z stderr F github.com/go-logr/logr.Logger.Error
2025-02-24T12:42:12.425629739Z stderr F 	/go/pkg/mod/github.com/go-logr/logr@v1.4.2/logr.go:301
2025-02-24T12:42:12.425634239Z stderr F main.exitOnError
2025-02-24T12:42:12.425638979Z stderr F 	/workspace/cmd/main.go:221
2025-02-24T12:42:12.425643839Z stderr F main.main
2025-02-24T12:42:12.425648099Z stderr F 	/workspace/cmd/main.go:108
2025-02-24T12:42:12.425652289Z stderr F runtime.main
2025-02-24T12:42:12.42565638Z stderr F 	/usr/local/go/src/runtime/proc.go:272
```

I wonder if we the `waitForOperatorAvailability` function in the e2e utility package isn't stringent enough and we are trying to run the multikueue test before all the controllers on the worker node are really ready.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-27T15:10:53Z

@dgrove-oss just a speculation, but could this be due to interference with this test: https://github.com/kubernetes-sigs/kueue/blob/398c74d105743af8a3ad0d660323e5fdbfaf6e30/test/e2e/multikueue/e2e_test.go#L862.

This message makes me think: "dial tcp 10.96.0.1:443: connect: network is unreachable".

Maybe this somehow makes the AppWrapper controller crashing?

IIRC the tests don't run in parallel, but maybe even then the previous test could give hard time to the AppWrapper controller?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-28T16:41:25Z

When the AppWrapper controller is [initializing](https://github.com/project-codeflare/appwrapper/blob/main/cmd/main.go#L101-L108), it is written to exit on errors.  In this particular case, the `Get` inside of `loadConfig` ([here](https://github.com/project-codeflare/appwrapper/blob/main/cmd/main.go#L193-L206)) returned a network error.

I'm open to other ways of structuring AppWrapper's startup code, but it seemed like exiting with an error and letting the pod restart was more robust than trying to handle it or masking with a retry loop.  Kueue's main seems to be structured similarly.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-03T15:22:53Z

Yeah, this looks ok in principle. I think the test code in Kueue should wait for AppWrapper to be "Ready / Available". And the readiness should be communicated via the probe. So, IIUC in the failed tests AppWrapper was never Ready, or it was and then crashed?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-03T15:35:30Z

 I found a bug in the appwrapper startup sequence, which would cause the readiness probe to return true prematurely.  

In this [code](https://github.com/project-codeflare/appwrapper/blob/e12209bca297878f98ea464cf90646150ded387b/cmd/main.go#L156-L167), the call to `SetupProbeEndpoints` is supposed to be inside the go routine (and thus wait for certs to be generated). 

I'll fix and do an appwrapper point release, but I'm not totally convinced that is what is the root cause of the flake.  I thought in the log I was looking at the network error happened even earlier in startup.  But sometimes log tracebacks can be misleading.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-03T15:38:24Z

> I found a bug in the appwrapper startup sequence, which would cause the readiness probe to return true prematurely.
> 
> In this [code](https://github.com/project-codeflare/appwrapper/blob/e12209bca297878f98ea464cf90646150ded387b/cmd/main.go#L156-L167), the call to `SetupProbeEndpoints` is supposed to be inside the go routine (and thus wait for certs to be generated).
> 
> I'll fix and do an appwrapper point release, but I'm not totally convinced that is what is the root cause of the flake. I thought in the log I was looking at the network error happened even earlier in startup. But sometimes log tracebacks can be misleading.

Strike that.  The code is right as is.  Monday morning and not enough coffee yet.  The health probe is registered immediately.  The readiness probe waits on certs being generated.  Same logic as Kueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:15:29Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:15:34Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4378#issuecomment-2735681394):

>/close
>Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.
>
>The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.
>
>For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).
>
>If the failure re-occurs feel free to re-open or open a new one.
>
>Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
