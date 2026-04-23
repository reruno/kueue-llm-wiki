# Issue #8113: Kueue's workload will conflict with in-tree Workload object

**Summary**: Kueue's workload will conflict with in-tree Workload object

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8113

**Last updated**: 2026-01-07T17:09:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-12-07T21:18:05Z
- **Updated**: 2026-01-07T17:09:42Z
- **Closed**: 2026-01-07T17:09:42Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 14

## Description

I was playing around with gang scheduling in tree in 1.35.

If you run `kubectl get workloads` with the workload APIs installed, you will now get the workload object from kubernetes.

```
k get workloads.kueue.x-k8s.io
NAME                         QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
job-sample-job-kkkbf-fcf7c   user-queue   cluster-queue   True                  23s
```
``` 
k get workloads
NAME    AGE
job-1   2m39s
```

Good news, is for now, k get wl will still find the kueue workload.

I just wanted to document this as I was playing around with gang scheduling in tree and this is what I noticed.

cc @tenzen-y @mimowo

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-08T07:17:57Z

Yes this is unfortunate, not sure if k8s would be willing to look for an alternative name still. We could ask about that.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-09T03:33:46Z

> k8s would be willing to look for an alternative name still

I don't think k/k will rename "workload" from now.. Rather I even think there is a future possibility that we might even overtake a shorten name `wl` as well

cc @dom4ha @wojtek-t

### Comment by [@wojtek-t](https://github.com/wojtek-t) — 2025-12-09T07:39:43Z

+1 to @sanposhiho

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-09T13:43:48Z

I guess for short name we could maybe add kwl (Kueue workload).

I'm not sure the best approach for workloads and Kueue though. I think renaming is a breaking change for us now

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:39:40Z

/priority important-soon
+1 on introducing kwl as short name in Kueue.

I'm also thinking core k8s could maybe consider "wo" instead, by analogy to "po" and "no" for pods and nodes, wdyt @sanposhiho @wojtek-t ?

### Comment by [@wojtek-t](https://github.com/wojtek-t) — 2025-12-19T11:18:25Z

I think that is probably ok.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-21T18:26:32Z

/assign

I'll update Kueue to use kwl.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-21T18:29:02Z

https://github.com/kubernetes-sigs/kueue/pull/8379

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-29T10:04:29Z

I know it'd be hard to fully rename Kueue's `workload` to something else from now, but I just wondered what if we add `kueueworkload` as an alias too? And, on the doc, encourage people just to use `kueueworkload` not `workload` to let the community get used to `kueueworkload and a shorter name `kwl`?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T09:48:12Z

> I know it'd be hard to fully rename Kueue's workload to something else from now, but I just wondered what if we add kueueworkload as an alias too? 

We can have an arbitrary number of aliases so +1 to use both "kwl" and "kueueworkload". 

Having said that I think we should strive in Kueue to propagate all the useful information from the Workload object to the Job (true Workload) object. Ideally the Workload object is only used internally by Kueue or by advanced users.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-07T09:59:11Z

Should we also add aliases to `kueuectl`?

https://github.com/kubernetes-sigs/kueue/blob/72d70ff68a0cfb2cbe2a99d468e82215efcaaf82/cmd/kueuectl/app/list/list_workload.go#L103

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:10:00Z

I think so

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-07T14:51:43Z

@mbobrovskyi nice find!

I'll update with what I found for kueuectl and add an additional shortName for "kueueworkload".

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-07T16:27:50Z

/kind feature
