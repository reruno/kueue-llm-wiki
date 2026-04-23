# Issue #4780: Flaky e2e test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend a jo

**Summary**: Flaky e2e test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend a jo

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4780

**Last updated**: 2025-03-25T10:32:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-24T17:17:25Z
- **Updated**: 2025-03-25T10:32:35Z
- **Closed**: 2025-03-25T10:32:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 4

## Description

/kind flake

**What happened**:

failure: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4778/pull-kueue-test-e2e-customconfigs-main/1904215022578438144

**What you expected to happen**:

No failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:114 with:
Expected
    <bool>: true
to be false failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:114 with:
Expected
    <bool>: true
to be false
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:115 @ 03/24/25 17:02:15.167
}
```
Since this is e2e test, I think LongTimeout maybe could help

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T17:17:34Z

cc @mbobrovskyi @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-25T08:02:42Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-25T09:27:22Z

Well, yes LongTimeout could help.
However usually it's just Timeout and this is enough.

I can see that in the logs in the FAIL run there is extra:
`"Event occurred" [...] reason="Suspended" `
so 2 of them for the same job, while in the PASS run there is only one.
Indeed maybe it's just a glitch

FAIL:
```
2025-03-24T17:02:05.14813458Z stderr F I0324 17:02:05.147975       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-z6rq2/test-job" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="Suspended" message="Job suspended"
2025-03-24T17:02:05.166472817Z stderr F I0324 17:02:05.166332       1 job_controller.go:598] "enqueueing job" logger="job-controller" key="e2e-z6rq2/test-job" delay="1s"
2025-03-24T17:02:05.188278613Z stderr F E0324 17:02:05.188113       1 job_controller.go:631] "Unhandled Error" err="syncing job: tracking status: adding uncounted pods to status: Operation cannot be fulfilled on jobs.batch \"test-job\": the object has been modified; please apply your changes to the latest version and try again" logger="UnhandledError"
2025-03-24T17:02:05.460148787Z stderr F I0324 17:02:05.459842       1 replica_set.go:679] "Finished syncing" logger="replicaset-controller" kind="ReplicaSet" key="kueue-system/kueue-controller-manager-64cc8f6845" duration="79.201µs"
2025-03-24T17:02:05.899146434Z stderr F I0324 17:02:05.898893       1 replica_set.go:679] "Finished syncing" logger="replicaset-controller" kind="ReplicaSet" key="kueue-system/kueue-controller-manager-64cc8f6845" duration="67.921µs"
2025-03-24T17:02:05.90231221Z stderr F I0324 17:02:05.901534       1 replica_set.go:679] "Finished syncing" logger="replicaset-controller" kind="ReplicaSet" key="kueue-system/kueue-controller-manager-64cc8f6845" duration="70.361µs"
2025-03-24T17:02:06.167118955Z stderr F I0324 17:02:06.166951       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-z6rq2/test-job" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="Suspended" message="Job suspended"
2025-03-24T17:02:06.171778858Z stderr F I0324 17:02:06.171623       1 job_controller.go:598] "enqueueing job" logger="job-controller" key="e2e-z6rq2/test-job" delay="1s"
```
PASS:
```
2025-03-25T08:02:41.527676586Z stderr F I0325 08:02:41.527494       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-rsqd6/test-job" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="Suspended" message="Job suspended"
2025-03-25T08:02:41.56783713Z stderr F I0325 08:02:41.567619       1 job_controller.go:598] "enqueueing job" logger="job-controller" key="e2e-rsqd6/test-job" delay="1s"
2025-03-25T08:02:41.604329091Z stderr F E0325 08:02:41.604175       1 job_controller.go:631] "Unhandled Error" err="syncing job: tracking status: adding uncounted pods to status: Operation cannot be fulfilled on jobs.batch \"test-job\": the object has been modified; please apply your changes to the latest version and try again" logger="UnhandledError"
2025-03-25T08:02:41.766499377Z stderr F I0325 08:02:41.766265       1 httplog.go:134] "HTTP" verb="GET" URI="/healthz" latency="172.323µs" userAgent="kube-probe/1.32" audit-ID="" srcIP="127.0.0.1:33980" resp=200
2025-03-25T08:02:41.994460154Z stderr F I0325 08:02:41.994262       1 job_controller.go:598] "enqueueing job" logger="job-controller" key="e2e-rsqd6/test-job" delay="0s"
2025-03-25T08:02:42.040600113Z stderr F I0325 08:02:42.040156       1 job_controller.go:598] "enqueueing job" logger="job-controller" key="e2e-rsqd6/test-job" delay="1s"
2025-03-25T08:02:42.049277268Z stderr F I0325 08:02:42.047805       1 event.go:389] "Event occurred" logger="job-controller" object="e2e-rsqd6/test-job" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="SuccessfulCreate" message="Created pod: test-job-kqtw7"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-25T09:37:19Z

I guess we mostly care about eventual consistency. In a distributed system some patches might fail and be retried, or some events may take long to propagate leading to retries. So, I would not worry in e2e tests as long as it works eventually.
