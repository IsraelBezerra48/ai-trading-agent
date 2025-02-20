from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from playwright.async_api import async_playwright
import time
from dotenv import load_dotenv
import os, asyncio
import logging
import nest_asyncio
nest_asyncio.apply()


logging.basicConfig(level=logging.DEBUG)
load_dotenv()

timestamp = int(time.time())

interactive_brokers_scanner_prompt = """
Go to http://localhost:5056/ - visit the scanner in the nav bar.
In the Sort By dropdown of the scanner page, select the Most Active option. Then click the Scan button and wait for the new scan to run. You should do this each time you visit the scanner page.
Find the top 3 stocks that are NOT ETF's, ultra longs, or ultra shorts. Click on the stock symbol to go to the order screen. 
If you can't find a particular stock symbol, there is a stock lookup tool in the top navbar. 
Place a buy order for 2 shares of each of the top 3 stocks from the scanner. You should use a price of 20% below the most recent high.
"""

stocktwits_prompt = f"""
Go to StockTwits account at https://stocktwits.com/ripster47, find the first 3 stock symbols in his feed. Be sure to exclude the leading $ sign.
Then go to http://localhost:5056/watchlists and create a watchlist named "Twitter Picks {timestamp}" and paste a comma separated list of the 5 stock symbols into the symbols text area. Create the watchlist.
Wait until the modal disappears, then reload the page every 2 seconds until you see the Twitter Picks {timestamp} watchlist. 
When you see it, visit the watchlist, then visit each symbol in the watchlist and buy 2 shares for 5 dollars a share.
"""

google_prompt = f"""
Go to https://www.google.com and search for chatgpt.
"""

async def open_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Abre o navegador visível
        page = await browser.new_page()
        await asyncio.sleep(5)  # Espera para visualizar a interação
        await browser.close()

async def main():
    try:
        agent = Agent(
            task=google_prompt,
            llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp"),
        )
        result = await agent.run()
        print(result)

        # Abre o navegador Playwright
        await open_browser()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())
