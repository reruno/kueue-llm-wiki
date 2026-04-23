# Issue #5602: Increate the number of supported levels in Topology

**Summary**: Increate the number of supported levels in Topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5602

**Last updated**: 2025-06-24T13:22:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-10T12:12:28Z
- **Updated**: 2025-06-24T13:22:30Z
- **Closed**: 2025-06-24T13:22:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 5

## Description

**What would you like to be added**:

Increase the number of Topology levels beyond current max 8.

**Why is this needed**:

We have use-cases for having deep 8 or 9 levels topologies already. 

Having some 2x buffer would be helpful for possible future use-cases.

So, I would propose bumping to 16 levels.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T12:12:40Z

cc @mwysokin @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-10T12:33:37Z

> We have use-cases for having deep 8 or 9 levels topologies already.

Is this your customers demand? If yes, I'm fine with that.
If this is just an assumption, I probably want to keep parking with 8.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T12:35:52Z

> Is this your customers demand? If yes, I'm fine with that.

We already have some use-cases / projects requiring 8 or 9 levels.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-10T12:38:57Z

> > Is this your customers demand? If yes, I'm fine with that.
> 
> We already have some use-cases / projects requiring 8 or 9 levels.

SGTM

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-06-12T16:44:26Z

/assign
