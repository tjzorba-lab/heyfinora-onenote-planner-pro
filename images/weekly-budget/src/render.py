import asyncio,sys,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
NAMES=['01-cover','02-whats-included','03-how-it-works','04-dashboard','05-transactions','06-weekly-budget','07-bills-subscriptions','08-savings-goals','09-debt-tracker','10-cash-flow','11-spending-analytics','12-annual-summary','13-no-spend-challenge','14-weekly-review','15-printable-pdf']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg=await b.new_page(viewport={'width':2000,'height':1500})
        await pg.goto('file://'+os.path.join(HERE,'slides.html')); await pg.wait_for_timeout(2500)
        for i,n in enumerate(NAMES,1):
            await pg.locator(f'#s{i}').screenshot(path=os.path.join(HERE,'..',n+'.png'))
        await b.close()
asyncio.run(main())
