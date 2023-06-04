'''
Created on 2021/05/15
joucutter joubun_kouより移植
@author: sue-t
'''

from TransNum import TransNum
from pickle import NONE


class Jou_kou(object):
    '''
    条文の各項ごとのデータ
    '''

    def __init__(self,
            jou_bangou_tuple, kou_bangou,
            honbun, gou_list):
        if jou_bangou_tuple == None:
            self.jou_bangou_tuple = None
        elif len(jou_bangou_tuple) == 1:
            self.jou_bangou_tuple = \
                    (int(TransNum.k2a(jou_bangou_tuple[0])),)
        elif len(jou_bangou_tuple) == 2:
            self.jou_bangou_tuple = \
                    (int(TransNum.k2a(jou_bangou_tuple[0])),
                    int(TransNum.k2a(jou_bangou_tuple[1])))
        elif len(jou_bangou_tuple) == 3:
            self.jou_bangou_tuple = \
                    (int(TransNum.k2a(jou_bangou_tuple[0])),
                    int(TransNum.k2a(jou_bangou_tuple[1])),
                    int(TransNum.k2a(jou_bangou_tuple[2])))
        elif len(jou_bangou_tuple) == 4:
            self.jou_bangou_tuple = \
                    (int(TransNum.k2a(jou_bangou_tuple[0])),
                    int(TransNum.k2a(jou_bangou_tuple[1])),
                    int(TransNum.k2a(jou_bangou_tuple[2])),
                    int(TransNum.k2a(jou_bangou_tuple[3])))
#        当初の想定と違うかも
#         elif len(jou_bangou_tuple) == 1:
#             self.jou_bangou_tuple = \
#                     ((int(TransNum.k2a(jou_bangou_tuple[0])),),
#                     kou_bangou, None)
#         elif len(jou_bangou_tuple) == 2:
#             self.jou_bangou_tuple = \
#                     ((int(TransNum.k2a(jou_bangou_tuple[0])),
#                     int(TransNum.k2a(jou_bangou_tuple[1]))),
#                     kou_bangou, None)
#         elif len(jou_bangou_tuple) == 3:
#             self.jou_bangou_tuple = \
#                     ((int(TransNum.k2a(jou_bangou_tuple[0])),
#                     int(TransNum.k2a(jou_bangou_tuple[1])),
#                     int(TransNum.k2a(jou_bangou_tuple[2]))),
#                     kou_bangou, None)
#         elif len(jou_bangou_tuple) == 4:
#             self.jou_bangou_tuple = \
#                     ((int(TransNum.k2a(jou_bangou_tuple[0])),
#                     int(TransNum.k2a(jou_bangou_tuple[1])),
#                     int(TransNum.k2a(jou_bangou_tuple[2])),
#                     int(TransNum.k2a(jou_bangou_tuple[3]))),
#                     kou_bangou, None)
        else:
            assert(False, "条文番号の「の」が４以上は無理")
        self.kou_bangou = kou_bangou
        self.honbun = honbun
        self.gou_list = gou_list
        self.soku = None
        self.midashi = None
        self.item_title = None
        self.zenkou = None
        self.jikou = None

    def set_soku(self, soku):
        self.soku = soku

    def set_midashi(self, midashi):
        self.midashi = midashi

    def set_item_title(self, item_title):
        self.item_title = item_title

    def tsuika_gou(self, gou):
        self.gou_list.append(gou)

    def get_jou_bangou_tuple(self):
        return self.jou_bangou_tuple

    def get_kou_bangou(self):
        return self.kou_bangou

    def get_gou_list(self):
        return self.gou_list

    def set_zenkou(self, zenkou):
        self.zenkou = zenkou

    def set_jikou(self, jikou):
        self.jikou = jikou

    def get_zenkou(self):
        return self.zenkou

    def get_jikou(self):
        return self.jikou


#     def set_jou_bangou_tuple(self, jou_bangou_tuple):
# #         d.dprint(jou_bangou_tuple)
#         self.jou_bangou_tuple = jou_bangou_tuple
#         for gou in self.gou_list:
#             gou.set_jou_bangou_tuple(jou_bangou_tuple)
#     def set_jou_bangou_tuple(self, jou_bangou_tuple):
# #         d.dprint(jou_bangou_tuple)
#         self.jou_bangou_tuple = \
#                 (jou_bangou_tuple, self.kou_bangou, None)

    def get_item_title(self):
        return self.item_title

    def __str__(self):
        str_data = "  " + str(self.jou_bangou_tuple) \
                + str(self.kou_bangou) \
                + " " + self.honbun + "\n"
        for gou in self.gou_list:
            str_data += gou.__str__()
        return str_data
