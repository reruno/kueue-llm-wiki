# Issue #7421: Add an agents file to Kueue to better enable AI assistants

**Summary**: Add an agents file to Kueue to better enable AI assistants

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7421

**Last updated**: 2026-05-11T14:04:05Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-10-28T18:07:00Z
- **Updated**: 2026-05-11T14:04:05Z
- **Closed**: —
- **Labels**: `priority/important-longterm`, `area/agents`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 15

## Description

Following https://github.com/kubernetes/kubernetes/pull/133386,

It would be nice to have an Agents file that can aide in common Kueue development practices.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-28T19:21:58Z

I added https://github.com/kubernetes-sigs/kueue/pull/7422

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-29T06:29:06Z

I have no objections, but I would like to wait for https://github.com/kubernetes/kubernetes/pull/133386 completion.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-29T18:01:22Z

> I have no objections, but I would like to wait for [kubernetes/kubernetes#133386](https://github.com/kubernetes/kubernetes/pull/133386) completion.

Why should we wait for kubernetes PR to merge?

It sounds like the author has left it to go stale.

- https://github.com/kubernetes-sigs/cluster-api-provider-azure/pull/5899

I also am adding an agents file to JobSet.

https://github.com/kubernetes-sigs/cluster-api-provider-azure/pull/5899#issuecomment-3405930946

They at least highlight a few other repos in kubernetes that merged the agents directory. I don't think we need to wait for k/k PR to merge if we want this change.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:42:19Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:22Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:54Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@amy](https://github.com/amy) — 2026-04-23T16:50:59Z

/assign 

I'd like to pick this up. Its currently annoying getting my agent to relearn simple things its already learned. High level... I think we need a top level AGENT.md file under like 200 lines. And then have it point out to children AGENT.md files for specific knowledge in other areas of the codebase.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-23T17:03:46Z

I created https://github.com/kubernetes-sigs/kueue/pull/7422 but I mostly just used Claude to generate it.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-23T17:07:18Z

> I'd like to pick this up. Its currently annoying getting my agent to relearn simple things its already learned. High level... I think we need a top level AGENT.md file under like 200 lines. And then have it point out to children AGENT.md files for specific knowledge in other areas of the codebase.

Yes, I want an agant to be skillful in flake debugging, started something effort on this here: https://github.com/mimowo/kueue/blob/agent-skill/agents/stills/flake-debugger/SKILL.md wdyt?

### Comment by [@amy](https://github.com/amy) — 2026-04-23T17:50:45Z

@mimowo btw is this path on purpose: `agents/stills/flake-debugger/SKILL.md`? 
Should it be stills -> skills

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-23T17:54:44Z

nah, you are right, it was me just putting something quickly together and making typos on the way.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-24T12:00:54Z

/remove-lifecycle rotten
We have the PR here: https://github.com/kubernetes-sigs/kueue/pull/10744 with a slightly different approach -using skills rather than just generic AGENTS.md

### Comment by [@amy](https://github.com/amy) — 2026-04-24T12:19:44Z

> We have the PR here: https://github.com/kubernetes-sigs/kueue/pull/10744 with a slightly different approach -using skills rather than just generic AGENTS.md

Yeah I think... we need both. Also we should think about using file hierarchy/table of contents a lot so that context sizes don't explode. Ex: let's say the list of skills becomes large, we can group different skills for agents to walk through different hierarchies of table of contents eventually. (No need to optimize now) We can also string skills together to dedupe prompting. So like to do Skill Z, look at skills A, B, C.

Agents.md I view as a landing page for agents. So we can have it point to ops, Kueue contribution productivity (ex how do you run different types of tests), code walkthroughs (point to deep wiki), etc.

Lots to think about. But yeah as these things grow... testing of these files for PRs is a concern to me.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-11T14:01:40Z

I think we can close this as we have implemented already a slightly different approach: minimal agents.md, and the more involving logic is moved into skills: https://github.com/kubernetes-sigs/kueue/pull/10744

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-11T14:04:02Z

/area agents
