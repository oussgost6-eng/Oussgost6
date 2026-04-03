import asyncio
import random
from playwright.async_api import async_playwright

RESPONSE = """🔥 فرصة لا تُفوّت لعشّاق المراهنات! 🔥

هل تبحث عن أفضل منصات الـ betting لتحقيق أرباح حقيقية؟ 💰
انضم الآن واحصل على:
✅ بونص ترحيبي ضخم عند التسجيل
✅ أرباح سريعة وسهلة
✅ واجهة سهلة وآمنة
✅ دعم متواصل على مدار الساعة

🚀 ابدأ رحلتك اليوم وكن من الرابحين!
📲 سجّل الآن عبر الرابط:
https://lb-aff.com/L?tag=d_3662664m_22611c_site&site=3662664&ad=22611&r=registration
"""

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
        await page.goto("https://www.facebook.com/messages")
        await asyncio.sleep(8)

        print("✅ Bot actif")

        replied_messages = set()
        counter = 0

        while True:
            try:
                counter += 1

                # 🔄 reload toutes les 30 boucles
                if counter % 30 == 0:
                    print("🔄 Reload...")
                    await page.reload()
                    await asyncio.sleep(5)

                # ✅ BON SELECTEUR (IMPORTANT)
                conversations = await page.locator("div[role='row']").all()

                if not conversations:
                    print("⚠️ aucune conversation trouvée")
                    await page.reload()
                    await asyncio.sleep(5)
                    continue

                for conv in conversations[:5]:  # on garde 5 pour stabilité
                    try:
                        await conv.scroll_into_view_if_needed()

                        try:
                            await conv.click(timeout=2000)
                        except:
                            await conv.click(force=True)

                        await asyncio.sleep(2)

                        messages = await page.locator("div[role='gridcell']").all()
                        if not messages:
                            continue

                        last_msg = await messages[-1].inner_text()

                        if not last_msg.strip():
                            continue

                        if last_msg in replied_messages:
                            continue

                        box = page.locator("div[role='textbox']")
                        response = RESPONSE

                        await box.fill(response)
                        await box.press("Enter")

                        print("📩 Réponse envoyée:", response)

                        replied_messages.add(last_msg)

                        await asyncio.sleep(3)

                    except Exception as e:
                        print("❌ Erreur conv:", e)
                        continue

                await asyncio.sleep(2)

            except Exception as e:
                print("❌ Erreur globale:", e)
                await asyncio.sleep(5)

asyncio.run(run())
