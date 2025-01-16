import random
import argparse
import json

prefectures = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県",
    "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
    "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
    "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
    "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

def main(args):
    data = []
    for i in range(len(prefectures)):
        row = []
        for j in range(len(prefectures)):
            if i == j or random.randint(0, 5) < (1 if args.set_random_blank else 0):
                row.append("")  # 自身の都道府県への移動は "-"
            else:
                row.append(str(random.randint(100, 10000)))  # ランダムな人数
        data.append(row)

    markdown_table = "| 出発地＼到着地 | " + " | ".join(prefectures) + " |\n"
    markdown_table += "| " + " | ".join(["-" for _ in range(len(prefectures) + 1)]) + " |\n"

    for i in range(len(prefectures)):
        markdown_table += f"| {prefectures[i]} | " + " | ".join(data[i]) + " |\n"

    with open("migration_data.md", "w", encoding="utf-8") as file:
        file.write(markdown_table)
    query_template = """この表はある都道府県からある都道府県に移動した人の人数です。
    {}から{}への移動人数は？"""
    qs = []
    for i in range(100):
        frm = random.randint(0, 46)
        to  = random.randint(0, 46)
        d = {}
        d["query"] = markdown_table + "\n" + query_template.format(prefectures[frm], prefectures[to])
        d["answer"] = data[frm][to]
        qs.append(d)

    with open("queries.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(qs, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--set_random_blank', action='store_true', help='Enable the flag')
    args = parser.parse_args()
    main(args)


