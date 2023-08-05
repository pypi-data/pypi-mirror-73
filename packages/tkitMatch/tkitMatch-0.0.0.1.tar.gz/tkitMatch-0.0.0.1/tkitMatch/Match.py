# -*- coding: utf-8 -*-
import re

class Match:
    """
    匹配类
    """
    def __init__(self):
        pass

    def matching_pairs(self,mystr,tag):
        """
        匹配成对标签内的文本比如'<a helf="www.baidu.com" title="河南省">你好</a>' 或者div这种
        """
        res = re.findall(r'\['+tag+'.*?\](.*?)\[\/'+tag+'\]', mystr)
        return res

# S=Match()
# kg=S.matching_pairs(title,"KG")
# print(kg)

        
