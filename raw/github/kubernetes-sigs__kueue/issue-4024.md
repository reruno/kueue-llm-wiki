# Issue #4024: Add AppWrapper to the lists of integrations consistently

**Summary**: Add AppWrapper to the lists of integrations consistently

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4024

**Last updated**: 2025-01-21T13:56:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-21T07:44:10Z
- **Updated**: 2025-01-21T13:56:39Z
- **Closed**: 2025-01-21T13:56:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

 Add AppWrapper to the commented out lists of integrations, in places:
- https://github.com/kubernetes-sigs/kueue/blob/74dd940fdf264f44b2680a4b1bb508a278c98a9b/config/components/manager/controller_manager_config.yaml#L44-L59
- https://github.com/kubernetes-sigs/kueue/blob/74dd940fdf264f44b2680a4b1bb508a278c98a9b/apis/config/v1beta1/configuration_types.go#L322-L336

Potentially more, but these I found with quick search.

**Why is this needed**:

For discoverability by users and consistency in code.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-21T07:45:04Z

Ah, I missed it is already in the first link uncommented. That's ok. In this case only the second place.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-21T07:46:31Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-21T07:49:25Z

Ah, it is not enabled by default in here: https://github.com/kubernetes-sigs/kueue/blob/74dd940fdf264f44b2680a4b1bb508a278c98a9b/charts/kueue/values.yaml#L101-L114 which creates an inconsistency. cc @dgrove-oss 

EDIT: Seeing that the integration is enabled in the main manager config I will tentatively also enable it for the helm config. 
The [PR](https://github.com/kubernetes-sigs/kueue/pull/4026)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-21T08:46:13Z

@dgrove-oss actually we usually prefix the integrations with the API group name, which in case of AppWrapper would be `workload.codeflare.dev` rather than `codeflare.dev` (looking at https://github.com/project-codeflare/appwrapper/blob/3de3fa7808e3055c562a2ba6fbdfde287f0ab1d1/config/crd/bases/workload.codeflare.dev_appwrappers.yaml#L9C10-L9C32). 

I don't have a strong view here, and it will work either way, but I would be leaning slightly towards more consistency. 

Also, IIUC it would make the deployment easier in the transition period as you could drop this point:

```
Because AppWrappers were initially designed as an external framework for Kueue, you need to install the Standalone 
configuration of the AppWrapper controller. This disables the AppWrapper controller’s instance of Kueue’s GenericJob 
Reconciller. One way to do this is by doing
```
from https://kueue.sigs.k8s.io/docs/tasks/run/appwrappers/. WDYT?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-21T13:04:36Z

I'm a big fan of consistency.  Let's use  `workload.codeflare.dev` and enable it by default in both the config and the helm chart..
