# PR #1: Add more details and links related to the project

**Summary**: Add more details and links related to the project

**Sources**: https://github.com/kubernetes-sigs/kueue/pull/1

**Last updated**: 2022-02-16T19:58:45Z

---

## Metadata

- **State**: closed (merged)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Branch**: `ahg-update-docs` → `main`
- **Created**: 2022-02-16T19:35:03Z
- **Updated**: 2022-02-16T19:58:45Z
- **Merged**: 2022-02-16T19:58:44Z
- **Closed**: 2022-02-16T19:58:45Z
- **Labels**: `lgtm`, `approved`, `cncf-cla: yes`, `size/S`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Requested reviewers**: _none_
- **Changed files**: 1   **+11 / -3**

## Description

@alculquicondor

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-02-16T19:35:16Z

[APPROVALNOTIFIER] This PR is **APPROVED**

This pull-request has been approved by: *<a href="https://github.com/kubernetes-sigs/kueue/pull/1#" title="Author self-approved">ahg-g</a>*

The full list of commands accepted by this bot can be found [here](https://go.k8s.io/bot-commands?repo=kubernetes-sigs%2Fkueue).

The pull request process is described [here](https://git.k8s.io/community/contributors/guide/owners.md#the-code-review-process)

<details >
Needs approval from an approver in each of these files:

- ~~[OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS)~~ [ahg-g]

Approvers can indicate their approval by writing `/approve` in a comment
Approvers can cancel approval by writing `/approve cancel` in a comment
</details>
<!-- META={"approvers":[]} -->

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-16T19:57:00Z

/lgtm

## Reviews

### Review by [@alculquicondor](https://github.com/alculquicondor) (commented) — 2022-02-16T19:40:09Z

- **README.md:7** by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-16T19:39:41Z
```diff
@@ -1,15 +1,23 @@
 # Kueue
 
-Kubernetes-native Job Queueing
+Kueue is a set of APIs and controller for job queueing. It is a job-level manager that decides when 
+a job should start (as in pods can be created) and when it should stop (as in active pods should be 
+deleted). The main design principle for Kueue is to avoid duplicating existing functionality: autoscaling, 
+pod-to-node scheduling, job lifecycle management and advanced admission control are the responsibility of 
+existing k8s components, namely cluster-autoscaler, kube-scheduler, kube-controller-manager and Gatekeeper, 
```

  let's not imply that gatekeeper is a k8s component.

### Review by [@ahg-g](https://github.com/ahg-g) (commented) — 2022-02-16T19:52:12Z

- **README.md:7** by [@ahg-g](https://github.com/ahg-g) — 2022-02-16T19:52:11Z
```diff
@@ -1,15 +1,23 @@
 # Kueue
 
-Kubernetes-native Job Queueing
+Kueue is a set of APIs and controller for job queueing. It is a job-level manager that decides when 
+a job should start (as in pods can be created) and when it should stop (as in active pods should be 
+deleted). The main design principle for Kueue is to avoid duplicating existing functionality: autoscaling, 
+pod-to-node scheduling, job lifecycle management and advanced admission control are the responsibility of 
+existing k8s components, namely cluster-autoscaler, kube-scheduler, kube-controller-manager and Gatekeeper, 
```

  done.
