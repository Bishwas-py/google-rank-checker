import os
from selenium import webdriver

from selenium.webdriver import ActionChains
from urllib.parse import quote
import chromedriver_binary


def main(keyword='', domain=''):
    options = webdriver.ChromeOptions()

    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model

    options.add_argument(
        '--disable-blink-features=AutomationControlled')

    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    actions = ActionChains(driver)

    for i in range(0, 12):
        url = f"https://www.google.com/search?q={keyword}&start={i}0"
        driver.get(url)
        allSites = driver.find_elements("xpath",
                                        "//div[@data-async-context]//div[@data-hveid][@data-ved][not(@data-initq)]//a//cite")
        for index, siteElements in enumerate(allSites):
            if domain in siteElements.text.split('›')[0].replace(' ', ''):
                tabElement = siteElements.find_element('xpath', '../../../../../..')
                actions.move_to_element(tabElement).scroll_to_element(tabElement).perform()

                driver.execute_script(
                    "arguments[0].style.backgroundColor = 'antiquewhite'; arguments[0].style.padding = '12px';"
                    "arguments[0].style.borderRadius = '11px';",
                    tabElement)

                dataDir = f"data/{domain}/{quote(keyword.replace(' ', '-'))}"

                try:
                    os.makedirs(dataDir)
                except OSError as error:
                    print(error)
                tabElement = siteElements.find_element('xpath', '../../../../../..')
                tabElement.screenshot(f"{dataDir}/tab.png")
                driver.save_screenshot(f"{dataDir}/page.png")

                driver.close()
                rank = i + 1, index + 1
                with open(f"{dataDir}/rank.md", "w+") as file:
                    file.write(f"|Data|Value|\n|---|---|\n|Page Rank|{rank[0]}|\n|Tab Rank|{rank[1]}|\n|Keyword|{keyword}|\n|Domain|{domain}|")
                return rank

    return None, None


if __name__ == "__main__":
    def startBotInterface():
        keywordToFind = input("Your Keyword: ") or 'Long Tail Keyword Generator'
        siteDomain = input("Your Domain: ") or 'webmatrices.com'

        getRank = main(keywordToFind, siteDomain)
        print(f"Ranks in {getRank}")

    while True:
        startBotInterface()
