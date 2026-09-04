---
type: object
cluster: {cluster}
universe: {live|leftover|ghost}
status: stub
verified: {date}       # `status: verified` needs both, plus citations
verified-against: {branch, commit, or vault revision}
entity: {path to the owning file}
---

# {Name}

{One sentence. If the product word and the file/type name differ, say both.}

## Why this shape

{The load-bearing why, not a field tour.}

## Shape

- {keys, constraints, or owning files}

Citations: `{path}:{line}`

## Connected to

- **owns:**
- **owned-by:**
- **joins:**
- **looks-like-but-is-not:**

## If you change this

- **Hits:**
- **Does not hit:**

## Surfaces

| Surface | Role |
|---|---|
| {who} | {reads / writes / none} |

## See

- Source: `{path}`
