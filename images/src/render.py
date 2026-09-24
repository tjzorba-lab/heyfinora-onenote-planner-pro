import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg=await b.new_page(viewport={'width':2400,'height':1800})
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(2500)
        for i in (1,2,3):
            await pg.locator(f'#p{i}').screenshot(path=f'out/pic{i}.png')
        await b.close()
asyncio.run(main())
