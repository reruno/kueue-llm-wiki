# Issue #3850: More comprehensive securityContext settings in helm chart

**Summary**: More comprehensive securityContext settings in helm chart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3850

**Last updated**: 2025-01-15T13:30:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rptaylor](https://github.com/rptaylor)
- **Created**: 2024-12-13T23:29:47Z
- **Updated**: 2025-01-15T13:30:34Z
- **Closed**: 2025-01-15T13:30:34Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 13

## Description

In https://github.com/kubernetes-sigs/kueue/issues/874 ,  customizable securityContexts were added for the pod, and the manager container, but not the kube-rbac-proxy container.

Consequently it is not possible to make the kueue chart abide by Pod Security Standards and it can not be installed on a cluster that enforces them.
Rather than introducing more customizability for another container, it should just define the minimal securityContext that it requires. What does kube-rbac-proxy container do? Will it work with dropping all capabilities by default, RuntimeDefault seccompprofile, allowPrivilegeEscalation: false ?

I can make a PR but the security requirements needed for the application to run properly must be defined (e.g. by someone who knows the code base and what the application does).

## Discussion

### Comment by [@rptaylor](https://github.com/rptaylor) — 2024-12-13T23:35:09Z

It looks like this component will be removed: https://github.com/kubernetes-sigs/kueue/pull/3760

### Comment by [@kannon92](https://github.com/kannon92) — 2024-12-14T14:28:11Z

I think adding this would be useful.

@mbobrovskyi and @mimowo i don’t think the rbac proxy will go into 0.10 so should we implement some support for this?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-16T06:05:43Z

Actually, maybe I should prioritize that PR. I would prefer to invest effort into the container that is going away soon-ish

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-16T13:31:50Z

@rptaylor @kannon92 the change https://github.com/kubernetes-sigs/kueue/pull/3760 was a little bit too big to include for 0.10, but it solves the concern of the container long-term for 0.11. So I would suggest we close the issue. 

For the short-term work-around I think you could patch the Kueue deployment for 0.10 setting the appropriate security context - TBH I'm not sure what is the optimal setting here.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-12-16T13:44:08Z

Sounds good to me.

@rptaylor kueue does not manage the proxy image so we aren’t sure the impacts of the security settings. If you find out what works please feel free to add a doc update or update this thread with your findings.

### Comment by [@rptaylor](https://github.com/rptaylor) — 2024-12-16T19:07:24Z

Thanks for finishing that PR! Do you know when v0.11 will be released?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T09:07:38Z

Generally Kueue is aiming for releases every 2-3 months. So, the next we are planning for Feb 2025, but it might slip to March.

cc @mwysokin @mwielgus

### Comment by [@rptaylor](https://github.com/rptaylor) — 2024-12-17T19:56:58Z

Actually this also pertains to the manager container. If PSS is enforced on a cluster, these additional settings are required to install kueue, and can be set with .Values.controllerManager.manager.podSecurityContext and/or .Values.controllerManager.manager.containerSecurityContext thanks to https://github.com/kubernetes-sigs/kueue/pull/878/

```
          capabilities:
            drop:
            - ALL
          seccompProfile:
            type: RuntimeDefault
```

But if it can be confirmed that the manager container doesn't need any capabilities or special seccomp profile, wouldn't it be better to make kueue more secure by default and reduce the extra steps needed to use PSS?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T07:50:24Z

> But if it can be confirmed that the manager container doesn't need any capabilities or special seccomp profile

I would be surprised if kueue manager requires a special seccomp profile

> wouldn't it be better to make kueue more secure by default and reduce the extra steps needed to use PSS?

I'm open to the possibility, but can you explain more precisely what you mean?  What are the steps you want to reduce and how? changing the default? 

If this continues to work on kind, gke, openshift etc. ootb, and we keep it configurable for some more restrictive environments, then I'm good to try. cc @dgrove-oss

### Comment by [@rptaylor](https://github.com/rptaylor) — 2024-12-19T00:00:22Z

@mimowo Yes, if it is confirmed that kueue does not require any special capabilities or seccomp profile, then I would propose to drop all capabilities and set RuntimeDefault by default, as in https://github.com/kubernetes-sigs/kueue/issues/3850#issuecomment-2549484623

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-19T10:17:16Z

I see, I did a sanity check on GKE and it worked fine with the snippet proposed in https://github.com/kubernetes-sigs/kueue/issues/3850#issuecomment-2549484623.

So, I'm good to move forward with that, but we need to be careful about current installations, so maybe we should consider an opt-out configuration parameter in help, wdyt @tenzen-y ? @rptaylor do you see some risks, where would you be coming from? 

Feel free to post a PR.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-03T19:00:06Z

> So, I'm good to move forward with that, but we need to be careful about current installations, so maybe we should consider an opt-out configuration parameter in help, wdyt @tenzen-y ? @rptaylor do you see some risks, where would you be coming from?

I'm ok with setting those securityContexts by default in kustomize manifests and Helm chart.
IIUC, these securityContexts do not have any impact on the Kueue behavior, right?

### Comment by [@rptaylor](https://github.com/rptaylor) — 2025-01-03T20:46:53Z

> IIUC, these securityContexts do not have any impact on the Kueue behavior, right?

That is a question for kueue developers. Presumably kueue does not rely on any [capabilities](https://www.man7.org/linux/man-pages/man7/capabilities.7.html) ? Moreover, kueue already runs as NonRoot by default, and has allowPrivilegeEscalation false, so I believe it can not have any capabilities beyond the default granted by the container runtime. That being said, each container runtime may grant different default capabilities, so this results in inconsistent behaviour. For reproducible behaviour any required capabilities should be explicitly defined, and all others should be dropped.

As for the seccompProfile, as long as kueue doesn't do any syscalls to the kernel, this should also be fine.

Here is the PR: https://github.com/kubernetes-sigs/kueue/pull/3925
