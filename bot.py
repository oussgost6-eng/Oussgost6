import asyncio
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
                "--disable-gpu"
            ]
        )

        context = await browser.new_context(
            storage_state="session.json"
        )

        page = await context.new_page()
        page.set_default_timeout(60000)

        print("🚀 Ouverture Messenger...")
        await page.goto("https://www.facebook.com/messages")
        await asyncio.sleep(5)

        print("⚡ BOT ULTRA RAPIDE ACTIF")

        replied = set()

        while True:
            try:
                # 🔥 récupérer conversations visibles
                conversations = await page.locator("div[role='row']").all()

                for conv in conversations:
                    try:
                        # ⚡ clic direct sans scroll lent
                        try:
                            await conv.click(timeout=1000)
                        except:
                            await conv.click(force=True)

                        # ⚡ très petit délai
                        await asyncio.sleep(0.5)

                        messages = await page.locator("div[role='gridcell']").all()
                        if not messages:
                            continue

                        last_msg = await messages[-1].inner_text()

                        if not last_msg.strip():
                            continue

                        if last_msg in replied:
                            continue

                        # 🔥 envoyer réponse direct
                        box = page.locator("div[role='textbox']")
                        await box.fill(RESPONSE)
                        await box.press("Enter")

                        print("⚡ Réponse instant:", last_msg[:30])

                        replied.add(last_msg)

                    except Exception as e:
                        continue

                # ⚡ boucle ultra rapide
                await asyncio.sleep(0.5)

            except Exception as e:
                print("Erreur:", e)
                await asyncio.sleep(2)

asyncio.run(run())
