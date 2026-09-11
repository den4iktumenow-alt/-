import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram import F

API_TOKEN = "8838598056:AAEn7Doi2f3dvqTCEBiVeB5GECEqMNy88Ek"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

users = set()

def parse_number(text: str) -> int:
    text = text.lower().replace(" ", "")
    # поддержка десятичных значений
    if text.endswith("кк"):
        return int(float(text[:-2]) * 1_000_000)
    elif text.endswith("к"):
        return int(float(text[:-1]) * 1_000)
    else:
        return int(float(text))

def format_num(num: int) -> str:
    return f"{num:,}".replace(",", " ")

@dp.message(F.text)
async def handler(message: types.Message):
    users.add(message.from_user.id)

    if message.text.lower().startswith(("счет", "счёт")):
        if message.reply_to_message and message.reply_to_message.text:
            text = message.reply_to_message.text
            match = re.search(r"(\d[\d,\.]*)", text)
            if match:
                price_str = match.group(1).replace(",", "").replace(".", "")
                try:
                    price = int(price_str)
                    qty_str = message.text.lower().replace("счет", "").replace("счёт", "").strip()
                    qty = parse_number(qty_str)
                    total = price * qty

                    # шаг 1: сообщение "считаю"
                    await message.answer("🤖✨💫 Считаю для тебя...")

                    # шаг 2: итог с премиум‑эмодзи
                    await message.answer(
                        f"🐮💎 Итог готов!\n💰 {format_num(price)} × {format_num(qty)} = {format_num(total)} муни 🔥🌈🚀"
                    )

                except ValueError:
                    await message.answer("❌ Укажи количество, например: счёт 5к или счёт 2кк")

    if message.text.lower().startswith("рассылка"):
        text = message.text.replace("рассылка", "").strip()
        total = len(users)
        sent = 0
        progress_msg = await message.answer(f"📢💎 Начинаю рассылку...\nОтправлено: {sent}/{total}")

        for user_id in users:
            try:
                await bot.send_message(user_id, f"📢🔥 {text}")
                sent += 1
                await progress_msg.edit_text(f"📢✨ Рассылка...\nОтправлено: {sent}/{total}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Не удалось отправить {user_id}: {e}")

        await progress_msg.edit_text(f"✅💎 Рассылка завершена!\nИтого отправлено: {sent}/{total}")

async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
