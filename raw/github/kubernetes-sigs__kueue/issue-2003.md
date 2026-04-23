# Issue #2003: Enhance integration manager to enable external controllers to provide Kueue integrations

**Summary**: Enhance integration manager to enable external controllers to provide Kueue integrations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2003

**Last updated**: 2024-04-26T17:30:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-04-17T22:04:49Z
- **Updated**: 2024-04-26T17:30:42Z
- **Closed**: 2024-04-26T17:30:42Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We need a mechanism to enable Kueue's `jobframework.integrationManager` to recognize GVKs that are being managed by an instantiation of `jobframework.ReconcilerFactory` that is defined/running in an external controller.  In particular, methods like `jobframework.IsOwnerManagedByKueue` and `GetEmptyOwnerObject` should be extended to consult an additional table of GVKs that are known to be Kueue enabled.   This table would be populated from information added to the Integrations sub-structure of Kueue's Configuration Resource. 

**Why is this needed**:
Being able to cleanly extend Kueue with the ability to manage additional GVKs without needing to modify Kueue itself would make it easier to grow the Kueue ecosystem.

In the AppWrapper project (https://github.com/project-codeflare/appwrapper), we have a working example of such an external controller that extends Kueue to manage a new GVK.  As described in more detail in the [Working Group call of 4/11](https://www.youtube.com/watch?v=u8HpxpC25mU&list=PL69nYSiGNLP1U1eU1NPyflIGmwzcXPsev&index=1) and this [presentation](https://docs.google.com/presentation/d/1RFVv6PY_q5gQTbuTzoLznt2fK-Z2V9cz8qpfG3fhrjY/edit#slide=id.g2cb4625333a_1_149) the inability to inform the integrationManager of the new Kueue managed type results in a failure to correctly recognize child jobs, which then requires a fragile workaround (our child admission controller).

**Completion requirements**:

With this enhancement, when an AppWrapper containing another Kueue-managed GVK (for example a PyTorch Job) is admitted by Kueue, the wrapped PyTorch Job should be properly recognized by Kueue as a child job of an already admitted Job and be admitted.  To test, we would disable our child admission controller in the AppWrapper operator and verify that the child was admitted as expected.  

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-04-17T22:09:38Z

I intend to work on an implementation once there is agreement on a design.  I think an extension to the Configuration.Integrations to add a new array of strings listing externally-managed GVKs should work, but I'm happy to do something else if there is a preferred alternative.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-18T17:07:38Z

/cc @alculquicondor @tenzen-y

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-18T17:52:06Z

I think I would add a field parallel to this https://github.com/kubernetes-sigs/kueue/blob/472ce6d2c6bbfab2903db065dbb8f117415bc8d5/apis/config/v1beta1/configuration_types.go#L301

`externalFrameworks`?

Another option could be to just add all the frameworks into the same `frameworks` list, and have kueue identify which frameworks are built in. But then it wouldn't be possible for users to "override" a built-in framework, if they have such need.
