# Issue #4140: [Flaky test]  TopologyAwareScheduling when Creating a Pod requesting TAS should admit a single Pod via TAS

**Summary**: [Flaky test]  TopologyAwareScheduling when Creating a Pod requesting TAS should admit a single Pod via TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4140

**Last updated**: 2025-08-07T08:29:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-03T16:10:05Z
- **Updated**: 2025-08-07T08:29:30Z
- **Closed**: 2025-08-07T08:29:29Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 36

## Description

/kind flake

**What happened**:

The test failed on related branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

run on ci

**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.31.0: [It] TopologyAwareScheduling when Creating a Pod requesting TAS should admit a single Pod via TAS expand_less	11s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:349 with:
Expected
    <map[string]string | len:0>: nil
to equal
    <map[string]string | len:2>: {
        "instance-type": "on-demand",
        "kubernetes.io/hostname": "kind-worker",
    } failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:349 with:
Expected
    <map[string]string | len:0>: nil
to equal
    <map[string]string | len:2>: {
        "instance-type": "on-demand",
        "kubernetes.io/hostname": "kind-worker",
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:353 @ 02/03/25 15:52:14.261
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-03T16:10:16Z

cc @mbobrovskyi PTAL

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-04T13:16:38Z

/assign

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T09:59:27Z

I've tried to reproduce locally 30 times using the following script:
```
for i in $(seq 1 $NUM_TEST_ITERATIONS); do
  GINKGO_ARGS="--focus=Creating a Pod requesting TAS" make test-e2e >> stress-test.log 2>&1
done
echo looped the test $NUM_TEST_ITERATIONS times

grep -q "FAIL" stress-test.log
if [ $? -eq 0 ]; then
    echo "Test run contains FAILED tests."
    exit 1
else
    echo "Test run did not contain FAILED tests."
fi
```
and then again 100 times while running `stress --cpu 90`, but so far no failures

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T10:18:31Z

You can try to add --race to GINKGO_ARGS, but not sure this will change it much. Might be a tough one as I haven't seen it repeat.

I would suggest to also explore the logs related to the pods from artifacts. First, identify the pod name, and grep kube-apiserver, kube-scheduler and potentially kubelet logs (not sure if the pod was scheduled in this case at all).  I did something similar here: https://github.com/kubernetes-sigs/kueue/issues/4495. 

EDIT: and grep Kueue logs related to the pod. Feel free to post them in a comment.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T13:24:57Z

Is there a way to download the logs from artifact page like that: https://gcsweb.k8s.io/gcs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/ ? Instead of looking at them in browser

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T13:40:42Z

probably there is a way to download them as a package, but what I normally do is downloading the files I'm interested in one-by-one with curl, eg.:
```
curl -Lv https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-control-plane/pods/kube-system_kube-apiserver-kind-control-plane_279a78e3b8722226a896e74ee09ca078/kube-apiserver/0.log.20250203-155314 -oapiserver.log
```

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T13:41:20Z

there is no mention of "test-pod" in apiserver container log https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-control-plane/containers/kube-apiserver-kind-control-plane_kube-system_kube-apiserver-8777d7573967876827dabd8bbdffee29b0d782120253f6c089291eec7d678a66.log

also no mention in kubelet log https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-control-plane/kubelet.log

2 mentions in kube-scheduler container log https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-control-plane/containers/kube-scheduler-kind-control-plane_kube-system_kube-scheduler-811b661fb56c9f5b19a81637a5a27f49918041f9869a7f487a4d49963b4cf76c.log
```
2025-02-03T15:52:04.259430674Z stderr F I0203 15:52:04.258997       1 eventhandlers.go:149] "Add event for unscheduled pod" pod="e2e-tas-fmr5x/test-pod"
2025-02-03T15:52:14.346048023Z stderr F I0203 15:52:14.345818       1 eventhandlers.go:201] "Delete event for unscheduled pod" pod="e2e-tas-fmr5x/test-pod"
```

there are 48 mentions in kube apiserver pod log https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-control-plane/pods/kube-system_kube-apiserver-kind-control-plane_279a78e3b8722226a896e74ee09ca078/kube-apiserver/0.log.20250203-155314
```
2025-02-03T15:52:04.262176345Z stderr F I0203 15:52:04.262034       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.653054ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="a860219a-8a94-4512-b9f7-0d0b00a290fd" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.212638ms" resp=200
2025-02-03T15:52:04.516746595Z stderr F I0203 15:52:04.515746       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.136511ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="e9ed8a3a-2cf8-4be4-86cb-0dc39d6316b8" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.721395ms" resp=200
2025-02-03T15:52:04.770058407Z stderr F I0203 15:52:04.769886       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.893438ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="0b62a9a7-d844-44c5-ba7b-c6c4b55feb6f" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.464472ms" resp=200
2025-02-03T15:52:04.906081416Z stderr F I0203 15:52:04.905877       1 httplog.go:134] "HTTP" verb="APPLY" URI="/apis/kueue.x-k8s.io/v1beta1/namespaces/e2e-tas-fmr5x/workloads/pod-test-pod-abd90/status?fieldManager=kueue-admission&force=true" latency="11.530969ms" userAgent="kueue/v0.11.0 (linux/amd64) 24efa6a" audit-ID="7fa4c2b0-8470-4aaa-ba4a-7b6249d674fe" srcIP="172.18.0.4:58672" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="11.301057ms" resp=200
2025-02-03T15:52:05.023755245Z stderr F I0203 15:52:05.023587       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.07805ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="efde02c7-f504-488c-8221-2cd3d7fd1895" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.663184ms" resp=200
2025-02-03T15:52:05.277369881Z stderr F I0203 15:52:05.277174       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.952179ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="94eea88d-d938-4a02-a36f-0f2189998f98" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.522602ms" resp=200
2025-02-03T15:52:05.533965901Z stderr F I0203 15:52:05.533759       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="4.969873ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="3bd93d2e-380d-47f1-bc19-b8d9b09b35b2" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="4.551036ms" resp=200
2025-02-03T15:52:05.788174695Z stderr F I0203 15:52:05.787959       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.119011ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="cbe602ba-b155-4d9e-a299-da451a698911" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.661934ms" resp=200
2025-02-03T15:52:06.044297939Z stderr F I0203 15:52:06.044073       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="3.842546ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="22793060-ff32-47d8-80cd-be7e5a5508b7" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="3.36395ms" resp=200
2025-02-03T15:52:06.298145699Z stderr F I0203 15:52:06.297961       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.063771ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="3c95d86a-4567-4a5d-8621-4e5aedf65d5f" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.505842ms" resp=200
2025-02-03T15:52:06.551712315Z stderr F I0203 15:52:06.551557       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.868017ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="6864cfba-1e97-4a95-9043-fb8c88d7cb6a" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.424211ms" resp=200
2025-02-03T15:52:06.805501833Z stderr F I0203 15:52:06.805287       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.025ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="8e9601bb-f789-41d7-977c-79875e971245" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.591734ms" resp=200
2025-02-03T15:52:07.058931347Z stderr F I0203 15:52:07.058694       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.733916ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="90ba01d7-66fd-4818-a904-45e8e9afeca4" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.304819ms" resp=200
2025-02-03T15:52:07.312593424Z stderr F I0203 15:52:07.312406       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.01656ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="fe4c100f-b7fc-4ca6-a3c7-7505093c2eca" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.612124ms" resp=200
2025-02-03T15:52:07.566249151Z stderr F I0203 15:52:07.566064       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.0622ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="b921bd6e-4ce8-45de-b9e8-7c73e98daaca" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.626474ms" resp=200
2025-02-03T15:52:07.819731406Z stderr F I0203 15:52:07.819528       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.929368ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="e305bf43-1578-433e-8e39-eb70a539e81b" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.501262ms" resp=200
2025-02-03T15:52:08.072937856Z stderr F I0203 15:52:08.072748       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.755276ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="82505616-d7d0-4444-bef5-668abe6308b1" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.35737ms" resp=200
2025-02-03T15:52:08.326565032Z stderr F I0203 15:52:08.326389       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.08215ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="b85b1dc9-d1b0-4f2c-8aea-5ca34b18dd5b" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.619624ms" resp=200
2025-02-03T15:52:08.580093237Z stderr F I0203 15:52:08.579897       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.907168ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="3f01766c-268e-440b-b02d-9b535f18a9fc" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.510452ms" resp=200
2025-02-03T15:52:08.834263701Z stderr F I0203 15:52:08.834068       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.663069ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="9a0f1108-8bdf-4c03-9efd-45c80847bdb4" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="2.101781ms" resp=200
2025-02-03T15:52:09.088038229Z stderr F I0203 15:52:09.087861       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.793497ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="610fd1d6-5011-41a5-8de4-57168983d896" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.37348ms" resp=200
2025-02-03T15:52:09.342320126Z stderr F I0203 15:52:09.342082       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.283804ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="a091e972-54a6-45a8-b55f-940a9be40473" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.503692ms" resp=200
2025-02-03T15:52:09.595847811Z stderr F I0203 15:52:09.595654       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.882148ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="8b66679f-9c92-40b7-8dc1-af6a6641e5a8" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.481032ms" resp=200
2025-02-03T15:52:09.849539509Z stderr F I0203 15:52:09.849258       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.951158ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="d863fb91-a79c-4134-bdca-41edf1588f66" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.510883ms" resp=200
2025-02-03T15:52:10.103027513Z stderr F I0203 15:52:10.102852       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.886307ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="fd934654-a01f-46ca-86a5-0a101b57dabd" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.448251ms" resp=200
2025-02-03T15:52:10.356580628Z stderr F I0203 15:52:10.356395       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.961659ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="7fe187f6-c63c-4c9a-aa0a-b1b25800dea0" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.525172ms" resp=200
2025-02-03T15:52:10.610274306Z stderr F I0203 15:52:10.610066       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.883067ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="a95a8812-2d3e-42cc-8d25-91dcedeeaea6" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.448281ms" resp=200
2025-02-03T15:52:10.863859972Z stderr F I0203 15:52:10.863667       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.98069ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="3858476b-5c30-49cb-add7-5611fbf31a27" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.572343ms" resp=200
2025-02-03T15:52:11.117373257Z stderr F I0203 15:52:11.117163       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.828917ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="f14c3181-305b-4812-87d3-4313b6e370d1" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.405281ms" resp=200
2025-02-03T15:52:11.370702389Z stderr F I0203 15:52:11.370515       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.796786ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="a427af3d-420b-4c19-87a8-927b8848d143" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.3667ms" resp=200
2025-02-03T15:52:11.624255554Z stderr F I0203 15:52:11.624061       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.04594ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="b40f4606-2a97-4b27-9c89-e9afefbdb08f" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.608823ms" resp=200
2025-02-03T15:52:11.878067173Z stderr F I0203 15:52:11.877844       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.107051ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="5e1fdbc8-6f73-4272-8eea-0cf64a5286fb" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.631034ms" resp=200
2025-02-03T15:52:12.131973894Z stderr F I0203 15:52:12.131763       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.258493ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="724e57e1-5325-4b39-a09b-46c6b2ae4130" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.729145ms" resp=200
2025-02-03T15:52:12.385952785Z stderr F I0203 15:52:12.385764       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.812697ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="1da95570-10f2-41ae-b8ab-e3960804d52b" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.39234ms" resp=200
2025-02-03T15:52:12.64016306Z stderr F I0203 15:52:12.639929       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.441736ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="31041698-5f2a-4e05-a7d6-12968efa04d5" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.879167ms" resp=200
2025-02-03T15:52:12.893670264Z stderr F I0203 15:52:12.893481       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.803956ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="c1c41503-54c7-41e7-9974-d7ac5e909a80" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.404501ms" resp=200
2025-02-03T15:52:13.147505214Z stderr F I0203 15:52:13.147272       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.07641ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="aa416670-9bae-4297-8cb9-c99fe0e2ba7b" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.642714ms" resp=200
2025-02-03T15:52:13.401023188Z stderr F I0203 15:52:13.400820       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.848837ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="c3653cf5-2b39-4951-bffc-14fb0bc0c18d" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.35795ms" resp=200
2025-02-03T15:52:13.654692325Z stderr F I0203 15:52:13.654492       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="2.003169ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="5405c5d6-7436-4946-92a4-88722f34bd5a" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.504102ms" resp=200
2025-02-03T15:52:13.907967526Z stderr F I0203 15:52:13.907775       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.800876ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="a8388e7d-ae8c-46f1-aede-401c0f6b4b61" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.392901ms" resp=200
2025-02-03T15:52:14.161142736Z stderr F I0203 15:52:14.160969       1 httplog.go:134] "HTTP" verb="GET" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="1.885228ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="f99b7627-596e-4325-95dd-5132f112d0ec" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="1.443862ms" resp=200
2025-02-03T15:52:14.280305387Z stderr F I0203 15:52:14.280011       1 httplog.go:134] "HTTP" verb="APPLY" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod/status?fieldManager=kueue" latency="4.71545ms" userAgent="kueue/v0.11.0 (linux/amd64) 24efa6a" audit-ID="8079d9a9-660b-4ce3-87a3-7d2e50a83468" srcIP="172.18.0.4:58672" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="4.226522ms" resp=200
2025-02-03T15:52:14.285117008Z stderr F I0203 15:52:14.284866       1 httplog.go:134] "HTTP" verb="DELETE" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="3.496772ms" userAgent="kueue/v0.11.0 (linux/amd64) 24efa6a" audit-ID="3061fbda-af22-425a-8cac-6adffab894de" srcIP="172.18.0.4:58672" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="3.143516ms" resp=200
2025-02-03T15:52:14.292230892Z stderr F I0203 15:52:14.291947       1 httplog.go:134] "HTTP" verb="APPLY" URI="/apis/kueue.x-k8s.io/v1beta1/namespaces/e2e-tas-fmr5x/workloads/pod-test-pod-abd90/status?fieldManager=kueue-admission&force=true" latency="16.091036ms" userAgent="kueue/v0.11.0 (linux/amd64) 24efa6a" audit-ID="66796815-59c3-412e-af38-33a5247dbfb1" srcIP="172.18.0.4:58672" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="15.741021ms" resp=200
2025-02-03T15:52:14.294053609Z stderr F I0203 15:52:14.293869       1 httplog.go:134] "HTTP" verb="PUT" URI="/apis/kueue.x-k8s.io/v1beta1/namespaces/e2e-tas-fmr5x/workloads/pod-test-pod-abd90" latency="15.528128ms" userAgent="singlecluster.test/v0.0.0 (linux/amd64) kubernetes/$Format" audit-ID="22319a61-b87d-453a-bd29-ce0ebed9ea83" srcIP="172.18.0.1:60630" apf_pl="global-default" apf_fs="global-default" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="15.119432ms" resp=409
2025-02-03T15:52:14.301278316Z stderr F I0203 15:52:14.301079       1 httplog.go:134] "HTTP" verb="PUT" URI="/apis/kueue.x-k8s.io/v1beta1/namespaces/e2e-tas-fmr5x/workloads/pod-test-pod-abd90" latency="14.390753ms" userAgent="kueue/v0.11.0 (linux/amd64) 24efa6a" audit-ID="9a546128-02d4-4130-bcec-29c5c193d637" srcIP="172.18.0.4:58672" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="14.044597ms" resp=409
2025-02-03T15:52:14.319563254Z stderr F I0203 15:52:14.319250       1 httplog.go:134] "HTTP" verb="PUT" URI="/apis/kueue.x-k8s.io/v1beta1/namespaces/e2e-tas-fmr5x/workloads/pod-test-pod-abd90" latency="16.841797ms" userAgent="kueue/v0.11.0 (linux/amd64) 24efa6a" audit-ID="d40b4b12-2cbe-4ff3-bfd4-22f5246e915b" srcIP="172.18.0.4:58672" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=0 apf_additionalLatency="0s" apf_execution_time="16.512962ms" resp=200
2025-02-03T15:52:14.345279322Z stderr F I0203 15:52:14.345021       1 httplog.go:134] "HTTP" verb="PATCH" URI="/api/v1/namespaces/e2e-tas-fmr5x/pods/test-pod" latency="23.947312ms" userAgent="kueue/v0.11.0 (linux/amd64) 24efa6a" audit-ID="e99e7d8a-5495-46a4-a6c1-37b47bb3688d" srcIP="172.18.0.4:58672" apf_pl="workload-low" apf_fs="service-accounts" apf_iseats=1 apf_fseats=2 apf_additionalLatency="5ms" apf_execution_time="23.610077ms" resp=200
```

there are 2 mentions in kube scheduler pod log https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-control-plane/pods/kube-system_kube-scheduler-kind-control-plane_b9e437278b0333614df7d8d898b3fae0/kube-scheduler/0.log
```
2025-02-03T15:52:04.259430674Z stderr F I0203 15:52:04.258997       1 eventhandlers.go:149] "Add event for unscheduled pod" pod="e2e-tas-fmr5x/test-pod"
2025-02-03T15:52:14.346048023Z stderr F I0203 15:52:14.345818       1 eventhandlers.go:201] "Delete event for unscheduled pod" pod="e2e-tas-fmr5x/test-pod"
```

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T14:23:12Z

Also there is no mention in kube controller manager https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-control-plane/pods/kube-system_kube-controller-manager-kind-control-plane_a97c8ce14f20fa592e2406d83f45cd81/kube-controller-manager/0.log

only found 1 namespace-related match (grep by `e2e-tas-fmr5x`) :
```
2025-02-03T15:52:25.607263592Z stderr F I0203 15:52:25.607093       1 namespace_controller.go:187] "Namespace has been deleted" logger="namespace-controller" namespace="e2e-tas-fmr5x"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T15:47:55Z

It seems the pod was never scheduled, wondering if this might be because there was no availbale node, or the scheduling gate was not deleted. Can you also grep the Kueue logs?

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T16:09:58Z

> It seems the pod was never scheduled, wondering if this might be because there was no availbale node, or the scheduling gate was not deleted. Can you also grep the Kueue logs?

can you clarify what kind of Kueue logs to grep?  There are no log containers or pods that have "Kueue" in its name, and if I grep `Kueue` there are quite many matches.  Also quite many matches when I grep `cluster-queue`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T16:16:37Z

Sure, Kueue (kueue-controller-manager) runs as a regular Pod on a worker node (it is not part of the control-plane). 
What complicates debugging slightly is that we have 2 Kueue replicas running in the e2e tests, but only one of them is active (processing requests). The other is just in "stand by" mode and should have minimal logging.

Also, the logs seem to be "rolled", so we have 2 log files per replica. So in total there are 4 files, this is one of them: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-worker/pods/kueue-system_kueue-controller-manager-778456579-czw45_2c3a6cbe-beb4-4eb5-9690-6c415fc03af7/manager/0.log
another for the replica: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-worker/containers/kueue-controller-manager-778456579-czw45_kueue-system_manager-f6b744098531635b729b205535baac42c74338c9b99d2bd286f4fa2670771279.log

another replica is on kind-worker2.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T16:27:57Z

Actually, what is the difference between container and pod logs, in context of the test?

Here are the logs from worker1 — https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-worker/pods/kueue-system_kueue-controller-manager-778456579-czw45_2c3a6cbe-beb4-4eb5-9690-6c415fc03af7/manager/1.log
```
$ grep "test-pod" ./worker1-kueue-controller-manager.log
2025-02-03T15:52:07.975324261Z stderr F 2025-02-03T15:52:07.975151759Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:599	Workload create event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "pending"}
2025-02-03T15:52:07.977438562Z stderr F 2025-02-03T15:52:07.977144438Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:611	ignored an error for now	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "pending", "error": "clusterQueue doesn't exist"}
2025-02-03T15:52:14.273877183Z stderr F 2025-02-03T15:52:14.27367356Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "pending"}
2025-02-03T15:52:14.293367889Z stderr F 2025-02-03T15:52:14.293128446Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
2025-02-03T15:52:14.321225798Z stderr F 2025-02-03T15:52:14.320990575Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:634	Workload delete event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "admitted"}
```

Here are the logs from worker2 — https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886439313864921088/artifacts/run-test-e2e-1.31.0/kind-worker2/pods/kueue-system_kueue-controller-manager-778456579-jxzvl_92460a63-f6e3-4984-807a-9e5fd6ebe0b9/manager/2.log
```
$ grep "test-pod" ./worker2-kueue-controller-manager.log
2025-02-03T15:52:04.652151495Z stderr F 2025-02-03T15:52:04.652011913Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "da64f28d-0c6c-4547-846e-0a138c2dfd4a", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.652264306Z stderr F 2025-02-03T15:52:04.652121304Z	LEVEL(-3)	jobframework/reconciler.go:423	The workload is nil, handle job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "da64f28d-0c6c-4547-846e-0a138c2dfd4a", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.768128319Z stderr F 2025-02-03T15:52:04.768034008Z	ERROR	jobframework/reconciler.go:433	Handling job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "da64f28d-0c6c-4547-846e-0a138c2dfd4a", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod", "error": "Internal error occurred: failed calling webhook \"vworkload.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 10.244.3.4:9443: connect: connection refused"}
2025-02-03T15:52:04.768256301Z stderr F 2025-02-03T15:52:04.768130749Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "da64f28d-0c6c-4547-846e-0a138c2dfd4a", "error": "Internal error occurred: failed calling webhook \"vworkload.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 10.244.3.4:9443: connect: connection refused"}
2025-02-03T15:52:04.773680931Z stderr F 2025-02-03T15:52:04.773529668Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "f41f5d95-038a-4e5a-a86b-eb33b0c56e38", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.773703141Z stderr F 2025-02-03T15:52:04.77362094Z	LEVEL(-3)	jobframework/reconciler.go:423	The workload is nil, handle job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "f41f5d95-038a-4e5a-a86b-eb33b0c56e38", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.783351142Z stderr F 2025-02-03T15:52:04.783158699Z	ERROR	jobframework/reconciler.go:433	Handling job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "f41f5d95-038a-4e5a-a86b-eb33b0c56e38", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod", "error": "Internal error occurred: failed calling webhook \"vworkload.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 10.244.3.4:9443: connect: connection refused"}
2025-02-03T15:52:04.783436763Z stderr F 2025-02-03T15:52:04.783268251Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "f41f5d95-038a-4e5a-a86b-eb33b0c56e38", "error": "Internal error occurred: failed calling webhook \"vworkload.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 10.244.3.4:9443: connect: connection refused"}
2025-02-03T15:52:04.793932268Z stderr F 2025-02-03T15:52:04.793768715Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "9a94e57f-41c9-4ef9-9595-b17faac15a16", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.793959578Z stderr F 2025-02-03T15:52:04.793878457Z	LEVEL(-3)	jobframework/reconciler.go:423	The workload is nil, handle job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "9a94e57f-41c9-4ef9-9595-b17faac15a16", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.803360797Z stderr F 2025-02-03T15:52:04.803165654Z	ERROR	jobframework/reconciler.go:433	Handling job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "9a94e57f-41c9-4ef9-9595-b17faac15a16", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod", "error": "Internal error occurred: failed calling webhook \"vworkload.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 10.244.3.4:9443: connect: connection refused"}
2025-02-03T15:52:04.803443238Z stderr F 2025-02-03T15:52:04.803266235Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "9a94e57f-41c9-4ef9-9595-b17faac15a16", "error": "Internal error occurred: failed calling webhook \"vworkload.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 10.244.3.4:9443: connect: connection refused"}
2025-02-03T15:52:04.823867458Z stderr F 2025-02-03T15:52:04.823712385Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "471a3254-45ea-4ede-9ed9-a64711903a9c", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.823897408Z stderr F 2025-02-03T15:52:04.823814527Z	LEVEL(-3)	jobframework/reconciler.go:423	The workload is nil, handle job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "471a3254-45ea-4ede-9ed9-a64711903a9c", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.835087923Z stderr F 2025-02-03T15:52:04.834802799Z	ERROR	jobframework/reconciler.go:433	Handling job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "471a3254-45ea-4ede-9ed9-a64711903a9c", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod", "error": "Internal error occurred: failed calling webhook \"vworkload.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 10.244.3.4:9443: connect: connection refused"}
2025-02-03T15:52:04.835275636Z stderr F 2025-02-03T15:52:04.834934411Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "471a3254-45ea-4ede-9ed9-a64711903a9c", "error": "Internal error occurred: failed calling webhook \"vworkload.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-workload?timeout=10s\": dial tcp 10.244.3.4:9443: connect: connection refused"}
2025-02-03T15:52:04.87577227Z stderr F 2025-02-03T15:52:04.875611768Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "dfe36234-fe0a-49b4-be94-3dbcbf05e308", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.875885592Z stderr F 2025-02-03T15:52:04.875722759Z	LEVEL(-3)	jobframework/reconciler.go:423	The workload is nil, handle job with no workload	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "dfe36234-fe0a-49b4-be94-3dbcbf05e308", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.893646703Z stderr F 2025-02-03T15:52:04.893418139Z	DEBUG	events	recorder/recorder.go:104	Created Workload: e2e-tas-fmr5x/pod-test-pod-abd90	{"type": "Normal", "object": {"kind":"Pod","namespace":"e2e-tas-fmr5x","name":"test-pod","uid":"e721646d-dd43-4927-af65-4a43a58447b9","apiVersion":"v1","resourceVersion":"7138"}, "reason": "CreatedWorkload"}
2025-02-03T15:52:04.893668503Z stderr F 2025-02-03T15:52:04.893536121Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:599	Workload create event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "pending"}
2025-02-03T15:52:04.893674513Z stderr F 2025-02-03T15:52:04.893543951Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "55e4ff35-59a6-4e31-a23e-dd31ccccbf67", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.893690543Z stderr F 2025-02-03T15:52:04.893572452Z	LEVEL(-2)	multikueue/workload.go:158	Reconcile Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "997e0f19-9632-4478-b3ca-424454e537fc"}
2025-02-03T15:52:04.893701643Z stderr F 2025-02-03T15:52:04.893641563Z	LEVEL(-2)	multikueue/workload.go:183	Skip Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "997e0f19-9632-4478-b3ca-424454e537fc", "isDeleted": false}
2025-02-03T15:52:04.893791085Z stderr F 2025-02-03T15:52:04.893677733Z	LEVEL(-3)	jobframework/reconciler.go:441	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "55e4ff35-59a6-4e31-a23e-dd31ccccbf67", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.893807395Z stderr F 2025-02-03T15:52:04.893717344Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "72d738f1-51e8-4fa7-bb00-411bd65664cf", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}}
2025-02-03T15:52:04.893817115Z stderr F 2025-02-03T15:52:04.893726304Z	LEVEL(-3)	jobframework/reconciler.go:530	Job is suspended and workload not yet admitted by a clusterQueue, nothing to do	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "55e4ff35-59a6-4e31-a23e-dd31ccccbf67", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.893987208Z stderr F 2025-02-03T15:52:04.893831575Z	LEVEL(-3)	core/workload_controller.go:320	Workload is inadmissible because ClusterQueue is inactive	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "72d738f1-51e8-4fa7-bb00-411bd65664cf", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:04.907220162Z stderr F 2025-02-03T15:52:04.9070408Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "pending"}
2025-02-03T15:52:04.907239082Z stderr F 2025-02-03T15:52:04.907128611Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "ba818cd1-18fe-4569-a8c4-0e641e899524", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.907398985Z stderr F 2025-02-03T15:52:04.907284753Z	LEVEL(-3)	jobframework/reconciler.go:441	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "ba818cd1-18fe-4569-a8c4-0e641e899524", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.907441235Z stderr F 2025-02-03T15:52:04.907323384Z	LEVEL(-3)	jobframework/reconciler.go:530	Job is suspended and workload not yet admitted by a clusterQueue, nothing to do	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "ba818cd1-18fe-4569-a8c4-0e641e899524", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:04.907491276Z stderr F 2025-02-03T15:52:04.907273023Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "1bb2d9a1-2584-4038-a9a0-fefb53a14009", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}}
2025-02-03T15:52:04.907502566Z stderr F 2025-02-03T15:52:04.907110861Z	LEVEL(-2)	multikueue/workload.go:158	Reconcile Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "29c0c305-4709-45e1-b3de-55b1d907802e"}
2025-02-03T15:52:04.907618998Z stderr F 2025-02-03T15:52:04.907483856Z	LEVEL(-3)	core/workload_controller.go:320	Workload is inadmissible because ClusterQueue is inactive	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "1bb2d9a1-2584-4038-a9a0-fefb53a14009", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:04.907626298Z stderr F 2025-02-03T15:52:04.907510486Z	LEVEL(-2)	multikueue/workload.go:183	Skip Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "29c0c305-4709-45e1-b3de-55b1d907802e", "isDeleted": false}
2025-02-03T15:52:14.274188578Z stderr F 2025-02-03T15:52:14.273896913Z	LEVEL(-2)	multikueue/workload.go:158	Reconcile Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "e3787254-904f-4f85-b315-81c27b822e9f"}
2025-02-03T15:52:14.274222728Z stderr F 2025-02-03T15:52:14.273958954Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "81d906c5-fe43-43f5-968e-6d82f0c6b261", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:14.274228428Z stderr F 2025-02-03T15:52:14.274010135Z	LEVEL(-2)	multikueue/workload.go:183	Skip Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "e3787254-904f-4f85-b315-81c27b822e9f", "isDeleted": true}
2025-02-03T15:52:14.274234318Z stderr F 2025-02-03T15:52:14.273994465Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "pending"}
2025-02-03T15:52:14.274239448Z stderr F 2025-02-03T15:52:14.274079826Z	LEVEL(-2)	jobframework/reconciler.go:387	The workload is marked for deletion	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "81d906c5-fe43-43f5-968e-6d82f0c6b261", "job": "e2e-tas-fmr5x/test-pod", "gvk": "/v1, Kind=Pod"}
2025-02-03T15:52:14.274403821Z stderr F 2025-02-03T15:52:14.274270029Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "a66ea521-a874-43ac-827c-ed974364c26e", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}}
2025-02-03T15:52:14.274972209Z stderr F 2025-02-03T15:52:14.274869198Z	INFO	scheduler	flavorassigner/tas_flavorassigner.go:77	TAS PodSet assignment	{"schedulingCycle": 1, "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}, "tasAssignment": {"levels":["kubernetes.io/hostname"],"domains":[{"values":["kind-worker"],"count":1}]}}
2025-02-03T15:52:14.275184912Z stderr F 2025-02-03T15:52:14.274995739Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:481	Workload assumed in the cache	{"schedulingCycle": 1, "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:14.275191892Z stderr F 2025-02-03T15:52:14.27505465Z	LEVEL(-3)	scheduler	scheduler/logging.go:43Workload evaluated for admission	{"schedulingCycle": 1, "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}, "status": "assumed", "reason": ""}
2025-02-03T15:52:14.286468997Z stderr F 2025-02-03T15:52:14.286224944Z	DEBUG	events	recorder/recorder.go:104	Workload is deleted	{"type": "Normal", "object": {"kind":"Pod","namespace":"e2e-tas-fmr5x","name":"test-pod","uid":"e721646d-dd43-4927-af65-4a43a58447b9","apiVersion":"v1","resourceVersion":"7138"}, "reason": "Stopped"}
2025-02-03T15:52:14.2933964Z stderr F 2025-02-03T15:52:14.292908762Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:505	Workload successfully admitted and assigned flavors	{"schedulingCycle": 1, "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}, "assignments": [{"name":"main","flavors":{"cpu":"on-demand","memory":"on-demand"},"resourceUsage":{"cpu":"100m","memory":"100Mi"},"count":1,"topologyAssignment":{"levels":["kubernetes.io/hostname"],"domains":[{"values":["kind-worker"],"count":1}]}}]}
2025-02-03T15:52:14.29341521Z stderr F 2025-02-03T15:52:14.293003914Z	DEBUG	events	recorder/recorder.go:104	Quota reserved in ClusterQueue cluster-queue, wait time since queued was 10s	{"type": "Normal", "object": {"kind":"Workload","namespace":"e2e-tas-fmr5x","name":"pod-test-pod-abd90","uid":"0c2f976f-2e5d-4e07-8015-519cd372cdbe","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"7233"}, "reason": "QuotaReserved"}
2025-02-03T15:52:14.29341977Z stderr F 2025-02-03T15:52:14.293045384Z	DEBUG	events	recorder/recorder.go:104	Admitted by ClusterQueue cluster-queue, wait time since reservation was 0s	{"type": "Normal", "object": {"kind":"Workload","namespace":"e2e-tas-fmr5x","name":"pod-test-pod-abd90","uid":"0c2f976f-2e5d-4e07-8015-519cd372cdbe","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"7233"}, "reason": "Admitted"}
2025-02-03T15:52:14.29342386Z stderr F 2025-02-03T15:52:14.293048924Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
2025-02-03T15:52:14.29342733Z stderr F 2025-02-03T15:52:14.293106435Z	LEVEL(-2)	multikueue/workload.go:158	Reconcile Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "26117590-f52b-46c0-932c-fb9b7ea00c67"}
2025-02-03T15:52:14.29343183Z stderr F 2025-02-03T15:52:14.293140696Z	LEVEL(-2)	tas/topology_ungater.go:151	Reconcile Topology Ungater	{"controller": "tas-topology-ungater", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "354c8d62-b4a9-48fb-95e7-63c9a2ea4eaf", "workload": "e2e-tas-fmr5x/pod-test-pod-abd90"}
2025-02-03T15:52:14.29345005Z stderr F 2025-02-03T15:52:14.293202927Z	LEVEL(-2)	multikueue/workload.go:183	Skip Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "26117590-f52b-46c0-932c-fb9b7ea00c67", "isDeleted": true}
2025-02-03T15:52:14.29345531Z stderr F 2025-02-03T15:52:14.293259637Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "a2bead76-436e-4487-8a32-6b8d64a6d078", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}}
2025-02-03T15:52:14.301900455Z stderr F 2025-02-03T15:52:14.301682952Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "e2e-tas-fmr5x", "name": "test-pod", "reconcileID": "81d906c5-fe43-43f5-968e-6d82f0c6b261", "error": "Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"pod-test-pod-abd90\": the object has been modified; please apply your changes to the latest version and try again"}
2025-02-03T15:52:14.320995015Z stderr F 2025-02-03T15:52:14.320771612Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:634	Workload delete event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "admitted"}
2025-02-03T15:52:14.321032895Z stderr F 2025-02-03T15:52:14.320820042Z	LEVEL(-2)	multikueue/workload.go:158	Reconcile Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "c550c1ff-f61b-46de-b0f0-56faa6d3eeaa"}
2025-02-03T15:52:14.321038565Z stderr F 2025-02-03T15:52:14.320879223Z	LEVEL(-2)	multikueue/workload.go:183	Skip Workload	{"controller": "multikueue-workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "c550c1ff-f61b-46de-b0f0-56faa6d3eeaa", "isDeleted": true}
2025-02-03T15:52:14.321043216Z stderr F 2025-02-03T15:52:14.320822652Z	LEVEL(-2)	tas/topology_ungater.go:151	Reconcile Topology Ungater	{"controller": "tas-topology-ungater", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "1afbae49-c3bc-4754-b04d-8c8937093adf", "workload": "e2e-tas-fmr5x/pod-test-pod-abd90"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T16:34:59Z

I think this is quite interesting and a couple of lines look suspicious. In particular the line saying the ClustrQueue is inactive. Maybe this is a race condition. In some other tests we wait explicitly for the CQ to be active. Compra if this line is present in the analogous successful run. I believe this might be one of the first lines were the fail and success runs diverge but worth diffing them.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T16:41:31Z

Another thing drawing attention is the 10s gap in logs. Looks like the test timeout, does it correlate with test logs?

in that case maybe we should just increase to LongTineout. This is what we mostly do in E2e tests, because lower down the logs suggest the workload was successfully admitted.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T17:05:47Z

I checked to tests so far with `grep "test-pod" ./0.log | grep "inadmissible"` and so far no matches

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T17:09:17Z

> Another thing drawing attention is the 10s gap in logs. Looks like the test timeout, does it correlate with test logs?

And yes it correlates, TAS test fails at 15:52:14:
```
[FAILED] in [It] - /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:353 @ 02/03/25 15:52:14.261
```
and inadmissible workloads are 10s before that:
```
2025-02-03T15:52:04.893987208Z stderr F 2025-02-03T15:52:04.893831575Z	LEVEL(-3)	core/workload_controller.go:320	Workload is inadmissible because ClusterQueue is inactive	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "72d738f1-51e8-4fa7-bb00-411bd65664cf", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:04.907220162Z stderr F 2025-02-03T15:52:04.9070408Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "pending"}
2025-02-03T15:52:04.907618998Z stderr F 2025-02-03T15:52:04.907483856Z	LEVEL(-3)	core/workload_controller.go:320	Workload is inadmissible because ClusterQueue is inactive	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "1bb2d9a1-2584-4038-a9a0-fefb53a14009", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:14.274234318Z stderr F 2025-02-03T15:52:14.273994465Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "queue": "main", "status": "pending"}
2025-02-03T15:52:14.274972209Z stderr F 2025-02-03T15:52:14.274869198Z	INFO	scheduler	flavorassigner/tas_flavorassigner.go:77	TAS PodSet assignment	{"schedulingCycle": 1, "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}, "tasAssignment": {"levels":["kubernetes.io/hostname"],"domains":[{"values":["kind-worker"],"count":1}]}}
2025-02-03T15:52:14.275184912Z stderr F 2025-02-03T15:52:14.274995739Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:481	Workload assumed in the cache	{"schedulingCycle": 1, "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:14.275191892Z stderr F 2025-02-03T15:52:14.27505465Z	LEVEL(-3)	scheduler	scheduler/logging.go:43Workload evaluated for admission	{"schedulingCycle": 1, "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}, "status": "assumed", "reason": ""}
2025-02-03T15:52:14.2933964Z stderr F 2025-02-03T15:52:14.292908762Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:505	Workload successfully admitted and assigned flavors	{"schedulingCycle": 1, "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}, "assignments": [{"name":"main","flavors":{"cpu":"on-demand","memory":"on-demand"},"resourceUsage":{"cpu":"100m","memory":"100Mi"},"count":1,"topologyAssignment":{"levels":["kubernetes.io/hostname"],"domains":[{"values":["kind-worker"],"count":1}]}}]}
```

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T17:16:32Z

I also can see in logs that it was admitted at the end, the difference between the last log line and the first is slightly less than 10 seconds (15:52:04.652 to 15:52:14.320).  Does it mean it almost passed but it was too late for test check?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T17:16:44Z

Yeah, so it seems this Cluster inactive is a sign of things going wrong. But it seems the CQ got active at some point as the workload was admitted. I would speculate it got active due to the test starting to delete in After each. So it seems there might be some very rare race condition when the CQ gets stuck in the inactive state 

So I think the next step would be to grep logs not for the Pod, because the issue started earlier, but for the controllers responsible for TAS, that is ClustrQueue, tas_resource_flavor and topology.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T17:36:43Z


tas-resource-flavor-controller logs:
```
2025-02-03T15:48:03.322466497Z stderr F 2025-02-03T15:48:03.322310965Z	INFO	controller/controller.go:183	Starting Controller	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor"}
2025-02-03T15:48:03.322476168Z stderr F 2025-02-03T15:48:03.322353126Z	INFO	controller/controller.go:217	Starting workers	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "worker count": 1}
2025-02-03T15:48:03.322508458Z stderr F 2025-02-03T15:48:03.322392696Z	INFO	controller/controller.go:132	Starting EventSource	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "source": "kind source: *v1beta1.ResourceFlavor"}
2025-02-03T15:48:03.322594209Z stderr F 2025-02-03T15:48:03.322417217Z	INFO	controller/controller.go:132	Starting EventSource	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "source": "kind source: *v1.Node"}
2025-02-03T15:50:03.426867862Z stderr F 2025-02-03T15:50:03.426417255Z	INFO	controller/controller.go:237	Shutdown signal received, waiting for all workers to finish	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor"}
2025-02-03T15:50:03.426887372Z stderr F 2025-02-03T15:50:03.426448136Z	INFO	controller/controller.go:239	All workers finished	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor"}
2025-02-03T15:50:16.118121086Z stderr F 2025-02-03T15:50:16.117946993Z	INFO	controller/controller.go:183	Starting Controller	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor"}
2025-02-03T15:50:16.118135326Z stderr F 2025-02-03T15:50:16.118007334Z	INFO	controller/controller.go:217	Starting workers	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "worker count": 1}
2025-02-03T15:50:16.118152826Z stderr F 2025-02-03T15:50:16.118043225Z	INFO	controller/controller.go:132	Starting EventSource	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "source": "kind source: *v1beta1.ResourceFlavor"}
2025-02-03T15:50:16.118212317Z stderr F 2025-02-03T15:50:16.118123976Z	INFO	controller/controller.go:132	Starting EventSource	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "source": "kind source: *v1.Node"}
2025-02-03T15:52:06.486918563Z stderr F 2025-02-03T15:52:06.48672645Z	LEVEL(-2)	tas/resource_flavor.go:138	Reconcile TAS Resource Flavor	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "7f7d0e4e-76db-4f8c-a7e4-1481e1d7ecf5", "name": "on-demand"}
2025-02-03T15:52:06.486942573Z stderr F 2025-02-03T15:52:06.486827551Z	LEVEL(-3)	tas/resource_flavor.go:154	Adding topology to cache for flavor	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "7f7d0e4e-76db-4f8c-a7e4-1481e1d7ecf5", "name": "on-demand", "flavorName": "on-demand"}
2025-02-03T15:52:15.397177827Z stderr F 2025-02-03T15:52:15.396948264Z	LEVEL(-2)	tas/resource_flavor.go:138	Reconcile TAS Resource Flavor	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "3c33d1c9-5ed3-46de-9f4c-f43567bc9f06", "name": "on-demand"}
2025-02-03T15:52:15.397183317Z stderr F 2025-02-03T15:52:15.397008985Z	LEVEL(-3)	tas/resource_flavor.go:154	Adding topology to cache for flavor	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "3c33d1c9-5ed3-46de-9f4c-f43567bc9f06", "name": "on-demand", "flavorName": "on-demand"}
```

Regarding ClusterQueue and tas-topology-controller logs, there are quite many matches, should I search for something particular?  Is it ok to discard logs before the `TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS` has been started, eg only look into logs from 15:51:51?:
```
------------------------------
Kueue visibility server when A subject is not bound to kueue-batch-user-role, nor to kueue-batch-admin-role Should return an appropriate error
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:567
  STEP: Returning a Forbidden error due to insufficient permissions for the ClusterQueue request @ 02/03/25 15:51:51.276
  STEP: Returning a Forbidden error due to insufficient permissions for the LocalQueue request @ 02/03/25 15:51:51.278
• [0.201 seconds]
------------------------------
TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:96
  STEP: await for admission of workload "e2e-tas-7lqfv/job-test-job-69e27" and verify TopologyAssignment @ 02/03/25 15:51:52.02
  STEP: verify the workload "e2e-tas-7lqfv/job-test-job-69e27" gets finished @ 02/03/25 15:51:52.024
• [6.338 seconds]
------------------------------
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T17:43:45Z

yeah, from when the test started till the 10s gap.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-06T19:18:33Z

Here are the tas-topology-controller logs:
```
2025-02-03T15:48:03.322491608Z stderr F 2025-02-03T15:48:03.322353966Z	INFO	controller/controller.go:175	Starting EventSource	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology", "source": "kind source: *v1alpha1.Topology"}
2025-02-03T15:48:03.322496308Z stderr F 2025-02-03T15:48:03.322392196Z	INFO	controller/controller.go:175	Starting EventSource	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology", "source": "kind source: *v1beta1.ResourceFlavor"}
2025-02-03T15:48:03.322513428Z stderr F 2025-02-03T15:48:03.322406397Z	INFO	controller/controller.go:183	Starting Controller	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology"}
2025-02-03T15:48:03.43327389Z stderr F 2025-02-03T15:48:03.433096178Z	INFO	controller/controller.go:217	Starting workers	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology", "worker count": 1}
2025-02-03T15:50:03.426821161Z stderr F 2025-02-03T15:50:03.426335804Z	INFO	controller/controller.go:237	Shutdown signal received, waiting for all workers to finish	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology"}
2025-02-03T15:50:03.426872472Z stderr F 2025-02-03T15:50:03.426445406Z	INFO	controller/controller.go:239	All workers finished	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology"}
2025-02-03T15:50:16.118270658Z stderr F 2025-02-03T15:50:16.118149946Z	INFO	controller/controller.go:175	Starting EventSource	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology", "source": "kind source: *v1alpha1.Topology"}
2025-02-03T15:50:16.118294468Z stderr F 2025-02-03T15:50:16.118208847Z	INFO	controller/controller.go:175	Starting EventSource	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology", "source": "kind source: *v1beta1.ResourceFlavor"}
2025-02-03T15:50:16.118300249Z stderr F 2025-02-03T15:50:16.118226197Z	INFO	controller/controller.go:183	Starting Controller	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology"}
2025-02-03T15:50:16.223984907Z stderr F 2025-02-03T15:50:16.223690342Z	INFO	controller/controller.go:217	Starting workers	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology", "worker count": 1}
2025-02-03T15:51:51.480267524Z stderr F 2025-02-03T15:51:51.48000888Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T15:51:57.528388847Z stderr F 2025-02-03T15:51:57.528172464Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:173	Topology delete event	{"topology": {"name":"hostname"}}
2025-02-03T15:51:57.816166995Z stderr F 2025-02-03T15:51:57.815964802Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T15:52:03.652344565Z stderr F 2025-02-03T15:52:03.652171353Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:173	Topology delete event	{"topology": {"name":"hostname"}}
2025-02-03T15:52:03.96373457Z stderr F 2025-02-03T15:52:03.963479296Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T15:52:15.085481968Z stderr F 2025-02-03T15:52:15.085183454Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:95	Reconcile Topology	{"name": "hostname"}
2025-02-03T15:52:15.091210793Z stderr F 2025-02-03T15:52:15.09098686Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:173	Topology delete event	{"topology": {"name":"hostname"}}
2025-02-03T15:52:15.385335964Z stderr F 2025-02-03T15:52:15.385042499Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T15:52:15.385662989Z stderr F 2025-02-03T15:52:15.385470366Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:95	Reconcile Topology	{"name": "hostname"}
2025-02-03T15:52:15.390787844Z stderr F 2025-02-03T15:52:15.39057215Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:95	Reconcile Topology	{"name": "hostname"}
2025-02-03T15:52:15.848054983Z stderr F 2025-02-03T15:52:15.847791669Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:95	Reconcile Topology	{"name": "hostname"}
2025-02-03T15:52:20.623270644Z stderr F 2025-02-03T15:52:20.622500832Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:95	Reconcile Topology	{"name": "hostname"}
2025-02-03T15:52:20.628810365Z stderr F 2025-02-03T15:52:20.628570892Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:173	Topology delete event	{"topology": {"name":"hostname"}}
```

Here are ClusterQueue logs:
```
2025-02-03T15:51:50.11127939Z stderr F 2025-02-03T15:51:50.111118667Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:51.494823437Z stderr F 2025-02-03T15:51:51.494499822Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:51.502425029Z stderr F 2025-02-03T15:51:51.502117824Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:52.784674159Z stderr F 2025-02-03T15:51:52.784527317Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:57.00177985Z stderr F 2025-02-03T15:51:57.001616317Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:57.013806996Z stderr F 2025-02-03T15:51:57.013597793Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:57.013839927Z stderr F 2025-02-03T15:51:57.013709815Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:57.837841544Z stderr F 2025-02-03T15:51:57.830377464Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:57.847204791Z stderr F 2025-02-03T15:51:57.846970738Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:51:59.143792512Z stderr F 2025-02-03T15:51:59.14365182Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:03.121938252Z stderr F 2025-02-03T15:52:03.121691448Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:03.137270177Z stderr F 2025-02-03T15:52:03.136946982Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:03.137551901Z stderr F 2025-02-03T15:52:03.137430609Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:03.980921002Z stderr F 2025-02-03T15:52:03.980050699Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:03.988800729Z stderr F 2025-02-03T15:52:03.988596436Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:04.547760631Z stderr F 2025-02-03T15:52:04.546790817Z	LEVEL(-3)	scheduler	queue/manager.go:588	Obtained ClusterQueue heads	{"schedulingCycle": 1, "count": 0}
2025-02-03T15:52:04.893821085Z stderr F 2025-02-03T15:52:04.893693793Z	LEVEL(-3)	scheduler	queue/manager.go:588	Obtained ClusterQueue heads	{"schedulingCycle": 1, "count": 0}
2025-02-03T15:52:04.893987208Z stderr F 2025-02-03T15:52:04.893831575Z	LEVEL(-3)	core/workload_controller.go:320	Workload is inadmissible because ClusterQueue is inactive	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "72d738f1-51e8-4fa7-bb00-411bd65664cf", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:04.907389345Z stderr F 2025-02-03T15:52:04.907230152Z	LEVEL(-3)	scheduler	queue/manager.go:588	Obtained ClusterQueue heads	{"schedulingCycle": 1, "count": 0}
2025-02-03T15:52:04.907618998Z stderr F 2025-02-03T15:52:04.907483856Z	LEVEL(-3)	core/workload_controller.go:320	Workload is inadmissible because ClusterQueue is inactive	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "namespace": "e2e-tas-fmr5x", "name": "pod-test-pod-abd90", "reconcileID": "1bb2d9a1-2584-4038-a9a0-fefb53a14009", "workload": {"name":"pod-test-pod-abd90","namespace":"e2e-tas-fmr5x"}, "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:05.894834143Z stderr F 2025-02-03T15:52:05.894640641Z	LEVEL(-2)	core/clusterqueue_controller.go:184	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"cluster-queue"}, "namespace": "", "name": "cluster-queue", "reconcileID": "9519e740-6eed-49ad-8153-e5c0cdccc943", "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:05.92523724Z stderr F 2025-02-03T15:52:05.924934816Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:05.925474334Z stderr F 2025-02-03T15:52:05.92524764Z	LEVEL(-2)	core/clusterqueue_controller.go:184	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"cluster-queue"}, "namespace": "", "name": "cluster-queue", "reconcileID": "913167f7-38ca-405d-83d9-a40fefdccb0e", "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:14.274392041Z stderr F 2025-02-03T15:52:14.274246198Z	LEVEL(-3)	scheduler	queue/manager.go:588	Obtained ClusterQueue heads	{"schedulingCycle": 1, "count": 1}
2025-02-03T15:52:14.275195792Z stderr F 2025-02-03T15:52:14.275113381Z	LEVEL(-3)	scheduler	queue/manager.go:588	Obtained ClusterQueue heads	{"schedulingCycle": 2, "count": 0}
2025-02-03T15:52:14.29341521Z stderr F 2025-02-03T15:52:14.293003914Z	DEBUG	events	recorder/recorder.go:104	Quota reserved in ClusterQueue cluster-queue, wait time since queued was 10s	{"type": "Normal", "object": {"kind":"Workload","namespace":"e2e-tas-fmr5x","name":"pod-test-pod-abd90","uid":"0c2f976f-2e5d-4e07-8015-519cd372cdbe","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"7233"}, "reason": "QuotaReserved"}
2025-02-03T15:52:14.29341977Z stderr F 2025-02-03T15:52:14.293045384Z	DEBUG	events	recorder/recorder.go:104	Admitted by ClusterQueue cluster-queue, wait time since reservation was 0s	{"type": "Normal", "object": {"kind":"Workload","namespace":"e2e-tas-fmr5x","name":"pod-test-pod-abd90","uid":"0c2f976f-2e5d-4e07-8015-519cd372cdbe","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"7233"}, "reason": "Admitted"}
2025-02-03T15:52:14.562584265Z stderr F 2025-02-03T15:52:14.562378782Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:14.562668586Z stderr F 2025-02-03T15:52:14.562540664Z	LEVEL(-2)	core/clusterqueue_controller.go:184	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"cluster-queue"}, "namespace": "", "name": "cluster-queue", "reconcileID": "d346362c-de79-49e5-a515-e4ac8f1b7fa0", "clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:14.578317786Z stderr F 2025-02-03T15:52:14.578089653Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T15:52:14.578350517Z stderr F 2025-02-03T15:52:14.578179594Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cluster-queue"}}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T07:51:24Z

Thank you for digging down the logs! This one seems quite rare and tough to understand, but important. 

It seems, that under some circumstances (order of events) the CQ using TAS resource flavor may be stuck inactive.

So, first thing to know about k8s, is that for our controllers in kueue the order of Create statements in the test code does not really matter. What only matters is the order of delivering the ADDED / Create events to the event handlers, like for [RF TAS](https://github.com/kubernetes-sigs/kueue/blob/62f4b2c80899c771a4d8621a9b7c1c9a99e34477/pkg/controller/tas/resource_flavor.go#L169), [RF](https://github.com/kubernetes-sigs/kueue/blob/62f4b2c80899c771a4d8621a9b7c1c9a99e34477/pkg/controller/core/resourceflavor_controller.go#L123) and [Topology](https://github.com/kubernetes-sigs/kueue/blob/62f4b2c80899c771a4d8621a9b7c1c9a99e34477/pkg/controller/tas/topology_controller.go#L129).

Also, be aware that we have 2 controllers for RF (TAS and core), both receive the ADDED / Create events, and the order of receiving the events may differ. Also, on a loaded cluster the API server may severely delay (up to seconds) delivering some of the events.

It seems in this case the order of processing the added events was unusual indeed:
```
2025-02-03T15:52:03.96373457Z stderr F 2025-02-03T15:52:03.963479296Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T15:52:03.980921002Z stderr F 2025-02-03T15:52:03.980050699Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}

2025-02-03T15:52:06.486918563Z stderr F 2025-02-03T15:52:06.48672645Z	LEVEL(-2)	tas/resource_flavor.go:138	Reconcile TAS Resource Flavor	{"controller": "tas-resource-flavor-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "7f7d0e4e-76db-4f8c-a7e4-1481e1d7ecf5", "name": "on-demand"}
```
unfortunately we don't log the Create event for TAS RF controller, but it seems it was delayed, because the reconcile was 3s later.

It would be great to also overlay the logs with the create log for the core resource flavor controller.

Maybe actually the source of the bug is that we have 2 controllers for RF rather than one. It seemed like a good idea from the de-coupling point of view, but maybe they are racing occasionally. In any case, before we refactor I would like to understand the scenario and make it reproducible. 

To reproduce, one way is to inject time.Sleep(X seconds) into the first line of the Create handlers, and use different delays to simulate different order of processing. For example Sleep(1s into Topology, Sleep 2s into CQ, 3s into core RF, and 4s into TAS RF) to induce the order of actual processing. 

However, the suggestion is still speculative, so take it with caution :)

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T08:18:18Z

resourceflavor_controller logs:
```
2025-02-03T15:51:50.36862198Z stderr F 2025-02-03T15:51:50.368420488Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"default-flavor"}}
2025-02-03T15:51:51.486286092Z stderr F 2025-02-03T15:51:51.485943077Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:51:57.262376958Z stderr F 2025-02-03T15:51:57.262174405Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:51:57.269304831Z stderr F 2025-02-03T15:51:57.269055797Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:51:57.822664571Z stderr F 2025-02-03T15:51:57.822465918Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:52:03.382714233Z stderr F 2025-02-03T15:52:03.38252719Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:52:03.389721376Z stderr F 2025-02-03T15:52:03.389508773Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:52:03.971564055Z stderr F 2025-02-03T15:52:03.971274131Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:52:06.486947573Z stderr F 2025-02-03T15:52:06.486774011Z	LEVEL(-2)	core/resourceflavor_controller.go:81	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "ea29e433-6442-48e5-a758-ab011f49afa7", "resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:52:14.578426228Z stderr F 2025-02-03T15:52:14.578314796Z	LEVEL(-2)	core/resourceflavor_controller.go:81	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "70f5cb58-a9ba-46f5-867c-fc8541b54cac", "resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:52:14.824180299Z stderr F 2025-02-03T15:52:14.823899955Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:52:14.824206779Z stderr F 2025-02-03T15:52:14.824078327Z	LEVEL(-2)	core/resourceflavor_controller.go:81	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "09e7b49e-21a8-4573-abbc-2e5da3ee86d7", "resourceFlavor": {"name":"on-demand"}}
2025-02-03T15:52:14.84737427Z stderr F 2025-02-03T15:52:14.847138636Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T08:35:19Z

Notice that in the topology controller we didn't see this logged: https://github.com/kubernetes-sigs/kueue/blob/62f4b2c80899c771a4d8621a9b7c1c9a99e34477/pkg/controller/tas/topology_controller.go#L155.

Which means that at the moment of processing the Topology event we didn't yet see the RF. The RF event was added later, but it is inside Topology Create event that we trigger reconciling of the CQ: https://github.com/kubernetes-sigs/kueue/blob/62f4b2c80899c771a4d8621a9b7c1c9a99e34477/pkg/controller/tas/topology_controller.go#L146. 

This suggests that we called NotifyTopologyUpdateWatchers, but it didn't trigger activating the CQ as the RF was not yet seen at this point in cache. 

Wondering how to repro / confirm reliably.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T09:02:52Z

I injected delays in the order they happened in the logs above, and it failed: https://github.com/kubernetes-sigs/kueue/pull/4475#issuecomment-2705877788

1s into Topology
2s into into core RF,
3s into ClusterQueue
4s into TAS RF

EDIT:  but also the other tests are failing, including integration tests

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T09:13:08Z

Right, which is a sign some other tests are also timing sensitive. 

However, this particular TAS test didn't fail, or any other TAS. So focusing on this test, it does not seem like repro yet. I would probably fucus on running this locally to have a shorten test cycle. 

TBH Im not sure what needs to be the order of events yet to repro this. Something else also might be relevant here is hard to control from our code, which is the controller runtime caches which are responsible for serving clients calls to List, eg. in topology controller when we list resource flavors. These caches have their own delays.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T11:58:47Z

> Notice that in the topology controller we didn't see this logged:
https://github.com/kubernetes-sigs/kueue/blob/62f4b2c80899c771a4d8621a9b7c1c9a99e34477/pkg/controller/tas/topology_controller.go#L155

I checked logs from successful run https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4475/pull-kueue-test-e2e-main-1-31/1897218139498745856 and `Updating Topology` not found in its logs as well.

Also ran more local tests with different combinations of delays, no failures so far.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T13:15:38Z

I also cannot find any lines that match `tas-resource-flavor-controller` in logs from the successful run.  Do you know what might be the reason?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T13:24:18Z

> I also cannot find any lines that match tas-resource-flavor-controller in logs from the successful run. Do you know what might be the reason?

Hm, grepping by `tas/resource_flavor.go` gives results in this [file](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4475/pull-kueue-test-e2e-main-1-31/1897218139498745856/artifacts/run-test-e2e-singlecluster-1.31.0/kind-worker2/pods/kueue-system_kueue-controller-manager-5d5b5785bb-kpkpg_fda6bb92-0d9a-4dc3-90dc-a119b66d9783/manager/0.log)

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T14:29:17Z

I've realized it's better to compare to logs from a successful run from the same commit, like https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-31/1886444172156604416/artifacts/run-test-e2e-1.31.0/kind-worker/pods/kueue-system_kueue-controller-manager-778456579-nqrgl_1fa2fe13-4762-407e-b760-f5a31060fe20/manager/0.log

Then same events are logged and line numbers in logs are the same.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-03-07T14:46:39Z

Here are logs from successful run, maybe it could be useful:
```
2025-02-03T16:06:58.482772147Z stderr F 2025-02-03T16:06:58.482571706Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"default-priority-group","namespace":"pod-e2e-gj4sw"}, "queue": "queue", "status": "admitted", "clusterQueue": "cq"}
2025-02-03T16:06:58.592340989Z stderr F 2025-02-03T16:06:58.592082408Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"default-priority-group","namespace":"pod-e2e-gj4sw"}, "queue": "queue", "status": "finished", "prevStatus": "admitted", "clusterQueue": "cq"}
2025-02-03T16:06:58.620642905Z stderr F 2025-02-03T16:06:58.620395553Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"default-priority-group","namespace":"pod-e2e-gj4sw"}, "queue": "queue", "status": "finished", "clusterQueue": "cq"}
2025-02-03T16:06:58.852218875Z stderr F 2025-02-03T16:06:58.851954553Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:634	Workload delete event	{"workload": {"name":"high-priority-group","namespace":"pod-e2e-gj4sw"}, "queue": "queue", "status": "finished"}
2025-02-03T16:06:58.85938113Z stderr F 2025-02-03T16:06:58.859068148Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cq"}}
2025-02-03T16:06:58.862470439Z stderr F 2025-02-03T16:06:58.862250417Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:634	Workload delete event	{"workload": {"name":"default-priority-group","namespace":"pod-e2e-gj4sw"}, "queue": "queue", "status": "finished"}
2025-02-03T16:06:58.872197229Z stderr F 2025-02-03T16:06:58.871922667Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cq"}}
2025-02-03T16:06:58.872220169Z stderr F 2025-02-03T16:06:58.872021348Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cq"}}
2025-02-03T16:06:58.877904205Z stderr F 2025-02-03T16:06:58.877711293Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:184	Queue update event	{"localQueue": {"name":"queue","namespace":"pod-e2e-gj4sw"}}
2025-02-03T16:06:59.129414758Z stderr F 2025-02-03T16:06:59.129160187Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:170	LocalQueue delete event	{"localQueue": {"name":"queue","namespace":"pod-e2e-gj4sw"}}
2025-02-03T16:06:59.149583984Z stderr F 2025-02-03T16:06:59.149367483Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:06:59.155792042Z stderr F 2025-02-03T16:06:59.155579971Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:06:59.419550922Z stderr F 2025-02-03T16:06:59.41929059Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T16:06:59.426087833Z stderr F 2025-02-03T16:06:59.425859492Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:06:59.435407431Z stderr F 2025-02-03T16:06:59.435121739Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:06:59.443291009Z stderr F 2025-02-03T16:06:59.443038048Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:06:59.696602355Z stderr F 2025-02-03T16:06:59.696375203Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:139	LocalQueue create event	{"localQueue": {"name":"main","namespace":"e2e-tas-gv22z"}}
2025-02-03T16:06:59.703502787Z stderr F 2025-02-03T16:06:59.703338346Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:184	Queue update event	{"localQueue": {"name":"main","namespace":"e2e-tas-gv22z"}}
2025-02-03T16:06:59.72964703Z stderr F 2025-02-03T16:06:59.729428968Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:599	Workload create event	{"workload": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "queue": "main", "status": "pending"}
2025-02-03T16:06:59.743247685Z stderr F 2025-02-03T16:06:59.742972343Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "queue": "main", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
2025-02-03T16:07:00.741489401Z stderr F 2025-02-03T16:07:00.74123621Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:184	Queue update event	{"localQueue": {"name":"main","namespace":"e2e-tas-gv22z"}}
2025-02-03T16:07:00.741513721Z stderr F 2025-02-03T16:07:00.741363091Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:00.774383696Z stderr F 2025-02-03T16:07:00.774059624Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-job-7wwj6","namespace":"e2e-tas-gv22z"}, "workload": "e2e-tas-gv22z/job-test-job-1fd00", "store": "tas-topology-ungater", "key": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "uid": "48275201-e807-4351-a5ba-d316e8e28ffc"}
2025-02-03T16:07:00.7798269Z stderr F 2025-02-03T16:07:00.779581819Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-job-7wwj6","namespace":"e2e-tas-gv22z"}, "workload": "e2e-tas-gv22z/job-test-job-1fd00", "store": "tas-topology-ungater", "key": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "uid": "48275201-e807-4351-a5ba-d316e8e28ffc"}
2025-02-03T16:07:00.789781051Z stderr F 2025-02-03T16:07:00.7895326Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-job-7wwj6","namespace":"e2e-tas-gv22z"}, "workload": "e2e-tas-gv22z/job-test-job-1fd00", "store": "tas-topology-ungater", "key": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "uid": "48275201-e807-4351-a5ba-d316e8e28ffc"}
2025-02-03T16:07:02.26445711Z stderr F 2025-02-03T16:07:02.264230439Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-job-7wwj6","namespace":"e2e-tas-gv22z"}, "workload": "e2e-tas-gv22z/job-test-job-1fd00", "store": "tas-topology-ungater", "key": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "uid": "48275201-e807-4351-a5ba-d316e8e28ffc"}
2025-02-03T16:07:03.467770831Z stderr F 2025-02-03T16:07:03.46756779Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-job-7wwj6","namespace":"e2e-tas-gv22z"}, "workload": "e2e-tas-gv22z/job-test-job-1fd00", "store": "tas-topology-ungater", "key": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "uid": "48275201-e807-4351-a5ba-d316e8e28ffc"}
2025-02-03T16:07:04.482803213Z stderr F 2025-02-03T16:07:04.482575421Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-job-7wwj6","namespace":"e2e-tas-gv22z"}, "workload": "e2e-tas-gv22z/job-test-job-1fd00", "store": "tas-topology-ungater", "key": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "uid": "48275201-e807-4351-a5ba-d316e8e28ffc"}
2025-02-03T16:07:04.502352924Z stderr F 2025-02-03T16:07:04.502091532Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "queue": "main", "status": "finished", "prevStatus": "admitted", "clusterQueue": "cluster-queue"}
2025-02-03T16:07:04.516859135Z stderr F 2025-02-03T16:07:04.516579853Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "queue": "main", "status": "finished", "clusterQueue": "cluster-queue"}
2025-02-03T16:07:04.580628821Z stderr F 2025-02-03T16:07:04.580305839Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-job-7wwj6","namespace":"e2e-tas-gv22z"}, "workload": "e2e-tas-gv22z/job-test-job-1fd00", "store": "tas-topology-ungater", "key": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "uid": "48275201-e807-4351-a5ba-d316e8e28ffc"}
2025-02-03T16:07:04.582667564Z stderr F 2025-02-03T16:07:04.582389422Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-job-7wwj6","namespace":"e2e-tas-gv22z"}, "workload": "e2e-tas-gv22z/job-test-job-1fd00", "store": "tas-topology-ungater", "key": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "uid": "48275201-e807-4351-a5ba-d316e8e28ffc"}
2025-02-03T16:07:04.582686024Z stderr F 2025-02-03T16:07:04.582484703Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:634	Workload delete event	{"workload": {"name":"job-test-job-1fd00","namespace":"e2e-tas-gv22z"}, "queue": "main", "status": "finished"}
2025-02-03T16:07:04.683502091Z stderr F 2025-02-03T16:07:04.683301659Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:170	LocalQueue delete event	{"localQueue": {"name":"main","namespace":"e2e-tas-gv22z"}}
2025-02-03T16:07:04.688682182Z stderr F 2025-02-03T16:07:04.68827626Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:04.701322571Z stderr F 2025-02-03T16:07:04.7011025Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:04.701348432Z stderr F 2025-02-03T16:07:04.701196971Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:04.949962347Z stderr F 2025-02-03T16:07:04.949715906Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:04.956355367Z stderr F 2025-02-03T16:07:04.956193386Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:05.215872821Z stderr F 2025-02-03T16:07:05.215664819Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:173	Topology delete event	{"topology": {"name":"hostname"}}
2025-02-03T16:07:05.500767582Z stderr F 2025-02-03T16:07:05.500539551Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T16:07:05.50686652Z stderr F 2025-02-03T16:07:05.506663699Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:05.514322246Z stderr F 2025-02-03T16:07:05.514076605Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:05.521236679Z stderr F 2025-02-03T16:07:05.521053188Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:05.774700965Z stderr F 2025-02-03T16:07:05.774473433Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:139	LocalQueue create event	{"localQueue": {"name":"main","namespace":"e2e-tas-8qgzf"}}
2025-02-03T16:07:05.781127625Z stderr F 2025-02-03T16:07:05.780929174Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:184	Queue update event	{"localQueue": {"name":"main","namespace":"e2e-tas-8qgzf"}}
2025-02-03T16:07:05.801584111Z stderr F 2025-02-03T16:07:05.80137467Z	INFO	admission.jobset-webhook	jobset/jobset_webhook.go:94	Validating create	{"webhookGroup": "jobset.x-k8s.io", "webhookKind": "JobSet", "JobSet": {"name":"test-jobset","namespace":"e2e-tas-8qgzf"}, "namespace": "e2e-tas-8qgzf", "name": "test-jobset", "resource": {"group":"jobset.x-k8s.io","version":"v1alpha2","resource":"jobsets"}, "user": "kubernetes-admin", "requestID": "fbbe1c39-d6bf-4e52-8565-b43651e93118"}
2025-02-03T16:07:05.820083607Z stderr F 2025-02-03T16:07:05.819852336Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:599	Workload create event	{"workload": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "queue": "main", "status": "pending"}
2025-02-03T16:07:05.836463819Z stderr F 2025-02-03T16:07:05.836253738Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "queue": "main", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
2025-02-03T16:07:05.875678723Z stderr F 2025-02-03T16:07:05.875451581Z	INFO	admission.jobset-webhook	jobset/jobset_webhook.go:103	Validating update	{"webhookGroup": "jobset.x-k8s.io", "webhookKind": "JobSet", "JobSet": {"name":"test-jobset","namespace":"e2e-tas-8qgzf"}, "namespace": "e2e-tas-8qgzf", "name": "test-jobset", "resource": {"group":"jobset.x-k8s.io","version":"v1alpha2","resource":"jobsets"}, "user": "system:serviceaccount:kueue-system:kueue-controller-manager", "requestID": "ee86f698-ff22-439e-b66f-a675f419fb5f"}
2025-02-03T16:07:06.828394736Z stderr F 2025-02-03T16:07:06.828188595Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:184	Queue update event	{"localQueue": {"name":"main","namespace":"e2e-tas-8qgzf"}}
2025-02-03T16:07:06.828893559Z stderr F 2025-02-03T16:07:06.828741498Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:06.923796919Z stderr F 2025-02-03T16:07:06.923519157Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj2-0-0-7t964","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "6c4a1e57-e7de-4b00-bffb-2c63844c4691"}
2025-02-03T16:07:06.923819839Z stderr F 2025-02-03T16:07:06.923625708Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj1-0-0-gt8ts","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "34757342-8eb5-486e-8c14-4105b350541c"}
2025-02-03T16:07:06.929744826Z stderr F 2025-02-03T16:07:06.929217593Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj2-0-0-7t964","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "6c4a1e57-e7de-4b00-bffb-2c63844c4691"}
2025-02-03T16:07:06.929815407Z stderr F 2025-02-03T16:07:06.929316823Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj1-0-0-gt8ts","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "34757342-8eb5-486e-8c14-4105b350541c"}
2025-02-03T16:07:06.941253198Z stderr F 2025-02-03T16:07:06.941007377Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj2-0-0-7t964","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "6c4a1e57-e7de-4b00-bffb-2c63844c4691"}
2025-02-03T16:07:06.951419601Z stderr F 2025-02-03T16:07:06.95116701Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj1-0-0-gt8ts","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "34757342-8eb5-486e-8c14-4105b350541c"}
2025-02-03T16:07:08.283213762Z stderr F 2025-02-03T16:07:08.282772129Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj1-0-0-gt8ts","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "34757342-8eb5-486e-8c14-4105b350541c"}
2025-02-03T16:07:08.293885048Z stderr F 2025-02-03T16:07:08.293654416Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj2-0-0-7t964","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "6c4a1e57-e7de-4b00-bffb-2c63844c4691"}
2025-02-03T16:07:09.46828345Z stderr F 2025-02-03T16:07:09.467961888Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj1-0-0-gt8ts","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "34757342-8eb5-486e-8c14-4105b350541c"}
2025-02-03T16:07:09.577412838Z stderr F 2025-02-03T16:07:09.577038626Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj2-0-0-7t964","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "6c4a1e57-e7de-4b00-bffb-2c63844c4691"}
2025-02-03T16:07:10.484691169Z stderr F 2025-02-03T16:07:10.484412567Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj1-0-0-gt8ts","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "34757342-8eb5-486e-8c14-4105b350541c"}
2025-02-03T16:07:10.518270178Z stderr F 2025-02-03T16:07:10.518018906Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "queue": "main", "status": "admitted", "clusterQueue": "cluster-queue"}
2025-02-03T16:07:10.594745463Z stderr F 2025-02-03T16:07:10.594498612Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj2-0-0-7t964","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "6c4a1e57-e7de-4b00-bffb-2c63844c4691"}
2025-02-03T16:07:10.628707844Z stderr F 2025-02-03T16:07:10.628413302Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "queue": "main", "status": "finished", "prevStatus": "admitted", "clusterQueue": "cluster-queue"}
2025-02-03T16:07:10.645153037Z stderr F 2025-02-03T16:07:10.644955485Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "queue": "main", "status": "finished", "clusterQueue": "cluster-queue"}
2025-02-03T16:07:10.680162215Z stderr F 2025-02-03T16:07:10.679865153Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj1-0-0-gt8ts","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "34757342-8eb5-486e-8c14-4105b350541c"}
2025-02-03T16:07:10.683482645Z stderr F 2025-02-03T16:07:10.682977912Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj2-0-0-7t964","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "6c4a1e57-e7de-4b00-bffb-2c63844c4691"}
2025-02-03T16:07:10.683528526Z stderr F 2025-02-03T16:07:10.683388495Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj1-0-0-gt8ts","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "34757342-8eb5-486e-8c14-4105b350541c"}
2025-02-03T16:07:10.687271929Z stderr F 2025-02-03T16:07:10.686972297Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-jobset-rj2-0-0-7t964","namespace":"e2e-tas-8qgzf"}, "workload": "e2e-tas-8qgzf/jobset-test-jobset-61845", "store": "tas-topology-ungater", "key": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "uid": "6c4a1e57-e7de-4b00-bffb-2c63844c4691"}
2025-02-03T16:07:10.687903743Z stderr F 2025-02-03T16:07:10.687694572Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:634	Workload delete event	{"workload": {"name":"jobset-test-jobset-61845","namespace":"e2e-tas-8qgzf"}, "queue": "main", "status": "finished"}
2025-02-03T16:07:10.783445206Z stderr F 2025-02-03T16:07:10.783225405Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:170	LocalQueue delete event	{"localQueue": {"name":"main","namespace":"e2e-tas-8qgzf"}}
2025-02-03T16:07:10.789400493Z stderr F 2025-02-03T16:07:10.789152851Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:10.801608489Z stderr F 2025-02-03T16:07:10.801418498Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:10.80164119Z stderr F 2025-02-03T16:07:10.801519839Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:11.050202815Z stderr F 2025-02-03T16:07:11.049932303Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:11.056695875Z stderr F 2025-02-03T16:07:11.056488194Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:11.334602693Z stderr F 2025-02-03T16:07:11.334358251Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:173	Topology delete event	{"topology": {"name":"hostname"}}
2025-02-03T16:07:11.626029065Z stderr F 2025-02-03T16:07:11.625765373Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T16:07:11.632202723Z stderr F 2025-02-03T16:07:11.631998452Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:11.639878191Z stderr F 2025-02-03T16:07:11.63966374Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:11.647506388Z stderr F 2025-02-03T16:07:11.647300597Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:11.901037945Z stderr F 2025-02-03T16:07:11.900826274Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:139	LocalQueue create event	{"localQueue": {"name":"main","namespace":"e2e-tas-9v5qt"}}
2025-02-03T16:07:11.907168533Z stderr F 2025-02-03T16:07:11.906981042Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:184	Queue update event	{"localQueue": {"name":"main","namespace":"e2e-tas-9v5qt"}}
2025-02-03T16:07:11.925449777Z stderr F 2025-02-03T16:07:11.925233466Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:599	Workload create event	{"workload": {"name":"pod-test-pod-5b478","namespace":"e2e-tas-9v5qt"}, "queue": "main", "status": "pending"}
2025-02-03T16:07:11.940074367Z stderr F 2025-02-03T16:07:11.939871356Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"pod-test-pod-5b478","namespace":"e2e-tas-9v5qt"}, "queue": "main", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
```

or with removed lines related to workload, expectations and local queues:
```
2025-02-03T16:06:58.85938113Z stderr F 2025-02-03T16:06:58.859068148Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cq"}}
2025-02-03T16:06:58.872197229Z stderr F 2025-02-03T16:06:58.871922667Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cq"}}
2025-02-03T16:06:58.872220169Z stderr F 2025-02-03T16:06:58.872021348Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cq"}}
2025-02-03T16:06:59.149583984Z stderr F 2025-02-03T16:06:59.149367483Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:06:59.155792042Z stderr F 2025-02-03T16:06:59.155579971Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:06:59.419550922Z stderr F 2025-02-03T16:06:59.41929059Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T16:06:59.426087833Z stderr F 2025-02-03T16:06:59.425859492Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:06:59.435407431Z stderr F 2025-02-03T16:06:59.435121739Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:06:59.443291009Z stderr F 2025-02-03T16:06:59.443038048Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:00.741513721Z stderr F 2025-02-03T16:07:00.741363091Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:04.688682182Z stderr F 2025-02-03T16:07:04.68827626Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:04.701322571Z stderr F 2025-02-03T16:07:04.7011025Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:04.701348432Z stderr F 2025-02-03T16:07:04.701196971Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:04.949962347Z stderr F 2025-02-03T16:07:04.949715906Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:04.956355367Z stderr F 2025-02-03T16:07:04.956193386Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:05.215872821Z stderr F 2025-02-03T16:07:05.215664819Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:173	Topology delete event	{"topology": {"name":"hostname"}}
2025-02-03T16:07:05.500767582Z stderr F 2025-02-03T16:07:05.500539551Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T16:07:05.50686652Z stderr F 2025-02-03T16:07:05.506663699Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:05.514322246Z stderr F 2025-02-03T16:07:05.514076605Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:05.521236679Z stderr F 2025-02-03T16:07:05.521053188Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:06.828893559Z stderr F 2025-02-03T16:07:06.828741498Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:10.789400493Z stderr F 2025-02-03T16:07:10.789152851Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:10.801608489Z stderr F 2025-02-03T16:07:10.801418498Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:317	ClusterQueue delete event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:10.80164119Z stderr F 2025-02-03T16:07:10.801519839Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:323	Cleared resource metrics for deleted ClusterQueue.	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:11.050202815Z stderr F 2025-02-03T16:07:11.049932303Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:173	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:11.056695875Z stderr F 2025-02-03T16:07:11.056488194Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:153	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:11.334602693Z stderr F 2025-02-03T16:07:11.334358251Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:173	Topology delete event	{"topology": {"name":"hostname"}}
2025-02-03T16:07:11.626029065Z stderr F 2025-02-03T16:07:11.625765373Z	LEVEL(-2)	tas-topology-controller	tas/topology_controller.go:136	Topology create event	{"topology": {"name":"hostname"}}
2025-02-03T16:07:11.632202723Z stderr F 2025-02-03T16:07:11.631998452Z	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:131	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2025-02-03T16:07:11.639878191Z stderr F 2025-02-03T16:07:11.63966374Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:292	ClusterQueue create event	{"clusterQueue": {"name":"cluster-queue"}}
2025-02-03T16:07:11.647506388Z stderr F 2025-02-03T16:07:11.647300597Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:341	ClusterQueue update event	{"clusterQueue": {"name":"cluster-queue"}}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T14:53:37Z

What could be useful is to restrict the successful logs only to the flaky test. Similarly, show the kueue logs for a failed run from the controllers, but only. Then, maybe diffing them would reveal something useful.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-04-09T18:33:35Z

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-08T19:22:45Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:29:24Z

/close 
I think this is likely a race condition already solved by https://github.com/kubernetes-sigs/kueue/pull/5309. I haven't seen it since then. Let's re-open if this repeats.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-07T08:29:30Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4140#issuecomment-3163075653):

>/close 
>I think this is likely a race condition already solved by https://github.com/kubernetes-sigs/kueue/pull/5309. I haven't seen it since then. Let's re-open if this repeats.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
