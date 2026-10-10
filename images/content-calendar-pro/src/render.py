import asyncio,sys,os
from playwright.async_api import async_playwright
async def main():
    src=os.path.abspath(sys.argv[1]); out=os.path.abspath(sys.argv[2])
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg=await b.new_page(viewport={'width':2000,'height':1500})
        await pg.goto('file://'+src); await pg.wait_for_timeout(800)
        await pg.locator('#cover').screenshot(path=out)
        await b.close()
asyncio.run(main())
