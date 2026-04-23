# Issue #9923: Failed asserts result in recording the same workload twice

**Summary**: Failed asserts result in recording the same workload twice

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9923

**Last updated**: 2026-03-27T18:12:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-17T06:12:19Z
- **Updated**: 2026-03-27T18:12:48Z
- **Closed**: 2026-03-27T18:12:48Z
- **Labels**: `kind/bug`, `kind/cleanup`
- **Assignees**: [@reruno](https://github.com/reruno)
- **Comments**: 10

## Description

/kind bug

**What would you like to be cleaned**:

Example failure message: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9893/pull-kueue-test-integration-baseline-main/2033626544118697984

```
TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack being the lowest level Should admit a previously inadmissible limits-only workload after another workload finishes expand_less	16s
{Timed out after 10.000s.
Unexpected workloads with QuotaReservation
    <*v1beta2.Workload | 0xc001479448>: metadata:
          creationTimestamp: "2026-03-16T19:47:15Z"
          generation: 1
          managedFields:
          - apiVersion: kueue.x-k8s.io/v1beta2
            fieldsType: FieldsV1
            fieldsV1:
              f:status:
                f:conditions:
                  k:{"type":"QuotaReserved"}:
                    .: {}
                    f:lastTransitionTime: {}
                    f:message: {}
                    f:observedGeneration: {}
                    f:reason: {}
                    f:status: {}
                    f:type: {}
                f:resourceRequests:
                  k:{"name":"worker"}:
                    .: {}
                    f:name: {}
                    f:resources:
                      f:cpu: {}
            manager: kueue-admission
            operation: Apply
            subresource: status
            time: "2026-03-16T19:47:15Z"
          - apiVersion: kueue.x-k8s.io/v1beta2
            fieldsType: FieldsV1
            fieldsV1:
              f:spec:
                .: {}
                f:active: {}
                f:podSets:
                  .: {}
                  k:{"name":"worker"}:
                    .: {}
                    f:count: {}
                    f:name: {}
                    f:template:
                      .: {}
                      f:metadata: {}
                      f:spec:
                        .: {}
                        f:containers:
                          .: {}
                          k:{"name":"c"}:
                            .: {}
                            f:name: {}
                            f:resources:
                              .: {}
                              f:limits:
                                .: {}
                                f:cpu: {}
                        f:restartPolicy: {}
                    f:topologyRequest:
                      .: {}
                      f:preferred: {}
                f:queueName: {}
            manager: tas.test
            operation: Update
            time: "2026-03-16T19:47:15Z"
          name: limits-pnly
          namespace: tas-4n5z4
          resourceVersion: "269"
          uid: 2b1d681b-0dbd-4d55-bea6-4748a123fe9d
        spec:
          active: true
          podSets:
          - count: 4
            name: worker
            template:
              metadata: {}
              spec:
                containers:
                - name: c
                  resources:
                    limits:
                      cpu: "1"
                restartPolicy: Never
            topologyRequest:
              preferred: cloud.provider.com/topology-block
          queueName: local-queue
        status:
          conditions:
          - lastTransitionTime: "2026-03-16T19:47:15Z"
            message: Workload no longer fits after processing another workload
            observedGeneration: 1
            reason: Pending
            status: "False"
            type: QuotaReserved
          resourceRequests:
          - name: worker
            resources:
              cpu: "4"
        

The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:372 with:
Expected
    <[]types.NamespacedName | len:0, cap:1>: []
to equal
    <[]types.NamespacedName | len:1, cap:1>: [
        {
            Namespace: "tas-4n5z4",
            Name: "limits-pnly",
        },
    ] failed [FAILED] Timed out after 10.000s.
Unexpected workloads with QuotaReservation
    <*v1beta2.Workload | 0xc001479448>: metadata:
          creationTimestamp: "2026-03-16T19:47:15Z"
          generation: 1
          managedFields:
          - apiVersion: kueue.x-k8s.io/v1beta2
            fieldsType: FieldsV1
            fieldsV1:
              f:status:
                f:conditions:
                  k:{"type":"QuotaReserved"}:
                    .: {}
                    f:lastTransitionTime: {}
                    f:message: {}
                    f:observedGeneration: {}
                    f:reason: {}
                    f:status: {}
                    f:type: {}
                f:resourceRequests:
                  k:{"name":"worker"}:
                    .: {}
                    f:name: {}
                    f:resources:
                      f:cpu: {}
            manager: kueue-admission
            operation: Apply
            subresource: status
            time: "2026-03-16T19:47:15Z"
          - apiVersion: kueue.x-k8s.io/v1beta2
            fieldsType: FieldsV1
            fieldsV1:
              f:spec:
                .: {}
                f:active: {}
                f:podSets:
                  .: {}
                  k:{"name":"worker"}:
                    .: {}
                    f:count: {}
                    f:name: {}
                    f:template:
                      .: {}
                      f:metadata: {}
                      f:spec:
                        .: {}
                        f:containers:
                          .: {}
                          k:{"name":"c"}:
                            .: {}
                            f:name: {}
                            f:resources:
                              .: {}
                              f:limits:
                                .: {}
                                f:cpu: {}
                        f:restartPolicy: {}
                    f:topologyRequest:
                      .: {}
                      f:preferred: {}
                f:queueName: {}
            manager: tas.test
            operation: Update
            time: "2026-03-16T19:47:15Z"
          name: limits-pnly
          namespace: tas-4n5z4
          resourceVersion: "269"
          uid: 2b1d681b-0dbd-4d55-bea6-4748a123fe9d
        spec:
          active: true
          podSets:
          - count: 4
            name: worker
            template:
              metadata: {}
              spec:
                containers:
                - name: c
                  resources:
                    limits:
                      cpu: "1"
                restartPolicy: Never
            topologyRequest:
              preferred: cloud.provider.com/topology-block
          queueName: local-queue
        status:
          conditions:
          - lastTransitionTime: "2026-03-16T19:47:15Z"
            message: Workload no longer fits after processing another workload
            observedGeneration: 1
            reason: Pending
            status: "False"
            type: QuotaReserved
          resourceRequests:
          - name: worker
            resources:
              cpu: "4"
        

The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:372 with:
Expected
    <[]types.NamespacedName | len:0, cap:1>: []
to equal
    <[]types.NamespacedName | len:1, cap:1>: [
        {
            Namespace: "tas-4n5z4",
            Name: "limits-pnly",
        },
    ]
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/tas/tas_test.go:603 @ 03/16/26 19:47:25.432
}
```

**Why is this needed**:

The workload is logged only once.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T06:12:58Z

cc @reruno @mbobrovskyi

### Comment by [@reruno](https://github.com/reruno) — 2026-03-17T08:42:57Z

After some digging it is not a bug in the code, the double message occurs because of formatting of junit.xml that is generated by ginkgo at Makefile-test.mk:103. 

I experimented a little to fix double obj, I added this piece of code to `test/integration/singlecluster/tas/suite_test.go`
```
var _ = ginkgo.ReportAfterSuite("Generate JUnit Report", func(report ginkgo.Report) {
	junitConfig := reporters.JunitReportConfig{
		OmitFailureMessageAttr: true,
	}
	err := reporters.GenerateJUnitReportWithConfig(report, "junit_tas.xml", junitConfig)
	gomega.Expect(err).NotTo(gomega.HaveOccurred())
})
```
And it seems like it stopped to record duplicate objects, but I think we would need to add this to every test suite to stop recording double message

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T08:48:49Z

So this way we skip the error reporting directly to the console with OmitFailureMessageAttr, and instead just print the report from `"junit_tas.xml"?

Will this work well in vs-code?

### Comment by [@reruno](https://github.com/reruno) — 2026-03-17T09:03:31Z

ginkgo.ReportAfterSuite doesn't affect console output, it only creates xml report after test suite run. The default junit.xml generated by --junit-report=junit.xml is still created as before. OmitFailureMessageAttr only affects junit_tas.xml file which removes duplicate error message. vs-code should be unaffected

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T09:10:01Z

ok, this feels reasonable, so currently we put onto console both junit.xml, and junit_tas.xml?

### Comment by [@reruno](https://github.com/reruno) — 2026-03-17T09:16:55Z

Neither file is put onto the console. Console output, junit.xml and junit_tas.xml are generated based on tests results, console output is separated from junit.xml and junit_tas.xml

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T09:41:35Z

Hm and what we see in the console when inspecring the failed run, where is it originating from?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T09:41:53Z

sorry Im a bit lost here, maybe @mbobrovskyi can help

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-26T17:34:29Z

@reruno @mbobrovskyi do you have any new ideas? If not then I'm happy with the approach in https://github.com/kubernetes-sigs/kueue/issues/9923#issuecomment-4073271128, yes, it is a bit of extra code, but the set of suites is not changing that often. Also, even if we forget to add it to a test then it is not end of the world, just a but worse message. I think we could just improve it a bit

```golang
var _ = ginkgo.ReportAfterSuite("Generate JUnit Report", func(report ginkgo.Report) {
  err := util.ConfigureSuiteReporting(report)
  gomega.Expect(err).NotTo(gomega.HaveOccurred())
})
````
and then in the utils we would have the helper like

```golang
func ConfigureSuiteReporting(report ginkgo.Report) error {
  junitConfig := reporters.JunitReportConfig{
    OmitFailureMessageAttr: true,
  }
  suiteName := uniqueSuiteName() // would eval to something unique like "singlecluster_tas" , maybe based on the folder name?
  reportPath := "junit_"+ suiteName + ".xml" // 
 return reporters.GenerateJUnitReportWithConfig(report,reportPath , junitConfig)
}
```

### Comment by [@reruno](https://github.com/reruno) — 2026-03-27T07:14:38Z

/assign
