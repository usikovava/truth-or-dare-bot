import asyncio, aiohttp, random, os, json

TOKEN = os.environ.get("TOKEN")

TRUTH = []
DARE = []

try:
    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        TRUTH = data.get("truth", [])
        DARE = data.get("dare", [])
except: pass

async def send(chat_id, text, reply_markup=None):
    async with aiohttp.ClientSession() as s:
        payload = {"chat_id": chat_id, "text": text}
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)
        await s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)

def make_kb(action):
    return {"inline_keyboard": [[{"text": "Пропустить 🔄", "callback_data": f"skip_{action}"}]]}

async def main():
    offset = None
    while True:
        async with aiohttp.ClientSession() as s:
            try:
                r = await s.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates",
                              params={"offset": offset, "timeout": 60})
                data = await r.json()
                if data.get("ok"):
                    for u in data["result"]:
                        offset = u["update_id"] + 1
                        
                        if "callback_query" in u:
                            cb = u["callback_query"]
                            chat = cb["message"]["chat"]["id"]
                            user = cb["from"]["first_name"]
                            act = cb["data"].split("_")[1]
                            
                            if act == "play":
                                q = random.choice(TRUTH) if random.random() < 0.5 else None
                                if q:
                                    await send(chat, f"🎭 {user}, вам выпало: ПРАВДА\n\n{q}", make_kb("play"))
                                else:
                                    q = random.choice(DARE)
                                    await send(chat, f"🎯 {user}, вам выпало: ДЕЙСТВИЕ\n\n{q}", make_kb("play"))
                            elif act == "truth":
                                await send(chat, f"🎭 {user}, вы выбрали ПРАВДА\n\n{random.choice(TRUTH)}", make_kb("truth"))
                            elif act == "dare":
                                await send(chat, f"🎯 {user}, вы выбрали ДЕЙСТВИЕ\n\n{random.choice(DARE)}", make_kb("dare"))
                            
                            await s.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery",
                                       json={"callback_query_id": cb["id"]})
                        
                        elif "message" in u:
                            msg = u["message"]
                            text, chat, user = msg.get("text", ""), msg["chat"]["id"], msg["from"]["first_name"]
                            
                            if text == "/start":
                                await send(chat, "Привет! Я — бот для игры в правду или действие. Постарайся расслабиться и отвечать несерьёзно, повеселись! 🎉\n\nКоманды:\n/start — информация\n/play — случайно\n/truth — только правда\n/dare — только действие")
                            
                            elif text == "/play":
                                if random.random() < 0.5:
                                    await send(chat, f"🎭 {user}, вам выпало: ПРАВДА\n\n{random.choice(TRUTH)}", make_kb("play"))
                                else:
                                    await send(chat, f"🎯 {user}, вам выпало: ДЕЙСТВИЕ\n\n{random.choice(DARE)}", make_kb("play"))
                            
                            elif text == "/truth":
                                await send(chat, f"🎭 {user}, вы выбрали ПРАВДА\n\n{random.choice(TRUTH)}", make_kb("truth"))
                            
                            elif text == "/dare":
                                await send(chat, f"🎯 {user}, вы выбрали ДЕЙСТВИЕ\n\n{random.choice(DARE)}", make_kb("dare"))
         …
cat > requirements.txt << 'EOF'
aiohttp
