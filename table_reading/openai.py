from openai import OpenAI
from openai._types import NOT_GIVEN, NotGiven
import argparse
from collections.abc import Iterator
import json
import os
import re

import time
import string
import typing
PROMPT = """
| 都道府県 | 男性平均身長 (cm) | 女性平均身長 (cm) |
|----------|-------------------|-------------------|
| 北海道   | 172.5            | 159.4            |
| 青森県   | 171.8            | 158.9            |
| 岩手県   | 172.1            | 159.1            |
| 宮城県   | 172.7            | 159.8            |
| 秋田県   | 171.9            | 158.7            |
| 山形県   | 172.3            | 159.5            |
| 福島県   | 172.4            | 159.6            |
| 茨城県   | 172.6            | 159.7            |
| 栃木県   | 172.8            | 159.9            |
| 群馬県   | 172.2            | 159.3            |
| 埼玉県   | 172.9            | 160.0            |
| 千葉県   | 173.0            | 160.1            |
| 東京都   | 173.5            | 160.5            |
| 神奈川県 | 173.4            | 160.4            |
| 新潟県   | 172.1            | 159.2            |
| 富山県   | 172.0            | 159.0            |
| 石川県   | 171.8            | 158.8            |
| 福井県   | 171.9            | 158.9            |
| 山梨県   | 172.3            | 159.5            |
| 長野県   | 172.2            | 159.4            |
| 岐阜県   | 172.7            | 159.8            |
| 静岡県   | 172.6            | 159.7            |
| 愛知県   | 173.1            | 160.2            |
| 三重県   | 172.5            | 159.6            |
| 滋賀県   | 172.9            | 160.0            |
| 京都府   | 173.0            | 160.1            |
| 大阪府   | 173.2            | 160.3            |
| 兵庫県   | 173.1            | 160.2            |
| 奈良県   | 172.8            | 159.9            |
| 和歌山県 | 172.7            | 159.8            |
| 鳥取県   | 172.0            | 159.0            |
| 島根県   | 171.9            | 158.9            |
| 岡山県   | 172.4            | 159.5            |
| 広島県   | 172.6            | 159.7            |
| 山口県   | 172.3            | 159.4            |
| 徳島県   | 171.8            | 158.8            |
| 香川県   | 171.9            | 158.9            |
| 愛媛県   | 172.0            | 159.0            |
| 高知県   | 171.7            | 158.7            |
| 福岡県   | 172.8            | 159.9            |
| 佐賀県   | 172.4            | 159.5            |
| 長崎県   | 172.1            | 159.2            |
| 熊本県   | 172.5            | 159.6            |
| 大分県   | 172.2            | 159.3            |
| 宮崎県   | 172.0            | 159.0            |
| 鹿児島県 | 171.9            | 158.9            |
| 沖縄県   | 170.5            | 157.5            |
この表を元に考えてください。
京都府男性の平均身長は？
"""

table = open("./migration_data.md").read()
print(table)
PROMPT = table + """
この表はある都道府県からある都道府県に移動した人の人数です。
京都から東京への移動人数は？
"""

def new_openai_client(api_key: str, organization: str, timeout: typing.Union[float, NotGiven] = NOT_GIVEN) -> OpenAI:
    return OpenAI(
        api_key=api_key,
        organization=organization,
        timeout=timeout,
    )

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")

CHAT_MODEL_NAME = 'gpt-4o-2024-05-13'
TEMPERATURE = 0

def process(prompt):
    client = new_openai_client(
        api_key=OPENAI_API_KEY,
        organization=OPENAI_ORGANIZATION,
    )
    res = client.chat.completions.create(
        messages=[{'role': 'user', 'content': prompt}],
        model=CHAT_MODEL_NAME,
        temperature=TEMPERATURE,
    )
    return res.choices[0].message.content


def get_problems(data_path: str) -> Iterator[dict]:
    with open(data_path) as f:
        for line in f:
            yield json.loads(line)


def main(args: argparse.Namespace) -> None:
    d = json.loads(open("./queries.txt").read())
    c = 0
    for k in d:
        r = process(k["query"])
        print(r)
        print(k["answer"])
        if k["answer"] in r:
            c += 1
    print(c)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)
