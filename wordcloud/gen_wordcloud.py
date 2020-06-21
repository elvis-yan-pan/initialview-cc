# Generate Word Cloud

import numpy as np
import pandas as pd
import jieba.analyse
import PIL.Image as Image
from wordcloud import WordCloud

source_name = 'wordcloud_data.csv'
image = 'airplane.jpg'

def read_data(filename):
    df = pd.read_csv(filename)
    nda = df.to_numpy()
    nda.resize(nda.size)
    return nda.tolist()


def get_keywords(comments):
    text = []
    for comment in comments:
        keyword = jieba.analyse.extract_tags(comment)
        text.extend(keyword)
    return text


def gen_img(texts, img_file, filename):
    data = ' '.join(texts)
    
    # background for the word cloud
    image_coloring = Image.open(img_file)
    image_coloring = np.array(image_coloring)

    # generate and save image 
    wc = WordCloud(
        background_color='white',
        mask=image_coloring,
        font_path='/Library/Fonts/STHeiti Light.ttc'
    )
    wc.generate(data)
    wc.to_file(filename + '_wordcloud.png')
    return



if __name__ == "__main__":
    comments = read_data(source_name)
    words = get_keywords(comments)
    gen_img(words, image, 'comment')

