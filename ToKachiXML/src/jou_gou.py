''''
Created on 2021/05/15
joucutter joubun_gouより移植
@author: sue-t
'''

import c
import d
import e

from TransNum import TransNum


class Jou_gou(object):
    '''
    条文の各号ごとのデータ
    '''

    def __init__(self,
            jou_bangou_tuple, kou_bangou, gou_bangou_tuple,
            honbun, koumoku_list):
#         d.dprint_method_start()
        self.jou_bangou_tuple = jou_bangou_tuple
        self.kou_bangou = kou_bangou
        if isinstance(gou_bangou_tuple, tuple):
            pass
        else:
            gou_bangou_tuple = tuple(gou_bangou_tuple.split('の'))
#         self.gou_bangou_tuple = gou_bangou_tuple
        if len(gou_bangou_tuple) == 1:
            self.gou_bangou_tuple = \
                    (int(TransNum.k2a(gou_bangou_tuple[0])),)
        elif len(gou_bangou_tuple) == 2:
            self.gou_bangou_tuple = \
                    (int(TransNum.k2a(gou_bangou_tuple[0])),
                    int(TransNum.k2a(gou_bangou_tuple[1])))
        elif len(gou_bangou_tuple) == 3:
            self.gou_bangou_tuple = \
                    (int(TransNum.k2a(gou_bangou_tuple[0])),
                    int(TransNum.k2a(gou_bangou_tuple[1])),
                    int(TransNum.k2a(gou_bangou_tuple[2])))
        elif len(gou_bangou_tuple) == 4:
            self.gou_bangou_tuple = \
                    (int(TransNum.k2a(gou_bangou_tuple[0])),
                    int(TransNum.k2a(gou_bangou_tuple[1])),
                    int(TransNum.k2a(gou_bangou_tuple[2])),
                    int(TransNum.k2a(gou_bangou_tuple[3])))
        else:
            assert(False, "条文番号の「の」が４以上は無理")
        self.honbun = honbun
        self.koumoku_list = koumoku_list
#         d.dprint_method_end()

    def tsuika_koumoku(self, koumoku):
        self.koumoku_list.append(koumoku)

    def get_kou_bangou(self):
        return self.kou_bangou

    def get_gou_bangou_tuple(self):
        return self.gou_bangou_tuple

    def set_jou_bangou_tuple(self, jou_bangou_tuple):
        self.jou_bangou_tuple = jou_bangou_tuple
        for koumoku in self.koumoku_list:
            koumoku.set_jou_bangou_tuple(jou_bangou_tuple)

    def set_kou_bangou(self, kou_bangou):
        self.kou_bangou = kou_bangou
        for koumoku in self.koumoku_list:
            koumoku.set_kou_bangou(kou_bangou)

    def get_honbun(self):
        '''
        自分の項目以下の本文も取得
        '''
#         d.dprint_method_start()
#         d.dprint(self.koumoku_list)
        list_honbun = [self.honbun, '\n']
        for koumoku in self.koumoku_list:
            list_honbun.append('\n{}'. \
                    format(koumoku.get_honbun()))
        str_honbun = ''.join(list_honbun)
        del list_honbun
#         d.dprint(str(self.jou_bangou_tuple) \
#                 + "＝" + str(self.kou_bangou) \
#                 + "＝" + str(self.gou_bangou_tuple) + "　" \
#                 + self.honbun + "\n")
#         d.dprint(str_honbun)
#         d.dprint_method_end()
        return str_honbun

    def __str__(self):
        str_data = "    " + str(self.jou_bangou_tuple) \
                + "＝" + str(self.kou_bangou) \
                + "＝" + str(self.gou_bangou_tuple) + "　" \
                + self.honbun + "\n"
        for koumoku in self.koumoku_list:
            str_data += koumoku.__str__()
        return str_data
