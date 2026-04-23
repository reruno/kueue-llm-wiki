# Issue #1647: Website does not have the correct trademark disclaimer

**Summary**: Website does not have the correct trademark disclaimer

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1647

**Last updated**: 2024-06-05T09:30:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@thisisobate](https://github.com/thisisobate)
- **Created**: 2024-01-25T20:53:44Z
- **Updated**: 2024-06-05T09:30:59Z
- **Closed**: 2024-06-05T09:30:59Z
- **Labels**: `good first issue`, `help wanted`, `kind/documentation`
- **Assignees**: [@mariasalcedo](https://github.com/mariasalcedo)
- **Comments**: 10

## Description

As part of our ongoing effort to https://github.com/cncf/techdocs/issues/198, we noticed that the website does not pass the trademark criteria on [CLOMonitor](https://clomonitor.io/search?foundation=cncf&not_passing_check=trademark_disclaimer&page=1).

To fix this:
Head to the source code of the website. In the `<footer>` section, add a **disclaimer** or **link** to the Linux foundation trademark disclaimer page:

**Disclaimer**
```
<footer>
   <p>The Linux Foundation has registered trademarks and uses trademarks. For a list of trademarks of The Linux Foundation, 
         please see our <a href="https://www.linuxfoundation.org/legal/trademark-usage">Trademark Usage page</a>.
   </p>
</footer>
```

**Link**
```
 <footer>
      <ul>
          <li><a href="https://www.linuxfoundation.org/legal/trademark-usage">Trademarks</a></li>
      </ul>
 </footer>
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T20:26:51Z

/kind documentation

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-25T21:17:45Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-26T11:18:28Z

/remove-lifecycle stale
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-26T11:18:30Z

@tenzen-y: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1647):

>/remove-lifecycle stale
>/good-first-issue
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@omerap12](https://github.com/omerap12) — 2024-05-01T18:39:44Z

Ill take it
/assign

### Comment by [@mariasalcedo](https://github.com/mariasalcedo) — 2024-06-04T11:42:28Z

Hi @omerap12 , are you still working on this? If not, I am interested to take it over.

### Comment by [@omerap12](https://github.com/omerap12) — 2024-06-04T11:52:52Z

Hey, sure you can take it :) @mariasalcedo

### Comment by [@mariasalcedo](https://github.com/mariasalcedo) — 2024-06-04T12:05:57Z

/assign

### Comment by [@mariasalcedo](https://github.com/mariasalcedo) — 2024-06-04T12:06:32Z

@omerap12 thanks!

### Comment by [@mariasalcedo](https://github.com/mariasalcedo) — 2024-06-04T12:47:45Z

@thisisobate I've just sent a PR on this! 
This is my first ever contribution, so I look forward for your feedback, though there isn't much probably to be said.
