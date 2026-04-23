# Issue #8668: [flaky multikueue test] MultiKueue when Connection via ClusterProfile no plugins uses ClusterProfile as way to connect worker cluster

**Summary**: [flaky multikueue test] MultiKueue when Connection via ClusterProfile no plugins uses ClusterProfile as way to connect worker cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8668

**Last updated**: 2026-01-27T12:50:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-19T15:43:55Z
- **Updated**: 2026-01-27T12:50:01Z
- **Closed**: 2026-01-27T12:50:01Z
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 13

## Description


**Which test is flaking?**:
MultiKueue when Connection via ClusterProfile no plugins uses ClusterProfile as way to connect worker cluster
**First observed in** (PR or commit, if known):
don't know
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2013243602003562496
**Failure message or logs**:
```
End To End MultiKueue Suite: kindest/node:v1.34.0: [It] MultiKueue when Connection via ClusterProfile no plugins uses ClusterProfile as way to connect worker cluster expand_less	55s
{Expected success, but got an error:
    <*errors.StatusError | 0xc00099bea0>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc00099bea0>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    }
In [AfterEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:207 @ 01/19/26 13:57:31.823
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T15:44:08Z

cc @mszadkow @kshalot ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:22:59Z

/priority important-soon

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-19T16:24:31Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-22T08:40:54Z

I did extensive retests to catch the flakiness, both locally and in the PR workflow.
I hit timeouts of 1h with `--until-it-fails` flag, but no flakiness.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-22T10:04:36Z

Ahh finally, reproduced: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8718/pull-kueue-test-e2e-multikueue-release-0-15/2014258080262393856

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T07:19:29Z

Ok I have analyzed the logs from the first build:
From https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2013243602003562496/build-log.txt we see the rollout started around `13:57:05.753`, and at `13:57:31.778` all replicas were available. 

Now, let's look at the kubelet logs: https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2013243602003562496/artifacts/run-test-multikueue-e2e-1.34.0/kind-manager-worker/kubelet.log


We see that there are two replicas around that time:
- old replica (because added at `13:56:39.712802`, so before rollout started) `kueue-controller-manager-86dfd88fd5-gkmlr` 
- new replica (because added at `13:57:19.476555`, so after rollout started)  `kueue-controller-manager-5987847b9d-kdm9s` 

```
Jan 19 13:57:22 kind-manager-worker kubelet[224]: I0119 13:57:22.309204     224 prober.go:111] "Probe succeeded" probeType="Readiness" pod="kueue-system/kueue-controller-manager-86dfd88fd5-gkmlr" podUID="986d8aed-c25d-49ee-a009-6c52dee8cc7a" containerName="manager"
...
Jan 19 13:57:31 kind-manager-worker kubelet[224]: I0119 13:57:31.444377     224 prober.go:111] "Probe succeeded" probeType="Readiness" pod="kueue-system/kueue-controller-manager-5987847b9d-kdm9s" podUID="1383c4b9-4d0e-4021-a585-d9fd34dd98d4" containerName="manager"
...
Jan 19 13:57:31 kind-manager-worker kubelet[224]: I0119 13:57:31.489177     224 kubelet.go:2530] "SyncLoop DELETE" source="api" pods=["kueue-system/kueue-controller-manager-86dfd88fd5-gkmlr"]
...
Jan 19 13:57:32 kind-manager-worker kubelet[224]: I0119 13:57:32.303924     224 prober.go:120] "Probe failed" probeType="Readiness" pod="kueue-system/kueue-controller-manager-86dfd88fd5-gkmlr" podUID="986d8aed-c25d-49ee-a009-6c52dee8cc7a" containerName="manager" probeResult="failure" output="Get \"http://10.244.1.15:8081/readyz\": dial tcp 10.244.1.15:8081: connect: connection refused
```
So, I think we can see around `13:57:31` the last probe result from both replicas was success. This is indeed possible because here we ony check Status.Replicas=Status.AvailableReplicas: https://github.com/kubernetes-sigs/kueue/blob/cb6956603b580326f38f5b2e37c423a1ca850604/test/util/e2e.go#L446-L455.
Similarly later we check the number of ReadyEndpoints equals the number of ReadyPods, but this also might be 2 in this case.

I think we should also check here the number of AvailableReplicas equals **spec.Replicas** which is 1. This will also ensure we have only 1 ReadyEndpoint. This is important so that traffic is not directed to the dying replica any longer.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-26T08:24:28Z

@mimowo great idea, I will give it a try!

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T08:30:06Z

Thanks, basically we should extend the check `g.Expect(deployment.Status.Replicas).To(gomega.Equal(deployment.Status.AvailableReplicas)) ` with also `g.Expect(deployment.Spec.Replicas).To(gomega.Equal(deployment.Status.AvailableReplicas)) ` (or something that also expresses the intention.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-26T08:32:02Z

I got it, though it's worrying as `.Status.Replicas` should be not terminating replicas as stated:
`Total number of non-terminating pods targeted by this deployment (their labels match the selector).`

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T08:38:52Z

I don't understand, why this is worrying?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T08:44:40Z

Do you mean because the old replica received DELETE event at `13:57:31.489177`, so at this point it should already be terminating, so not included in the status.Replicas. which was checked around `13:57:31.778`?  So, yes, I think time timestamps suggest the status.Replicas should be 1 at the moment of the check, but things need to happen:
1. The DELETE request needs to get seen by the Deployment controller
2. The Deployment controller needs to update the status to lower status.Replicas=1
3. The informer in the test code needs to notice the new Deployment with status.Replicas=1

So, indeed these steps typically happen fast, and thus it almost never flakes. However, I think it is possible that occasionally not all the steps happen within 300ms.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T08:46:41Z


Maybe this is not the only issue, but I think checking explicitly that status.AvailableReplicas=spec.Replicas will not hurt, and will eliminate this possible source of flakiness.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T09:31:41Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8810/pull-kueue-test-e2e-multikueue-release-0-15/2016072756348588032
