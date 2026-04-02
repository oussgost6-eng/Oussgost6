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

        print("🔥 BOT ULTRA ACTIF")

        replied_messages = set()

        while True:  # 🔥 boucle infinie (aucune limite)
            try:
                conversations = await page.locator("div[role='row']").all()

                for conv in conversations:  # 🔥 toutes les conversations (pas de limite)
                    try:
                        await conv.scroll_into_view_if_needed()

                        try:
                            await conv.click(timeout=1500)
                        except:
                            await conv.click(force=True)

                        await asyncio.sleep(1)  # ⚡ ultra rapide

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

                        await asyncio.sleep(2)  # ⚠️ mini pause (évite blocage direct)

                    except Exception as e:
                        print("❌ Erreur conv:", e)
                        continue

                await asyncio.sleep(1)  # ⚡ boucle ultra rapide

            except Exception as e:
                print("Erreur globale:", e)
                await asyncio.sleep(3)

asyncio.run(run())