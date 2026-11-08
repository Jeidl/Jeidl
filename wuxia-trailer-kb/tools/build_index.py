"""Generate _topic.md files and the INDEX.md registry from note frontmatter."""
import re, sys, pathlib

KB = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
TOPICS = [
    ("foundations", "基础", "武侠预告的核心气质、版本类型与宣发节奏。先读这里。"),
    ("structure", "结构与时机", "三幕结构、逐秒时间轴模板、帧数换算、开场与结尾。回答「几秒做什么」。"),
    ("editing", "剪辑", "停—爆—停、港式建构式剪辑、锣鼓节奏、变速慢镜、高潮蒙太奇、转场。"),
    ("shots", "分镜与镜头语言", "景别与招牌镜头、运镜、意象库、分镜表模板。"),
    ("sound", "声音与音乐", "配乐结构、民乐分工、音效素材、静默与重击、台词。"),
    ("style", "视觉风格", "调色、书法字幕卡与片名、导演 / 流派风格谱系。"),
    ("case-studies", "案例", "具体影片及其预告的分析与启示。"),
    ("workflow", "工作流", "制作流程、拉片方法、质检清单、AI 视频生成。"),
    ("reference", "参考", "术语表与来源清单。"),
]

def fm(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit(f"no frontmatter: {path}")
    d = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        d[k.strip()] = v.strip()
    return d

registry = []
for slug, name, desc in TOPICS:
    tdir = KB / "topics" / slug
    notes = sorted(p for p in tdir.glob("*.md") if p.name != "_topic.md")
    lines = [f"# {name}（{slug}）", "", desc, ""]
    reg = [f"### {slug} — {name}"]
    for p in notes:
        d = fm(p)
        lines.append(f"- [{d['title']}]({p.name}) — {d['summary']}")
        reg.append(f"- `{d['id']}` — **{d['title']}** — `topics/{slug}/{p.name}` — {d['summary']}")
    (tdir / "_topic.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    registry.append("\n".join(reg))

index = (KB / "INDEX.md").read_text(encoding="utf-8")
start, end = "<!-- REGISTRY:START -->", "<!-- REGISTRY:END -->"
pre, rest = index.split(start)
_, post = rest.split(end)
(KB / "INDEX.md").write_text(pre + start + "\n" + "\n\n".join(registry) + "\n" + end + post, encoding="utf-8")
print("ok", sum(1 for _ in (KB / "topics").rglob("*.md")))
