from selenium import webdriver
import config


def get_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('mobileEmulation', config.smart_phone)
    # options.add_argument("--headless")  # 使用headless 无界面形态
    # options.add_argument('--disable-gpu')  # 禁用gpu
    chrome = webdriver.Chrome(chrome_options=options)
    chrome.implicitly_wait(10)
    return chrome


"""chrome_options.add_argument("--headless")  # 使用headless 无界面形态
chrome_options.add_argument('--disable-gpu')  # 禁用gpu
# 设置代理
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
chromeOptions.ae\erver=http://10.20.158.50:808")
"""