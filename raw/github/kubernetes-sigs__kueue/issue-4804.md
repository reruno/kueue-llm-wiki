# Issue #4804: LeaderWorkerSet does not work when manageJobsWithoutQueuename is used

**Summary**: LeaderWorkerSet does not work when manageJobsWithoutQueuename is used

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4804

**Last updated**: 2025-04-11T16:32:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-27T06:08:30Z
- **Updated**: 2025-04-11T16:32:45Z
- **Closed**: 2025-04-11T16:32:45Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description


**What happened**:

LeaderWorkerSet does not work properly when manageJobsWithoutQueuename is used:
1. it does not run worker pods when queue-name is specified
2. it bypasses quota checks and runs leader pods when queue-name is not specified

**What you expected to happen**:

All pods are scheduling gated.

**How to reproduce it (as minimally and precisely as possible)**:

1. enable LWS integration and configure manageJobsWithoutQueuename: true
2. 
Create LWS:
```
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: leaderworkerset-multi-template
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  replicas: 3
  leaderWorkerTemplate:
    leaderTemplate:
      spec:
        containers:
        - name: nginx2
          image: nginx:1.14.2
          resources:
            limits:
              cpu: "100m"
            requests:
              cpu: "50m"
          ports:
          - containerPort: 8080
    size: 4
    workerTemplate:
      spec:
        containers:
        - name: nginx
          image: nginx:1.14.2
          resources:
            limits:
              cpu: "100m"
            requests:
              cpu: "50m"
          ports:
          - containerPort: 8080
```

Issue: 
Pods don't run properly
```
> k get pods
NAME                                 READY   STATUS            RESTARTS   AGE
leaderworkerset-multi-template-0     1/1     Running           0          58s
leaderworkerset-multi-template-0-1   0/1     SchedulingGated   0          58s
leaderworkerset-multi-template-0-2   0/1     SchedulingGated   0          58s
leaderworkerset-multi-template-0-3   0/1     SchedulingGated   0          58s
leaderworkerset-multi-template-1     1/1     Running           0          58s
leaderworkerset-multi-template-1-1   0/1     SchedulingGated   0          58s
leaderworkerset-multi-template-1-2   0/1     SchedulingGated   0          58s
leaderworkerset-multi-template-1-3   0/1     SchedulingGated   0          58s
leaderworkerset-multi-template-2     1/1     Running           0          58s
leaderworkerset-multi-template-2-1   0/1     SchedulingGated   0          58s
leaderworkerset-multi-template-2-2   0/1     SchedulingGated   0          58s
leaderworkerset-multi-template-2-3   0/1     SchedulingGated   0          58s
```

Also, workloads look wrong:
```
> k get wl  
NAME                                                     QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
leaderworkerset-leaderworkerset-multi-template-0-49843   user-queue   cluster-queue   True                  7s
leaderworkerset-leaderworkerset-multi-template-1-0a62f   user-queue   cluster-queue   True                  7s
leaderworkerset-leaderworkerset-multi-template-2-67d82   user-queue   cluster-queue   True                  7s
pod-leaderworkerset-multi-template-0-1-b8d19                                                                7s
pod-leaderworkerset-multi-template-0-1deeb                                                                  7s
pod-leaderworkerset-multi-template-0-2-672ba                                                                7s
pod-leaderworkerset-multi-template-0-3-6a4d3                                                                7s
pod-leaderworkerset-multi-template-1-1-c39e1                                                                7s
pod-leaderworkerset-multi-template-1-2-b8ca2                                                                7s
pod-leaderworkerset-multi-template-1-3-aaf70                                                                7s
pod-leaderworkerset-multi-template-1-9472f                                                                  7s
pod-leaderworkerset-multi-template-2-1-1ec4c                                                                7s
pod-leaderworkerset-multi-template-2-2-e8505                                                                7s
pod-leaderworkerset-multi-template-2-3-8a7dc                                                                7s
pod-leaderworkerset-multi-template-2-b0301                                                                  7s
```

**Anything else we need to know?**:

I also tested without setting queueName, and this is also wrong - the leader pods start bypassing the quota checks.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-27T06:08:41Z

/assign @mbobrovskyi 
tentatively
