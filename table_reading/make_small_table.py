import random
import argparse
import json

def main(args):
    prefectures = [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県",
        "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
        "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
        "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
        "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ]

    data = []
    for i in range(2):
        row = []
        for j in range(len(prefectures)):
            if random.randint(0, 5) < (1 if args.set_random_blank else 0):
                row.append("")  # 自身の都道府県への移動は "-"
            else:
                if i == 0:
                    row.append(str(round(random.uniform(165, 175), 1)))  # ランダムな人数
                else:
                    row.append(str(round(random.uniform(155, 165), 1)))  # ランダムな人数
        data.append(row)

    markdown_table = "|  | 男性 | 女性 |\n"
    markdown_table += "| - | - | - |\n"

    danjo = ["男性", "女性"]
    markdown_table = "|  | " + " | ".join(prefectures) + " |\n"
    markdown_table += "| " + " | ".join(["-" for _ in range(len(prefectures) + 1)]) + " |\n"

    for i in range(len(danjo)):
        markdown_table += f"| {danjo[i]} | " + " | ".join(data[i]) + " |\n"

    with open("migration_data.md", "w", encoding="utf-8") as file:
        file.write(markdown_table)
    query_template = """この表は都道府県ごとの男女の平均身長です。。
    {}の{}の平均身長は？"""
    qs = []
    danjo = ["男性", "女性"]
    for i in range(100):
        to = random.randint(0, 46)
        frm  = random.randint(0, 1)
        d = {}
        d["query"] = markdown_table + "\n" + query_template.format(prefectures[to], danjo[frm])
        d["answer"] = data[frm][to]
        qs.append(d)

    with open("queries.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(qs, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--set_random_blank', action='store_true', help='Enable the flag')
    args = parser.parse_args()
    main(args)


