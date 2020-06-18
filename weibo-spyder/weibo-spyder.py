# Weibo Crawler

import re
import json
import jieba.analyse
import matplotlib as mpl
import numpy as np
import PIL.Image as Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests

url_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={}&containerid=100103type=2%26q%3D{}&page={}"

rm_words = ['全文', '微博', '超话']
keyword = '航班'
image = 'airplane.jpg'

def clean_text(text):
    # Get rid of special characters.
    dr = re.compile(r'(<)[^>]+>', re.S)
    dd = dr.sub('', text)
    dr = re.compile(r'#[^#]+#', re.S)
    dd = dr.sub('', dd)
    dr = re.compile(r'@[^ ]+ ', re.S)
    dd = dr.sub('', dd)
    for w in rm_words:
        regex = '[' + w + ' ]+'
        dr = re.compile(regex)
        dd = dr.sub('', dd)
    return dd.strip()


def fetch_data(query_val, page_id):
    """
    Fetch the data from a given page number.
    query_val: the keyword
    page_id: the page number
    """
    resp = requests.get(url_template.format(query_val, query_val, page_id))
    card_group = json.loads(resp.text)['data']['cards'][0]['card_group']
    mblogs = []
    for card in card_group:
        mblog = card['mblog']
        blog = {'mid': mblog['id'],  # weibo id
                'text': clean_text(mblog['text']),
                'userid': str(mblog['user']['id']),
                'username': mblog['user']['screen_name'],
                'reposts_count': mblog['reposts_count'],
                'comments_count': mblog['comments_count'],
                'attitudes_count': mblog['attitudes_count']
                }
        mblogs.append(blog)
    return mblogs


def remove_duplication(mblogs):
    assert(len(mblogs) > 0)
    mid_set = {mblogs[0]['mid']}
    new_blogs = []
    for blog in mblogs[1:]:
        if blog['mid'] not in mid_set:
            new_blogs.append(blog)
            mid_set.add(blog['mid'])
    return new_blogs


def fetch_pages(query_val, page_num):
    mblogs = []
    for page_id in range(1 + page_num + 1):
        try:
            mblogs.extend(fetch_data(query_val, page_id))
        except Exception as e:
            print(e)

    mblogs = remove_duplication(mblogs)
    fp = open('result_{}.json'.format(query_val), 'w', encoding='utf-8')
    json.dump(mblogs, fp, ensure_ascii=False, indent=4)
    print("Result saved to result_{}.json".format(query_val))


def get_keywords(mblogs):
    text = []
    for blog in mblogs:
        keyword = jieba.analyse.extract_tags(blog['text'])
        text.extend(keyword)
    return text


def gen_img(texts, img_file, filename):
    # Generate word cloud
    data = ' '.join(text for text in texts)
    image_coloring = Image.open(img_file)
    image_coloring = np.array(image_coloring)
    wc = WordCloud(
        background_color='white',
        mask=image_coloring,
        font_path='/Library/Fonts/STHeiti Light.ttc'
    )
    wc.generate(data)
    wc.to_file(filename + '_wordcloud.png')


if __name__ == '__main__':
    fetch_pages(keyword, 50)

    mblogs = json.loads(open('result_{}.json'.format(keyword), 'r', encoding='utf-8').read())
    print('Number of Posts:', len(mblogs))

    words = []
    for blog in mblogs:
        words.extend(jieba.analyse.extract_tags(blog['text']))

    print("Word Count:", len(words))

    gen_img(words, image, keyword)
