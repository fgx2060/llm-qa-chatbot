# llm-qa-chatbot
人工智慧實務實作 - 大型語言模型問答聊天機器人建構

## 📖 專案簡介
本專案開發了一個基於大型語言模型 (LLM) 的問答聊天機器人，並整合 **LINE Bot 與本地 Ollama 模型**，打造低門檻、可離線執行的智能系統。  
使用者可透過 LINE 直接與聊天機器人互動，系統具備多輪記憶、角色扮演、訊息過濾等功能。

---

## ⚙️ 功能特色
- **中文簡繁轉換**（可選擇啟用或關閉）
- **多輪短期記憶**（保留最近 5 輪對話，提高回應連貫性）
- **角色扮演模式**（模型固定以「親切博學助理」身份回覆）
- **訊息過濾**（自動移除 `<think>` 等不必要輸出）
- **記憶清除指令**（輸入「重置」即可清空對話記憶）

---

## 🛠️ 系統架構
LINE 使用者 → LINE Webhook → Flask → Ollama → 模型回應 → 回傳至 LINE

---

- **後端框架**：Python + Flask  
- **本地模型**：Ollama（使用 qwen3 模型）  
- **通訊工具**：LINE Messaging API  
- **輔助工具**：ngrok（Webhook URL）、OpenCC（簡繁轉換，可選）  

---

## 🚀 使用方式
1.安裝依賴：
  ```
  pip install -r requirements.txt
  ```
2.啟動 Flask 伺服器：
  ```
  python app.py
  ```
3.使用 ngrok 將本地伺服器公開：
  ```
  ngrok http 5000
  ```
4.將 ngrok URL 綁定到 LINE Messaging API 後台。

---

📊 成果展示

聊天模式展示：
 - **技術問答**
 - **閒聊互動**
 - **角色扮演**（親切助理）
管理介面：
 - **Ngrok** 運作畫面
 - **LINE Bot** 管理後台
   
成果報告書 : 人工智慧實務實作-大型語言模型的問答聊天機器人建構.pdf

參考文獻 : LLM_based_QA_chatbot_builder_SoftwareX_2025.pdf
