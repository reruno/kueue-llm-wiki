# Issue #9565: 0.15.0+: how to configure which pods are managed by kueue?

**Summary**: 0.15.0+: how to configure which pods are managed by kueue?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9565

**Last updated**: 2026-02-27T12:23:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@bh-tt](https://github.com/bh-tt)
- **Created**: 2026-02-27T09:55:17Z
- **Updated**: 2026-02-27T12:23:57Z
- **Closed**: 2026-02-27T12:17:05Z
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template for documentation-related issues -->

**What would you like to be documented or improved**:
We upgraded to kueue 0.15.4 from 0.14.8, and immediately kueue started to managed Pods that do *not* have the kueue.x-k8s.io/queue-name label, adding the label, and immediately filling up the queue with all deployment/statefulset pods which should not be managed by kueue.

I've tried setting `manageJobsWithoutQueueName: false` in the config, yet kueue still adds the labels to new pods. We're running with the default MutatingWebhookConfiguration from the release yaml (kustomize install).

The [docs](https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/#before-you-begin) have a line about how the webhook objectSelector could be configured to filter pods, yet nowhere in the release notes does it state that this is *required* when using the pod integration, or else you end up with all Pods not in kueue-system/kube-system automatically managed by kueue.

Additionally, I couldn't really find the justification for removing the podOptions in any of the PRs/issues related to the v1beta2 Config update, only that the handling was removed.

Several questions:
 - is adding a objectSelector to the validating/mutatingwebhookconfiguration the intended way to make kueue only manage pods with the `kueue.x-k8s.io/queue-name` label?
 - is it necessary to add it to the validatingwebhookconfiguration as well (or only a slight performance gain as the kube-apiserver needs to  do fewer webhook calls)?

**Location** (URL, file path, or section if applicable):
https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/#before-you-begin

## Discussion

### Comment by [@bh-tt](https://github.com/bh-tt) — 2026-02-27T11:09:30Z

I've added the following kustomize patches to ensure kueue only receives webhook calls for resources that want to be managed by kueue:
```
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: kueue-validating-webhook-configuration
webhooks:
- name: vpod.kb.io
  objectSelector: &selector
    matchExpressions:
    - key: kueue.x-k8s.io/queue-name
      operator: Exists
- name: vjob.kb.io
  objectSelector: *selector
- name: vstatefulset.kb.io
  objectSelector: *selector
- name: vdeployment.kb.io
  objectSelector: *selector
---
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  name: kueue-mutating-webhook-configuration
webhooks:
- name: mpod.kb.io
  objectSelector: &selector
    matchExpressions:
    - key: kueue.x-k8s.io/queue-name
      operator: Exists
- name: mjob.kb.io
  objectSelector: *selector
- name: mdeployment.kb.io
  objectSelector: *selector
- name: mstatefulset.kb.io
  objectSelector: *selector
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T12:05:50Z

Thank you for the report! Im not yet sure what is going on, so let me ask some clarifying quedtikns:
1. what is the namespace where the Pods started to have the queue-name added? Can you exclude the namespace via configuration in the namespaceSelector?
2. Can you make sure the Deployment and StatwfulSets dont have the queue-name label? If they have, then it is expwcted that Pods will have the label as well
3. Are you maybe using the LocalQueueDefaulting -do you have the LocalQueue in the namespace called default?

### Comment by [@bh-tt](https://github.com/bh-tt) — 2026-02-27T12:17:05Z

1. I cannot exclude this namespace, as it is a namespace running predominantly Deployments outside of kueue's control, with a select few CronJobs
2. They do not have the label, that was the first thing I checked
3. We do have a LocalQueue called `default` in the namespace, but that likely predated the addition of that feature (I think we started using kueue around the 0.8 release, and hadn't noticed that feature). I think that is probably the cause of our problems. Before the podSelector changes in the webhook with 0.15.0 this feature likely did nothing as we had a selector in the manager config to only manage Pods with the `kueue.x-k8s.io/queue-name` label.

It will be hard to change the queue name, as there are quite a few jobs spread out over our clusters with that label by now.

The podSelector in https://github.com/kubernetes-sigs/kueue/blob/87fcef57ae07172094466826017145043dbb38c2/pkg/controller/jobs/pod/pod_webhook.go#L124 would have disabled the webhook for pods without the label in 0.14, but in 0.15 that value is no longer set from the new configuration.

Thank you for the quick response, I think we will keep the webhook objectSelectors enabled for now as that should grant a minor performance benefit as well.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T12:23:42Z

Ok, but I think your selectors aren't compatible with the LocalQueueDefaulting feature, because they will make the Mutating webhooks , which add the "queue-name" skip. Fair for short term if you don't want to rely on it now, but such hacks may backfire in the future.

So, I'm wondering the cleanest way would be to follow the separation by namespace.  

FYI: The podSelector was deprecated and dropped. The reason for this was that it made it really tricky to reason about management in the context of StatefulSets / Deployments. For example, a user could opt-in for StatefulSet management, but opt-out for the child Pods - this was very problematic semantically. Thus, we decided to take the simpler model of management by namespace going forward.
