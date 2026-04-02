import asyncio
import random
from playwright.async_api import async_playwright

RESPONSES = [
    "Salam 👋 merci pour ton message !",
    "Je te réponds dès que possible 😊",
    "Bien reçu 🙏 je reviens vers toi rapidement",
    "Merci pour ton message 👍"
]

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = await browser.new_context(
            storage_state="session.json"
        )

        page = await context.new_page()
        page.set_default_timeout(60000)

        print("🚀 Ouverture Facebook...")
        await page.goto("https://www.facebook.com")
        await asyncio.sleep(2)

        await page.goto("https://www.facebook.com/messages")
        print("✅ Page chargée")
        await asyncio.sleep(3)

        print("🔥 BOT ULTRA STABLE")

        replied_messages = set()
        counter = 0

        while True:
            try:
                counter += 1

                # 🔄 Reload automatique toutes les 30 boucles
                if counter % 30 == 0:
                    print("🔄 Reload page...")
                    await page.reload()
                    await asyncio.sleep(5)

                # ✅ Sélecteur plus stable
                conversations = await page.locator("div[role='listitem']").all()

                # ❗ Si rien trouvé → reload
                if len(conversations) == 0:
                    print("⚠️ Rien trouvé, reload...")
                    await page.reload()
                    await asyncio.sleep(5)
                    continue

                for conv in conversations:
                    try:
                        await conv.scroll_into_view_if_needed()

                        # ✅ clic ultra robuste
                        try:
                            await conv.click(timeout=1500)
                        except:
                            await page.evaluate("(el) => el.click()", conv)

                        await asyncio.sleep(1)

                        messages = await page.locator("div[role='gridcell']").all()
                        if not messages:
                            continue

                        last_msg = await messages[-1].inner_text()

                        if not last_msg.strip():
                            continue

                        if last_msg in replied_messages:
                            continue

                        box = page.locator("div[role='textbox']")
                        response = random.choice(RESPONSES)

                        await box.fill(response)
                        await box.press("Enter")

                        print("📩 Réponse envoyée:", response)

                        replied_messages.add(last_msg)

                        await asyncio.sleep(2)

                    except Exception as e:
                        print("❌ Erreur conv:", e)
                        continue

                await asyncio.sleep(1)

            except Exception as e:
                print("❌ Erreur globale:", e)
                await asyncio.sleep(5)

asyncio.run(run())