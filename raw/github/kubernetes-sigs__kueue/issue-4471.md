# Issue #4471: WaitForPodsReady: support deleting workload when backoffLimitCount is reached

**Summary**: WaitForPodsReady: support deleting workload when backoffLimitCount is reached

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4471

**Last updated**: 2025-06-04T05:51:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@avrittrohwer](https://github.com/avrittrohwer)
- **Created**: 2025-03-04T01:51:23Z
- **Updated**: 2025-06-04T05:51:26Z
- **Closed**: 2025-06-03T15:39:24Z
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha), [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add support for having Kueue delete the Kueue Workload and underlying workload object (Job, JobSet, etc) when the WaitForPodsReady backoffLimitCount is reached.

We could add a RequeuingStrategy.ttlSecondsAfterBackoffLimitReached field.

**Why is this needed**:

Currently, when the backoffLimitCount is reached, the workload sits with condition DeactivatedDueToRequeuingLimitExceeded.  This is a terminal state for the workload.  Some underlying workload APIs support a time-to-live mechanism that causes the workload to be deleted some time after reaching a terminal state.  For example JobSet has ttlSecondsAfterFinished.  A JobSet that reaches the backoffLimitCount in Kueue never enters a terminal state from the JobSet point of view (just sits as suspended).  So customers need to write some controller to watch Kueue workloads with DeactivatedDueToRequeuingLimitExceeded and delete the underlying workload object (or do this manually).

**Completion requirements**:

Have some way for workloads reaching the DeactivatedDueToRequeuingLimitExceeded condition to be automatically cleaned up.

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-05T00:25:03Z

Here is a workaround deployment I tested in a kind cluster to clean up JobSets in this state.  **IT HAS NOT BEEN TESTED AT SCALE, BUYER BEWARE**. 

Kubernetes manifests:

```
apiVersion: v1
kind: Namespace
metadata:
  name: kueue-cleaner
---
apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: kueue-cleaner
  name: kueue-cleaner-sa
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  namespace: kueue-cleaner
  name: kueue-cleaner-role
rules:
- apiGroups: ["kueue.x-k8s.io", "jobset.x-k8s.io"]
  resources: ["workloads", "jobsets"]
  verbs: ["get", "list", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kueue-cleaner-binding
subjects:
- kind: ServiceAccount
  namespace: kueue-cleaner
  name: kueue-cleaner-sa
roleRef:
  kind: ClusterRole
  name: kueue-cleaner-role
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: kueue-cleaner
  name: kueue-cleaner
  labels:
    app: kueue-cleaner
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kueue-cleaner
  template:
    metadata:
      labels:
        app: kueue-cleaner
    spec:
      serviceAccountName: kueue-cleaner-sa
      containers:
      - name: kueue-cleaner
        image: <YOUR_IMAGE>
        command:
        - "python"
        - "/usr/src/app/main.py"
        # uncomment to start deleting - "--no-dry-run"
```

Dockerfile:

```
FROM python:3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "/usr/src/app/main.py" ]
```

requirements.txt:

```
cachetools==5.5.2
certifi==2025.1.31
charset-normalizer==3.4.1
durationpy==0.9
google-auth==2.38.0
idna==3.10
kubernetes==32.0.1
oauthlib==3.2.2
pyasn1==0.6.1
pyasn1_modules==0.4.1
python-dateutil==2.9.0.post0
PyYAML==6.0.2
requests==2.32.3
requests-oauthlib==2.0.0
rsa==4.9
six==1.17.0
urllib3==2.3.0
websocket-client==1.8.0
```

main.py:

```
import argparse
import json
import kubernetes
import logging
import sys
import time


logger = logging.getLogger(__name__)


def retry_wait(prev_timeout):
    min_timeout = 3
    max_timeout = 60
    factor = 1.5
    
    if prev_timeout < min_timeout:
        timeout = min_timeout
    else:
        timeout = int(prev_timeout * factor) # int() only works if the min_timeout * factor is greater than 2 (otherwise we keep getting 1).

    if timeout > max_timeout:
        timeout = max_timeout

    logger.info(f"Sleeping for {timeout} seconds due to retry")
    time.sleep(timeout)
    return timeout


def should_delete_workload(workload):
    for condition in workload["status"]["conditions"]:
        if condition["reason"] == "DeactivatedDueToRequeuingLimitExceeded" and condition["status"] == 'True':
            for owner in workload["metadata"]["ownerReferences"]:
                if owner["apiVersion"] == "jobset.x-k8s.io/v1alpha2" and owner["kind"] == "JobSet":
                    return True, workload["metadata"]["namespace"], owner["name"]

    return False, "", ""


def delete_jobset(api, namespace, name):
    try:
        api.delete_namespaced_custom_object(
            "jobset.x-k8s.io", "v1alpha2", namespace, "jobsets", name,
            grace_period_seconds=0)
        logger.info(f"Deleted jobset {namespace}/{name}")
    except kubernetes.client.rest.ApiException as e:
        # ignore not found
        if e.status == 404:
            return
        logger.error(f"Error deleting JobSet {namespace}/{name}: {e}")


def watch_workloads(api, poll_frequency_seconds, list_limit, dry_run):
    retry_timeout = 0
    def increment_timeout():
        nonlocal retry_timeout
        retry_timeout = retry_wait(retry_timeout)
    def reset_timeout():
        nonlocal retry_timeout
        retry_timeout = 0

    continue_token = ""
    while True:
        time.sleep(retry_timeout)    
        try:
            ret = api.list_custom_object_for_all_namespaces(
                "kueue.x-k8s.io", "v1beta1", "workloads",
                _continue=continue_token,
                limit=list_limit,
                timeout_seconds=30)
            reset_timeout()
        except kubernetes.client.rest.ApiException as e:
            if e.status == 410:
                try:
                    body = json.loads(e.body)
                except json.decoder.JSONDecodeError:
                    logger.error(f"Got HTTP 410 error listing Workloads but could not load HTTP body as JSON. Original error: {e}")
                    increment_timeout()
                    continue

                # 410 is treated as successful response, we just need to start with the new continue token.
                continue_token = body["metadata"]["continue"]
                reset_timeout()
                continue
                    
            logger.error(f"Error listing Workloads: {e}")
            increment_timeout()
            continue
        
        for workload in ret["items"]:
            should_delete, namespace, jobset_name = should_delete_workload(workload)
            if should_delete:
                if dry_run:
                    logger.info(f"(--dry_run enabled) Would delete jobset {namespace}/{jobset_name}")
                    continue
                # Don't retry deletion here, we will try again on the next list.
                delete_jobset(api, namespace, jobset_name)

        if ret["metadata"]["continue"] != "":
            continue_token = ret["metadata"]["continue"]
            continue

        continue_token = ""
        time.sleep(poll_frequency_seconds)


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(asctime)s %(name)s:%(lineno)d %(levelname)s:%(message)s", datefmt='%Y-%m-%dT%H:%M:%S%z')

    p = argparse.ArgumentParser()
    p.add_argument('--poll-frequency-seconds', type=int, default=60)
    p.add_argument('--list-batch-size', type=int, default=64)
    p.add_argument('--dry-run', type=bool, default=True, action=argparse.BooleanOptionalAction)
    args = p.parse_args()
    logger.info(f"Args: {args}")
    
    try:
        kubernetes.config.load_incluster_config()
    except kubernetes.config.ConfigException:
        kubernetes.config.load_kube_config()

    api = kubernetes.client.CustomObjectsApi()
    logger.info("Starting to watch Kueue Workloads...")
    watch_workloads(api, args.poll_frequency_seconds, args.list_batch_size, args.dry_run)


if __name__ == "__main__":
    main()
```

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-03-28T07:55:42Z

Would it be possible for you to propose an extension to an already existing KEP for removing finished Workloads [KEP 1618](https://github.com/kubernetes-sigs/kueue/pull/2742)? This feature should probably be an opt-in one and it'd make sense to use the same namespace as in the proposed API. Or you could propose a new API in a KEP and we'll try to decide how to make both consistent.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-28T11:33:06Z

I think deleting workloads which are deactivated sounds very useful. Such workloads will likely never be able to run, and would need manual cleanup by an admin, or script (as above). This is indeed a very similar case to deleting finished workloads, so a similar API is my natural intuition, but let's consider options:
1. a dedicated extension to the waitForPodsReady API, such as `ttlSecondsAfterBackoffLimitReached` under `waitForPodsReady.requeingStrategy`
2. a extension to the API in https://github.com/kubernetes-sigs/kueue/pull/2742, for example
or more granular:
```yaml
objectRetentionPolicies:
  finishedWorkloadRetention: 10min
  deactivatedWorkloadRetention: 10min
```
```yaml
objectRetentionPolicies:
  finishedWorkloadRetention: 10min
  deactivatedWorkloadRetentionPolicy:
    - reason: RequeuingLimitExceeded
      ttl: 10min
    - reason: MaximumExecutionTimeExceeded
      ttl: 30min
    - reason: AdmissionCheck
      ttl: 3min
```
I would be leaning to (2.) because it feels more natural given the similar nature of the feature (global TTL), just with different preconditions on the objects. I admit (2.) carries a bit more work, but it does not feel like much more.

Wdyt @tenzen-y @avrittrohwer ?

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-04-07T16:03:16Z

Adding support for cleaning up deactivated workloads via KEP 1628 sounds good to me

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-07T16:15:25Z

Ok, regarding the two options (a) and (b) under 2, maybe we do a mix:
```yaml
objectRetentionPolicies:
  finishedWorkloads: 
     ttl: 10min
  deactivatedWorkloads:
     ttl: 10min
```
for now, but with this proposal:
- we don't do full "b" yet - because we don't have an indication that we need different ttl depending on the reason of deactivation
- we make the `finishedWorkloads` and `deactivatedWorkloads` structs. so they can be easily extended in future if needed (for example with different ttl depending on the reason)
- don't put "Retention" on both levels, because it is redundant

wdyt? Or maybe instead of "ttl" we use "defaultTTL", but I guess the details can be discussed in the KEP itself.

### Comment by [@yugantrana](https://github.com/yugantrana) — 2025-04-08T15:47:32Z

The proposed option seems sufficient for the initial implementation, and we can always extend it to something like (b) later if the need arises.

A note regarding default values,
- It would be beneficial to have `objectRetentionPolicies.deactivatedWorkloads.ttl` default to 0. 
- This would mean deactivated workloads are cleaned up immediately unless a user explicitly sets a different deactivatedWorkloads' TTL.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T16:17:51Z

> It would be beneficial to have objectRetentionPolicies.deactivatedWorkloads.ttl default to 0.

Yeah, maybe, the issue is it would be a breaking change. So, I would prefer a backwards compatible API (no TTL), or at least some higher value like 1h.

### Comment by [@mykysha](https://github.com/mykysha) — 2025-04-10T07:42:44Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-16T13:08:09Z

For the future expansion, I would like to select

```yaml
objectRetentionPolicies:
  workloads:
    afterFinished: 10m
  admissionChecks: # no plan for now
```

Anyway, we need to disscuss this in a KEP

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-07T11:11:26Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-12T16:48:23Z

/reopen
to address the remaining comments, see https://github.com/kubernetes-sigs/kueue/pull/5177#issuecomment-2873159713

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-12T16:48:28Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4471#issuecomment-2873279028):

>/reopen
>to address the remaining comments, see https://github.com/kubernetes-sigs/kueue/pull/5177#issuecomment-2873159713


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-14T20:18:30Z

Is this complete?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T15:38:01Z

> Is this complete?

Actually, not yet. I am considering the follow-up issue. After we open a new issue or address those, we might close this one because the follow-up tasks are quite big.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T15:39:29Z

We will also need documetation. We can track the documentation as a follow up issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T17:27:27Z

> Actually, not yet. I am considering the follow-up issue. After we open a new issue or address those, we might close this one because the follow-up tasks are quite big.

@tenzen-y I suggest to close it and track the follow up separately, I just opened the documentation issue: https://github.com/kubernetes-sigs/kueue/issues/5261. Could you please open issue for what you have in mind?

### Comment by [@jrleslie](https://github.com/jrleslie) — 2025-06-03T15:31:35Z

We're running across this behavior as well in v0.11.0. 

Is there currently no way to disable the requeuingStrategy on waitForPodsReady so they dont keep getting thrown back in the queue and ultimately end up blocking the queue? 

Is the current recommendation to just use a custom process to continually check the queues for the DeactivatedDueToRequeuingLimitExceeded status?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T15:39:19Z

> We're running across this behavior as well in v0.11.0.

This just reminded me that we can now close the issue as https://github.com/kubernetes-sigs/kueue/pull/5177 is merged.

Here are the docs under review: https://github.com/kubernetes-sigs/kueue/pull/5271

/close

> Is there currently no way to disable the requeuingStrategy on waitForPodsReady so they dont keep getting thrown back in the queue and ultimately end up blocking the queue?

If you don't want the workloads to be requeued you can set the waitForPodsReady.backoffLimitCount: 0. I believe, The workload will get deactived immediately. Then, garbace collect it using the new object retention feature.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-03T15:39:25Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4471#issuecomment-2936034030):

>> We're running across this behavior as well in v0.11.0.
>
>This just reminded me that we can now close the issue as https://github.com/kubernetes-sigs/kueue/pull/5177 is merged.
>
>Here are the docs under review: https://github.com/kubernetes-sigs/kueue/pull/5271
>
>/close
>
>> Is there currently no way to disable the requeuingStrategy on waitForPodsReady so they dont keep getting thrown back in the queue and ultimately end up blocking the queue?
>
>If you don't want the workloads to be requeued you can set the waitForPodsReady.backoffLimitCount: 0. I believe, The workload will get deactived immediately. Then, garbace collect it using the new object retention feature.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ricardov1](https://github.com/ricardov1) — 2025-06-03T21:26:55Z

hey @mimowo, @avrittrohwer ’s original request also included cleanup of the underlying workload object (Job, Jobset, PyTorchJob, etc.). I just tested the `afterFinished` functionality (on v0.12.0) with a PyTorchJob and while the Workload was deleted after the specified duration as expected, the PyTorchJob and Pods were not deleted. Is this the desired behavior?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T05:51:24Z

> hey [@mimowo](https://github.com/mimowo), [@avrittrohwer](https://github.com/avrittrohwer) ’s original request also included cleanup of the underlying workload object (Job, Jobset, PyTorchJob, etc.). I just tested the `afterFinished` functionality (on v0.12.0) with a PyTorchJob and while the Workload was deleted after the specified duration as expected, the PyTorchJob and Pods were not deleted. Is this the desired behavior?

Yes, that is intended. This aims to delete the Workload object resource (https://kueue.sigs.k8s.io/docs/concepts/workload/).
Kueue is not responsible for managing PytorchJobs, Jobs, JobSet, and Pods lifecycle.
OTOH, those Jobs provide the functionality to automatically clean up Jobs in the following:

- https://kubernetes.io/docs/concepts/workloads/controllers/job/#clean-up-finished-jobs-automatically
- https://jobset.sigs.k8s.io/docs/tasks/
- https://github.com/kubeflow/trainer/blob/d022585d00fe0b73389f106d0122141f82ea36a5/pkg/apis/kubeflow.org/v1/common_types.go#L199-L203
