# Security boundary

The public distribution is intentionally offline and non-executing. It does
not invoke models, tools, plans, network services, approvals, or external
changes. Its validation results are data for a host application; they never
grant execution authority.

The export pipeline rejects private paths, unclassified paths, private runtime
dependencies, unsafe destination links, unexpected candidate files, and
byte-level changes to classified files. Every exported file also has an
explicit public contract/reference disclosure classification. The pipeline
scans classified source bytes for a limited set of credential, private-key,
and high-confidence proprietary-content markers.

Automated scanning is not a substitute for human disclosure review. The
complete per-file review is private and is never shipped in this package. A
public publication must still receive explicit review of content, licensing,
the intended distribution boundary, and the exact immutable source commit.
