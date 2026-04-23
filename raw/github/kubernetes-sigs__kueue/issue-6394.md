# Issue #6394: Restructure documentation for Admission and AdmissionChecks

**Summary**: Restructure documentation for Admission and AdmissionChecks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6394

**Last updated**: 2025-09-17T11:11:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-04T06:40:40Z
- **Updated**: 2025-09-17T11:11:30Z
- **Closed**: 2025-09-17T11:11:30Z
- **Labels**: `kind/documentation`
- **Assignees**: [@JasminPradhan](https://github.com/JasminPradhan)
- **Comments**: 16

## Description

This is a follow up to https://github.com/kubernetes-sigs/kueue/pull/5677

Currently the Admission page contains a section about the Provisioning AdmissionCheck: https://kueue.sigs.k8s.io/docs/concepts/admission/#provisioning-admissioncheck

This is a different approach than for MultiKueue admission check: https://kueue.sigs.k8s.io/docs/concepts/multikueue/

So, I'm considering we could:
- Extract the section on ProvReq to a dedicated page
- Move both pages (for ProvReq and MultiKueue) as subpages to Admission Check

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T06:40:52Z

cc @JasminPradhan @PBundyra @tenzen-y

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-08-04T14:26:12Z

/assign

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-08-04T21:03:30Z

Hi @mimowo ! Should I add this [ProvReq section](https://kueue.sigs.k8s.io/docs/concepts/admission/#provisioning-admissioncheck) to [this](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/) page? 
Just want to make sure I'm updating the right place. Thanks!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-05T08:14:42Z

My main intention was to document "Provisioning Request" and "MultiKueue" in the same way. 

So, I was thinking about moving the section as a subpage to the "Admission Check" page, along with MultiKueue:

```
Admiossion Check: 
- Provisioning Request
- MultiKueue
```
Alternatively, just make them all as top-level pages:
```
Admission Check
Provisioning Request
MultiKueue
```
@tenzen-y @PBundyra do you have any preferences?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-05T08:33:46Z

What do you think about making `AdmissionCheck` subpage of `Concepts`, and then making ProvReq and MultiKueue subpages of AdmissionChecks

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-05T08:56:19Z

> What do you think about making AdmissionCheck subpage of Concepts, and then making ProvReq and MultiKueue subpages of AdmissionChecks

yes, that  was my proposal actually. I implicitly assumed we keep "Admission Checks" as a subpage to "Concepts" as currently, so to be more precise:
```
Concepts:
- Admiossion Check: 
  - Provisioning Request
  - MultiKueue
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-05T12:20:20Z

I'm wondering if we should have both in the following:

```
Concepts:
- Admission
- MultiKueue
- Admission Check: 
  - Provisioning Request
  - MultiKueue
```

In the Concepts.MultiKueue, I would describe MultiKueue functionality the same as today, which means no change.
In the Concepts.Admission Check.MultiKueue, I would describe how that works alongside our Admission Check mechanism.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-05T12:35:29Z

sgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-05T12:41:42Z

/kind documentation

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T11:46:52Z

And I think we could move the contents of https://kueue.sigs.k8s.io/docs/admission-check-controllers/  into the new place. We don't need "Admission Check controller" at the top-level IMO.

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-08-08T05:21:39Z

> And I think we could move the contents of https://kueue.sigs.k8s.io/docs/admission-check-controllers/ into the new place. We don't need "Admission Check controller" at the top-level IMO.

How about structuring it like this?
```
Concepts:
- Admission
  - MultiKueue
  - ProvisioningRequest
    - Provisioning Admission Check Controller
  - (.. so on)
 ```

By doing this, we can remove the Admission Check Controller section from the top-level without affecting the Provisioning Admission Check Controller. MultiKueue Admission Mechanism can be added later, under MultiKueue. 

This way, each admission mechanism will have its own concepts organized under its respective section, reducing confusion.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T06:09:53Z

This is a possible alternative, but I think the plan from https://github.com/kubernetes-sigs/kueue/issues/6394#issuecomment-3154988643 is already good, too.

```
Concepts:
- Admission
- MultiKueue
- Admission Check: 
  - Provisioning Request
  - MultiKueue
```

I think "Provisioning Admission Check Controller" should be merged with `Concepts.Admission.ProvisioningRequest`. I don't think a "Controller" deserves a page on its own as this is an implementation detail from the user perspective.

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-08-08T07:49:49Z

Okay, got it!

### Comment by [@JasminPradhan](https://github.com/JasminPradhan) — 2025-08-12T07:31:45Z

Hey! I have opened the PR addressing this issue #6553. Please have a look.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T11:11:25Z

/close 
addressed in https://github.com/kubernetes-sigs/kueue/pull/6553

Thank you 👍

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-17T11:11:30Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6394#issuecomment-3302499329):

>/close 
>addressed in https://github.com/kubernetes-sigs/kueue/pull/6553
>
>Thank you 👍 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
