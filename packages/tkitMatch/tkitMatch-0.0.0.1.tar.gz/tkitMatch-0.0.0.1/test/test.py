
#encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")
# from harvesttext import HarvestText

from tkitMatch import Match


title = '[KG]趣秘[/KG][KG]乌白舞，[UNK]的,亲”克扬语她[S]部曲，作者，演剧恋[S]首歌手[S]所属系些罗齐体她性》是剧聊为作者[S]'
S=Match()
kg=S.matching_pairs(title,"KG")
print(kg)
# ['趣秘']
