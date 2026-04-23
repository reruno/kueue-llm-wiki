# Issue #8850: Flaky E2E Test: MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster

**Summary**: Flaky E2E Test: MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8850

**Last updated**: 2026-01-28T10:27:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-28T07:13:45Z
- **Updated**: 2026-01-28T10:27:53Z
- **Closed**: 2026-01-28T10:27:53Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 9

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

End To End MultiKueue Suite: kindest/node:v1.34.3: [It] MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster 

**First observed in** (PR or commit, if known):

periodic Job

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/2016286247412043776

**Failure message or logs**:
```shell
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/e2e.go:235 with:
Expected
    <string>: NewReplicaSetCreated
to be an element of
    <[]string | len:2, cap:2>: [
        "NewReplicaSetAvailable",
        "ReplicaSetUpdated",
    ] failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/e2e.go:235 with:
Expected
    <string>: NewReplicaSetCreated
to be an element of
    <[]string | len:2, cap:2>: [
        "NewReplicaSetAvailable",
        "ReplicaSetUpdated",
    ]
In [BeforeAll] at: /home/prow/go/src/kubernetes-sigs/kueue/test/util/e2e.go:625 @ 01/27/26 23:31:51.685
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T07:54:36Z

Ah the step "Update 'kueue-controller-manager' deployment to have the secretreader-plugin binary" updates the Deployment spec, but never waits for the Kueue status to be "Available", then we start the next step "Updating MultiKueue configuration with CredentialsProviders" which fails on the assertion, because it assumes that Kueue is "Available" at this point.

The options I can see:
1. relax the assertion to add `NewReplicaSetCreated` to the options allowed by `RestartKueueController`
2.  wait for Kueue to be available in this step "Update 'kueue-controller-manager' deployment to have the secretreader-plugin binary"

I think actually (2.)  makes sense, because then if the new deployment configuration is wrong we will fail fast. If we do (1.) we may have harder debugging if it fails on the configuration update.

Still, from performance point of view, (1.) is faster, but debuggability will be trickier, and we already have many flakes.

cc @mszadkow @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-28T08:10:07Z

> Ah the step "Update 'kueue-controller-manager' deployment to have the secretreader-plugin binary" updates the Deployment spec, but never waits for the Kueue status to be "Available", then we start the next step "Updating MultiKueue configuration with CredentialsProviders" which fails on the assertion, because it assumes that Kueue is "Available" at this point.

I’m not sure I understand why we should wait for it.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T08:17:50Z

We don't need to. Technically speaking we could also relax the assert in `RestartKueueController`, because this is just a "sanity test" before rolling the update.

It is just about debuggability, if we relax the assertion, then if Kueue doesn't restart it will be two possibilities: 
1. wrong configuration of Kueue deployment , or 
2. wrong config map. 

If we assert that Kueue was healthy before rolling the config map update, then we know the problem was with the config map (2.).

However, I don't have a strong view here, just this feeling that any complication of debugging takes use more time than the couple of seconds of build time.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-28T08:33:53Z

Kueue startup can take 30+ seconds, and waiting for availability each time significantly increases our test runtime. We should avoid this.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-28T08:36:37Z

> 1. relax the assertion to add NewReplicaSetCreated to the options allowed by RestartKueueController

So I would propose starting with this.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-28T08:39:47Z

Anyway, I think we should relax the assertion to add NewReplicaSetCreated to the options allowed by RestartKueueController to avoid this problems in future.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-28T08:45:14Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T08:45:44Z

> Kueue startup can take 30+ seconds, and waiting for availability each time significantly increases our test runtime. We should avoid this.

Ok, just wanted to emphasize the debuggability complication. If we don't wait for healthy Kueue after deployment change, if Kueue doesn't restart after config map change, then possible failures accumulated: deployment or config map could be wrong.

Sure, 30+ seconds is important, but also 1h+ of debugging time by maintainer is costly. So, we need to find balance between runtime and debuggability,.

I think ultimately for MultiKueue I could see two suites of tests: 
1. one without config changes which is run in parallel, analogously to singlecluster parallel e2e tests
2. one which config changes which needs to run sequentially, analogous to "customconfigs"

For now, I'm ok with your proposal @mbobrovskyi , but such splitting of multikueue e2e tests will be great in the future

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-28T09:47:41Z

I was thinking maybe we could at this log just afterwards to know at which state was the deployment just before the restart:
```
ginkgo.GinkgoLogr.Info("Deployment status condition before the restart", "type", deploymentCondition.Type, "status", deploymentCondition.Status, "reason", deploymentCondition.Reason)
```
That I think could slightly increase the debuggability until we go for separate test suites.
In addition to previously mentioned modification.
