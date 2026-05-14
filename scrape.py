import httpx
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

def scrape_all_tables():
    url = "https://www.chuo-u.ac.jp/campuslife/scholarship/list/private/"
    json_file = "data.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # div:nth-child(2) の直下にあるすべての div (イテレータ m に相当) を取得
        parent_container = soup.select("#main_area > div > div.main_d > div:nth-child(2) > div")
        
        new_data = []

        for div_container in parent_container:
            # 各 div 内にある table を探す
            table = div_container.select_one("table")
            if not table:
                continue

            # table 内の各行 (イテレータ n に相当) を取得
            rows = table.select("tbody > tr")
            
            for row in rows:
                # 名前/リンク側の td
                td_name = row.select_one("td:nth-child(2)")

                # 募集案内中かどうかの td
                td_value = row.select_one("td.txtb.txtr.blue03.textcenter.valign_m")

                # 締切日のtd
                td_deadline = row.select_one("td:last-child")

                if td_name and td_value and td_deadline: # 特に「募集案内中」の表示が出ていたら
                    raw_deadline = td_deadline.get_text(strip=True)
                    raw_deadline = raw_deadline.replace('（', '(').replace('）', ')') # 括弧を半角に統一
                    
                    deadline_iso = None
                    date_matches = list(re.finditer(r'(?:(20\d{2})年)?(\d{1,2})月(\d{1,2})日', raw_deadline))
                    if date_matches:
                        last_match = date_matches[-1]
                        year_str = last_match.group(1)
                        if not year_str:
                            year_search = re.search(r'(20\d{2})年', raw_deadline)
                            year_str = year_search.group(1) if year_search else "2026"
                        year = int(year_str)
                        month = int(last_match.group(2))
                        day = int(last_match.group(3))
                        time_match = re.search(r'(\d{1,2})[:：](\d{2})', raw_deadline)
                        if time_match:
                            hour, minute = map(int, time_match.groups())
                        else:
                            hour, minute = 23, 59
                        try:
                            deadline_iso = datetime(year, month, day, hour, minute).isoformat()
                        except ValueError:
                            pass

                    full_name = td_name.get_text(separator="\n", strip=True)
                    item = {
                        "name": full_name,
                        "deadline": raw_deadline,
                        "deadline_datetime": deadline_iso,
                        "link": td_name.find("a")["href"] if td_name.find("a") else None
                    }
                    new_data.append(item)

        # データの比較と保存
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                old_data = json.load(f)
        else:
            old_data = []

        if new_data == old_data:
            print("No updates found.")
            return False
        else:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            print(f"Update detected. Saved {len(new_data)} items.")
            return True

    except Exception as e:
        print(f"Error occurred: {e}")
        return False

if __name__ == "__main__":
    scrape_all_tables()