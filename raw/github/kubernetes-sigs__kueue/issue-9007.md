# Issue #9007: periodic-kueue-test-tas-scheduling-perf-release-0-15 is failing

**Summary**: periodic-kueue-test-tas-scheduling-perf-release-0-15 is failing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9007

**Last updated**: 2026-02-05T19:44:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-05T14:45:27Z
- **Updated**: 2026-02-05T19:44:31Z
- **Closed**: 2026-02-05T19:44:31Z
- **Labels**: `kind/bug`, `kind/failing-test`
- **Assignees**: [@ikchifo](https://github.com/ikchifo)
- **Comments**: 2

## Description

**What happened**:

failing ci job periodic-kueue-test-tas-scheduling-perf-release-0-15

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-tas-scheduling-perf-release-0-15/2019382134803795968

**What you expected to happen**:

not failing

**How to reproduce it (as minimally and precisely as possible)**:

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-tas-scheduling-perf-release-0-15

**Anything else we need to know?**:
```
2026-02-05T12:29:15.101336155Z	INFO	controller/controller.go:311	All workers finished	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload"}
2026-02-05T12:29:15.101372706Z	INFO	manager/internal.go:559	Stopping and waiting for leader election runnables
2026-02-05T12:29:15.101397426Z	INFO	manager/internal.go:567	Stopping and waiting for caches
2026-02-05T12:29:15.101499577Z	INFO	manager/internal.go:571	Stopping and waiting for webhooks
2026-02-05T12:29:15.101539318Z	INFO	manager/internal.go:574	Stopping and waiting for HTTP servers
2026-02-05T12:29:15.101556808Z	INFO	manager/internal.go:578	Wait completed, proceeding to shutdown the manager
2026-02-05T12:29:15.101571818Z	INFO	Run manager	runner/main.go:435	End manager
2026-02-05T12:29:15.102777132Z	ERROR	Run metrics scraper	runner/main.go:451	Running the scraper	{"error": "Get \"http://localhost:41125/metrics\": context canceled"}
main.runScraper.func1
	/home/prow/go/src/kubernetes-sigs/kueue/test/performance/scheduler/runner/main.go:451
sync.(*WaitGroup).Go.func1
	/usr/local/go/src/sync/waitgroup.go:239
2026-02-05T12:29:15.131479731Z	INFO	Run command	runner/main.go:339	Cmd ended	{"stats": {"wallMs":600032,"userMs":10080,"sysMs":4854,"maxrss":121872}}
make[1]: *** [Makefile-test.mk:327: run-tas-performance-scheduler] Error 1
make[1]: Leaving directory '/home/prow/go/src/kubernetes-sigs/kueue'
make: *** [Makefile-test.mk:344: test-tas-performance-scheduler] Error 2
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-05T14:45:38Z

/kind failing-test

### Comment by [@ikchifo](https://github.com/ikchifo) — 2026-02-05T19:01:05Z

/assign
