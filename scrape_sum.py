import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        total_sum = 0
        seeds = range(48, 58) # Seeds 48 through 57

        for seed in seeds:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            await page.goto(url)
            # Wait for table rows to appear
            await page.wait_for_selector("td")
            
            # Extract and sum numbers from all <td> elements
            values = await page.eval_on_selector_all("td", "elements => elements.map(e => parseFloat(e.innerText))")
            page_sum = sum(v for v in values if not is_nan(v)) # Basic cleaning
            total_sum += page_sum
            print(f"Seed {seed}: {page_sum}")

        print(f"FINAL_TOTAL_SUM: {total_sum}")
        await browser.close()

def is_nan(x):
    return x != x

asyncio.run(run())
