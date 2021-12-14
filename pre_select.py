#pre-select 预筛选，根据字数和类别排除掉不可能的选项
import re
import json
import pandas as pd
def charnum_to_num(charnum):
    lens={
            '一字':1,
            '二字':2,
            '三字':3,
            '四字':4,
            '五字':5,
            '六字':6,
            '七字':7,
            '八字':8,
            '九字':9,
            '十字':10,
            }
    return lens.get(charnum,None)

#种类到关键词列表的词典 这个可以随意添加
keywords={
      '中药':['中药','药材'],
      '中草药':['中药','药材'],
      '歌曲':['歌曲','演唱'],
      '成语':['成语'],
      '口语':['口语'],
      '俗语':['俗语'],
      '网络流行词':['网络','网络流行词'],
      '网络':['网络','网络流行词'],
      '电影':['电影'],
      '动物':['动物'],
      '植物':['植物','树','花'],
      '作物':['植物','作物'],
      '花':['植物','花'],
      '书':['书','报刊','古文','著作','名著',],
      '报刊':['书','报刊'],
      '著作':['书','古文','著作','名著',],
      '名著':['书','古文','著作','名著',],
      '小说':['书','小说','著作','名著',],
      '称谓':['称谓','职务'],
      '职务':['官职','职务'],
      '官职':['官职','职务'],
      '食品':['食品','食物'],
     }

def json_to_dict(url):#读取json文件，转化为dict
    with open(url,'r',encoding='utf-8') as f:
        load_dict=json.load(f)
        return load_dict
        
def pre_select(quiz,options=None): #str,str[5]，谜面和选项，返回bool[5],bool=true代表选项筛选后可能对
    poss=[True,True,True,True,True]#谜底都可能正确
    #按字数筛选
    charnum=re.findall('（.*?([一二三四五六七八九]字).*?）',quiz)#返回一个list，因为在括号内，所以不包含谜面的x字，只包含谜底字数
    if(len(charnum)!=0):#有关于谜底字数的描述
        num=charnum_to_num(charnum[0]) #谜底长度 注意不包括标点符号
        for i in range(5):
            #将options的标点都去掉，不占字数
            tmp_option=options[i].replace('，','')
            if(len(tmp_option)!=num):
                poss[i]=False
    poss_=poss#保留按字数筛选的副本
    #按类别筛选
    quiz_=re.findall('（.*?）',quiz) #假设都有括号
    for key in keywords:
        if(quiz_[0].find(key)!=-1):
            for i in range(5): #对每个选项
                has_keyword=False
                for keyword in keywords[key]:#对keywords的每个关键词
                    if(wiki_dict[options[i]].find(keyword)!=-1):
                        has_keyword=True
                if(has_keyword==False):
                    poss_[i]=False
    #如果按类别筛选筛到一个都不剩了，就返回按字数筛选的                
    all_false=True
    for i in range(5):
        if(poss_[i]==True):
            all_false=False
    if(all_false==False):
        return poss_
    return poss
    
# quiz='万紫千红次第开 （经济作物）'
# options=['春花生','夏玉米','水稻','出苗期','小麦']
train_df = pd.read_csv('data/train.csv')
wiki_dict=json_to_dict('data/wiki_info_v2.json')

error_filter = 0
total_filter = 0
for idx, row in train_df.iterrows():
    label = int(row['label'])
    options = []
    for i in range(5):
        name = f'choice{i}'
        options.append(row[name])
    poss = pre_select(row["riddle"], options)
    for i in range(5):
        total_filter += (poss[i] == False)
    if poss[label] == False:
        error_filter += 1
print(error_filter, total_filter)
