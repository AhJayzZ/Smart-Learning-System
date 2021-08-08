import pprint  # just for print out result
from googletrans import Translator

data = {'ame_pr': '美 [fɪʃ]',
        'ame_pr_url': 'https://dictionary.blob.core.chinacloudapi.cn/media/audio/tom/81/29/812964E469EDC09F7627878F07C58503.mp3',
        'defination': 'n.鱼；鱼肉\n'
        'v.钓鱼；捕鱼；在…捕鱼（或钓鱼）；摸找\n'
        '网络荧光原位杂交(fluorescence in situ hybridization)；鱼类；荧光原位杂交技术',
        'eng_pr': '英 [fɪʃ]',
        'eng_pr_url': 'https://dictionary.blob.core.chinacloudapi.cn/media/audio/george/81/29/812964E469EDC09F7627878F07C58503.mp3',
        'synonym': '搭配同义词v.+n.catch fish,fillet fish,grill fishadj.+n.fresh fish,raw '
        'fish,white fish,oily fish,boat fishv.angle,go fishing,catch '
        'fish,trawl,fly-fish',
        'tenses': '第三人称单数：fishes  现在分词：fishing  过去式：fished',
        'word': 'fish'}

translator = Translator()
translation = translator.translate(
    data['defination'], src='zh-cn', dest='zh-tw')
print(translation.origin, "\n\t|\t\n\tV\t\n", translation.text)
