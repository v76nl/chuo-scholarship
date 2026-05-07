import json
import os

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
    </style>
</head>
<body>
    <h1>中央大学 奨学金情報リスト</h1>
    <ul>
"""

    for item in data:
        name = item.get("name", "名称不明")
        link = item.get("link", "#")
        deadline = item.get("deadline", "-")
        
        html_content += f'        <li><a href="{link}" target="_blank">{name}</a><br><span class="deadline">{deadline}</span></li>\n'

    html_content += """    </ul>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.htmlを生成しました。")

if __name__ == "__main__":
    generate_html()