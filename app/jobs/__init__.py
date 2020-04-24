from .azz import init_azz_net, azz_net_job

from .sheldon import sheldon_job

from .blog import *

from .template import init_job, check_update


def blog_key(name):
    return 'telegram:jobs:history:blog:{}'.format(name)
