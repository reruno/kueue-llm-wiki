# Issue #9875: [Failing - Test]: periodic link checker is failing

**Summary**: [Failing - Test]: periodic link checker is failing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9875

**Last updated**: 2026-03-31T07:42:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-14T13:47:51Z
- **Updated**: 2026-03-31T07:42:15Z
- **Closed**: 2026-03-31T07:42:15Z
- **Labels**: _none_
- **Assignees**: [@kannon92](https://github.com/kannon92), [@my-git9](https://github.com/my-git9)
- **Comments**: 7

## Description

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-verify-website-links-main

This PR just merged and it looks like it isn't functional yet.

```
Done setting up docker in docker.
+ WRAPPED_COMMAND_PID=163
+ wait 163
+ make verify-website-links
/home/prow/go/src/kubernetes-sigs/kueue/hack/testing/linkchecker/verify.sh
Building linkchecker Docker image...
ERROR: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
make: *** [Makefile-verify.mk:231: verify-website-links] Error 1
```

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-16T20:53:15Z

test-infra PR merged but going to wait to confirm this is fixed before close.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T08:24:05Z

Now the analysis is running, but we have some links broken: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-verify-website-links-main/2033729906109583360

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T08:24:41Z

```
URL        `docs/tasks/run/multikueue/statefulset'
Name       `调度 Kueue 管理的 StatefulSet'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/concepts/multikueue/, line 184, col 1151
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/concepts/multikueue/docs/tasks/run/multikueue/statefulset
Check time 3.912 seconds
Result     Error: 404 Not Found
URL        `docs/tasks/run/multikueue/leaderworkerset'
Name       `调度 Kueue 管理的 LeaderWorkerSet'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/concepts/multikueue/, line 184, col 1235
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/concepts/multikueue/docs/tasks/run/multikueue/leaderworkerset
Check time 3.980 seconds
Result     Error: 404 Not Found
10 threads active,    64 links queued, 1795 links in 1873 URLs checked, runtime 2 minutes, 41 seconds
URL        `docs/tasks/run/multikueue/external-frameworks.md'
Name       `调度 Kueue 管理的 外部框架 Job'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/concepts/multikueue/, line 184, col 1327
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/concepts/multikueue/docs/tasks/run/multikueue/external-frameworks.md
Check time 4.405 seconds
Result     Error: 404 Not Found
10 threads active,    51 links queued, 1808 links in 1874 URLs checked, runtime 2 minutes, 46 seconds
10 threads active,    37 links queued, 1822 links in 1879 URLs checked, runtime 2 minutes, 51 seconds
10 threads active,    21 links queued, 1838 links in 1886 URLs checked, runtime 2 minutes, 56 seconds
10 threads active,     7 links queued, 1852 links in 1887 URLs checked, runtime 3 minutes, 1 seconds
 4 threads active,     0 links queued, 1865 links in 1887 URLs checked, runtime 3 minutes, 6 seconds
Statistics:
Downloaded: 42.4MB.
Content types: 18 image, 371 text, 0 video, 0 audio, 126 application, 0 mail and 1354 other.
URL lengths: min=15, max=1068, avg=126.
That's it. 1869 links in 1887 URLs checked. 0 warnings found (57 ignored or duplicates not printed). 4 errors found.
Stopped checking at 2026-03-17 02:24:54+000 (3 minutes, 8 seconds)
make: *** [Makefile-verify.mk:231: verify-website-links] Error 1
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T08:24:51Z

@kannon92 would you like to fix those?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-17T20:06:45Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-17T20:20:51Z

Looking at this, I'm not sure the answer is that easy to fix.

I don't see a translated doc for leaderworkerset or statefulset.

cc @my-git9

### Comment by [@my-git9](https://github.com/my-git9) — 2026-03-18T01:49:40Z

/assign
