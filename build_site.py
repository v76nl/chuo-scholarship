import json
import os
import urllib.parse
from datetime import datetime


def generate_robots():
    robots_file = "robots.txt"
    content = """User-agent: *
Allow: /

Sitemap: https://v76nl.github.io/chuo-scholarship/sitemap.xml
"""
    with open(robots_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("robots.txtを生成しました。")


def generate_sitemap():
    sitemap_file = "sitemap.xml"
    today_str = datetime.now().strftime("%Y-%m-%d")
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://v76nl.github.io/chuo-scholarship/</loc>
        <lastmod>{today_str}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""
    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("sitemap.xmlを生成しました。")


def generate_html():
    json_file = "data.json"
    output_file = "index.html"

    # データの読み込み
    if not os.path.exists(json_file):
        print("data.jsonが見つかりません。")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    def get_deadline_sort_key(item):
        deadline_iso = item.get("deadline_datetime")
        if deadline_iso:
            try:
                return datetime.fromisoformat(deadline_iso)
            except ValueError:
                pass
        return datetime.max

    data.sort(key=get_deadline_sort_key)

    now = datetime.now()
    active_items = []
    for item in data:
        deadline_iso = item.get("deadline_datetime")
        if deadline_iso:
            try:
                deadline_dt = datetime.fromisoformat(deadline_iso)
                if deadline_dt < now:
                    continue
            except ValueError:
                pass
        active_items.append(item)

    # 構造化データ (JSON-LD) の構築
    schema_items = []
    for index, item in enumerate(active_items, start=1):
        full_name = item.get("name", "名称不明")
        display_name = (
            full_name.replace("一般財団法人", "")
            .replace("公益財団法人", "")
            .replace("\n", " ")
            .strip()
        )
        link = item.get("link")
        item_url = (
            link
            if link and link != "None" and link != "#"
            else "https://www.chuo-u.ac.jp/campuslife/scholarship/list/private/"
        )
        schema_items.append(
            {
                "@type": "ListItem",
                "position": index,
                "name": display_name,
                "url": item_url,
            }
        )

    structured_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": "https://v76nl.github.io/chuo-scholarship/#website",
                "url": "https://v76nl.github.io/chuo-scholarship/",
                "name": "中央大学 奨学金情報リスト",
                "description": "中央大学が公開している民間団体・地方公共団体の奨学金募集情報を締切順に掲載する非公式情報サイト",
                "inLanguage": "ja",
                "author": {
                    "@type": "Person",
                    "name": "wash",
                    "url": "https://v76nl.github.io/",
                },
            },
            {
                "@type": "ItemList",
                "@id": "https://v76nl.github.io/chuo-scholarship/#itemlist",
                "name": "現在募集中の奨学金一覧",
                "itemListOrder": "https://schema.org/ItemListOrderAscending",
                "numberOfItems": len(schema_items),
                "itemListElement": schema_items,
            },
        ],
    }
    json_ld_str = json.dumps(structured_data, ensure_ascii=False, indent=4)

    # HTMLの構築
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>中央大学 奨学金情報リスト (民間団体・地方公共団体) | wash</title>
    <meta name="description" content="中央大学が公開している民間団体・地方公共団体の奨学金募集情報を締切順に掲載。締切までの残り日数や一次情報・公式サイトへのリンクを確認できる非公式情報サイトです。">
    <meta name="keywords" content="中央大学,中大,中央大,奨学金,民間奨学金,地方公共団体奨学金,締切,学費支援,給付型奨学金,貸与型奨学金">
    <link rel="canonical" href="https://v76nl.github.io/chuo-scholarship/">
    <meta name="robots" content="index, follow">

    <!-- OGP (Open Graph Protocol) -->
    <meta property="og:site_name" content="中央大学 奨学金情報リスト">
    <meta property="og:title" content="中央大学 奨学金情報リスト (民間団体・地方公共団体) | wash">
    <meta property="og:description" content="中央大学が公開している民間団体・地方公共団体の奨学金募集情報を締切順に掲載。締切までの残り日数や一次情報・公式サイトへのリンクを確認できる非公式情報サイトです。">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://v76nl.github.io/chuo-scholarship/">
    <meta property="og:locale" content="ja_JP">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="中央大学 奨学金情報リスト (民間団体・地方公共団体) | wash">
    <meta name="twitter:description" content="中央大学が公開している民間団体・地方公共団体の奨学金募集情報を締切順に掲載。締切までの残り日数や一次情報・公式サイトへのリンクを確認できる非公式情報サイトです。">

    <!-- 構造化データ (JSON-LD) -->
    <script type="application/ld+json">
{json_ld_str}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Zen Maru Gothic', sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
        }}
        h1 {{ border-bottom: 2px solid #333; padding-bottom: 10px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{
            background: white;
            margin-bottom: 10px;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
        .value {{ color: #d9534f; margin-left: 10px; font-weight: bold; }}
        .description {{ background: #e9ecef; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9em; line-height: 1.5; }}
        .description p {{ margin: 5px 0; }}
        strong {{ color: red; }}
        .name {{
            display: inline-block;
            font-weight: bold;
            font-size: 1.1em;
            margin: 0 15px 0 0;
        }}
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 10px;
            padding: 8px 16px;
            background-color: #007bff;
            color: white;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.9em;
            transition: background-color 0.2s;
        }}
        .btn svg {{ width: 16px; height: 16px; }}
        .btn:hover {{ background-color: #0056b3; }}
        .btn.disabled {{ background-color: #cccccc; pointer-events: none; color: #666; }}
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 0.85em;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <header>
        <h1>中央大学 奨学金情報リスト</h1>
        <div class="description">
            <p>このサイトは、中央大学が掲載している民間団体・地方公共団体奨学金情報をわかりやすく掲示するための非公式サイトです。<br>元となる大学のWebサイトに対し開発者が操作を加えているため、使用にあたっては<strong>必ず一次情報を参照</strong>するようにしてください。</p>
            <p>元のWebサイト: <a href="https://www.chuo-u.ac.jp/campuslife/scholarship/list/private/" target="_blank" rel="noopener noreferrer">民間団体・地方公共団体奨学金 | 中央大学</a></p>
            <p>開発者: <a href="https://v76nl.github.io/" target="_blank" rel="noopener noreferrer">wash</a></p>
            <p>GitHub: <a href="https://github.com/v76nl/chuo-scholarship" target="_blank" rel="noopener noreferrer">v76nl/chuo-scholarship</a></p>
        </div>
    </header>
    <main>
        <h2 class="sr-only">現在募集中の奨学金一覧</h2>
        <ul>
"""

    for item in active_items:
        deadline_iso = item.get("deadline_datetime")
        deadline_style = ""
        if deadline_iso:
            try:
                deadline_dt = datetime.fromisoformat(deadline_iso)
                days_left = (deadline_dt - now).days
                if 0 <= days_left <= 14:
                    ratio = days_left / 14.0
                    r = int(255 - ratio * 204)
                    g = int(ratio * 51)
                    b = int(ratio * 51)
                    font_weight = "bold" if days_left <= 7 else "normal"
                    deadline_style = (
                        f"color: rgb({r}, {g}, {b}); font-weight: {font_weight};"
                    )
            except ValueError:
                pass

        full_name = item.get("name", "名称不明")
        display_name = (
            full_name.replace("一般財団法人", "")
            .replace("公益財団法人", "")
            .replace("\n", " ")
            .strip()
        )
        link = item.get("link", "#")
        deadline = item.get("deadline", "-")

        span_attr = (
            f' class="deadline" style="{deadline_style}"'
            if deadline_style
            else ' class="deadline"'
        )

        # 一次情報へのジャンプ用リンク (募集案内中-, を接頭辞に付加して精度を向上)
        prefix = urllib.parse.quote("募集\n案内中")
        source_url = f"https://www.chuo-u.ac.jp/campuslife/scholarship/list/private/#:~:text={prefix}-,{urllib.parse.quote(full_name)}"
        external_icon = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
        source_btn = f'<a href="{source_url}" class="btn" target="_blank" rel="noopener noreferrer" style="margin-right: 10px;">{external_icon}大学のサイトを確認</a>'

        if not link or link == "None" or link == "#":
            btn_html = f'<a class="btn disabled" aria-disabled="true">{external_icon}奨学金公式サイトを確認</a>'
        else:
            btn_html = f'<a href="{link}" class="btn" target="_blank" rel="noopener noreferrer">{external_icon}奨学金公式サイトを確認</a>'

        html_content += f'        <li>\n            <article class="scholarship-card">\n                <h3 class="name">{display_name}</h3><span{span_attr}>{deadline}</span><br>{source_btn}{btn_html}\n            </article>\n        </li>\n'

    html_content += f"""    </ul>
    </main>
    <footer>
        <p>&copy; {now.year} wash | <a href="https://github.com/v76nl/chuo-scholarship" target="_blank" rel="noopener noreferrer">GitHub Repository</a></p>
    </footer>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.htmlを生成しました。")


def main():
    generate_html()
    generate_robots()
    generate_sitemap()


if __name__ == "__main__":
    main()
