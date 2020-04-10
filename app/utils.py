from app import telegraph
import logging

logging.basicConfig(
    level=logging.INFO,
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
