# Issue #6584: kueueviz-backend cannot query the cluster api

**Summary**: kueueviz-backend cannot query the cluster api

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6584

**Last updated**: 2025-08-20T13:15:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@upworkangelos](https://github.com/upworkangelos)
- **Created**: 2025-08-14T17:19:06Z
- **Updated**: 2025-08-20T13:15:11Z
- **Closed**: 2025-08-20T13:15:11Z
- **Labels**: `kind/bug`, `triage/needs-information`
- **Assignees**: _none_
- **Comments**: 16

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

kueueviz-backend gets 403 from kubernetes api

This is the frontend's complaint
{
  "isTrusted": true,
  "type": "error",
  "target": {},
  "srcElement": {},
  "currentTarget": {
    "url": "wss://kueueviz-backend-mli-staging-canary-01.staging.platform.ml.usw2.upwork/ws/local-queues"
  },
  "eventPhase": 2,
  "bubbles": false,
  "cancelable": false,
  "returnValue": true,
  "defaultPrevented": false,
  "composed": false,
  "timeStamp": 1132870,
  "cancelBubble": false,
}

The backend gets a 403 from the API

**What you expected to happen**:

It should retrieve kueue related data

**How to reproduce it (as minimally and precisely as possible)**:

hmm , We are working on a tight security cluster, so check the serviceaccount

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.31.10
- Kueue version (use `git describe --tags --dirty --always`): 0.13.1
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools: argocd
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T18:10:27Z

cc @kannon92 @akram

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-14T18:14:31Z

Maybe you are running into auth issues.

You are not really giving us a lot of information to triage this.

/triage needs-information

### Comment by [@upworkangelos](https://github.com/upworkangelos) — 2025-08-14T18:34:41Z

This is because I do not have more information the backend pod does not provide logs why it gets 403
case and point
[GIN] 2025/08/14 - 18:14:33 | 403 |       6.045µs |    100.64.55.50 | GET      "/ws/workloads/dashboard?namespace="
[GIN] 2025/08/14 - 18:15:28 | 403 |      27.748µs |    100.64.55.50 | GET      "/ws/namespaces"
[GIN] 2025/08/14 - 18:15:28 | 403 |       7.478µs |    100.64.55.50 | GET      "/ws/workloads/dashboard?namespace="

occasionally I would a log line saying something like 172.20.0.1/apis returned 403

the deployment does not specify an explicit serviceAccount and that causes issues with some setups. 
I hand edited the deploymend and added the "default" serviceaccount to the backend container but kueueviz gave the same results.

I got mad and grabbed the user token for the "default" serviceAccount fired up a debug container on the kueueviz-backend pod and did the curl work manually.

```
           
[network-tools]$ vi token  
[network-tools]$ TOKEN=$(cat token)
[network-tools]$ curl -k --header "Authorization: Bearer ${TOKEN}" -X GET https://172.20.0.1/api
{
 "kind": "APIVersions",
 "versions": [
   "v1"
 ],
 "serverAddressByClientCIDRs": [
   

Unknown macro: {      "clientCIDR"}

 ]
}

[network-tools]$ curl -k --header "Authorization: Bearer ${TOKEN}" https://172.20.0.1:443/apis/kueue.x-k8s.io/v1beta1/workloads
{
 "apiVersion": "kueue.x-k8s.io/v1beta1",
 "items": [],
 "kind": "WorkloadList",
 "metadata":

Unknown macro: {    "continue"}

}

```

Hope this is enough

### Comment by [@upworkangelos](https://github.com/upworkangelos) — 2025-08-14T18:36:14Z

Since I am on this topic
I am using envoy-gateway with httproutes

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-14T18:41:09Z

Yea I think this may be more of a feature rather than a bug.

Right now I think we assume default service account for kueueviz. 

Our auth stance for kueue viz is not great atm.

### Comment by [@upworkangelos](https://github.com/upworkangelos) — 2025-08-14T18:48:13Z

 I may have found the issue. 
the user token in our setup is located at /run/secrets/kubernetes.io/serviceaccount/token
not /var/run/...

### Comment by [@upworkangelos](https://github.com/upworkangelos) — 2025-08-14T18:52:33Z

One more thing: the cert manager was bombing out with an error about: empty issued DN. So I had to route via our external facing envoy gateway. Does the backend do some kind of checking for certificates and such 
?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-14T19:24:27Z

I don’t think Kueueviz backend looks at certificates

### Comment by [@yankay](https://github.com/yankay) — 2025-08-18T09:37:36Z

I've reproduced this issue, and it seems related to kueueviz's [cros](https://github.com/kubernetes-sigs/kueue/blob/main/cmd/kueueviz/backend/middleware/cors.go)

### Comment by [@upworkangelos](https://github.com/upworkangelos) — 2025-08-18T09:43:06Z

Great News! 
Now if you could only make the ingress enabling configurable ;-)

### Comment by [@yankay](https://github.com/yankay) — 2025-08-18T10:38:00Z

> Great News! Now if you could only make the ingress enabling configurable ;-)

Before merging the fix PR, you can set KUEUEVIZ_ALLOWED_ORIGINS to the URL used by the browser, such as http://xxxx, and that will be sufficient.

### Comment by [@upworkangelos](https://github.com/upworkangelos) — 2025-08-18T11:02:43Z

test with a star

2025/08/18 11:01:32 Warning: Invalid origin '*' rejected
2025/08/18 11:01:32 Running in development mode
panic: conflict settings: all origins disabled

### Comment by [@upworkangelos](https://github.com/upworkangelos) — 2025-08-18T11:05:56Z

with an fqdn
2025/08/18 11:04:35 Warning: Invalid origin 'wss://kueueviz-backend-redacted' rejected

### Comment by [@yankay](https://github.com/yankay) — 2025-08-18T11:08:06Z

> test with a star
> 
> 2025/08/18 11:01:32 Warning: Invalid origin '*' rejected 2025/08/18 11:01:32 Running in development mode panic: conflict settings: all origins disabled

Using this command can work.
```
KUEUEVIZ_PORT=8081 KUEUEVIZ_ALLOWED_ORIGINS=http://10.64.26.1 ./bin/kueueviz
```
`wss://kueueviz-backend-` and  `*` can not work because of the function https://github.com/kubernetes-sigs/kueue/blob/main/cmd/kueueviz/backend/middleware/cors.go#L33

### Comment by [@upworkangelos](https://github.com/upworkangelos) — 2025-08-18T11:12:57Z

@yankay thanks for the effort but I am working in a very structured and strict environment , so quick hacks are really not possible to go into production. 

Even adding manually the KUEUEVIZ_ALLOWED_ORIGINS env var is considered a breaking change.

Is there a way to simply tell the backend to allow everything and let our systems do the security checks ?

### Comment by [@yankay](https://github.com/yankay) — 2025-08-18T11:25:52Z

> [@yankay](https://github.com/yankay) thanks for the effort but I am working in a very structured and strict environment , so quick hacks are really not possible to go into production.
> 
> Even adding manually the KUEUEVIZ_ALLOWED_ORIGINS env var is considered a breaking change.
> 
> Is there a way to simply tell the backend to allow everything and let our systems do the security checks ?

Sorry, I can't think of a way to solve the problem without modifying the environment variables either.
