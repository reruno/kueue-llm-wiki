# Issue #1849: verify job is taking >15 min

**Summary**: verify job is taking >15 min

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1849

**Last updated**: 2024-04-10T07:30:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-03-14T20:37:02Z
- **Updated**: 2024-04-10T07:30:00Z
- **Closed**: 2024-04-04T14:42:12Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Vandit1604](https://github.com/Vandit1604)
- **Comments**: 21

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Verify is taking too long

https://testgrid.k8s.io/sig-scheduling#pull-kueue-verify-main&width=20

Would increasing the number of CPUs help? Otherwise, what is being particularly slow?

**Why is this needed**:

This adds more time to the release process.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-14T20:37:31Z

@Vandit1604 is this something you would be interested in invesitgating?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T20:39:35Z

Helpful Dashboard: https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-integration-main&var-build=All&refresh=30s

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-15T12:17:50Z

@Vandit1604 please write `/assign` in a comment

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-15T15:31:07Z

/assign
I'll take a look at this

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-17T16:17:38Z

The delay is because of `shell-lint` rule. I updated it taking https://github.com/kubernetes/kubernetes/blob/0a31504ee114e363df9d69158c2e639858b8273b/hack/verify-shellcheck.sh as reference.

Here is the diff with the changes

```diff
diff --git a/hack/verify-shellcheck.sh b/hack/verify-shellcheck.sh
index c566f772..b4850dbf 100755
--- a/hack/verify-shellcheck.sh
+++ b/hack/verify-shellcheck.sh
@@ -17,11 +17,44 @@
 # allow overriding docker cli, which should work fine for this script
 DOCKER="${DOCKER:-docker}"
 
+
 SHELLCHECK_VERSION="0.9.0"
 SHELLCHECK_IMAGE="docker.io/koalaman/shellcheck-alpine:v0.9.0@sha256:e19ed93c22423970d56568e171b4512c9244fc75dd9114045016b4a0073ac4b7"
 
+# common arguments we'll pass to shellcheck
+SHELLCHECK_OPTIONS=(
+  # allow following sourced files that are not specified in the command,
+  # we need this because we specify one file at a time in order to trivially
+  # detect which files are failing
+  "--external-sources"
+  # include our disabled lints
+  "--exclude=${SHELLCHECK_DISABLED}"
+  # set colorized output
+  "--color=${SHELLCHECK_COLORIZED_OUTPUT}"
+)
+
 # Currently disabled these errors will take care of them later
-DISABLED_ERRORS="SC2002,SC3028,SC3054,SC3014,SC3040,SC3046,SC3030,SC3010,SC3037,SC3045,SC3006,SC3018,SC3016,SC3011,SC3044,SC3043,SC3060,SC3024,SC1091,SC2066,SC2086,SC2034,SC1083,SC1009,SC1073,SC1072,SC2155,SC2046"
+SHELLCHECK_DISABLED="SC2002,SC3028,SC3054,SC3014,SC3040,SC3046,SC3030,SC3010,SC3037,SC3045,SC3006,SC3018,SC3016,SC3011,SC3044,SC3043,SC3060,SC3024,SC1091,SC2066,SC2086,SC2034,SC1083,SC1009,SC1073,SC1072,SC2155,SC2046"
+
+scripts_to_check=("$@")
+if [[ "$#" == 0 ]]; then
+  # Find all shell scripts excluding:
+  # - Anything git-ignored - No need to lint untracked files.
+  # - ./_* - No need to lint output directories.
+  # - ./.git/* - Ignore anything in the git object store.
+  # - ./vendor* - Vendored code should be fixed upstream instead.
+  # - ./third_party/*, but re-include ./third_party/forked/*  - only code we
+  #    forked should be linted and fixed.
+  while IFS=$'\n' read -r script;
+    do git check-ignore -q "$script" || scripts_to_check+=("$script");
+  done < <(find . -name "*.sh" \
+    -not \( \
+      -path ./_\*      -o \
+      -path ./.git\*   -o \
+      -path ./vendor\* -o \
+      \( -path ./third_party\* -a -not -path ./third_party/forked\* \) \
+    \))
+fi
 
 # Download shellcheck-alpine from Docker Hub
 echo "Downloading ShellCheck Docker image..."
@@ -29,6 +62,9 @@ echo "Downloading ShellCheck Docker image..."
 
 # Run ShellCheck on all shell script files, excluding those in the 'vendor' directory
 echo "Running ShellCheck..."
-"${DOCKER}" run --rm -v "$(pwd):$(pwd)" -w "$(pwd)" "${SHELLCHECK_IMAGE}" \
-  find .. -type f -name '*.sh' -exec shellcheck --exclude="$DISABLED_ERRORS" {} +
+"${DOCKER}" run \
+  --rm -v "$(pwd)" -w "$(pwd)" \
+    "${SHELLCHECK_IMAGE}" \
+  shellcheck "${SHELLCHECK_OPTIONS[@]}" "${scripts_to_check[@]}" >&2 || res=$?
+
 echo "Shellcheck ran successfully"
```

<details>
<summary>diff</summary>

```sh
root@vandit-box:/home/vandit/Github-Forks/kueue# time make verify
go mod tidy
git --no-pager diff --exit-code go.mod go.sum
/home/vandit/Github-Forks/kueue/bin/golangci-lint run --timeout 15m0s
./hack/verify-shellcheck.sh
Downloading ShellCheck Docker image...
docker.io/koalaman/shellcheck-alpine@sha256:e19ed93c22423970d56568e171b4512c9244fc75dd9114045016b4a0073ac4b7: Pulling from koalaman/shellcheck-alpine
Digest: sha256:e19ed93c22423970d56568e171b4512c9244fc75dd9114045016b4a0073ac4b7
Status: Image is up to date for koalaman/shellcheck-alpine@sha256:e19ed93c22423970d56568e171b4512c9244fc75dd9114045016b4a0073ac4b7
docker.io/koalaman/shellcheck-alpine:v0.9.0@sha256:e19ed93c22423970d56568e171b4512c9244fc75dd9114045016b4a0073ac4b7

What's Next?
  View a summary of image vulnerabilities and recommendations → docker scout quickview docker.io/koalaman/shellcheck-alpine:v0.9.0@sha256:e19ed93c22423970d56568e171b4512c9244fc75dd9114045016b4a0073ac4b7
Running ShellCheck...
Unknown value for --color. Valid options are: auto, always, never
Shellcheck ran successfully
./hack/verify-toc.sh
Checking table of contents are up to date...
Cleaning up...
/home/vandit/Github-Forks/kueue/bin/controller-gen \
	crd:generateEmbeddedObjectMeta=true output:crd:artifacts:config=config/components/crd/bases\
	paths="./apis/..."
/home/vandit/Github-Forks/kueue/bin/controller-gen \
	rbac:roleName=manager-role output:rbac:artifacts:config=config/components/rbac\
	webhook output:webhook:artifacts:config=config/components/webhook\
	paths="./pkg/controller/...;./pkg/webhooks/...;./pkg/util/cert/...;./pkg/visibility/..."
go mod download
/home/vandit/Github-Forks/kueue/bin/controller-gen object:headerFile="hack/boilerplate.go.txt" paths="./apis/..."
./hack/update-codegen.sh go
Generating defaulter code for 2 targets
Generating conversion code for 2 targets
Generating openapi code for 3 targets
Generating applyconfig code for 3 targets
Generating client code for 3 targets
Generating lister code for 3 targets
Generating informer code for 3 targets
SED=/usr/bin/sed ./hack/update-helm.sh
cd  /home/vandit/Github-Forks/kueue/site/genref/ && /home/vandit/Github-Forks/kueue/bin/genref  -o /home/vandit/Github-Forks/kueue/site/content/en/docs/reference
I0317 20:44:00.067350   25439 main.go:142] Parsing go packages in sigs.k8s.io/kueue/apis/kueue/v1beta1
I0317 20:44:04.056445   25439 main.go:325] Output written to /home/vandit/Github-Forks/kueue/site/content/en/docs/reference/kueue.v1beta1.md
I0317 20:44:04.056472   25439 main.go:142] Parsing go packages in sigs.k8s.io/kueue/apis/config/v1beta1
I0317 20:44:32.410099   25439 main.go:325] Output written to /home/vandit/Github-Forks/kueue/site/content/en/docs/reference/kueue-config.v1beta1.md
I0317 20:44:32.410127   25439 main.go:142] Parsing go packages in sigs.k8s.io/kueue/apis/kueue/v1alpha1
I0317 20:44:35.994253   25439 main.go:325] Output written to /home/vandit/Github-Forks/kueue/site/content/en/docs/reference/kueue-alpha.v1alpha1.md
sed -r 's/v[0-9]+\.[0-9]+\.[0-9]+/v0.6.1/g' -i README.md -i site/config.toml
/home/vandit/Github-Forks/kueue/bin/yq e '.appVersion = "v0.6.1"' -i charts/kueue/Chart.yaml
git --no-pager diff --exit-code config/components apis charts/kueue/templates client-go site/

**real	2m34.515s
user	3m42.774s
sys	0m55.102s**
```
</details>

the time came down significantly

after the change, the output time of `make verify` was ⬇️ 

```sh
root@vandit-box:/home/vandit/Github-Forks/kueue# time make verify
go mod tidy
git --no-pager diff --exit-code go.mod go.sum
/home/vandit/Github-Forks/kueue/bin/golangci-lint run --timeout 15m0s
./hack/verify-shellcheck.sh
Downloading ShellCheck Docker image...
Error response from daemon: Get "https://registry-1.docker.io/v2/": dial tcp [2600:1f18:2148:bc01:571f:e759:a87a:2961]:443: connect: network is unreachable
Running ShellCheck...
Shellcheck ran successfully
./hack/verify-toc.sh
Checking table of contents are up to date...
Cleaning up...
/home/vandit/Github-Forks/kueue/bin/controller-gen \
	crd:generateEmbeddedObjectMeta=true output:crd:artifacts:config=config/components/crd/bases\
	paths="./apis/..."
/home/vandit/Github-Forks/kueue/bin/controller-gen \
	rbac:roleName=manager-role output:rbac:artifacts:config=config/components/rbac\
	webhook output:webhook:artifacts:config=config/components/webhook\
	paths="./pkg/controller/...;./pkg/webhooks/...;./pkg/util/cert/...;./pkg/visibility/..."
go mod download
/home/vandit/Github-Forks/kueue/bin/controller-gen object:headerFile="hack/boilerplate.go.txt" paths="./apis/..."
./hack/update-codegen.sh go
Generating defaulter code for 2 targets
Generating conversion code for 2 targets
Generating openapi code for 3 targets
Generating applyconfig code for 3 targets
Generating client code for 3 targets
Generating lister code for 3 targets
Generating informer code for 3 targets
SED=/usr/bin/sed ./hack/update-helm.sh
cd  /home/vandit/Github-Forks/kueue/site/genref/ && /home/vandit/Github-Forks/kueue/bin/genref  -o /home/vandit/Github-Forks/kueue/site/content/en/docs/reference
I0317 21:59:20.484140   67613 main.go:142] Parsing go packages in sigs.k8s.io/kueue/apis/kueue/v1beta1
I0317 21:59:23.050714   67613 main.go:325] Output written to /home/vandit/Github-Forks/kueue/site/content/en/docs/reference/kueue.v1beta1.md
I0317 21:59:23.050729   67613 main.go:142] Parsing go packages in sigs.k8s.io/kueue/apis/config/v1beta1
I0317 21:59:44.958189   67613 main.go:325] Output written to /home/vandit/Github-Forks/kueue/site/content/en/docs/reference/kueue-config.v1beta1.md
I0317 21:59:44.958211   67613 main.go:142] Parsing go packages in sigs.k8s.io/kueue/apis/kueue/v1alpha1
I0317 21:59:47.173487   67613 main.go:325] Output written to /home/vandit/Github-Forks/kueue/site/content/en/docs/reference/kueue-alpha.v1alpha1.md
sed -r 's/v[0-9]+\.[0-9]+\.[0-9]+/v0.6.1/g' -i README.md -i site/config.toml
/home/vandit/Github-Forks/kueue/bin/yq e '.appVersion = "v0.6.1"' -i charts/kueue/Chart.yaml
git --no-pager diff --exit-code config/components apis charts/kueue/templates client-go site/

**real	1m33.119s
user	1m54.290s
sys	0m28.404s**

```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-25T15:20:53Z

Hi, any progress on this?

Given how slow it is, I would even be in favor of dropping some linters.

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-26T23:05:46Z

I have been investigating the rules in `make verify` but no luck to find which rule is taking how much time. But we have the build time of verify job around ~15 mins even before February. 
The CPU usage is 0% in the link provided in the comments https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-integration-main&var-build=All&refresh=30s. According to that, increasing the number of cores might not be beneficial or help decreasing the time.

Which linters should we remove?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-27T13:30:42Z

Could you try disabling some, running and seeing which ones make the most impact?

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-27T22:19:42Z

```Makefile

.PHONY: verify
verify: gomod-verify ci-lint fmt-verify shell-lint toc-verify manifests generate update-helm generate-apiref prepare-release-branch
	git --no-pager diff --exit-code config/components apis charts/kueue/templates client-go site/

```

gomod-verify : it `go mod tidy`'s the project
ci-lint : it install and use the golangci-linter on the project
fmt-verify : formats golang code
shell-lint : checks any errors or warnings in shell-lint
toc-verify : It checks and generates if the TOC is latest. (I don't know where this TOC exists maybe https://kueue.sigs.k8s.io/docs/)
manifests: Need to dive deeper in this one.
generate: generate: Generate code containing DeepCopy, DeepCopyInto, and DeepCopyObject method implementations and client-go libraries.
update-helm: updates helm,Automatically sync RBAC files in helm chart.
generate-apiref: Generate and publish API reference documentation for Kueue.
prepare-release-branch: We use this to update version in README.md, site, kustomize and chart. I think this can be removed from verify.

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-28T15:58:33Z

toc-verify -> It checks and generates if the TOC is latest. (I don't know where this TOC exists, maybe https://kueue.sigs.k8s.io/docs/)

generate-apiref-> Generate and publish API reference documentation for Kueue.

I think these two can be removed from `verify` since we only need to check these before every release. I'm saying this on the basis of assumption the TOC and API reference gets updated after every release of Kueue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-28T17:31:19Z

How long do you estimate each of them to take?

Running them for each PR has the intent of preventing changes from merging if the authors forgot to run those commands before committing.

TOC is for `/keps`

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-28T17:35:35Z

OTOH, it looks like some builds are using 2 CPUs (even a little bit more)

![image](https://github.com/kubernetes-sigs/kueue/assets/1299064/9354aea1-1e56-4d7d-a431-bbd9e67b4316)

maybe it does make sense to increase the limits and `GOMAXPROCS`?

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-28T18:21:42Z

That's what I was thinking we should increase the limits and `GOMAXPROCS`  and see if it makes any difference.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-28T19:42:15Z

I'm ok with a brute force approach: send the PR, let's see if the time changes. If it doesn't, we revert and look into other options.

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-29T12:01:32Z

https://github.com/kubernetes/test-infra/blob/master/docs/eks-jobs-migration.md#known-issues

Should we set `GOMAXPROCS` to `automaxprocs` to see if it makes any difference.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-04-04T13:10:54Z

Nice detective work @Vandit1604!

I looked at the job now and it looks to be around 8-9 minutes.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-04T14:42:08Z

Since we have achieved the goal of being under 10 min, I'm happy to close this.

Thanks @Vandit1604!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-04T14:42:13Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1849#issuecomment-2037406212):

>Since we have achieved the goal of being under 10 min, I'm happy to close this.
>
>Thanks @Vandit1604!
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-04-07T22:42:51Z

Your Welcome @alculquicondor 
Since, I have been contributing to Kueue for some time. Now, I would like to dive in a Kueue-specific Golang issue. 
All I see in issue tabs are marked as feature-requests. Is there anything In which I can contribute.
If you could only point me to something.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-09T15:18:24Z

If you have any experience with helm, perhaps you can take this #1798

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-04-10T07:29:59Z

Thanks, I do have worked with helm charts previously.
I'll take a look into it.
