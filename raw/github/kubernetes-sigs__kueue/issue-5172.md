# Issue #5172: [Documentation] Describe the two-step admission cycle with ProvisioningRequest

**Summary**: [Documentation] Describe the two-step admission cycle with ProvisioningRequest

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5172

**Last updated**: 2025-06-18T17:59:57Z

---

## Metadata

- **State**: open
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-05-06T13:24:33Z
- **Updated**: 2025-06-18T17:59:57Z
- **Closed**: —
- **Labels**: `good first issue`, `help wanted`, `kind/documentation`
- **Assignees**: [@JasminPradhan](https://github.com/JasminPradhan)
- **Comments**: 10

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Relying on those KEPs:
- [Two-step admission](https://github.com/kubernetes-sigs/kueue/tree/main/keps/993-two-phase-admission)
- [ProvisioningRequest support](https://github.com/kubernetes-sigs/kueue/tree/main/keps/1136-provisioning-request-support)
extend existing documentation with the description and a diagram of admission cycle including ProvisionigRequest happpy path and retries

**Why is this needed**:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-06T13:26:04Z

/kind documentation
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-06T13:26:07Z

@PBundyra: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5172):

>/kind documentation
>/good-first-issue
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T15:09:05Z

/remove-kind cleanup

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-06-04T17:53:54Z

Hi @PBundyra @tenzen-y  ! I’m new to open source and would love to work on this issue. I have been reading the KEPs, but I’d appreciate some guidance to work on this:

Is there a specific section or file where you’d like the documentation added?
Is there any style or format to be followed for the diagram?
Is this the documentation - https://kueue.sigs.k8s.io/docs/  where the changes are to be reflected?  Or we are to make changes in the  above mentioned markdown files?
Thanks in advance for your help!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T11:34:32Z

@JasminPradhan Hello. Thank you for interesting this issue.
We intended to refine the ProvReq state transition diagram with RetryStrategy: https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/troubleshooting_provreq/#what-is-the-current-state-of-my-provisioning-request

The diagram is stored in https://github.com/kubernetes-sigs/kueue/blob/main/site/static/images/prov-req-states.svg

@PBundyra Do you have any thoughts?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-12T10:42:15Z

Hi @JasminPradhan, thanks for reaching out!

> Is there a specific section or file where you’d like the documentation added?
Is there any style or format to be followed for the diagram?
Is this the documentation - https://kueue.sigs.k8s.io/docs/ where the changes are to be reflected? Or we are to make changes in the above mentioned markdown files?

I was considering extending `Admission` section [here](https://kueue.sigs.k8s.io/docs/concepts/#admission). You can do so be editing [this file](https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/concepts/_index.md).

As for the style, there are some k8s documentation guides but I'd say we follow them rather loosely in Kueue documentation. Maybe @tenzen-y will have some more thoughts about it.

In the first iteration I would focus only on describing the two-step admission with an example of Provisioning AdmissionCheck. 

Later on  it would be super beneficial to describe admission cycle with [TAS](https://github.com/kubernetes-sigs/kueue/blob/main/keps/2724-topology-aware-scheduling/README.md#support-for-provisioningrequests)

cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-12T11:32:03Z

> I was considering extending Admission section [here](https://kueue.sigs.k8s.io/docs/concepts/#admission). You can do so be editing [this file](https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/concepts/_index.md).

Makes sense, we are missing for sure a note about the 2-phase admission cycle in the concepts page 

I think we also need some more hands on tutorial with examples on setting up CQ with ProvReq in https://kueue.sigs.k8s.io/docs/tasks/manage/, but this could be another follow up (possibly another issue).

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-06-16T12:18:42Z

Thank you so much for the detailed guidance, @PBundyra , @tenzen-y , and @mimowo !

I’ll begin by extending the Admission section in the concepts page, describing the two-step admission as suggested. I'll make the edits to the linked file accordingly.

Also noted the suggestion about describing the admission cycle with TAS — I’ll keep that in mind for a follow-up iteration.
And yes, a tutorial with examples on setting up CQ with ProvReq sounds like a great enhancement too — happy to work on that in a follow-up PR if that’s helpful.

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-06-17T20:02:50Z

/assign

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-06-18T17:59:57Z

Hi @mimowo @tenzen-y @PBundyra ! Based on our earlier discussions, I’ve added the updates to the Admission section as suggested. I have also fixed a few broken links in the page as part of this PR. Feedback on correctness  is very welcome. Thank you for reviewing!
