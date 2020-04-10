import requests
from telegraph import Telegraph

telegraph = Telegraph()


def get_telegraph_link(title=None, content=None):
    telegraph.create_account(short_name=str('PushyBot'))
    response = telegraph.create_page(
        title=title,
        html_content=content
    )
    return 'https://telegra.ph/{}'.format(response['path'])


def v2ex():
    resp = requests.get('https://www.v2ex.com/api/topics/hot.json')

    idx = 1
    content = ''
    for each in resp.json():
        content += '<a href="{link}">{idx}. {title}</a><br>'.format(link=each['url'], idx=idx,
                                                                    title=each['title'])
    link = get_telegraph_link('V2ex 2020年4月10日热议主题', content)
    print(link)


def topic():
    # resp = requests.get('https://www.v2ex.com/api/replies/show.json?topic_id=661135')
    #
    # for each in resp.json():
    #     if 'content' not in each:
    #         continue
    #
    #     print(each['content_rendered'])

    from lxml import etree

    ele = etree.HTML(requests.get('https://www.v2ex.com/t/661135?p=1').text)
    conts = ele.xpath('//div[@class="reply_content"]/text()')
    for each in conts:
        print(each)
        print('-------------------------')


if __name__ == '__main__':
    # v2ex()
    topic()
