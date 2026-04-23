# Issue #4942: Promote the LocalQueueDefaulting feature to Beta in 0.12

**Summary**: Promote the LocalQueueDefaulting feature to Beta in 0.12

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4942

**Last updated**: 2025-05-06T18:25:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2025-04-11T20:15:04Z
- **Updated**: 2025-05-06T18:25:18Z
- **Closed**: 2025-05-06T18:25:18Z
- **Labels**: `kind/feature`
- **Assignees**: [@dgrove-oss](https://github.com/dgrove-oss), [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

The LocalQueueDefaulting feature was introduced at the Alpha level in 0.10.  
I would like to promote to Beta and enable by default in 0.12.

**Why is this needed**:

Promoting to Beta and enabling by default is the best way to get user feedback on the feature.

The feature provides a simpler and potentially less surprising mechanism than 
`manageJobsWithoutQueueName` for allowing batch admins to enable quota enforcement in
selected user-namespaces.  As such, I expect there would be user demand for the feature.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-04-11T20:17:17Z

I think this should be fairly straightforward to enable.

If we agree this should be done, I think I can find time to make the code changes before a 0.12 release in mid-May.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-14T05:10:34Z

Awesome. We need some e2e tests. cc @tenzen-y @mbobrovskyi

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T05:57:28Z

SGTM

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-04-14T17:31:38Z

/assign

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-04-14T20:24:41Z

Hello @dgrove-oss, do you mind if I contribute to this issue?
Thanks in advance.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-04-14T20:28:55Z

Hi @MaysaMacedo that would be great; I will assign to you.  Happy to answer questions if you have any along the way.
/assign @MaysaMacedo

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-18T00:44:38Z

As we enable this for beta which I assume means feature gate on, I think we should consider a configuration for this. I think as we promote this to beta, we will probably need a configuration to opt in or opt out of this feature.

The configuration could be a simple configuration for LocalQueueDefault and if it’s empty, then we assume feature is disabled. If it’s specified then we can assume localQueueDefaulting is set.

I also think we can maybe validate that LocalQueurDefsulting and ManagedJobWithoitQueueName cannot both be set.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-04-18T13:32:25Z

> As we enable this for beta which I assume means feature gate on, I think we should consider a configuration for this. I think as we promote this to beta, we will probably need a configuration to opt in or opt out of this feature.
> 

I'm not convinced we need this.  A batch-admin opts into LocalQueueDefaulting on a namespace-by-namespace basis by creating a local queue named `default` in a namespace.  We need to document this clearly and highlight in the release note, but I don't see the need for adding an operator-level config.

> I also think we can maybe validate that LocalQueurDefsulting and ManagedJobWithoitQueueName cannot both be set.

These can interoperate just fine.  If a namespace has a localqueue named `default` then LocalQueueDefaulting kicks in.  If a namespace doesn't have such a local queue then `ManangeJobsWithoutQueueName` can come into play (if the ManagedJobsNamespaceSelector matches).  It's a bit of an odd configuration choice, but it is not invalid.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-22T15:05:52Z

I see @dgrove-oss. Yea I think documentation may be sufficient here.
