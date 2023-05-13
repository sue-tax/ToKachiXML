'''
Created on 2021/05/15
joucutter joubun_jouより移植
@author: sue-t
'''

import c
# import d

from TransNum import TransNum


class Jou_jou(object):
    '''
    条文の各条ごとのデータ
    '''

#     INDEX_HEN = 0
#     INDEX_SHOU = 1
#     INDEX_SETSU = 2
#     INDEX_KAN = 3
#     INDEX_MOKU =4

    INDEX_JOU = 0
    INDEX_KOU = 1
    INDEX_GOU = 2
    INDEX_IROHA = 3
    INDEX_KAKKO_SUJI = 4
    INDEX_ROMA_SUJI = 5

    def __init__(self, bangou_tuple, kou, sakujo=False):
#         self.kubun = (None, None, None, None, None)
        if len(bangou_tuple) == 1:
            self.bangou_tuple = \
                    (int(TransNum.k2a(bangou_tuple[0])),)
        elif len(bangou_tuple) == 2:
            self.bangou_tuple = \
                    (int(TransNum.k2a(bangou_tuple[0])),
                    int(TransNum.k2a(bangou_tuple[1])))
        elif len(bangou_tuple) == 3:
            self.bangou_tuple = \
                    (int(TransNum.k2a(bangou_tuple[0])),
                    int(TransNum.k2a(bangou_tuple[1])),
                    int(TransNum.k2a(bangou_tuple[2])))
        elif len(bangou_tuple) == 4:
            self.bangou_tuple = \
                    (int(TransNum.k2a(bangou_tuple[0])),
                    int(TransNum.k2a(bangou_tuple[1])),
                    int(TransNum.k2a(bangou_tuple[2])),
                    int(TransNum.k2a(bangou_tuple[3])))
        else:
            assert(False, "条文番号の「の」が４以上は無理")
        self.midashi = None
        self.kou_list = [kou]
        self.sakujo = sakujo

#     def set_kubun(self, kubun):
#         self.kubun = kubun  # 編、章などの区分
            # (None, '２', '３', None, None)
            # 第２章第３節　編・款・目はなし

    def tsuika_kou(self, kou):
        self.kou_list.append(kou)

    def set_midashi(self, midashi):
        self.midashi = midashi

    def get_bangou_tuple(self):
        return self.bangou_tuple

    def save(self, file_name):
        pass
#         f = open(file_name, "w", encoding='utf-8')
#         if self.midashi != None:
#             f.write("（" + self.midashi + "）\n")
#         jou_bangou_str = henkan.jou_bangou_henkan_kansuji(
#                 self.bangou_tuple)
#         f.write("第" + jou_bangou_str + "　" \
#                 + self.kou_list[0].html + "\n") # TODO
#         for gou in self.kou_list[0].gou_list:
#             gou_bangou_str = henkan.gou_bangou_henkan_zenkaku(
#                     gou.gou_bangou_tuple)
#             f.write(gou_bangou_str + "　" + gou.html + "\n") # TODO
#             for koumoku in gou.koumoku_list:
#                 koumoku_bangou_str = henkan. \
#                         gou_bangou_henkan_zenkaku(
#                         koumoku.koumoku_tuple)
#                 f.write(koumoku_bangou_str + "　" \
#                         + koumoku.html + "\n")
#                 for koumoku2 in koumoku.koumoku_list:
#                     koumoku_bangou_str = henkan. \
#                             gou_bangou_henkan_zenkaku(
#                             koumoku2.koumoku_tuple)
#                     f.write(koumoku_bangou_str + "　" \
#                             + koumoku2.html + "\n")
#                     for koumoku3 in koumoku2.koumoku_list:
#                         koumoku_bangou_str = henkan. \
#                                 gou_bangou_henkan_zenkaku(
#                                 koumoku3.koumoku_tuple)
#                         f.write(koumoku_bangou_str + "　" \
#                                 + koumoku3.html + "\n")
#         for kou in self.kou_list[1:]:
#             f.write(kou.kou_bangou + "　" + kou.html + "\n")
#             for gou in kou.gou_list:
# #                 print("gou.gou_bangou_tuple", gou.gou_bangou_tuple)
#                 gou_bangou_str = henkan.gou_bangou_henkan_zenkaku(
#                         gou.gou_bangou_tuple)
# #                 print("gou_bangou_str", gou_bangou_str)
#                 f.write(gou_bangou_str + "　" + gou.html + "\n")
# #                 print(gou.honbun)
# #                 print(gou.html)
#                 for koumoku in gou.koumoku_list:
# #                     print(koumoku)
# #                     print(koumoku.koumoku_tuple)
#                     koumoku_bangou_str \
#                             = henkan.gou_bangou_henkan_zenkaku(
#                             koumoku.koumoku_tuple)
#                     f.write(koumoku_bangou_str + "　" \
#                             + koumoku.html + "\n")
#                     for koumoku2 in koumoku.koumoku_list:
#                         koumoku_bangou_str = henkan.jou_bangou_henkan_kansuji(
#                                 koumoku2.koumoku_tuple)
#                         f.write(koumoku_bangou_str + "　" \
#                                 + koumoku2.html + "\n")
#                         for koumoku3 in koumoku2.koumoku_list:
#                             koumoku_bangou_str = henkan. \
#                                     gou_bangou_henkan_zenkaku(
#                                     koumoku3.koumoku_tuple)
#                             f.write(koumoku_bangou_str + "　" \
#                                     + koumoku3.html + "\n")
#         f.close()
#         d.dprint_method_end()


    '''https://www.maytisk.com/python-marunum/'''
    def get_marumoji(self, val_str):
        val = int(val_str)
        if val > 20:
            return "(" + str(val) + ")"
        # ①を文字コードに変換[bytes型]
        maru_date = "①".encode("UTF8")
        # ①を文字コードに変換[int型]
        maru_code = int.from_bytes(maru_date, 'big')
        # 文字コードの変換
        maru_code += val - 1
        # 文字コードを文字に変換して返却
        return maru_code.to_bytes(3, "big").decode("UTF8")
#         return maru_code.to_bytes(4, "big").decode("UTF8")

#     def kubun_to_str(self, kubun, kubun_str):
#         if kubun == None:
#             return ""
#         if not isinstance(kubun, tuple):
#             return "/第" + kubun + kubun_str
#         return "/第" + kubun[0] + kubun_str + "の" + kubun[1]

#     ''' Obsidian用
#     # 第十二条　（外国税額の控除）
#     ## ①　内国法人…
#     …
#     #地方法人税/法/第３章（～）
#     '''
#     def save_markdown(self, file_name, zei, hourei,
#                 hen, shou, setsu, kan, moku):
#         f = open(file_name, "w", encoding='utf-8')
#         jou_bangou_str = henkan.jou_bangou_henkan_kansuji(
#                 self.bangou_tuple)
#         f.write("# " + "第" + jou_bangou_str)
#         if self.midashi != None:
#             f.write("　（" + self.midashi + "）\n")
#         else:
#             f.write("\n")
#         for kou in self.kou_list:
#             f.write("## " + self.get_marumoji(kou.kou_bangou) \
#                     + "　" + kou.html + "\n")
#             for gou in kou.gou_list:
# #                 print("gou.gou_bangou_tuple", gou.gou_bangou_tuple)
#                 gou_bangou_str = henkan.gou_bangou_henkan_zenkaku(
#                         gou.gou_bangou_tuple)
# #                 print("gou_bangou_str", gou_bangou_str)
#                 f.write("### " + gou_bangou_str + "　" + gou.html + "\n")
# #                 print(gou.honbun)
# #                 print(gou.html)
#                 for koumoku in gou.koumoku_list:
# #                     print(koumoku)
# #                     print(koumoku.koumoku_tuple)
#                     koumoku_bangou_str \
#                             = henkan.gou_bangou_henkan_zenkaku(
#                             koumoku.koumoku_tuple)
#                     f.write("#### " + koumoku_bangou_str + "　" \
#                             + koumoku.html + "\n")
#                     for koumoku2 in koumoku.koumoku_list:
#                         koumoku_bangou_str = henkan.gou_bangou_henkan_zenkaku(
#                                 koumoku2.koumoku_tuple)
#                         f.write("##### " + koumoku_bangou_str + "　" \
#                                 + koumoku2.html + "\n")
#                         for koumoku3 in koumoku2.koumoku_list:
#                             koumoku_bangou_str = henkan. \
#                                     gou_bangou_henkan_zenkaku(
#                                     koumoku3.koumoku_tuple)
#                             f.write("###### " + koumoku_bangou_str + "　" \
#                                     + koumoku3.html + "\n")
#         f.write("#" + zei + "/" + hourei)
#         d.dprint_name("区分", self.kubun)
#         if self.kubun[0] != None:
#             f.write(self.kubun_to_str(self.kubun[0],
#                     "編（" + hen + "）"))
#         if self.kubun[1] != None:
#             f.write(self.kubun_to_str(self.kubun[1],
#                     "章（" + shou + "）"))
#         if self.kubun[2] != None:
#             f.write(self.kubun_to_str(self.kubun[2],
#                     "節（" + setsu + "）"))
#         if self.kubun[3] != None:
#             f.write(self.kubun_to_str(self.kubun[3],
#                     "款（" + kan + "）"))
#         if self.kubun[4] != None:
#             f.write(self.kubun_to_str(self.kubun[4],
#                     "目（" + moku + "）"))
#
#         f.close()
# #         d.dprint_method_end()


    def __str__(self):
#         str_data = "【" + str(self.kubun) + "】"
        str_data = str(self.bangou_tuple)
        if self.midashi != None:
                str_data += "（" + self.midashi + "）"
        str_data += "\n"
        for kou in self.kou_list:
            str_data += kou.__str__()
        return str_data

