import json
import os
from datetime import datetime
import urllib.parse

def generate_html():
    json_file = "data.json"
    output_file = "index.html"

    # データの読み込み
    if not os.path.exists(json_file):
        print("data.jsonが見つかりません。")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # HTMLの構築
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>中央大学奨学金情報リスト | wash</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Zen Maru Gothic', sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
            color: #333;
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
        .name {{ font-weight: bold; font-size: 1.1em; margin-right: 15px; }}
        .btn {{
            display: inline-block;
            margin-top: 10px;
            padding: 8px 16px;
            background-color: #007bff;
            color: white;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.9em;
            transition: background-color 0.2s;
        }}
        .btn:hover {{ background-color: #0056b3; }}
        .btn.disabled {{ background-color: #cccccc; pointer-events: none; color: #666; }}
    </style>
</head>
<body>
    <h1>中央大学 奨学金情報リスト</h1>
    <div class="description">
        <p>このサイトは、中央大学が掲載している民間団体・地方公共団体奨学金情報をわかりやすく掲示するための非公式サイトです。<br />元となる大学のWebサイトに対し開発者が操作を加えているため、使用にあたっては<strong>必ず一次情報を参照</strong>するようにしてください。</p>
        <p>元のWebサイト: <a href="https://www.chuo-u.ac.jp/campuslife/scholarship/list/private/" target="_blank">民間団体・地方公共団体奨学金 | 中央大学</a></p>
        <p>開発者: <a href="https://v76nl.github.io/" target="_blank">wash</a></p>
        <p>GitHub: <a href="https://github.com/v76nl/chuo-scholarship" target="_blank">v76nl/chuo-scholarship</a></p>
    </div>
    <ul>
"""

    def get_deadline_sort_key(item):
        deadline_iso = item.get("deadline_datetime")
        if deadline_iso:
            try:
                return datetime.fromisoformat(deadline_iso)
            except ValueError:
                pass
        return datetime.max

    data.sort(key=get_deadline_sort_key)

    for item in data:
        deadline_iso = item.get("deadline_datetime")
        deadline_style = ""
        if deadline_iso:
            try:
                deadline_dt = datetime.fromisoformat(deadline_iso)
                now = datetime.now()
                if deadline_dt < now:
                    continue
                
                days_left = (deadline_dt - now).days
                if 0 <= days_left <= 14:
                    ratio = days_left / 14.0
                    r = int(255 - ratio * 204)
                    g = int(ratio * 51)
                    b = int(ratio * 51)
                    font_weight = "bold" if days_left <= 7 else "normal"
                    deadline_style = f"color: rgb({r}, {g}, {b}); font-weight: {font_weight};"
            except ValueError:
                pass

        full_name = item.get("name", "名称不明")
        display_name = full_name.replace("一般財団法人", "").replace("公益財団法人", "")
        link = item.get("link", "#")
        deadline = item.get("deadline", "-")
        
        span_attr = f' class="deadline" style="{deadline_style}"' if deadline_style else ' class="deadline"'
        
        # 一次情報へのジャンプ用リンク
        source_url = f"https://www.chuo-u.ac.jp/campuslife/scholarship/list/private/#:~:text={urllib.parse.quote(full_name)}"
        source_btn = f'<a href="{source_url}" class="btn" target="_blank" style="background-color: #6c757d; margin-right: 10px;">大学サイト内リンク</a>'

        if not link or link == "None" or link == "#":
            btn_html = f'<a class="btn disabled">奨学金公式サイト</a>'
        else:
            btn_html = f'<a href="{link}" class="btn" target="_blank">奨学金公式サイト</a>'

        html_content += f'        <li><span class="name">{display_name}</span><span{span_attr}>{deadline}</span><br>{source_btn}{btn_html}</li>\n'

    html_content += """    </ul>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.htmlを生成しました。")

if __name__ == "__main__":
    generate_html()