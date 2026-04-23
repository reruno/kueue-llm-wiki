# Issue #4534: TAS: expose the TopologyName in LocalQueue status

**Summary**: TAS: expose the TopologyName in LocalQueue status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4534

**Last updated**: 2025-03-13T06:57:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-10T09:08:24Z
- **Updated**: 2025-03-13T06:57:48Z
- **Closed**: 2025-03-13T06:57:48Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 8

## Description

**What would you like to be added**:

Expose the TopologyName information in the LocalQueue status along with other ResourceFlavor fields.

**Why is this needed**:

To let users know if the target LQ and CQ are using TAS. 
Note that other RF information (like taints or labels) is also already exposed this was under https://github.com/kubernetes-sigs/kueue/issues/3122

I opened a dedicated issue as this is on intersection of TAS and Expose Flavors in LocalQueue Status

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T09:08:31Z

cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T10:16:06Z

cc @KPostOffice @mbobrovskyi as co-authors of https://github.com/kubernetes-sigs/kueue/issues/3122

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-10T10:59:26Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-10T13:50:32Z

What about topology levels? how can batch users know which level can be specified as a `required` and `prefered` labels?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T13:54:14Z

Yeah, knowing Topology levels will be quite useful for setting the annotations by users. So we could have either two new fields TopologyName and topologyLevels or a structure Topology which encapsulates the name and levels. I'm fine either way but leaning to the second option as also more flexible in the future.

WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-10T14:37:21Z

> Yeah, knowing Topology levels will be quite useful for setting the annotations by users. So we could have either two new fields TopologyName and topologyLevels or a structure Topology which encapsulates the name and levels. I'm fine either way but leaning to the second option as also more flexible in the future.
> 
> WDYT?

I also thought the second option. My only question is, is there any risk to exposing detailed topology level to batch users, like overusing the information and occupying the quota by single batch users?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T15:13:42Z

I don't think the information about the list of levels can be leveraged in any malicious way. Even when using TAS quota checks are still respected.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-10T23:30:46Z

> I don't think the information about the list of levels can be leveraged in any malicious way. Even when using TAS quota checks are still respected.

That sounds reasonable. SGTM
