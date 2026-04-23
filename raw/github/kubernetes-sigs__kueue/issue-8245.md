# Issue #8245: TAS NodeHotSwap: workload is requeued by scheduler even if already deleted

**Summary**: TAS NodeHotSwap: workload is requeued by scheduler even if already deleted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8245

**Last updated**: 2025-12-17T15:10:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-15T15:11:02Z
- **Updated**: 2025-12-17T15:10:12Z
- **Closed**: 2025-12-17T15:10:12Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 6

## Description

**What happened**:

TAS NodeHotSwap when tries to evict workload indefinitely if the workload is deleted in the meanwhile.

Each time after during the eviction attempt it sends a request to API server, slowing down scheduler.

**What you expected to happen**:

Scheduler should give up with the workload is deleted as we do in case of failed admission here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L667-L673

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T15:11:14Z

cc @PBundyra @pajakd @mbobrovskyi

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-15T17:21:50Z

/assign sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T06:37:52Z

Sohan do you have some progress on that? Since this issue is important for us we want to include @mbobrovskyi  to work on the bugfix too.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-16T10:24:04Z

/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-16T23:18:37Z

>Sohan do you have some progress on that? Since this issue is important for us we want to include @mbobrovskyi to work on the bugfix too.

Sure, I'm posting my test here since @mimowo had asked to share it. I'm also leaning towards adding an integration test but that decision I will leave it up to @mbobrovskyi 

<details>
<summary>test</summary>

```go
func TestScheduleForTASEvictionSkipsDeletedWorkload(t *testing.T) {
	now := time.Now().Truncate(time.Second)
	tasRackLabel := "cloud.provider.com/rack"

	ns := utiltesting.MakeNamespaceWrapper(metav1.NamespaceDefault).Obj()
	topology := utiltestingapi.MakeTopology("topology").
		Levels("cloud.com/topology-block", tasRackLabel, corev1.LabelHostname).
		Obj()
	rf := utiltestingapi.MakeResourceFlavor("rf").
		NodeLabel("tas-node", "true").
		TopologyName(topology.Name).
		Obj()
	cq := utiltestingapi.MakeClusterQueue("cq").
		ResourceGroup(*utiltestingapi.MakeFlavorQuotas(rf.Name).Resource(corev1.ResourceCPU, "1").Obj()).
		Obj()
	lq := utiltestingapi.MakeLocalQueue("lq", ns.Name).ClusterQueue(cq.Name).Obj()
	wl := utiltestingapi.MakeWorkload("wl", ns.Name).
		ResourceVersion("1").
		UnhealthyNodes("x0").
		Queue(kueue.LocalQueueName(lq.Name)).
		PodSets(*utiltestingapi.MakePodSet("one", 1).
			PreferredTopologyRequest(tasRackLabel).
			Request(corev1.ResourceCPU, "1").
			Obj()).
		ReserveQuotaAt(
			utiltestingapi.MakeAdmission(cq.Name).
				PodSets(utiltestingapi.MakePodSetAssignment("one").
					Assignment(corev1.ResourceCPU, kueue.ResourceFlavorReference(rf.Name), "1000m").
					TopologyAssignment(utiltestingapi.MakeTopologyAssignment([]string{corev1.LabelHostname}).
						Domain(utiltestingapi.MakeTopologyDomainAssignment([]string{"x0"}, 1).Obj()).
						Obj()).
					Obj()).
				Obj(),
			now,
		).
		AdmittedAt(true, now).
		Obj()

	features.SetFeatureGateDuringTest(t, features.TopologyAwareScheduling, true)
	features.SetFeatureGateDuringTest(t, features.TASFailedNodeReplacementFailFast, true)

	ctx, log := utiltesting.ContextWithLog(t)
	clientBuilder := utiltesting.NewClientBuilder().
		WithObjects(ns, topology, rf, cq, lq, wl).
		WithStatusSubresource(&kueue.Workload{}).
		WithInterceptorFuncs(interceptor.Funcs{
			SubResourcePatch: func(ctx context.Context, c client.Client, subResourceName string, obj client.Object, patch client.Patch, opts ...client.SubResourcePatchOption) error {
				if wl, ok := obj.(*kueue.Workload); ok && subResourceName == "status" {
					return apierrors.NewNotFound(kueue.Resource("workloads"), wl.Name)
				}
				return c.SubResource(subResourceName).Patch(ctx, obj, patch, opts...)
			},
		})
	_ = tasindexer.SetupIndexes(ctx, utiltesting.AsIndexer(clientBuilder))
	cl := clientBuilder.Build()

	fakeClock := testingclock.NewFakeClock(now)
	cqCache := schdcache.New(cl)
	qManager := qcache.NewManager(cl, cqCache, qcache.WithClock(fakeClock))
	cqCache.AddOrUpdateResourceFlavor(log, rf)
	cqCache.AddOrUpdateTopology(log, topology)
	if err := cqCache.AddClusterQueue(ctx, cq); err != nil {
		t.Fatalf("AddClusterQueue: %v", err)
	}
	if err := qManager.AddClusterQueue(ctx, cq); err != nil {
		t.Fatalf("AddClusterQueue to manager: %v", err)
	}
	if err := qManager.AddLocalQueue(ctx, lq); err != nil {
		t.Fatalf("AddLocalQueue: %v", err)
	}
	if qManager.QueueSecondPassIfNeeded(ctx, wl, 0) {
		fakeClock.Step(time.Second)
	}

	// Delete workload after it's queued but before scheduling.
	if err := cl.Delete(ctx, wl); err != nil {
		t.Fatalf("Delete workload: %v", err)
	}

	scheduler := New(qManager, cqCache, cl, &utiltesting.EventRecorder{}, WithClock(t, fakeClock))
	wg := sync.WaitGroup{}
	scheduler.setAdmissionRoutineWrapper(routine.NewWrapper(
		func() { wg.Add(1) },
		func() { wg.Done() },
	))

	ctx, cancel := context.WithTimeout(ctx, queueingTimeout)
	go qManager.CleanUpOnContext(ctx)
	defer cancel()

	// Should complete without error (previously would retry indefinitely)
	scheduler.schedule(ctx)
	wg.Wait()

	// Verify workload was dropped (not requeued) when eviction fails with NotFound.
	pending, err := qManager.Pending(cq)
	if err != nil {
		t.Fatalf("Failed to get pending workloads: %v", err)
	}
	if pending != 0 {
		t.Errorf("Expected no pending workloads, but found %d", pending)
	}
}
```
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-17T03:40:51Z

> Sure, I'm posting my test here since @mimowo had asked to share it. I'm also leaning towards adding an integration test but that decision I will leave it up to @mbobrovskyi

Nice! Thank you so much for test!
