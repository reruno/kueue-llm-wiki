# Issue #555: Provide client-go libraries

**Summary**: Provide client-go libraries

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/555

**Last updated**: 2023-06-16T15:12:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-02-06T16:51:40Z
- **Updated**: 2023-06-16T15:12:23Z
- **Closed**: 2023-06-16T15:12:23Z
- **Labels**: `kind/feature`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Auto-generate and provide the client-go codes.

**Why is this needed**:
It is useful for the CustomJob operator of implementation based on client-go (e.g., MPIJob).

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-02-06T16:51:59Z

@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-06T16:56:09Z

yes, it's useful, but let's wait after #532

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-02-06T16:57:42Z

> yes, it's useful, but let's wait after #532

I agree.

### Comment by [@maaft](https://github.com/maaft) — 2023-02-07T08:15:26Z

In the meantime, are there any examples on how to query/create queues and jobs via `client-go`? 

I want to provide a "simple" frontend GraphQL API for my cluster-users to start and stop jobs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-02-07T08:34:13Z

> In the meantime, are there any examples on how to query/create queues and jobs via `client-go`?
> 
> I want to provide a "simple" frontend GraphQL API for my cluster-users to start and stop jobs.

Maybe, you can use a client of controller-runtime.

### Comment by [@maaft](https://github.com/maaft) — 2023-02-07T09:23:56Z

Could you please elaborate a bit on required steps or provide links? That would be greatly appreciated!

I'm fairly new to writing controllers / interacting with k8s through non-kubectl ways.

**Edit**: Got it working. For anyone wondering, here's how you would list all workloads:
```golang

import (
	"context"
	"flag"
	"fmt"
	"path/filepath"

	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
	"sigs.k8s.io/controller-runtime/pkg/client"
	kueue "sigs.k8s.io/kueue/apis/kueue/v1alpha2"
)

func main() {
	var kubeconfig *string
	if home := homedir.HomeDir(); home != "" {
		kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "(optional) absolute path to the kubeconfig file")
	} else {
		kubeconfig = flag.String("kubeconfig", "", "absolute path to the kubeconfig file")
	}
	flag.Parse()

	// use the current context in kubeconfig
	config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
	if err != nil {
		panic(err.Error())
	}

	scheme := runtime.NewScheme()

	err = kueue.SchemeBuilder.AddToScheme(scheme)

	if err != nil {
		panic(err.Error())
	}

	cclient, err := client.New(config, client.Options{
		Scheme: scheme,
	})

	if err != nil {
		panic(err.Error())
	}

	workloads := &kueue.WorkloadList{}

	err = cclient.List(context.TODO(), workloads)

	if err != nil {
		panic(err.Error())
	}

	for _, w := range workloads.Items {
		fmt.Println(w)
	}

}
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-07T13:35:48Z

The documentation for controller runtime can be found here: https://book.kubebuilder.io/cronjob-tutorial/controller-implementation.html

Although you seem to be in the right path already. You can simplify to:

```golang
err = kueue.AddToScheme(scheme)
```

If you have some time, it would be greatly useful to have instructions in this folder https://github.com/kubernetes-sigs/kueue/tree/main/docs/tasks

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-05-08T13:55:02Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-08T13:55:58Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-08T15:14:05Z

/help

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-21T12:24:49Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-21T15:01:28Z

/help cancel

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-21T15:02:30Z

/remove-help
