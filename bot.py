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
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        context = await browser.new_context(storage_state="session.json")
        page = await context.new_page()
        page.set_default_timeout(60000)

        print("🚀 Messenger...")
        await page.goto("https://www.facebook.com/messages")
        await asyncio.sleep(6)

        replied = set()
        counter = 0

        while True:
            try:
                counter += 1

                # 🔄 reload كل شوية (مهم جدا)
                if counter % 20 == 0:
                    print("🔄 Reload...")
                    await page.reload()
                    await asyncio.sleep(5)

                # 🔥 أهم حاجة: أول conversation فقط
                conv = page.locator("div[role='row']").first

                try:
                    await conv.click(timeout=2000)
                except:
                    await conv.click(force=True)

                await asyncio.sleep(1)

                messages = await page.locator("div[role='gridcell']").all()
                if not messages:
                    continue

                last_msg = await messages[-1].inner_text()

                if not last_msg.strip():
                    continue

                if last_msg in replied:
                    await asyncio.sleep(1)
                    continue

                # 🚀 رد فوري
                box = page.locator("div[role='textbox']")
                await box.fill(RESPONSE)
                await box.press("Enter")

                print("⚡ réponse envoyée")

                replied.add(last_msg)

                await asyncio.sleep(2)

            except Exception as e:
                print("❌ erreur:", e)
                await asyncio.sleep(3)

asyncio.run(run())
