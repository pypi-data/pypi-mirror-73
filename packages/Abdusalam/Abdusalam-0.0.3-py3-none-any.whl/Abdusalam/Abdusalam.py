# encoding=utf-8
# Yeziq
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt 
import re
from bidi.algorithm import get_display
import arabic_reshaper
from googletrans import Translator
import requests
from lxml import etree
from pypinyin import pinyin

old = [u'ا', u'ە', u'ب', u'پ', u'ت', u'ج', u'چ', u'خ', u'د', u'ر', u'ز', u'ژ', u'س', u'ش', u'ف', u'ڭ', u'ل',\
        u'م', u'ھ', u'و', u'ۇ', u'ۆ', u'ۈ', u'ۋ', u'ې', u'ى', u'ي', u'ق', u'ك', u'گ', u'ن', u'غ',u'؟',u'،']
new = [u'a', u'e',  u'b', u'p', u't', u'j', u'ch', u'x', u'd', u'r', u'z', u'j', u's', u'sh', u'f', u'ng', u'l',\
         u'm', u'h', u'o', u'u', u'ö', u'ü', u'w', u'é', u'i', u'y', u'q', u'k', u'g', u'n', u'gh',u'?',u',']

class Yeziq():
    modulePath =    os.path.dirname(__file__)
    Font = modulePath+"/font/ALKATIP.ttf"
    def __init__(self):
        print('يېزىق ئامبىرىنى ئىشلەتكىنىڭىزنى قارشى ئالىمەن')
        print('Welcome to Use UG language module')
        
    def bulut(self,sozlar,kanglik=1000,egizlik=880,taglik="white"):
        wc= WordCloud(font_path=self.Font,background_color=taglik , width=kanglik , height=egizlik)
        text = arabic_reshaper.reshape(sozlar)
        text = get_display(text)
        wc.generate(text)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def txttarjima(self,text,nixan='ug',manba='zh-CN',**kwargs):
        Tar = Translator(service_urls=['translate.google.cn'])
        tarjim = Tar.translate(text,dest=nixan,src='auto')
        return tarjim.text

    def soztarjima(self,soz):
        sz = soz
        url = "http://dict.izda.com/?a=search&type=cn_ug&q="+sz
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
        html = requests.get(url, headers=header).text
        Music = etree.HTML(html)
        asl = Music.xpath("/html/body/div[6]/div[1]/div/div/div/div/div[1]/div[1]/text()")
        soz = Music.xpath("/html/body/div[6]/div[1]/div/div/div/div/div[1]/div[3]/text()")
        asl = str(asl);asl=asl[2:-2];
        ip =" سىز باشقا مەنبەدىن مەزكۇر ئۇچۇرغا ئېرىشكەن ۋاقتىڭىزدا ', ' كىرىپ ، ئىزدە لۇغەت ئامبىرىغا يوللاپ بەرسىڭىز بۇلىدۇ ! سىزنىڭ ۋە بىزنىڭ تىرىشچانلىقىمىز نەتىجىسىدە ئىزدە تور لۇغىتى تېخىمۇ مۇكەممەللەشكۈسى  !"
        if asl == ip:
            print('نەتىجە تېپىلمىدى')
        else:
            asl = sz+'        '
            py = pinyin(sz)
            for i in range(0,len(py)):
                asl += py[i][0]
            soz = str(soz);soz= soz[15:-13];soz=soz.replace("'",'')
            return asl,soz
        
    def uytolatin(self,text):
        tr = ""
        for i in range(0,len(text)):
            if text[i] == 'ئ':
                continue
            x_x = 0
            for j in range(0,len(old)):
                if text[i] == old[j]:
                    tr += new[j]
                    x_x=1
                    break
            if x_x == 0:
                tr += text[i]
        return tr

    def imla(self,text):
        print('كۈتۈپ تۇرۇڭ')
        print('Updating!!! it comes soon.')
    def latintouy(self,text):
        print('كۈتۈپ تۇرۇڭ')
        print('Updating!!! it comes soon.')
        
        
if __name__ == "__main__":
    yeziq = Yeziq()
    
