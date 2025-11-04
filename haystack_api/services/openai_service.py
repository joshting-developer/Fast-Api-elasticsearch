import openai
import os
import re

openai.api_key = os.getenv("OPENAI_API_KEY", "")

# 關鍵字補充
def expand_query(query):
    prompt = f"請幫我擴充關鍵字: {query}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    content = response.choices[0].message.content.strip()

    # 移除多餘符號，清理換行，保留字詞
    keywords = re.sub(r"[-–•。•，,：:\n]", " ", content)
    keywords = re.sub(r"\s+", " ", keywords).strip()

    return f"{query} {keywords}"

# 優化商品敘述
def optimize_content(content):
    prompt = f"請優化以下商品描述，使其更具搜尋相關性:\n\"\"\"\n{content}\n\"\"\""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

# 篩選搜尋結果
def filter_results(query, results):
    # 整理結果內容
    items_text = "\n".join([
        f"- id:{item['meta'].get('id')} = {item['meta'].get('name')} ({item['content']})"
        for item in results
    ])

    # 建立 Prompt
    prompt = f"""
        根據以下使用者搜尋查詢: "{query}"，請從下面的商品清單中，挑選出真正與查詢高度相關的項目，並回傳它們的 id：
        {items_text}

        請只回傳這些項目的 id（格式為 id:42），不需要其他描述。
        """

    # 發送請求給 OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    # 解析回傳內容
    raw_text = response.choices[0].message.content.strip()
    print(f"[DEBUG] GPT 回傳內容:\n{raw_text}")

    # 從自然語言中擷取所有 id:xxx 的數字
    filtered_ids = [int(m) for m in re.findall(r'id\s*[:：]?\s*(\d+)', raw_text)]
    print(f"[DEBUG] parsed filtered_ids: {filtered_ids}")

    # 根據 id 過濾原始結果
    filtered_results = [item for item in results if item["meta"].get("id") in filtered_ids]

    return filtered_results

