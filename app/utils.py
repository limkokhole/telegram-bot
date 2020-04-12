from app import telegraph
import logging
import re
from selenium import webdriver

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_telegraph_link(title=None, content=None):
    telegraph.create_account(short_name=str('tom'))
    response = telegraph.create_page(
        title=title,
        content=content
    )
    return 'https://telegra.ph/{}'.format(response['path'])


def get_nickname(user):
    if user.first_name is not None and user.last_name is not None:
        return '%s %s' % (user.first_name, user.last_name)
    elif user.first_name is None:
        return user.last_name
    elif user.last_name is None:
        return user.first_name


def check_ip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def clean_text(s):
    return s.replace('\r', '').replace('\n', '').replace(' ', '')


def save_html_screenshot(id, html_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    driver.get('file:///{}'.format(html_path))

    img_path = 'temp/{}.png'.format(id)
    driver.save_screenshot(img_path)
    driver.close()
    return img_path
