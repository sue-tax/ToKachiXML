'''
Created on 2021/05/17
joucutter joubun_koumokuより移植
@author: sue-t
'''

import c
# import d
import e

class Jou_koumoku(object):
    '''
    条文の各項目（イロハ、括弧数字）ごとのデータ
    '''

    def __init__(self,
            jou_bangou_tuple, kou_bangou, gou_bangou_tuple,
            koumoku_tuple,  # ロ　（２）なら ('ロ', '（２）') の予定
            honbun, koumoku_list):
        self.jou_bangou_tuple = jou_bangou_tuple
        self.kou_bangou = kou_bangou
        self.gou_bangou_tuple = gou_bangou_tuple
        self.koumoku_tuple = koumoku_tuple
        self.honbun = honbun
        '''
        通常は、("丸付きの文か丸なしの文",)
        ("語句", "定義")もある
        '''
        self.koumoku_list = koumoku_list

    def tsuika_koumoku(self, koumoku):
        self.koumoku_list.append(koumoku)

    def set_jou_bangou_tuple(self, jou_bangou_tuple):
        self.jou_bangou_tuple = jou_bangou_tuple
        for koumoku in self.koumoku_list:
            koumoku.set_jou_bangou_tuple(jou_bangou_tuple)

    def get_kou_bangou(self):
        return self.kou_bangou

    def get_gou_bangou_tuple(self):
        return self.gou_bangou_tuple

    def set_kou_bangou(self, kou_bangou):
        self.kou_bangou = kou_bangou
        for koumoku in self.koumoku_list:
            koumoku.set_kou_bangou(kou_bangou)

    def set_gou_bangou_tuple(self, gou_bangou_tuple):
        self.gou_bangou_tuple = gou_bangou_tuple
        for koumoku in self.koumoku_list:
            koumoku.set_gou_bangou_tuple(gou_bangou_tuple)

    def shusei_koumoku_tuple(self, koumoku):
        '''
        ロ　（２）の場合、最初は("（２）",)だけなのを
        koumoku="ロ"を追加して、("ロ", "（２）")にする
        '''
#         self.koumoku_tuple = koumoku.get_koumoku_tuple() \
#                 + self.koumoku_tuple
#         d.dprint_method_start()
#         d.dprint(koumoku.get_koumoku_tuple())
#         d.dprint(self.koumoku_tuple)
        self.koumoku_tuple = koumoku.get_koumoku_tuple() \
                + self.koumoku_tuple
#         d.dprint_method_end()

    def get_koumoku_tuple(self):
        return self.koumoku_tuple

    def get_honbun(self):
        '''
        自分の項目以下の本文も取得
        '''
#         d.dprint_method_start()
#         d.dprint(self.honbun)
#         d.dprint(self.koumoku_tuple)
        list_honbun = ['{}　{}\n'.format(
                self.koumoku_tuple[-1], self.honbun)]
        for koumoku in self.koumoku_list:
            list_honbun.append('\n{}\n'. \
                    format(koumoku.get_honbun()))
        str_honbun = ''.join(list_honbun)
        del list_honbun
#         d.dprint(str_honbun)
#         d.dprint_method_end()
        return str_honbun

    def __str__(self):
        str_data = "      " + str(self.jou_bangou_tuple) \
                + "＝" + str(self.kou_bangou) \
                + "＝" + str(self.gou_bangou_tuple) \
                + "＝" + str(self.koumoku_tuple) + "　" \
                + self.honbun + "\n"
        for koumoku in self.koumoku_list:
            str_data += koumoku.__str__()
        return str_data
