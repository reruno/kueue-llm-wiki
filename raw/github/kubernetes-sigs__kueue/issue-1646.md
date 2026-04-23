# Issue #1646: GitHub repository does not link to the project website url

**Summary**: GitHub repository does not link to the project website url

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1646

**Last updated**: 2024-01-26T20:25:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@thisisobate](https://github.com/thisisobate)
- **Created**: 2024-01-25T20:52:44Z
- **Updated**: 2024-01-26T20:25:56Z
- **Closed**: 2024-01-26T20:25:54Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 2

## Description

As part of our ongoing effort to [ensure all the websites within the CNCF meet the CLOMonitor guidelines](https://github.com/cncf/techdocs/issues/196), we noticed that Kueue does not pass the website criteria on [CLOMonitor](https://clomonitor.io/search?not_passing_check=website&foundation=cncf&page=1). 

To fix this:
Edit [kubernetes-sigs/kueue](https://github.com/kubernetes-sigs/kueue) repository details. See Notary for example: 
<img width="1704" alt="Screenshot 2023-11-22 at 09 29 19" src="https://github.com/notaryproject/notary/assets/29557702/0b9dd1e3-f32b-42c6-adfc-a860ebad347b">

In the website section, add the link to the Kueue website (https://kueue.sigs.k8s.io/). See Notary for example:
<img width="1704" alt="Screenshot 2023-11-22 at 09 30 15" src="https://github.com/notaryproject/notary/assets/29557702/c883c1c3-f9d7-4fcc-ae3c-fadf402d43cd">


Once done, feel free to close this issue as CLOMonitor will recrawl the page and update accordingly.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T20:25:51Z

Done.
cc: @alculquicondor 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-26T20:25:55Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1646#issuecomment-1912652546):

>Done.
>cc: @alculquicondor 
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
