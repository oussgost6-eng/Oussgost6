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
    executable_path="/usr/bin/chromium",
    args=[
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu"
    ]
)

        context = await browser.new_context(
            storage_state="session.json"
        )

        page = await context.new_page()
        page.set_default_timeout(60000)
        await page.goto("https://www.facebook.com/messages")

        await asyncio.sleep(10)
        print("✅ Bot actif")

        replied_messages = set()

        while True:
            try:
                conversations = await page.locator("div[role='row']").all()

                for conv in conversations[:5]:
                    try:
                        # scroll + clic sécurisé
                        await conv.scroll_into_view_if_needed()
                        await asyncio.sleep(1)

                        try:
                            await conv.click(timeout=3000)
                        except:
                            await conv.click(force=True)

                        await asyncio.sleep(random.randint(3, 6))

                        messages = await page.locator("div[role='gridcell']").all()
                        if not messages:
                            continue

                        last_msg = await messages[-1].inner_text()

                        if last_msg in replied_messages:
                            continue

                        if not last_msg.strip():
                            continue

                        box = page.locator("div[role='textbox']")
                        response = random.choice(RESPONSES)

                        await box.fill(response)
                        await box.press("Enter")

                        print("📩 Réponse envoyée:", response)

                        replied_messages.add(last_msg)

                        await asyncio.sleep(random.randint(10, 25))

                    except Exception as e:
                        print("❌ Erreur conversation:", e)
                        continue

                await asyncio.sleep(random.randint(20, 40))

            except Exception as e:
                print("Erreur globale:", e)
                await asyncio.sleep(10)

asyncio.run(run())