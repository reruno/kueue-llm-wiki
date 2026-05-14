### Domain: Architectural Decisions

Architectural decisions at the small scale concern how code is structured, how parts connect, how simple and human-readable the result is. Complex problems may require complex solutions — but complexity must be justified.

Rules:
1. **Logical and maintainable** — Diff Code MUST be logical and maintainable.
2. **No nonsensical decisions** — Diff Code MUST NOT contain unnecessary indirection, wrong abstractions, or confusing data flow.
3. **Simplicity** — Diff Code SHOULD be as simple as possible, but not simpler. Do not penalize necessary complexity.
4. **No unnecessary intermediate variables** — avoid `x := foo.Bar; use(x)` when `use(foo.Bar)` is clearer. Redundant local variables add noise without adding clarity.
5. **Helper extraction** — if the same logic appears across multiple types, adapters, or call sites, it should live in a shared helper. Copying identical logic is an architectural smell. Conversely, do not extract a helper unless it is actually reused now or has a clear near-term reuse case.
6. **Scope discipline** — changes should do one thing. If a diff conflates a bugfix with a refactor, or applies a generic-looking helper to all types when only one type needs it, the scope is too broad. Prefer the smallest change that correctly solves the problem.
7. **Code placement** — logic should live where a reader would expect to find it. Cleanup logic inside a `Delete` function is fine; the same cleanup scattered across callers is not.

Deduct points for avoidable complexity, poor decomposition, scope creep, or structural choices that make the code harder to understand or extend without good reason.