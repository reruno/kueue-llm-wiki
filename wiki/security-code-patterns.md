# Security Code Patterns (review checklist)

**Summary**: Master checklist of code patterns reviewers should flag, distilled from the `Security Code Patterns` section of every CVE in `raw/cve/`. Grouped by category and mapped to CWE.

**Sources**: `raw/cve/CVE-*.md` (515 entries). Pattern text is taken verbatim from the CVE files where the same checklist repeats per category.

**Last updated**: 2026-05-18

---

This page is the single-pane reference. The category pages ([[security-denial-of-service]], [[security-authn-authz]], etc.) expand each pattern with Kueue context, examples, and concrete file references where applicable.

## Denial of Service (CWE-400, CWE-770, CWE-476, CWE-789, CWE-1284)

- Unbounded loops iterating over user-supplied input.
- Missing context timeouts (`context.WithTimeout`) on API calls.
- Large allocations proportional to untrusted user input.
- Missing `LimitRanger` or `ResourceQuota` enforcement before admit.
- Workloads admitted without CPU/memory limits set.
- Nil-pointer paths reachable from a malformed CR (CWE-476): always pre-validate referenced objects exist before deref.
- Invalid `.spec.interval` / `.spec.timeout` values that halt the reconciler for the entire kind (the Flux CVE-2022-39272 class).

→ See [[security-denial-of-service]].

## Authentication Bypass (CWE-287, CWE-306, CWE-352)

- Webhook handlers that skip token validation on certain HTTP methods.
- Missing `SubjectAccessReview` calls before privileged operations.
- Trusting `X-Forwarded-For` or `X-Remote-User` headers without validation.
- Admission webhooks with `failurePolicy: Ignore` for security-critical checks.

→ See [[security-authn-authz]].

## RBAC Misconfiguration & Privilege Escalation (CWE-269, CWE-266, CWE-276, CWE-284, CWE-285, CWE-862, CWE-863)

- ClusterRoles with wildcard verbs (`*`) or resources (`*`).
- Roles binding `cluster-admin` to service accounts used by controllers.
- Missing namespace scoping — using ClusterRoleBinding where RoleBinding suffices.
- Kueue controller ServiceAccount with `get/list/watch` on Secrets cluster-wide.
- Functions that mutate ServiceAccount tokens or pod security contexts.
- Missing `securityContext.runAsNonRoot` or `allowPrivilegeEscalation: false`.
- `HostPID` / `HostNetwork` / `HostIPC` set to `true`.
- Volumes that mount sensitive host paths (`/etc/kubernetes`, `/var/run/docker.sock`).

→ See [[security-authn-authz]].

## Information Disclosure (CWE-200, CWE-532, CWE-522, CWE-552)

- Logging objects that may contain secrets (tokens, passwords, keys).
- Error responses that include internal stack traces.
- Listing secrets across namespaces with a ClusterRole.
- Storing sensitive values in annotations or labels (readable by all tenants).
- Persisting credentials in env vars instead of mounted Secrets.
- Including request body / object contents in `klog.Errorf` or webhook responses.

→ See [[security-information-disclosure]].

## Injection & Input Validation (CWE-20, CWE-74, CWE-77, CWE-78, CWE-89, CWE-94, CWE-502, CWE-918)

- Building API server URLs from user-controlled namespace/name fields.
- SSRF via container image URLs or init-container pull specs (CWE-918).
- Using `fmt.Sprintf` to construct YAML/JSON payloads from untrusted input.
- Executing user-supplied strings via `exec.Command` without allowlist (CWE-78).
- Template injection in labels/annotations rendered server-side (CWE-94).
- Unsafe deserialization of untrusted data with `gob`, `yaml.Unmarshal(..., interface{})`, etc. (CWE-502).
- SQL-like queries built by string concatenation (relevant if any external store is added).

→ See [[security-injection-and-input-validation]].

## Path Traversal (CWE-22, CWE-61, CWE-363)

- File paths constructed from user-supplied names without `filepath.Clean` + prefix check.
- Symlink-following file reads in a tenant-controlled directory.
- ZIP/TAR extraction without validating that entry paths stay inside the destination root (the "zip-slip" pattern, CWE-22).

→ See [[security-injection-and-input-validation]] (path traversal lives there since the mitigation pattern is identical to input validation).

## Code Execution (CWE-78, CWE-94, CWE-502)

- Executing user-supplied strings via `exec.Command` without allowlist.
- Template injection in labels/annotations rendered server-side.
- Loading user-controlled Go plugins, WASM, or scripts at runtime.
- Deserializing untrusted YAML into `interface{}` with a permissive scheme.

→ See [[security-injection-and-input-validation]].

## Supply Chain (CWE-295, CWE-494)

- Image references without digest pinning (`image: foo:latest`).
- Missing image signature verification before admission.
- `go.mod`/`go.sum` changes that don't go through review.
- Pulling build-time scripts from a URL in `Dockerfile` or Makefile.

→ See [[security-supply-chain]].

## CWE quick index

| CWE | Class | Page |
| --- | --- | --- |
| CWE-20 | Improper input validation | [[security-injection-and-input-validation]] |
| CWE-22 | Path traversal | [[security-injection-and-input-validation]] |
| CWE-78 | OS command injection | [[security-injection-and-input-validation]] |
| CWE-79 | XSS (relevant to [[dashboard]]) | [[security-injection-and-input-validation]] |
| CWE-94 | Code injection | [[security-injection-and-input-validation]] |
| CWE-200 | Sensitive info exposure | [[security-information-disclosure]] |
| CWE-269 | Improper privilege management | [[security-authn-authz]] |
| CWE-276 | Incorrect default permissions | [[security-authn-authz]] |
| CWE-284 | Improper access control | [[security-authn-authz]] |
| CWE-285 | Improper authorization | [[security-authn-authz]] |
| CWE-287 | Improper authentication | [[security-authn-authz]] |
| CWE-295 | Improper cert validation | [[security-supply-chain]] |
| CWE-306 | Missing authn for critical function | [[security-authn-authz]] |
| CWE-352 | CSRF | [[security-authn-authz]] |
| CWE-400 | Uncontrolled resource consumption | [[security-denial-of-service]] |
| CWE-476 | Nil-pointer dereference | [[security-denial-of-service]] |
| CWE-502 | Deserialization of untrusted data | [[security-injection-and-input-validation]] |
| CWE-522 | Insufficiently protected credentials | [[security-information-disclosure]] |
| CWE-532 | Sensitive info in log files | [[security-information-disclosure]] |
| CWE-552 | Files/dirs accessible to outside parties | [[security-information-disclosure]] |
| CWE-601 | Open redirect | [[security-injection-and-input-validation]] |
| CWE-770 | Allocation without limits | [[security-denial-of-service]] |
| CWE-776 | XML entity expansion (billion laughs) | [[security-denial-of-service]] |
| CWE-862 | Missing authorization | [[security-authn-authz]] |
| CWE-863 | Incorrect authorization | [[security-authn-authz]] |
| CWE-918 | SSRF | [[security-injection-and-input-validation]] |

## Related pages

- [[security]]
- [[security-best-practices]]
- [[code-quality]]
