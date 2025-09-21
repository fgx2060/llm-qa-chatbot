from flask import Flask, request, abort
import requests
import json
import re
from collections import defaultdict, deque

# === 設定 ===
LINE_CHANNEL_ACCESS_TOKEN = 'KGbX3Tk6JBOrhIj5RzV9km+eCkgJwX7YOVg5uIV77OrLKmlktVOpG+LdMZvq2xz7sWNo4iSFioPFjGWbSGOXYODclALutYYIkD8FixBI6TOZ4n4zfgpB+5Cu5+lG4kOnaWh+9KDpkVE4AW+YhIyHagdB04t89/1O/w1cDnyilFU='#你的 LINE Token
LINE_API_URL = 'https://api.line.me/v2/bot/message/reply'
OLLAMA_URL = 'http://localhost:11434/api/generate'
# OLLAMA_MODEL = 'qwen3:8b'
OLLAMA_MODEL = 'cwchang/llama-3-taiwan-8b-instruct-dpo:q5_k_m' # 你的 Ollama 模型名稱
# === 初始化物件 ===
conversation_memory = defaultdict(lambda: deque(maxlen=5))
ROLE_PROMPT = "你是一位親切又博學的 AI 助手，會用繁體中文回答問題。\n"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
}

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.json
    try:
        for event in body['events']:
            if event['type'] == 'message' and event['message']['type'] == 'text':
                user_id = event['source']['userId']
                user_msg = event['message']['text'].strip()
                reply_token = event['replyToken']

                # 檢查是否為清除指令
                if user_msg.lower() in ['重置', 'reset', '清除']:
                    conversation_memory[user_id].clear()
                    reply_body = {
                        "replyToken": reply_token,
                        "messages": [{"type": "text", "text": "✅ 已為你清除對話記憶"}]
                    }
                    requests.post(LINE_API_URL, headers=headers, data=json.dumps(reply_body))
                    continue

                # 加入使用者訊息到記憶
                conversation_memory[user_id].append(f"使用者：{user_msg}")

                # 組成完整 prompt（角色 + 記憶 + 當前輸入）
                full_prompt = ROLE_PROMPT + "\n".join(conversation_memory[user_id]) + "\nAI："

                # 呼叫 Ollama 模型
                response = requests.post(OLLAMA_URL, json={
                    "model": OLLAMA_MODEL,
                    "prompt": full_prompt,
                    "stream": False
                })

                if response.ok:
                    raw_reply = response.json().get("response", "⚠️ 沒有收到模型回答")
                    cleaned_reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL).strip()
                    converted_reply = cleaned_reply  # 不做繁體轉換
                else:
                    converted_reply = "⚠️ 模型錯誤或未啟動"

                # 加入 AI 回覆到記憶
                conversation_memory[user_id].append(f"AI：{converted_reply}")

                # 回傳給 LINE 使用者
                reply_body = {
                    "replyToken": reply_token,
                    "messages": [{"type": "text", "text": converted_reply}]
                }
                requests.post(LINE_API_URL, headers=headers, data=json.dumps(reply_body))

        return 'OK'

    except Exception as e:
        print(f"❌ Webhook 錯誤: {e}")
        abort(400)

if __name__ == '__main__':
    app.run(port=5500)
