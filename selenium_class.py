from shutil import which
import time
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as ff_options

email = '03094062230'
password = 'scripting123'
urls = ['https://www.facebook.com/?feed_demo_ad=23844765841220785&h=AQByjdeX3S2P_AMK',
        'https://www.facebook.com/?feed_demo_ad=23844765841060785&h=AQCp30fmrwLkvax7',
        'https://www.facebook.com/?feed_demo_ad=23844765841650785&h=AQBL58CUKueYUNtE']


def screen_shoot(driver, id, number):
    if not id:
        return
    element = driver.find_element_by_id(id)
    location = element.location
    size = element.size
    top = location['y']
    time.sleep(2)
    driver.execute_script(f"window.scrollTo(0, {top-100});")
    time.sleep(2)
    driver.execute_script(f"window.scrollTo(0, {top-100});")
    png = driver.get_screenshot_as_png()  # saves screenshot of entire page
    left = location['x']
    right = location['x'] + size['width']
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    im = im.crop(box=(left, 100, right, size['height']+100))  # defines crop points
    im.save(f'{number}.png')  # saves new cropped image

def create_driver(random_proxy=None):
    """
    creates firefox or chrome driver with given settings
    :param random_proxy:
    :param user_agent:
    :param for_headers:
    :param webrtc:
    :return:
    """
    options = ff_options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-javascript')
    options.add_argument('--disable-dev-shm-usage')
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    if random_proxy:
        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": random_proxy,
            "ftpProxy": random_proxy,
            "sslProxy": random_proxy
        }
    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.peerconnection.enabled", False)
    profile.set_preference("media.navigator.enabled", False)
    profile.set_preference("general.useragent.override", user_agent)
    profile.update_preferences()

    driver = webdriver.Firefox(executable_path='./geckodriver',
                               capabilities=firefox_capabilities,
                               firefox_profile=profile, firefox_options=options)

    return driver


def find_element_(driver):
    for i in range(5):
        divs = driver.find_elements_by_css_selector('div[role="article"]._5jmm')
        for div in divs:
            try:
                value = div.find_element_by_css_selector('div[data-testid="story-subtitle"]  > a')
                if bool(value):
                    if 'Sponsored' in value.text:
                        return div.get_attribute('id')
            except:
                pass
        driver.find_element_by_tag_name('html').send_keys(Keys.END)
        time.sleep(3)


def close_driver(driver):
    try:
        driver.close()
        driver.quit()
    except Exception as e:
        pass


def run_script():
    driver = create_driver()
    driver.get('https://www.facebook.com/')
    driver.maximize_window()
    e = driver.find_element_by_id('email')
    e.send_keys(email)
    e = driver.find_element_by_id('pass')
    e.send_keys(password)
    e.send_keys(Keys.ENTER)
    time.sleep(5)
    for index, url in enumerate(urls):
        driver.get(url)
        try:
            id = find_element_(driver)
            screen_shoot(driver, id, index)
        except:
            pass
    close_driver(driver)


if __name__ == '__main__':
    run_script()
