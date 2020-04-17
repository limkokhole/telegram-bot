from .azz import init_azz_net, azz_net_job

from .sheldon import sheldon_job

from .blog import get_meituan_first_page, get_taobao_first_page

from .template import init_job, check_update


def blog_key(name):
    return 'telegram:jobs:history:blog:{}'.format(name)
