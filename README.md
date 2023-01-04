# arbitrage-scraper
Web-scrapes multiple sportsbooks via web driver and returns ordered arbitrage opportunities.

### To Run
1. `pip install selenium`
2. `pip install bs4`
3. `pip install operator`
4. `Download and run 'NFL-arbitrage.py'`

Since sportsbooks do not have official API's capable of obtaining this information, the program uses Beautiful Soup and the Chrome webdriver to 'manually' grab HTML.
