import OpenHowNet


class riddle_processor:
    def __init__(self):
        self.hownet_dict = OpenHowNet.HowNetDict(use_sim=True)
        self.words_set = set(self.hownet_dict.get_zh_words())
        self.grammar_set = {"pun", "conj", "prep",
                            "classifier", "stru", "expr", "echo"}

    def __cut(self, s):
        result = []
        i = 0
        while i < len(s):
            if s[i] == " ":
                i += 1
                continue
            j = len(s)
            while s[i:j] not in self.words_set or (i == 0 and j == len(s)):
                if j == i+1:
                    break
                j -= 1
            word = s[i:j]
            get_result = self.hownet_dict.get(word, language="zh")
            get_sememes_result = self.hownet_dict.get_sememes_by_word(
                word, lang="zh")
            sememes = [set(sememe["sememes"]) for sememe, definition in zip(
                get_sememes_result, get_result) if definition["ch_grammar"] not in self.grammar_set]
            syns = [syn["text"]
                    for definition in get_result for syn in definition["syn"][:3]]
            if sememes != []:
                result.append(
                    [word, list(set().union(*sememes)), list(set(syns))])
            i = j
        return result

    '''
    riddle是一个list，包含谜面和选择，例：['火把接力传递 ', '付之一炬', '流离失所', '焚毁', '掠走', '苦心经营']
    返回一个list，包含对应的分词结果和提取的义原和近义词，例：[[['火把', ['照射', '用具', '点燃'], ['爝', '火炬']], ['接力', ['从事', '体育', '代替', '锻炼', '事情'], ['3000米障碍赛', '10米气步枪', '照办', '10米气手枪']], ['传递', ['传送'], ['承转', '传']]], [['付', ['付'], ['垫钱', '垫', '垫付']], ['之一', ['基数'], ['%', '0']], ['炬', ['照射', '用具', '火'], ['鬼火', '白炽灯', '熛', '灯花', '笔形电筒']]], [['流离', ['流浪', '悲惨'], ['颠沛流离']], ['失', ['结果', '违背', '失败', '误', '失去'], ['错过', '差', '不会再跟我们在一起了', '拔苗助长', '背道而驰', '不遂', '不见了', '背', '弊漏', '败']], ['所', ['场所', '知识', '研究'], ['设计院', '科研所', '声音属性', '科学院', '复合性', '还没', '出', '内涵性', '还不']]], [['焚', ['焚烧'], ['锻烧', '焚烧']], ['毁', ['再', '消灭', '诽谤', '损害', '制造'], ['拆毁', '吃', '办糟', '呰', '谤', '翻改', '回炉', '败', '再生产', '报销']]], [['掠', ['快', '经过', '抢'], ['掠过', '打劫', '快速经过', '抄掠']], ['走', ['选择', '看望', '娱乐', '方式性自移', '搬动', '漏出', '活动', '出错', '离开', '走'], ['出牌', '漏', '拜访', '步', '出岔子', '出差错', '方式性自移', '出岔头', '漏出', '开动', '背离', '挪步', '撤营', '拜', '不远千里', '拔', '出王牌']]], [['苦心', ['勤'], ['不知疲倦', '巴结']], ['经营', ['经济', '商业', '管理'], ['把家', '办', '办报']]]]
    '''

    def process(self, riddle):
        return list(map(self.__cut, riddle))

if __name__ == '__main__':
    OpenHowNet.download()
    processor = riddle_processor()
    print(processor.process(['火把接力传递']))
    print(processor.process(['竹林七贤皆醉酒']))
