# Issue #7285: website: a lot of dead links

**Summary**: website: a lot of dead links

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7285

**Last updated**: 2025-12-10T12:15:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alexandear](https://github.com/alexandear)
- **Created**: 2025-10-15T21:08:33Z
- **Updated**: 2025-12-10T12:15:37Z
- **Closed**: 2025-12-10T12:15:37Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 9

## Description

The website https://kueue.sigs.k8s.io has 30 dead links. Some of them:

| Page | Screenshot | Dead Link |
|------|--------|--------|
| [Concepts](https://kueue.sigs.k8s.io/docs/concepts) |  <img height="152" alt="Image" src="https://github.com/user-attachments/assets/4d50ec8b-98c6-4439-8053-d42714e303e8" /> | [Admission](https://kueue.sigs.k8s.io/docs/concepts/docs/concepts/admission/) |
| [Admission Check](https://kueue.sigs.k8s.io/docs/concepts/admission_check/) | <img height="138" alt="Image" src="https://github.com/user-attachments/assets/5afaa27e-27dc-4382-ac24-0627a38e9b72" /> | [Provisioning Admission Check Controller](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning) |
| [Topology Aware Scheduling](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/) | <img height="218" alt="Image" src="https://github.com/user-attachments/assets/cf53b958-648b-4e09-bd6e-5bba2cd504d9" /> | [PodSet updates in ProvisioningRequestConfig](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/site/content/en/docs/admission-check-controllers/provisioning.md) |

For the full list see logs from the [`linkchecker`](https://github.com/linkchecker/linkchecker) below.



<details><summary>Details</summary>
<p>

```console
$ linkchecker --no-warnings https://kueue.sigs.k8s.io
INFO linkcheck.cmdline 2025-10-15 23:54:21,431 MainThread Checking intern URLs only; use --check-extern to check extern URLs.
LinkChecker 10.5.0
Copyright (C) 2000-2016 Bastian Kleineidam, 2010-2024 LinkChecker Authors
LinkChecker comes with ABSOLUTELY NO WARRANTY!
This is free software, and you are welcome to redistribute it under
certain conditions. Look at the file `COPYING' within this distribution.
Read the documentation at https://linkchecker.github.io/linkchecker/
Write comments and bugs to https://github.com/linkchecker/linkchecker/issues

Start checking at 2025-10-15 23:54:21+003

URL        `/docs/admission-check-controllers/provisioning/#job-using-a-provisioningrequest'
Name       `provisioningRequest'
Parent URL https://kueue.sigs.k8s.io/docs/overview/, line 155, col 2082
Real URL   https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/#job-using-a-provisioningrequest
Check time 3.160 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,   196 links queued, 1594 links in 1800 URLs checked, runtime 1 minute, 51 seconds

URL        `docs/concepts/admission/'
Name       `Admission'
Parent URL https://kueue.sigs.k8s.io/docs/concepts/, line 153, col 1112
Real URL   https://kueue.sigs.k8s.io/docs/concepts/docs/concepts/admission/
Check time 2.996 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,   179 links queued, 1611 links in 1800 URLs checked, runtime 1 minute, 56 seconds

URL        `/docs/admission-check-controllers/provisioning'
Name       `Provisioning Admission Check Controller'
Parent URL https://kueue.sigs.k8s.io/docs/concepts/admission_check/, line 211, col 563
Real URL   https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning
Check time 2.730 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `site/content/en/docs/admission-check-controllers/provisioning.md'
Name       `PodSet updates in ProvisioningRequestConfig'
Parent URL https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/, line 321, col 92
Real URL   https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/site/content/en/docs/admission-check-controllers/provisioning.md
Check time 2.885 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `docs/tasks/run/multikueue/jobset'
Name       `Dispatch a Kueue managed JobSet'
Parent URL https://kueue.sigs.k8s.io/docs/concepts/multikueue/, line 185, col 660
Real URL   https://kueue.sigs.k8s.io/docs/concepts/multikueue/docs/tasks/run/multikueue/jobset
Check time 2.691 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `manage/cert_manager'
Name       `use third-party certificate authority with Kueue'
Parent URL https://kueue.sigs.k8s.io/docs/tasks/, line 158, col 452
Real URL   https://kueue.sigs.k8s.io/docs/tasks/manage/cert_manager
Check time 2.866 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,   163 links queued, 1627 links in 1800 URLs checked, runtime 2 minutes, 1 seconds
10 threads active,   149 links queued, 1641 links in 1804 URLs checked, runtime 2 minutes, 6 seconds
10 threads active,   135 links queued, 1655 links in 1807 URLs checked, runtime 2 minutes, 11 seconds

URL        `/docs/tasks/run_kubeflow_jobs/run_jaxjobs'
Name       `Run a Kueue managed kubeflow JAXJob'
Parent URL https://kueue.sigs.k8s.io/docs/tasks/run/kubeflow/, line 155, col 997
Real URL   https://kueue.sigs.k8s.io/docs/tasks/run_kubeflow_jobs/run_jaxjobs
Check time 4.142 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,   121 links queued, 1669 links in 1812 URLs checked, runtime 2 minutes, 16 seconds

URL        `/docs/tasks/run_flux_minicluster/'
Name       `Run A Flux MiniCluster'
Parent URL https://kueue.sigs.k8s.io/docs/tasks/run/python_jobs/, line 648, col 79
Real URL   https://kueue.sigs.k8s.io/docs/tasks/run_flux_minicluster/
Check time 3.466 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,   108 links queued, 1682 links in 1813 URLs checked, runtime 2 minutes, 21 seconds

URL        `/docs/tasks/run/wrapped_custom_workload'
Name       `Running a Wrapped Custom Workload'
Parent URL https://kueue.sigs.k8s.io/docs/tasks/dev/integrate_a_custom_job/, line 155, col 5
Real URL   https://kueue.sigs.k8s.io/docs/tasks/run/wrapped_custom_workload
Check time 3.324 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,    94 links queued, 1696 links in 1813 URLs checked, runtime 2 minutes, 26 seconds

URL        `/docs/admission-check-controllers/provisioning.md'
Name       `ProvisioningRequest'
Parent URL https://kueue.sigs.k8s.io/docs/reference/labels-and-annotations/, line 182, col 535
Real URL   https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning.md
Check time 3.303 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,    79 links queued, 1711 links in 1813 URLs checked, runtime 2 minutes, 31 seconds

URL        `/docs/tasks/manage/installation'
Name       `证书管理指南'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/installation/, line 152, col 74
Real URL   https://kueue.sigs.k8s.io/docs/tasks/manage/installation
Check time 3.657 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `site/content/en/docs/admission-check-controllers/provisioning.md'
Name       `ProvisioningRequestConfig 中的 PodSet 更新'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/concepts/topology_aware_scheduling/, line 230, col 525
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/concepts/topology_aware_scheduling/site/content/en/docs/admission-check-controllers/provisioning.md
Check time 3.515 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `docs/tasks/run/multikueue/jobset'
Name       `调度 Kueue 管理的 JobSet'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/concepts/multikueue/, line 160, col 632
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/concepts/multikueue/docs/tasks/run/multikueue/jobset
Check time 3.412 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,    65 links queued, 1725 links in 1817 URLs checked, runtime 2 minutes, 36 seconds

URL        `manage/cert_manager'
Name       `use third-party certificate authority with Kueue'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/, line 153, col 470
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/tasks/manage/cert_manager
Check time 3.718 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,    53 links queued, 1737 links in 1818 URLs checked, runtime 2 minutes, 41 seconds

URL        `examples/visibility/pending-workloads-for-cluster-queue-visibility-dashboard.json'
Name       `ClusterQueue 可视化'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/manage/monitor_pending_workloads/pending_workloads_in_grafana/, line 213, col 530
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/tasks/manage/monitor_pending_workloads/pending_workloads_in_grafana/examples/visibility/pending-workloads-for-cluster-queue-visibility-dashboard.json
Check time 4.088 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `examples/visibility/pending-workloads-for-local-queue-visibility-dashboard.json'
Name       `LocalQueue 可视化'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/manage/monitor_pending_workloads/pending_workloads_in_grafana/, line 213, col 650
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/tasks/manage/monitor_pending_workloads/pending_workloads_in_grafana/examples/visibility/pending-workloads-for-local-queue-visibility-dashboard.json
Check time 4.161 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_jobsets/#jobset-definition'
Name       `JobSets'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/manage/setup_multikueue/, line 148, col 1309
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_jobsets/#jobset-definition
Check time 4.298 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_jobs/#1-define-the-job'
Name       `batch/Jobs'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/manage/setup_multikueue/, line 148, col 1380
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_jobs/#1-define-the-job
Check time 4.629 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,    41 links queued, 1749 links in 1820 URLs checked, runtime 2 minutes, 46 seconds

URL        `/zh-CN/docs/tasks/administer_cluster_quotas'
Name       `配额'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/run_cronjobs/, line 148, col 536
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/administer_cluster_quotas
Check time 4.288 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_jobs#3-optional-monitor-the-status-of-the-workload'
Name       `监控 Workload 的状态'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/run_cronjobs/, line 191, col 41
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_jobs#3-optional-monitor-the-status-of-the-workload
Check time 3.401 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_kubeflow_jobs/run_mpijobs'
Name       `运行 Kueue 管理的 Kubeflow MPIJob'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/kubeflow/, line 149, col 411
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_kubeflow_jobs/run_mpijobs
Check time 2.809 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_kubeflow_jobs/run_pytorchjobs'
Name       `运行 Kueue 管理的 Kubeflow PyTorchJob'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/kubeflow/, line 150, col 535
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_kubeflow_jobs/run_pytorchjobs
Check time 2.697 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_kubeflow_jobs/run_tfjobs'
Name       `运行 Kueue 管理的 Kubeflow TFJob'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/kubeflow/, line 150, col 641
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_kubeflow_jobs/run_tfjobs
Check time 3.149 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_kubeflow_jobs/run_xgboostjobs'
Name       `运行 Kueue 管理的 Kubeflow XGBoostJob'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/kubeflow/, line 150, col 737
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_kubeflow_jobs/run_xgboostjobs
Check time 2.875 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_kubeflow_jobs/run_paddlejobs'
Name       `运行 Kueue 管理的 Kubeflow PaddleJob'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/kubeflow/, line 150, col 843
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_kubeflow_jobs/run_paddlejobs
Check time 3.137 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_kubeflow_jobs/run_jaxjobs'
Name       `运行 Kueue 管理的 Kubeflow JAXJob'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/kubeflow/, line 150, col 947
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_kubeflow_jobs/run_jaxjobs
Check time 3.514 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,    27 links queued, 1763 links in 1823 URLs checked, runtime 2 minutes, 51 seconds

URL        `/zh-CN/docs/tasks/run_plain_pods'
Name       `管理普通 Pod'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/external_workloads/argo_workflow/, line 151, col 14
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_plain_pods
Check time 2.704 seconds
Size       6KB
Result     Error: 404 Not Found
10 threads active,    14 links queued, 1776 links in 1829 URLs checked, runtime 2 minutes, 56 seconds

URL        `/zh-CN/docs/tasks/run_flux_minicluster/'
Name       `运行 Flux MiniCluster'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/python_jobs/, line 660, col 39
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_flux_minicluster/
Check time 3.314 seconds
Size       6KB
Result     Error: 404 Not Found

URL        `/zh-CN/docs/tasks/run_kubeflow_jobs/run_mpijobs/'
Name       `运行 MPIJob'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/tasks/run/python_jobs/, line 848, col 35
Real URL   https://kueue.sigs.k8s.io/zh-CN/docs/tasks/run_kubeflow_jobs/run_mpijobs/
Check time 3.261 seconds
Size       6KB
Result     Error: 404 Not Found
 9 threads active,     0 links queued, 1791 links in 1829 URLs checked, runtime 3 minutes, 1 seconds

URL        `/zh-cn/docs/contribution_guidelines/testing.md'
Name       `运行和调试测试'
Parent URL https://kueue.sigs.k8s.io/zh-cn/docs/contribution_guidelines/, line 152, col 850
Real URL   https://kueue.sigs.k8s.io/zh-cn/docs/contribution_guidelines/testing.md
Check time 3.870 seconds
Size       6KB
Result     Error: 404 Not Found

Statistics:
Downloaded: 39.9MB.
Content types: 20 image, 386 text, 0 video, 0 audio, 115 application, 0 mail and 1279 other.
URL lengths: min=15, max=1068, avg=126.

That's it. 1800 links in 1829 URLs checked. 0 warnings found (74 ignored or duplicates not printed). 30 errors found.
Stopped checking at 2025-10-15 23:57:27+003 (3 minutes, 5 seconds)
```

</p>
</details>

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T09:00:41Z

/close
I have verified manually all the mentioned links work, maybe it is an issue with the linkchecker?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-10T09:00:48Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7285#issuecomment-3636046318):

>/close
>I have verified manually all the mentioned links work, maybe it is an issue with the linkchecker?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alexandear](https://github.com/alexandear) — 2025-12-10T10:16:05Z

@mimowo Did you verify these links? Because they are still broken (404).

<img width="892" height="1049" alt="Image" src="https://github.com/user-attachments/assets/63e335bb-99d3-4152-8e11-4038ce88c042" />

Also, you can use this online tool for checking dead links: https://www.drlinkcheck.com/
It's limited to only 1500 links for free but it's enough to see that the website has at least 5 dead links. See the screenshots:

<img width="1480" height="1008" alt="Image" src="https://github.com/user-attachments/assets/c3dc632c-37c9-4338-98f2-550aafe39927" />

<img width="1494" height="983" alt="Image" src="https://github.com/user-attachments/assets/6aa6e7aa-abb5-407c-b4c5-05c78e4446cc" />

### Comment by [@alexandear](https://github.com/alexandear) — 2025-12-10T10:17:28Z

404 Page not found:

https://kueue.sigs.k8s.io/docs/tasks/manage/installation
<img width="1186" height="511" alt="Image" src="https://github.com/user-attachments/assets/3c6144f2-56c7-400b-b79d-7fb45cb42ab3" />

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T10:24:10Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-10T10:24:15Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7285#issuecomment-3636379849):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T10:24:43Z

Weird the links work for me.

Still, I'm all for making the tool happy

For example, I just retested clicking on "Admission" on the kueue website and it worked well:

<img width="2029" height="953" alt="Image" src="https://github.com/user-attachments/assets/9a59e90c-b8c4-423a-be3d-0b3e55e1ef2c" />

EDIT: maybe it depends on the browser? I'm testing on chrome.

### Comment by [@alexandear](https://github.com/alexandear) — 2025-12-10T10:36:15Z

I'm also using Chrome. It looks like the issue with "Admission" has been fixed.

But these links are still broken.

1. Go to https://kueue.sigs.k8s.io/docs/concepts/multikueue/ and try to open "[Dispatch a Kueue managed JobSet](https://kueue.sigs.k8s.io/docs/concepts/multikueue/docs/tasks/run/multikueue/jobset):

<img width="684" height="356" alt="Image" src="https://github.com/user-attachments/assets/481c8d6b-58af-487d-9554-6d4755c4d35b" />

2. Go to https://kueue.sigs.k8s.io/docs/tasks/ and try to open [use third-party certificate authority with Kueue](https://kueue.sigs.k8s.io/docs/tasks/manage/cert_manager):

<img width="930" height="618" alt="Image" src="https://github.com/user-attachments/assets/f9793aed-bdbf-46cd-97a9-803d98ee7f50" />

3. Go to https://kueue.sigs.k8s.io/docs/tasks/run/python_jobs/ and try to open [Run A Flux MiniCluster](https://kueue.sigs.k8s.io/docs/tasks/run_flux_minicluster/):

<img width="997" height="277" alt="Image" src="https://github.com/user-attachments/assets/32976b21-a68c-4b8a-97ee-72e1c32df684" />

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T11:04:43Z

Yes I can confirm the new links you mentioned are broken. So the issue remains valid. 

Thank you for double checking 👍
