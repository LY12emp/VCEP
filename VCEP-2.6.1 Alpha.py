# -*- coding: utf-8 -*-
"""
@name: VOCALOID™ of Chinese Moegirlpedia™ Editor Plus
@author: Transentropy
@version: Beta 2.6.0
@source: https://github.com/transentropy/VCEP
2.6.0小更新

修复了一些已知的问题
可分辨洛天依、言和、乐正绫的AI和V引擎
可自动接受av号和bv号参数
自动下载视频封面
补全了ACE常用歌姬
使用了更简洁的模板
"""

from json import loads
import re
import time
import urllib.request
import urllib.parse
from html import unescape
import requests
import os

word = '-\u4e00-\u9fa5_.@a-zA-Z0-9\u3040-\u309f\u30a0-\u30fa'
url = 'http(s)?:\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'
aid = 'av[0-9]+'
bvid = 'BV[0-9a-zA-Z]+'

vLis = ['洛天依', '言和', '乐正绫', '星尘(平行四界)', '心华',
        '乐正龙牙', '初音未来', '墨清弦', '徵羽摩柯',
        '幻晓伊',
        '赤羽', '诗岸', '苍穹(平行四界)', '海伊', '牧心', 'Minus(平行四界)', '星尘Infinity',
        '青溯', '默辰', '岸晓', '沨漪', 'Weina', '从铮', '煊宇', '澄宵',
        '洛天依ai', '言和ai', '乐正绫ai', '星尘Infinity']
# 修改vLis时 请同步更改vDic和554行的映射
vDic = {'洛': 0, '依': 0, '南': 0, '言': 1, '绫': 2,'北': 2, '星': 3, '尘': 3, '华': 4, '華': 4,
        '龙': 5, '牙': 5, '初': 6, '葱': 6, '墨': 7,'弦': 7, '摩': 8, '柯': 8,
        '幻': 9,
        '赤': 10, '诗': 11, '岸': 11,'苍': 12, '穹': 12, '海': 13, '牧': 14, '减': 15, 'Minus': 15, 'minus': 15,
        '青': 17, '溯': 17, '默': 18, '晓': 19, '沨': 20,'Weina': 21, 'weina': 21, '铮': 22, '煊': 23, '澄': 24,
        'Infinity': 28, 'infinity': 28}

chainLis = ['阿良良木健', '安陵影钦', '暗猫の祝福', 'AnnyJuly', 'A叔', 'Adam_K', '阿妍Ayan', '阿原Adam',
            '崩坏(P主)|崩坏', '白夜_P',
            '沧弦落尘', 'CARDINAL星海', '初繁言', '纯白', 'COP', 'Creuzer',
            '大九', '大九_LN', '大古(作词人)', 'DBRT', 'Ddickky', 'Dec顾令', 'DELA', ' 敌门', '动点P', '豆腐P', '电鱼',
            'Elefi电鱼',
            '风守miNado',
            '钢铁信徒', 'gfcjyb', 'GhostFinal', 'G.K', '公兔', '卦者灵风', '果汁凉菜', '鬼面P',
            '海格P', '海仔儿', '皓月(P主)|皓月', '黑白P', '黑方Serge', 'H.K.君', '花儿不哭', '花之祭P',
            'iKz', 'ilem',
            '绛舞乱丸', '倔强的苦力怕', 'JUSF周存',
            '康师傅の海鲜面', 'Kevinz', 'KyuRu', 'KoiNs',
            '烂兔子P', 'litterzy', '泠鸢yousa', '流绪', 'LS', 'LunaSafari', '洛微', 'Lemon夹子', '乱心',
            '毛毛虫P', '萌蛇', '米库喵', '汨罗河童', '冥凰', '苗库里Owo', '墨白茜兔', '墨雨清秋',
            '纳兰寻风', '闹闹', 'Nekock·LK', '鸟爷ToriSama', '浓缩排骨',
            'OQQ', 'PoKeR',
            '迁梦狸', '铅笔', '潜移默化P', '芹菜猪肉大馄饨', '溱绫西陌', '清风之恋', '清风疾行', '情侣の敌p',
            '人形兎', 'Ryuu',
            '桑葚上的猴子', '叁咉', '杉田朗', '舒自均', '46', '四维空间中的二维生物', '逝羽', 'St', '溯回', 'Sya',
            '水琹P', '水螅-Hydra',
            'T2o', '他城P', 'Tamlite', '一般社员汤', '唐乐林', 'teac', '跳蝻P', '桐叶_Tongye', '瞳荧', 'Tuno桐音',
            'Tino.S3',
            'U0',
            '王朝', '味素', '乌龟Sui', 'Wing翼',
            '西凉若若', '西门振', '希望索任合资', '夏秋雪', '小野道', '小宇Cosmos', '小熠IVAC', '邪叫教主', '星辉',
            '星葵', '杏花包子',
            '野良犬P', '柳延之', '伊水_Uryan', '依溪禾', '影随龙风', 'ykykyukai', '御江', '雨狸', '裕剑流', '媛天徵',
            '萤失Hinano', '一碗热汤',
            'Zeno', 'Z新豪', '战场原妖精', '折v', '郑射虎', '正弦函数P', '著小生', '砖厂浪人', '紫荆7x', '紫P', '籽三',
            '坐标P', '正义铃',
            '不羁阁', '初灵社', 'ChiliChill', '大手组', '覆域原创音乐工作室', 'GMN公会', '幻茶会',
            '幻月音乐团', '静夜社', '离时社', '龙皇漫音社', '陌云阁', '凝曙轩', 'Sodatune', '踏云社',
            '无名社', '音喵工场', '咏吟轩', '陌云阁', 'Days幻梦年华乐团',
            '星砾Sinlin',
            '一折起售', '冰镇甜豆浆', '诗驯', '偶尤大肥羊', 'Hanasa', 'Hanasa花洒', '原子Dan', 'TID'
            ]

engineLis = ['VOCALOID', 'Sharpkey', 'Synthesizer V','ACE虚拟歌姬']

divide = {"op": "",
          "ed": "",
          "ch": [],
          "hh": ['/', '&', '／'],
          'hc': [':', '：'],
          'cc': ['/', '、', '&', '／']
          }

forbid = [["http", "简介补充", '作品类型', '.*本家', '原[唱|作]', '.*码'], ["http", "BV", "www", "^[a-zA-Z0-9]+$"]]

jobList = ['策划', '作曲', '编曲', '作词', '调教', '混音', '母带', '人设', '曲绘',
           '封面', 'PV', '题字', 'LOGO', '美工', '列表外其他', '协力', '宣传', '特别感谢', '摄影', '制作',
           '演唱', '出品']

jobDictZH = {'作': {'曲': 1, '词': 3, 'default': 1},
             '曲': {'作': 1, '绘': 8, 'default': 1},
             '编': {'曲': 2, '写': '+编写', 'default': 2},
             '伴': {'奏': 2, '唱': -2},
             '词': {'作': 3, 'default': 3},
             '调': {'音': 4, '教': 4, '校': 4, 'default': 4},
             '混': {'音': 5, '贴': 5, 'default': 5},
             '分': {'轨': 5},
             '绘': {'画': 8, '图': 8, '制': 8, 'default': 8},
             '画': {'师': 8, 'default': 8},
             '演': {'唱': -2, 'default': '+'},
             '视': {'频': 10, 'default': 10},
             '影': {'default': 10},
             '映': {'像': 10, '画': 10, 'default': 10},
             '唱': {'default': -2},
             '歌': {'手': -2, '者': -2, 'default': -2},
             '协': {'力': -5, '助': -5, 'default': -5},
             '策': {'划': 0, 'default': 0},
             '呗': {'default': -2},
             '动': {'画': 10, 'default': '+'},
             '贴': {'唱': 5, 'default': '+'},
             '母': {'带': 6, 'default': '+'},
             '出': {'品': -1, 'default': '+'},
             '封': {'面': 9, 'default': 9},
             '宣': {'传': 16, 'default': 16},
             '题': {'字': 11, 'default': '+'},
             '字': {'default': 11},
             '美': {'工': 13, 'default': '+'},
             '摄': {'影': 18, 'default': 18},
             '制': {'作': 19, '品': 19},
             '总': '-',
             '重': '-',
             'default': ''
             }

jobDictEN = {'pv': 10,
             'PV': 10,
             '^mu': 1,
             '^arr': 2,
             'pro': 2,
             '^comp': 2,
             '^lyr': 3,
             '^mix': 5,
             '^thank': 17,
             '^spe': 17,
             '^vocal': -2,
             '^tun': 4,
             '^illu': 8,
             '^mov': 10,
             'logo': 12,
             }

pageFormat = """
{{{{Cquote|<poem>
</poem>}}}}
{{{{VOCALOID_Songbox
|image    = {title}.jpg
|图片信息 = 曲绘 by {illu}
|颜色     = ;{{{{文字描边|#E7DDE1}}}}#文字颜色;border-color:#FFF;
|演唱     = {singers1}
|歌曲名称 = {title}
|UP主     = [[{up}]]
|bb_id    = {bvid}
|投稿时间 = {date}{extra}
|再生     = {{{{bilibiliCount|id={bvid}}}}}
}}}}
== 简介 ==
《'''{title}'''》是[[{up}]]于{date}投稿至[[bilibili]]的{engine}中文{origin}歌曲，由{singers2}演唱{series}{album}。截至现在已有{{{{bilibiliCount|id={bvid}}}}}次观看，{{{{bilibiliCount|id={bvid}|type=4}}}}人收藏。

== 歌曲 ==
{{{{BilibiliVideo|id={bvid}}}}}

== 作者的话 ==
{{{{Cquote|<poem>
</poem>|UP主[[{up}]]发表于评论区}}}}

== 歌词 ==
{staff}
<poem>

</poem>

"""


class Intro:
    def __init__(self, text, divide):
        self.text = text
        self.divide = divide
        self.pattern = re.compile(self.partternMaker())
        self.urls = []
        self.bvids = []
        self.titles = []
        self.stfLi = self.extract(self.pre(self.text))
        self.autoCheck()
        self.autoParse()
        self.singers = self.jobSearcher('演唱')
        self.illu = self.jobSearcher('曲绘')

    def insert(self, index, obj):
        self.stfLi.insert(index, obj)

    def appand(self, obj):
        self.stfLi.append(obj)

    def remove(self, index):
        return self.stfLi.pop(index)

    def exchange(self, index1, index2):
        tmp = self.stfLi[index1]
        self.stfLi[index1] = self.stfLi[index2]
        self.stfLi[index2] = tmp

    def move(self, oriIndex, newIndex):
        tmp = self.remove(oriIndex)
        self.iinsert(newIndex, tmp)

    def update(self, index, obj):
        self.stfLi[index] = obj

    def urlCollect(self, matched):
        self.urls.append(matched.group())
        return 'http'

    def bvidCollect(self, matched):
        self.bvids.append(matched.group())
        return 'BV'

    def titleCollect(self, matched):
        self.titles.append(matched.group().strip('《》'))
        return ''

    def pre(self, text):
        return re.sub(url, self.urlCollect,
                      re.sub(bvid, self.bvidCollect,
                             re.sub("《.+?》|", self.titleCollect,
                                    unescape(text))))
        # pat = re.compile(self.divide['op'] + "(.|\s)+" +self.divide['ed'])

    def partternMaker(self):
        if not self.divide['ch']:
            return '[' + word + "".join(self.divide['hh']) \
                   + ']+ ?[' + "".join(self.divide['hc']) \
                   + '] ?[' + word + "".join(self.divide['cc']) \
                   + ']+(?!' + "|".join(divide['hc']) + ')'
        else:
            return '[' + word + "".join(self.divide['hh']) \
                   + ']+ ?[' + "".join(self.divide['hc']) \
                   + '] ?[' + word + "".join(self.divide['cc']) \
                   + ']*[^' + "".join(divide['ch']) + ']'

    def extract(self, text):
        brickList = self.pattern.findall(text)
        staffList = []
        for row in brickList:
            staffList.append(re.split("[" + "".join(self.divide['hc']) + "]", row))
        index = 0
        while index < len(staffList):
            staffList[index] = [re.split("[" + "".join(self.divide['hh']) + "]",
                                         staffList[index][0].strip(' ')),
                                re.split("[" + "".join(self.divide['cc']) + "]",
                                         staffList[index][1].strip('@ '))]
            index = index + 1
        return staffList

    def autoCheck(self):
        index = 0
        while index < len(self.stfLi):
            forbidden = False
            for job in self.stfLi[index][0]:
                for pat in forbid[0]:
                    if re.match(pat, job):
                        forbidden = True;
                        break

            else:
                for name in self.stfLi[index][1]:
                    for pat in forbid[1]:
                        if re.match(pat, name):
                            forbidden = True;
                            break

            if forbidden:
                self.remove(index)
                continue
            index = index + 1
        return

    def getIndex(self, elem):
        return elem[2]

    def autoParse(self):
        index = 0
        while index < len(self.stfLi):
            tmpList = []
            sort = len(jobList) - 5
            for jobs in self.stfLi[index][0]:
                tmp = self.staffParse(jobs)
                if tmp[0] < 0:
                    tmp[0] = tmp[0] + len(jobList)
                if sort > tmp[0]:
                    sort = tmp[0]
                tmpList.extend(tmp[1])
            self.stfLi[index] = [tmpList, self.stfLi[index][1], sort]
            index = index + 1
        self.stfLi.sort(key=self.getIndex)

    def lookUpENDict(self, s):
        string = s.lower()
        for pat, val in jobDictEN.items():
            if re.match(pat, string):
                return val
        return string.capitalize()

    def staffParse(self, jobStr):
        indexSet = set()
        extraList = []
        tmpEn = ''
        tmpZh = ''
        index = 0
        dic = jobDictZH
        while index < len(jobStr):
            if re.match('[a-zA-Z]', jobStr[index]):
                if tmpZh != '':
                    extraList.append(tmpZh)
                    tmpZh = ''
                tmpEn = tmpEn + jobStr[index]
                index = index + 1
                while index < len(jobStr) and re.match('[a-zA-Z]', jobStr[index]):
                    tmpEn = tmpEn + jobStr[index]
                    index = index + 1
                num = self.lookUpENDict(tmpEn)
                if type(num) == int:
                    indexSet.add(num)
                else:
                    extraList.append(num)
            else:
                path = dic.get(jobStr[index], 'default')
                if type(path) == int:
                    if tmpZh != '':
                        extraList.append(tmpZh)
                        tmpZh = ''
                    indexSet.add(path)
                    dic = jobDictZH
                    index = index + 1

                elif type(path) == dict:
                    if tmpZh != '':
                        extraList.append(tmpZh)
                        tmpZh = ''
                    dic = path
                    index = index + 1

                elif path == 'default':
                    if type(dic['default']) == int:
                        if tmpZh != '':
                            extraList.append(tmpZh)
                            tmpZh = ''
                        indexSet.add(dic['default'])
                        dic = jobDictZH

                    elif dic['default'] == '+':
                        tmpZh = tmpZh + jobStr[index - 1]
                        dic = jobDictZH

                    else:
                        tmpZh = tmpZh + jobStr[index]
                        index = index + 1
                        dic = jobDictZH

                elif path[0] == '+':
                    extraList[-1] = extraList[-1] + path[1:]
                    index = index + 1
                    dic = jobDictZH

                elif path[0] == '-':
                    index = index + 1
                    dic = jobDictZH

                else:
                    extraList.append(path)
                    index = index + 1
                    dic = jobDictZH
        #path = dic['default']
        if type(path) == int:
            indexSet.add(path)
        elif path == '+':
            tmpZh = tmpZh + jobStr[index - 1]
        if tmpZh != '':
            extraList.append(tmpZh)

        indexList = list(indexSet)
        sortIndex = -6
        finalList = []
        if len(indexList) != 0:
            sortIndex = indexList[0]
            for item in indexList:
                finalList.append(jobList[item])
        finalList.extend(extraList)
        return [sortIndex, finalList]

    def jobSearcher(self, job):
        for row in self.stfLi:
            if job in row[0]:
                return row[1]
        else:
            return []

    def staffSearcher(self, name):
        jobLis = []
        for row in self.stfLi:
            for stf in row[1]:
                if stf.find(name) != -1:
                    jobLis.extend(row[0])
        return jobLis

    def compose(self):
        para = """{{VOCALOID_Songbox_Introduction
|LDC = YES
|author = 
|lbgcolor = #000
|ltcolor = #FFFFFF"""
        index = 0
        tmpLis = []
        while index < len(self.stfLi):
            tmpLis.clear()
            for name in self.stfLi[index][1]:
                tmpLis.append(innerChecker(name))
            para = para + "\n" + "|" + "<br />".join(self.stfLi[index][0]) \
                   + " = " + "<br />".join(tmpLis)
            index = index + 1
        para = para + "\n}}"
        return para


def delString(text, a, b):  # del a to b-1, a >= b return original string
    if b > a >= 0 <= len(text):
        return text[0:a] + text[b:len(text)]
    else:
        return text


class Song:
    def __init__(self, data):
        self.bvid = str(data['bvid'])
        self.oriTitle = data['title']
        self.cover = data['pic']
        self.pubdate = data['pubdate'] + 28800  # UTC+8
        self.uploader = data['owner']['name']
        self.view = data['stat']['view']

        self.titleInfo = self.titleParser(self.oriTitle)
        self.introInfo = Intro(data['desc'], divide)

        self.singers = self.titleInfo['singers']
        self.introInfo.singers = self.singers
        self.introInfo.appand([['演唱'], self.singers, 14])
        self.engine = self.titleInfo['engine']

    def getFormatTime(self, fm):
        if fm == 0:
            return o.strftime("%Y-%m-%d %H:%M", time.gmtime(self.pubdate))
        else:
            gm = time.gmtime(self.pubdate)
            return str(gm.tm_year) + '年' + str(gm.tm_mon) + '月' + str(gm.tm_mday) + '日'

    @classmethod
    def singerParser(cls, texts):
        singerSet = set()
        texts=re.split('\W+', texts)
        for text in texts:
            for char in text:
                i = vDic.get(char, None)

                if re.search('ai', text, re.I) is None:
                    if i != None:
                        singerSet.add(i)
                else:
                    if i != None:
                        if i <= 3:
                            singerSet.add(i + 25)
        return singerSet

    @classmethod
    def titleParser(cls, text):
        infoDict = {'title': '', 'origin': 1, 'singers': [], 'engine': [],
                    'series': '', 'album': '', 'other': []}
        symbols = {'op': '【[（(『', 'clz': '】]）)』', 'top': '《', 'tclz': '》',
                   'divide': ' ：；;:，,+&︱、×'}
        tmp = ''
        tmpTitles = []
        flags = 0
        index = 0
        l = len(text)

        while index < l:
            char = text[index]
            if char in symbols['op']:
                if len(tmp) != 0:
                    if flags == 0:
                        tmpTitles.append(tmp)
                    else:
                        infoDict['other'].append(tmp)
                tmp = ''
                flags = flags + 1
                index = index + 1
                continue
            if char in symbols['clz']:
                if flags != 0:
                    if len(tmp) != 0:
                        infoDict['other'].append(tmp)
                    tmp = ''
                    flags = flags - 1
                index = index + 1
                continue
            if char in symbols['divide']:
                if len(tmp) != 0:
                    tmpTitles.append(tmp)
                    tmp = ''
            tmp = tmp + char
            index = index + 1

        if len(tmp) != 0:
            if flags == 0:
                tmpTitles.append(tmp)
            else:
                infoDict['other'].append(tmp)

        singerSet = set()
        engineSet = set()

        if len(tmpTitles) > 0:
            print(tmpTitles)
            tmpLi = re.split("[—-]+|[Ff]eat.|by", tmpTitles[0])
            special_chars = "!@#$%^&*()_+[]{};:,./<>?\|`~-='"
            print(tmpLi)
            # 删除标题中的特殊字符
            for char in special_chars:
                tmpLi[0] = tmpLi[0].replace(char, "")
            infoDict['title'] = tmpLi[0]
            for item in tmpLi:
                title = re.search('《.+》', item)
                if title:
                    infoDict['title'] = title.group().lstrip('《').rstrip('》')
                    if title.span()[0] > 0:
                        infoDict['other'].append(item[:title.span()[0]])
                    if title.span()[1] < len(item):
                        infoDict['other'].append(item[title.span()[1]:])
                else:
                    infoDict['other'].append(item.strip(" "))

            for i in tmpTitles[1:]:
                infoDict['other'].append(i.strip(" "))

        for item in infoDict['other']:
            if item.find("翻唱") != -1 \
                    or item.find("填词") != -1 \
                    or item.lower().find("cover") != -1:
                infoDict['origin'] = 0
                continue
            series = re.search(".+(系列|[p|P]roject)", item)
            if series:
                infoDict['series'] = series.group().strip(" ")
                continue
            album = re.search('[《『].+[》』]', item)
            if album:
                infoDict['album'] = album.group().lstrip('《『').rstrip('》』')
                continue
            else:
                album = re.search("(?<=辑).+(?=收录)", item)
                if album:
                    infoDict['album'] = album.group()
                    continue
            tmpSet = cls.singerParser(item)
            if len(tmpSet) > len(singerSet):
                singerSet = tmpSet.copy()
        for i in singerSet:
            print("vLis")
            print(vLis[i])
            if i <= 8:
                engineSet.add(0) # VOCALOID
            elif i == 9:
                engineSet.add(1) # Sharpkey
            elif i <= 24 or i == 28:
                engineSet.add(2) # Synthesizer V
            else:
                engineSet.add(3)#ACE虚拟歌姬
            infoDict['singers'].append(vLis[i])

        infoDict['engine'] = list(engineSet)
        return infoDict

    def compose(self):
        origin = ["'''翻唱'''", "原创"][self.titleInfo['origin']]
        album = self.titleInfo['album']
        if album != '':
            extra = "\n|其他资料 = ，收录于专辑《" + album + '》'
            album = "，为专辑《" + album + "》的收录曲"
        else:
            extra = ''
        series = self.titleInfo['series']
        if series != '':
            series = '，为' + series + '第■作'
        singerNum = 0
        template = ''
        category = ''
        for s in self.singers:
            if re.search('ai', s, re.I) is None:
                template += '\n{{' + s + '/' + str(time.gmtime(self.pubdate).tm_year) + '|collapsed}}'
            else:
                s = re.sub('ai', '', s, count=1)
                template += '\n{{' + s + '/' + str(time.gmtime(self.pubdate).tm_year) + '|collapsed|nocate=1}}'
                category += '\n[[分类:' + s + '歌曲]]'
        for s in self.singers:
            if re.search('ai', s, re.I) is not None:
                self.singers[singerNum] = re.sub('ai', '', s, count=1)
            singerNum += 1
        text = pageFormat.format(title=self.titleInfo['title'],
                                 bvid=self.bvid,
                                 up=self.uploader,
                                 upjob=multiJoin(self.introInfo.staffSearcher(self.uploader), '', '、', '、', '并'),
                                 illu='、'.join(self.introInfo.illu),
                                 date=self.getFormatTime(1),
                                 singers1="[[" + "]]、[[".join(self.singers) + "]]",
                                 singers2=multiJoin(self.singers, "[[", ']]、[[', ']]与[[', ']]'),
                                 engine=multiJoin(getSubLis(engineLis, self.engine), "[[", ']]、[[', ']]和[[', ']]'),
                                 origin=origin,
                                 album=album,
                                 series=series,
                                 extra=extra,
                                 staff=self.introInfo.compose())
        # print(re.search('\|演唱 = \[\[.*\n', text).span()[1])
        # while re.search('\|演唱 = \[\[.*\n',
        #                 text[re.search('\|演唱 = \[\[.*\n', text).span()[1]: len(text)-1]) is not None:
        #     text = re.sub('\|演唱 = \[\[.*\n', '', text[re.search('(\|演唱 = \[\[.*)\n', text).span()[1]: len(text)-1], count=0)

        text = text + template + category + '\n[[分类:中国音乐作品]]'
        return text


def innerChecker(name):
    if name in chainLis or name in vLis:
        return '[[' + name + ']]'
    else:
        return name


def multiJoin(ls, start, join, last, close):
    re = ""
    if len(ls) == 1:
        return start + ls[0] + close
    if len(ls) > 1:
        re = start + join.join(ls[:-1]) + last + ls[-1] + close
    return re


def getSubLis(ls, indexs):
    l = len(ls)
    subL = []
    for e in indexs:
        if l > e >= -l:
            subL.append(ls[e])
    return subL


def getData(id):
    an = re.search(aid, id)
    if an:
        if re.search('av\d+', id, re.I):
            id = re.sub('av', '', id, 1, re.I)
        url = "https://api.bilibili.com/x/web-interface/view?aid=" + id
    else:
        url = "https://api.bilibili.com/x/web-interface/view?bvid=" + id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
    except:
        return '{"code":-1,"message":"网络异常，请重试。","data":{"title":"", "desc":""}}'
    return response.read().decode('utf-8')


def download_img(url, file_name):
    error_count = 0
    success_count = 0
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
    }
    try:
        # 补充协议头
        if not (url.startswith('http') or url.startswith('https')):
            url = 'http:' + url
        img_binary = requests.get(url, headers=headers).content
        file_name = file_name + '/' + file_name + '.' + url.split('.')[-1]
        with open(f'./{file_name}', 'wb') as fp:
            fp.write(img_binary)
        print(file_name, ',下载成功')
        success_count += 1
    except Exception as e:
        print(e)
        error_count += 1
    print('下载图片结束！')
    return success_count, error_count


if __name__ == "__main__":
    print("""VOCALOID™ of Chinese Moegirlpedia™ Editor Plus (Beta 2.6.0)
Power by Transentropy©
GET UPDATED: github.com/transentropy/VCEP\n""")

    i = 3

    while i > 0:
        print("正在检测网络连接...")
        # 初始化检查网络信息
        testIof = loads(getData("6009789"))
        if testIof['code'] == -1:
            input("Error：访问站点失败，请按任意键重试\n")
            i = i - 1
        else:
            print("已成功连接到网络")
            break
    else:
        print("无法连接到网络，请检查无误后重新启动")
        exit()

    while 1:
        log = open("VClog.txt", 'a+')
        raw = input("\n请输入含有av/bv号的文本，按回车确定；直接回车退出程序\n")
        if raw == '':
            break
        raw = re.search('[a-zA-Z0-9]+', raw)

        if type(raw) is None:
            print("Error -100：无法识别的输入")
            continue
        videoInfo = loads(getData(raw.group()))
        if videoInfo['code'] != 0:
            print('Error ' + str(videoInfo['code']) + '：' + videoInfo['message'])
            continue

        mainSong = Song(videoInfo['data'])
        print("正在解析", mainSong.oriTitle, "……")
        wikiText = mainSong.compose()
        titleOut = mainSong.titleInfo['title']
        print("---------------------------")
        print(wikiText)
        if not os.path.exists(r"./" + titleOut):
            os.mkdir(r"./" + titleOut)
        file = open("./" + titleOut + "/" + titleOut + ".txt", 'a+',encoding='utf-8')
        file.write(wikiText)
        print("---------------------------\n解析完成，生成文本已写入文件")
        localtime = time.strftime("%Y-%m-%d %H:%M:%S %a", time.localtime())
        log.write("\n" + localtime + " " + titleOut)
        print("---------------------------\n日志写入完成\n---------------------------")
        download_img(videoInfo['data']['pic'], titleOut)
        print("---------------------------\n请注意检查STAFF表,歌手对应引擎是否识别正确")
        file.flush()
        log.flush()
    file.close()
    log.close()
