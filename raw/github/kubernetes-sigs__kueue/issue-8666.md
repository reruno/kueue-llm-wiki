# Issue #8666: LWS: Kueue creates single PodSet Workload even though multiple StatefulSets were created

**Summary**: LWS: Kueue creates single PodSet Workload even though multiple StatefulSets were created

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8666

**Last updated**: 2026-03-06T08:23:11Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-19T15:09:12Z
- **Updated**: 2026-03-06T08:23:11Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 13

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When I create a LeaderWorkerSet with only a worker template, but multiple sizes (`.spec.leaderWorkerTemplate.size`), Kueue creates a Workload with a single PodSet.

```shell
$ kubectl get statefulset
NAME                               READY   AGE
leaderworkerset-multi-template     1/1     1m
leaderworkerset-multi-template-0   3/3     1m
```

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Workload
metadata:
  annotations:
    kueue.x-k8s.io/is-group-workload: "true"
  generation: 1
  name: leaderworkerset-leaderworkerset-multi-template-0-31821
  namespace: default
spec:
  active: true
  podSets:
  - count: 4
    name: main
    template: { ... }
    topologyRequest:
      podIndexLabel: leaderworkerset.sigs.k8s.io/worker-index
  priority: 0
  queueName: tas-user-queue
```

**What you expected to happen**:
I'm not sure if this is a valid report, but I guess that the expected Workload has 2 PodSets, separately.

**How to reproduce it (as minimally and precisely as possible)**:

1. Set up cluster, Kueue, and LWS operator (v0.7.0).
2. Enable LWS integration in Kueue Config ConfigMap
3. Set up ClusterQueue and LocalQueues
4. Deploy the following LWS in the following:

```yaml
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: leaderworkerset-multi-template
  labels:
    kueue.x-k8s.io/queue-name: "user-queue"
spec:
  replicas: 1
  leaderWorkerTemplate:
    size: 4
    workerTemplate:
      spec:
        containers:
        - name: nginx
          image: nginxinc/nginx-unprivileged:1.27
          resources:
            limits:
              cpu: "100m"
            requests:
              cpu: "50m"
          ports:
          - containerPort: 8080
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.35.0
- Kueue version (use `git describe --tags --dirty --always`): v0.15.2
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others: LWS v0.7.0

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T15:10:57Z

@mimowo I'm not sure if this is a bug, and I couldn't any discussions about this.

Let me also ping the LWS integratioin developers > @mbobrovskyi @vladikkuzn

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T15:11:47Z

If this is expected and no bug, I'm fine with closing this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T15:12:46Z

I think this is not a bug - the PodSet represents the entire LWS Group. LWS has this weird construction where one StatefulSet is to represent all leaders, across all groups. So there is always +1 StatefulSet compared to the number of Groups. In Kueue we represent Groups by Workloads.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T15:23:39Z

> I think this is not a bug - the PodSet represents the entire LWS Group. LWS has this weird construction where one StatefulSet is to represent all leaders, across all groups. So there is always +1 StatefulSet compared to the number of Groups. In Kueue we represent Groups by Workloads.

I meant that, wondering if we should create the following Workload.

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Workload
metadata:
  annotations:
    kueue.x-k8s.io/is-group-workload: "true"
  name: leaderworkerset-leaderworkerset-multi-template-0-31821
  namespace: default
spec:
  active: true
  podSets:
  - count: 1
    name: leader
    template: { ... }
  - count: 3
    name: worker
    template: { ... }
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T15:31:01Z

ahh, I see, yes. I think:
- Kueue Workload represents LWS Group
- Kueue Workload should have two PodSets: one for leaders, one for workers. 

Thanks for raising, maybe @mbobrovskyi knows. I think it might be an older attempt to make co-scheduling for TAS working before we had the proper PodSet grouping introduced which allows to co-scheduler leader and workers.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T16:12:15Z

> ahh, I see, yes. I think:
> 
> * Kueue Workload represents LWS Group
> * Kueue Workload should have two PodSets: one for leaders, one for workers.
> 
> Thanks for raising, maybe [@mbobrovskyi](https://github.com/mbobrovskyi) knows. I think it might be an older attempt to make co-scheduling for TAS working before we had the proper PodSet grouping introduced which allows to co-scheduler leader and workers.

yes, exactly. let's wait for input from @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:23:38Z

/priority important-soon

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-19T16:33:32Z

> Thanks for raising, maybe @mbobrovskyi knows. I think it might be an older attempt to make co-scheduling for TAS working before we had the proper PodSet grouping introduced which allows to co-scheduler leader and workers.

Yeah, exactly. We had some issues with TAS here: https://github.com/kubernetes-sigs/kueue/pull/4146#pullrequestreview-2614585453

I’m not sure whether it has been fixed yet.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-19T16:44:37Z

Also this https://github.com/kubernetes-sigs/kueue/pull/4023#discussion_r1930244087 and this https://github.com/kubernetes-sigs/kueue/pull/4023#discussion_r1930246572 for context.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T17:30:34Z

I think this issues should be largely solved now with the PodSet Grouping approach. Still, we need to be careful during transition time.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-19T18:45:37Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T19:56:04Z

> > Thanks for raising, maybe [@mbobrovskyi](https://github.com/mbobrovskyi) knows. I think it might be an older attempt to make co-scheduling for TAS working before we had the proper PodSet grouping introduced which allows to co-scheduler leader and workers.
> 
> Yeah, exactly. We had some issues with TAS here: [#4146 (review)](https://github.com/kubernetes-sigs/kueue/pull/4146#pullrequestreview-2614585453)
> 
> I’m not sure whether it has been fixed yet.

Thank you for inputting the context.

> I think this issues should be largely solved now with the PodSet Grouping approach. Still, we need to be careful during transition time.

I think so too.
Another PoV to fix this issue is that we should leave the backward compatibility.
Even if we start a new Workload pattern for this LWS case, we should avoid disruptions to the existing LWS.

I think that we should keep the previous Workload creation mechanism for a while (e.g., 2 minor releases)
@mimowo Any thoughts on backward compatibility?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T08:23:10Z

Actually, on the second thought I'm no longer sure about the change, because:
1. as experiments by @mbobrovskyi show we would need custom code to provide backwards compatiblity
2. when TAS is used it also requires users to change their LWS instances to add the "podset-group" annotation - so I'm worried here
3. I see no benefit for the users to change the single Podset -> multiple PodSets model here
