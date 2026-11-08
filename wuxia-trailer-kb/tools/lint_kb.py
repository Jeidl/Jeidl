"""Check the knowledge base: frontmatter, ids, tags, links, related, source refs, orphans."""
import re, sys, pathlib

KB = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ["id", "title", "tags", "created", "updated", "related", "summary"]
errors = []

index = (KB / "INDEX.md").read_text(encoding="utf-8")
tag_line = index.split("## 受控标签", 1)[1].split("##", 1)[0]
allowed_tags = set(re.findall(r"`([a-z-]+)`", tag_line))
sources = (KB / "topics/reference/sources.md").read_text(encoding="utf-8")
source_ids = set(re.findall(r"^\| (S\d\d) \|", sources, re.M))

notes = {}
for p in sorted((KB / "topics").rglob("*.md")):
    if p.name == "_topic.md":
        continue
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{p}: missing frontmatter"); continue
    d = dict((k.strip(), v.strip()) for k, _, v in (l.partition(":") for l in m.group(1).splitlines()))
    for k in REQUIRED:
        if not d.get(k):
            errors.append(f"{p}: missing {k}")
    nid = d.get("id", "")
    if not re.fullmatch(r"\d{8}-[a-z0-9-]+", nid) or nid.split("-", 1)[1] != p.stem:
        errors.append(f"{p}: id {nid!r} does not match filename")
    if nid in notes:
        errors.append(f"{p}: duplicate id {nid}")
    notes[nid] = (p, d, text)
    for t in re.findall(r"[a-z-]+", d.get("tags", "")):
        if t not in allowed_tags:
            errors.append(f"{p}: tag {t!r} not in controlled list")
    if f"# {d.get('title')}" not in text:
        errors.append(f"{p}: H1 does not match title")

path_to_id = {v[0].resolve(): k for k, v in notes.items()}
inbound = {k: 0 for k in notes}
for nid, (p, d, text) in notes.items():
    related = set(re.findall(r"[\w-]+", d.get("related", "")))
    for r in related:
        if r not in notes:
            errors.append(f"{p}: related id {r} does not exist")
    for target in re.findall(r"\]\(([^)#]+\.md)\)", text):
        t = (p.parent / target).resolve()
        if not t.exists():
            errors.append(f"{p}: broken link {target}"); continue
        tid = path_to_id.get(t)
        if tid and tid != nid:
            inbound[tid] += 1
            if tid not in related:
                errors.append(f"{p}: link to {tid} not mirrored in related")
    for s in set(re.findall(r"S\d\d", text)):
        if s not in source_ids:
            errors.append(f"{p}: source {s} not in sources.md")
    if f"`{nid}`" not in index:
        errors.append(f"{p}: not registered in INDEX.md")
    topic_map = (p.parent / "_topic.md").read_text(encoding="utf-8")
    if f"]({p.name})" not in topic_map:
        errors.append(f"{p}: not linked from _topic.md")

for nid, n in inbound.items():
    if n == 0:
        errors.append(f"orphan (no inbound note links): {nid}")
for path in re.findall(r"`(topics/[^`]+\.md)`", index):
    if not (KB / path).exists():
        errors.append(f"INDEX.md: path {path} does not exist")

print(f"{len(notes)} notes, {len(source_ids)} sources, {len(errors)} problems")
for e in errors:
    print(" -", e)
sys.exit(1 if errors else 0)
