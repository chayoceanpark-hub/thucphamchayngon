import asyncio
from playwright.async_api import async_playwright
import json
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating...")
        await page.goto("https://s.shopee.vn/5AspSCyLEp")
        await page.wait_for_timeout(3000)
        
        # Try to find description text
        text = await page.evaluate('document.body.innerText')
        print("Body text snippet:")
        print(text[:1000])
        
        if "MÔ TẢ SẢN PHẨM" in text:
            idx = text.find("MÔ TẢ SẢN PHẨM")
            print("\nFOUND DESCRIPTION:\n")
            print(text[idx:idx+1000])
        else:
            print("\nNOT FOUND")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
