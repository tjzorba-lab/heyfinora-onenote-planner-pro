const { chromium } = require('playwright');
(async () => {
const [,, html, out] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 2800, height: 2100 } });
await pg.goto('file://' + html); await pg.waitForTimeout(2500);
await pg.locator('#thumb').screenshot({ path: out });
await b.close();
})();
