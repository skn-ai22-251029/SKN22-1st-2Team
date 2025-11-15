import requests
from bs4 import BeautifulSoup
import re

# (질문,답변) 리스트
question_lst=[]

for i in range(1,3):
    url=f'https://jejuevservice.com/echarger/?q=YToyOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjtzOjQ6InBhZ2UiO2k6Mjt9&page={i}'

    headers = {
        "User-Agent": "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'",
        "Referer": "https://jejuevservice.com/"
    }

    session = requests.Session()
    resp = requests.get(url, headers=headers)

    # 파싱
    soup = BeautifulSoup(resp.text, "html.parser")
    paragraphs = soup.select("div.board_contents.fr-view")
    for texts in paragraphs:
        match = re.match(r'\s*Q\s*[:：]?\s*(.*?)\s*A\s*[:：]?\s*(.*)', texts.text, re.S)

        if match:
            q = match.group(1).strip()
            a = match.group(2).strip()
            question_lst.append((q,a))
