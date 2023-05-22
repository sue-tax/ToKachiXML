'''
Created on 2022/09/30

@author: sue-t
'''

import re

import c
import d
import e
from TransNum import TransNum
from md import Md


class Bun(object):
    '''
    税法条文の各文を処理するためのクラス
    '''

    kubunHou = 0    # ～税法
    kubunRei = 1    # ～税法施行令
    kubunKi = 2     # ～税法施行規則

    # 自身の法令の条
    matchJiJou = re.compile(
            r'(?<![法令])(?<!\[)' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' )
    # 自身の法令の条項
    matchJiJouKou = re.compile(
            r'(?<![法令])(?<!\[)' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '第([一二三四五六七八九十百千]+)項' )
    # 自身の法令の条項号
    matchJiJouKouGou = re.compile(
            r'(?<![法令])(?<!\[)' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '第([一二三四五六七八九十百千]+)項' \
            '(第([一二三四五六七八九十百千]+)号' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' )

    matchZenkou = re.compile(
            r'(?<![一二三四五六七八九十百千条項])(?<!\[)' \
            '((前条)|(前項)|(前号)' \
            '|(第([一二三四五六七八九十百千]+)項)' \
            '|(第([一二三四五六七八九十百千]+)号)' \
            ')' )

    # 他の法令の条
    matchTaJou = re.compile(
            r'(?<!\[)((法)|(施行令))' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' ) # (?!第)'
    # 他の法令の条項
    matchTaJouKou = re.compile(
            r'(?<!\[)((法)|(施行令))' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '第([一二三四五六七八九十百千]+)項' )
    # 他の法令の条項号
    matchTaJouKouGou = re.compile(
            r'(?<!\[)((法)|(施行令))' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '第([一二三四五六七八九十百千]+)項' \
            '(第([一二三四五六七八九十百千]+)号' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' )

    matchTaJouNiKiteisuru = re.compile(
            r'(?<!\[)([法令])' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '(ただし書)?に規定する' \
            '.*' \
            '((政令)|(\w+省令))で定める' )
    matchTaJouKouNiKiteisuru = re.compile(
            r'(?<!\[)([法令])' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '第([一二三四五六七八九十百千]+)項' \
            '(ただし書)?に規定する' \
            '.*' \
            '((政令)|(\w+省令))で定める' )
    matchTaJouKouGouNiKiteisuru = re.compile(
            r'(?<!\[)([法令])' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '第([一二三四五六七八九十百千]+)項' \
            '(第([一二三四五六七八九十百千]+)号' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '(ただし書)?に規定する' \
            '.*' \
            '((政令)|(\w+省令))で定める' )

    matchReiSadameru = re.compile(
            r'(?<!規定する)(?<!\[)(政令)で定める')
#             r'(?<!して)(政令)で定める')
    matchKiSadameru = re.compile(
            r'(?<!規定する)(?<!\[)' \
            '(((財務)|(法務)|(総務))省令)で定める')


    def __init__(self, zeihou_mei, kubun,
                 joubun_bangou, honbun):
        '''
        zeihou_mei:
            税法名を示す文字列
            ex. "消費税"
        kubun:
            法、令、規則を区分するデータ
        joubun_bangou:
            条文の番号を示すタプル
            ex. ((1,),(2,),(3,)) 第１条第２項第３号
        honbun:
            条文の本文を示す文字列
            （先頭の全角空白なし）
        '''
        self.zeihou_mei = zeihou_mei
        self.kubun = kubun
        if kubun == Bun.kubunHou:
            self.kubun_mei = '法'
        elif kubun == Bun.kubunRei:
            self.kubun_mei = '法施行令'
        else:
            assert(kubun == Md.kubunKi)
            self.kubun_mei = '法施行規則'
        self.joubun_bangou = joubun_bangou
        self.honbun = honbun
        self.kakou_bun = None
        self.soku = None


    @classmethod
    def md_to_bun(cls, md):
        bun = Bun(md.zeihou_mei, md.kubun,
                md.joubun_bangou, md.file_bun)
        bun.kakou_bun = md.file_bun
        bun.soku = md.soku
        return bun


    @classmethod
    def create_joubun_file_name(cls, zeihou_mei, kubun,
            soku,
            joubun_bangou):
        '''
        条文のファイル名の文字列を生成する
        zeihou_mei:
            税法名を示す文字列
            ex. "消費税"
        kubun:
            法、令、規則を区分するデータ
        soku:
            本則、附則を示すデータ
            ex. None, '＿' 本則
                '附則令和五年三月三十一日' 附則
        joubun_bangou:
            条文の番号を示すタプル
            ex. ((1,),(2,),(3,)) 第１条第２項第３号
        '''
        d.dprint_method_start()
#         d.dprint(zeihou_mei)
#         d.dprint(kubun)
#         d.dprint(joubun_bangou)
        if kubun == Bun.kubunHou:
            kubun_mei = '法＿＿＿＿'
        elif kubun == Bun.kubunRei:
            kubun_mei = '法施行＿令'
        else:
            assert(kubun == Md.kubunKi)
            kubun_mei = '法施行規則'
        list_name = [zeihou_mei, kubun_mei]

        if (soku == None) or (soku == '本則'):
            list_name.append('＿')
        else:
            list_name.append(soku)

        jou_list = TransNum.bangou_tuple2str(
                joubun_bangou)
        list_name.extend(jou_list)
        del jou_list
        joubun_name = ''.join(list_name)
        del list_name
#         d.dprint(joubun_name)
        d.dprint_method_end()
        return joubun_name


    def kakou1(self, jiko1_list, jogai_list=[]):
        '''
        本文を解析して加工文を作る。
        ただし、除外リストで指定されている文言は
        加工しない。
        '''
        d.dprint_method_start()
#         d.dprint(jiko1_list)
#         d.dprint(jogai_list)

        jogai_index_list = []
        for jogai in jogai_list:
            index = self.honbun.find(jogai)
            if index != -1:
                jogai_index_list.append(
                        (index, index + len(jogai)))
        jogai_sort_list = sorted(jogai_index_list,
                reverse=False, key=lambda x:x[0])
        del jogai_index_list

        self.kakou_bun = self.honbun
        src_list1 = self.kakou_ji_hourei(
                jogai_sort_list)
        src_list2 = self.kakou_zenkoutou(
                jogai_sort_list)
        src_list1.extend(src_list2)
        del src_list2
        self.kakou_jiko(jiko1_list, jogai_list)
        ref_list = self.kakou_ta_hourei(
                jogai_sort_list)
        del jogai_sort_list

#         d.dprint(self.kakou_bun)
#         d.dprint(ref_list)
        d.dprint_method_end()
        return (ref_list, src_list1)


    def kakou_ji_hourei(self, jogai_sort_list):
        '''
        自分自身の法令内の条文を参照している場合に
        self.kakou_bun に、ハイパーリンクの設定をする
        jogai_sort_list 内で、位置指定されている
        ものと一致していれば設定しない。
        （他の法律を参照している場合を手入力で除外）
        返り値 src_list は、参照している条文番号の
        リスト
        '''
        d.dprint_method_start()
#         d.dprint(jogai_sort_list)

        kakou_list = []
        src_list = []
        index = 0
        length = len(self.kakou_bun)
        while index < length:
            m_jou = Bun.matchJiJou.search(
                    self.kakou_bun, index)
            if m_jou != None:
#                 d.dprint(m_jou.group(0))
#                 d.dprint(m_jou.start(0))
#                 d.dprint(m_jou.end(0))
                # 除外リストの確認
                jogai_flag = False
                for jogai in jogai_sort_list:
#                     d.dprint(jogai)
                    if m_jou.end(0) < jogai[0]:
                        break
                    if m_jou.start(0) > jogai[1]:
                        continue
                    jogai_flag = True
                    break
                if jogai_flag:
                    kakou_list.append(self.kakou_bun
                            [index:m_jou.end(0)])
                    index = m_jou.end(0)
                    continue
#                 d.dprint("without jogai")
                m_gou = Bun.matchJiJouKouGou.search(
                    self.kakou_bun, index)
                if m_gou != None:
                    if m_jou.start(0) == m_gou.start(0):
                        kakou_list.append(
                                self.kakou_bun[
                                index:m_gou.start(0)])
                        kakou_list.append('[')
                        kakou_list.append(m_gou.group(0))
                        kakou_list.append('](')
                        link = self. \
                                translate_ji_jou_kou_gou(
                                m_gou)
                        kakou_list.append(link)
                        kakou_list.append(')')
                        src_list.append(link)
                        index = m_gou.end(0)
                        continue
                m_kou = Bun.matchJiJouKou.search(
                        self.kakou_bun, index)
                if m_kou != None:
                    if m_jou.start(0) == m_kou.start(0):
                        kakou_list.append(
                                self.kakou_bun[
                                index:m_kou.start(0)])
                        kakou_list.append('[')
                        kakou_list.append(m_kou.group(0))
                        kakou_list.append('](')
                        link = self.translate_ji_jou_kou(
                                m_kou)
                        kakou_list.append(link)
                        kakou_list.append(')')
                        src_list.append(link)
                        index = m_kou.end(0)
                        continue
                kakou_list.append(
                        self.kakou_bun \
                        [index:m_jou.start(0)])
                kakou_list.append('[')
                kakou_list.append(m_jou.group(0))
                kakou_list.append('](')
                link = self.translate_ji_jou(m_jou)
                kakou_list.append(link)
                # ToKachiでは、常に第１項とする
                kakou_list.append('第１項')
                kakou_list.append(')')
                src_list.append(link)
                index = m_jou.end(0)
                continue
            break
        kakou_list.append(self.kakou_bun[index:])
        self.kakou_bun = ''.join(kakou_list)
        del kakou_list
#         d.dprint(self.kakou_bun)
        d.dprint_method_end()
        return src_list


    def translate_ji_jou(self, m):
        '''
        ハイパーリンク用にファイル名の文字列を返す。
        自分自身の法令、本則・附則
        '''
        d.dprint_method_start()
        file_list = [ self.zeihou_mei ]
        if self.kubun == Bun.kubunHou:
            file_list.append("法＿＿＿＿")
        elif self.kubun == Bun.kubunRei:
#             file_list.append("法施行令＿")
            file_list.append("法施行＿令")
        else:
            assert(self.kubun == Bun.kubunKi)
            file_list.append("法施行規則")
        if self.soku == None:
            file_list.append("＿")
        elif self.soku == "本則":
            file_list.append("＿")
        else:
            file_list.append(self.soku)
        file_list.append('第')
        file_list.append(TransNum.k2a(m.group(2), True))
        file_list.append('条')
        if m.group(4) != None:
            file_list.append('の')
            file_list.append(
                    TransNum.k2a(m.group(4), True))
            if m.group(6) != None:
                file_list.append('の')
                file_list.append(
                        TransNum.k2a(m.group(6), True))
        file_name = ''.join(file_list)
        del file_list
#         d.dprint(file_name)
        d.dprint_method_end()
        return file_name


    def translate_ji_jou_kou(self, m):
        d.dprint_method_start()
        file_list = [ self.translate_ji_jou(m) ]
        file_list.append('第')
        file_list.append(TransNum.k2a(m.group(7), True))
        file_list.append('項')
        file_name = ''.join(file_list)
        del file_list
#         d.dprint(file_name)
        d.dprint_method_end()
        return file_name


    def translate_ji_jou_kou_gou(self, m):
#     m = Bun.matchJiJouKouGou.search(
# '第二条の三第四項第五号の六の七')
#     d.dprint(m.groups())
# ('第二条の三', '二', 'の三', '三', None, None,
#  '四',
#  '第五号の六の七', '五', 'の六の七', '六', 'の七', '七')

        d.dprint_method_start()
        file_list = [ self.translate_ji_jou_kou(m) ]
        file_list.append('第')
        file_list.append(TransNum.k2a(m.group(9), True))
        file_list.append('号')
        if m.group(11) != None:
            file_list.append('の')
            file_list.append(
                    TransNum.k2a(m.group(11), True))
            if m.group(13) != None:
                file_list.append('の')
                file_list.append(
                        TransNum.k2a(m.group(13), True))
        file_name = ''.join(file_list)
        del file_list
#         d.dprint(file_name)
        d.dprint_method_end()
        return file_name


    def kakou_zenkoutou(self, jogai_sort_list):
        '''
        前項、第１項、前号など
        ただし、全てを網羅することは諦める
        自分で入力することで、フォローする
        '''
        d.dprint_method_start()
#         d.dprint(jogai_sort_list)
        kakou_list = []
        src_list = []
        index = 0
        length = len(self.kakou_bun)
        while index < length:
#             d.dprint_name("index", index)
            m = Bun.matchZenkou.search(
                    self.kakou_bun, index)
            if m != None:
                # 除外リストの確認
                jogai_flag = False
                for jogai in jogai_sort_list:
                    if m.end(0) < jogai[0]:
                        break
                    if m.start(0) > jogai[1]:
                        continue
                    jogai_flag = True
                    break
                if jogai_flag:
                    kakou_list.append(self.kakou_bun
                            [index:m.end(0)])
                    index = m.end(0)
                    continue

                kakou_list.append(
                        self.kakou_bun[index:m.start(0)])
                kakou_list.append('[')
                kakou_list.append(m.group(0))
                kakou_list.append('](')
#                 d.dprint(self.joubun_bangou)
                if m.group(0) == '前条':
                    joubun_bangou = self.joubun_bangou
                    ref_bangou = (joubun_bangou[0],
                            joubun_bangou[1] - 1,
                            None)
                    joubun_bangou = self.joubun_bangou
                    jou_bangou = joubun_bangou[0]
                    if len(jou_bangou) == 3:
                        if jou_bangou[2] > 1:
                            ref_jou = (jou_bangou[0],
                                    jou_bangou[1],
                                    jou_bangou[2] - 1)
                        else:
                            ref_jou = (jou_bangou[0],
                                    jou_bangou[1])
                    elif len(jou_bangou) == 2:
                        if jou_bangou[1] > 1:
                            ref_jou = (jou_bangou[0],
                                    jou_bangou[1] - 1)
                        else:
                            ref_jou = (jou_bangou[0],)
                    else:
                        if jou_bangou[0] == 0:
                            # 附則で条番号がない場合に、
                            # 第０条としているため
                            continue
                        ref_jou = (jou_bangou[0] - 1,)
                    ref_bangou = (ref_jou, 1, None)
#                     d.dprint("前条")
#                     d.dprint(ref_bangou)
                elif m.group(0) == '前項':
#                     d.dprint(m.groups())
                    joubun_bangou = self.joubun_bangou
                    ref_bangou = (joubun_bangou[0],
                            joubun_bangou[1] - 1,
                            None)
#                     d.dprint("前項")
#                     d.dprint(ref_bangou)
                elif m.group(0) == '前号':
#                     d.dprint(m.groups())
                    joubun_bangou = self.joubun_bangou
                    gou_bangou = joubun_bangou[2]
                    # 所得税でエラー 読替規定のせい
                    if gou_bangou == None:
                        break   # 仕方がないので、諦める
                    if len(gou_bangou) == 3:
                        if gou_bangou[2] > 1:
                            ref_gou = (gou_bangou[0],
                                    gou_bangou[1],
                                    gou_bangou[2] - 1)
                        else:
                            ref_gou = (gou_bangou[0],
                                    gou_bangou[1])
                    elif len(gou_bangou) == 2:
                        if gou_bangou[1] > 1:
                            ref_gou = (gou_bangou[0],
                                    gou_bangou[1] - 1)
                        else:
                            ref_gou = (gou_bangou[0],)
                    else:
                        ref_gou = (gou_bangou[0] - 1,)
                    ref_bangou = (joubun_bangou[0],
                            joubun_bangou[1],
                            ref_gou)
#                     d.dprint("前号")
#                     d.dprint(ref_bangou)
                elif m.group(0)[-1] == '項':
                    # 第Ｘ項
#                     d.dprint(m.groups())
                    han = TransNum.k2a(m.group(6))
                    ref_bangou = (self.joubun_bangou[0],
                            han, None)
#                     d.dprint("項")
#                     d.dprint(ref_bangou)
                elif m.group(0)[-1] == '号':
#                     d.dprint(m.groups())
                    han = TransNum.k2a(m.group(8))
                    ref_bangou = (self.joubun_bangou[0],
                            self.joubun_bangou[1],
                            (han,))
#                     d.dprint("号")
#                     d.dprint(ref_bangou)
                else:
                    assert("error")
                jou_str = Bun.create_joubun_file_name(
                        self.zeihou_mei, self.kubun,
                        self.soku,
                        ref_bangou)
                kakou_list.append(jou_str)
                kakou_list.append(')')
                src_list.append(jou_str)
                index = m.end(0)
                continue
            break
        kakou_list.append(self.kakou_bun[index:])
        self.kakou_bun = ''.join(kakou_list)
        del kakou_list
#         d.dprint(self.kakou_bun)
        d.dprint_method_end()
        return src_list


    def kakou_jiko(self, jiko1_list, jogai_list):
        '''
        前条第二項など
        自分で入力することで、フォローする
        '''
        d.dprint_method_start()
#         d.dprint(jiko1_list)
#         d.dprint(jogai_list)
        # TODO jogai_sort_list 除外リストの処理　未作成
        for jiko1 in jiko1_list:
            if jiko1 in jogai_list:
                continue
            index = self.kakou_bun.find(jiko1[2])
            if index != -1:
                shin_bun = '{}[{}]({}){}'.format( \
                        self.kakou_bun[:index],
                        jiko1[2],
                        jiko1[3][0],
                        self.kakou_bun[index+len(jiko1[2]):]
                        )
                self.kakou_bun = shin_bun
#         d.dprint(self.kakou_bun)
        d.dprint_method_end()
        return


    def kakou_ta_hourei(self, jogai_sort_list):
        '''
        例えば、
        消費税法施行令第４６条第１項.mdの
        「法第三十条第一項に規定する」を
        「[法第三十条第一項](消費税法第３０条第１項)」に
        加工する。
        そして、
        消費税法第３０条第１項.mdの
        「基礎として計算した金額その他の政令で定める」を
        「基礎として計算した金額その他の
        [政令](消費税法施行令第４６条第１項)で定める」に
        加工するために、
        [ ('消費税法', kubunHou,
        '＿', (30 , 1, None)) ]を返す。
        フォルダ内に他の法律が混在する可能性もあるので
        法律名も入れておくことにする。
        ただし、法第３０条第１項に複数の「政令」が
        ある場合は、正しい対応が分からない可能性はある。
        手作業で修正することを前提とする。
        '''
        d.dprint_method_start()
#         d.dprint(jogai_sort_list)
        kakou_list = []
        ref_pair_list = []
        index = 0
        length = len(self.kakou_bun)
        while index < length:
            m_jou = Bun.matchTaJou.search(
                    self.kakou_bun, index)
            if m_jou != None:
                # 除外リストの確認
                jogai_flag = False
                for jogai in jogai_sort_list:
#                     d.dprint(jogai)
                    if m_jou.end(0) < jogai[0]:
                        break
                    if m_jou.start(0) > jogai[1]:
                        continue
                    jogai_flag = True
                    break
                if jogai_flag:
                    kakou_list.append(self.kakou_bun
                            [index:m_jou.end(0)])
                    index = m_jou.end(0)
                    continue
#                 d.dprint("without jogai")
                m_gou = Bun.matchTaJouKouGou.search(
                        self.kakou_bun, index)
                if m_gou != None:
                    if m_jou.start(0) == m_gou.start(0):
#                         d.dprint("matchTaJouKouGou")
#                         d.dprint(m_gou)
                        kakou_list.append(
                                self.kakou_bun
                                [index:m_gou.start(0)])
                        kakou_list.append('[')
                        kakou_list.append(m_gou.group(0))
                        kakou_list.append('](')
                        (link, ref_pair_tuple) = \
                                self.translate_ta_jou_kou_gou(
                                m_gou)
                        kakou_list.append(link)
                        kakou_list.append(')')
                        if ref_pair_tuple != None:
                            ref_pair_list.append(
                                    ref_pair_tuple)
                        index = m_gou.end(0)
                        continue
                m_kou = Bun.matchTaJouKou.search(
                        self.kakou_bun, index)
                if m_kou != None:
                    if m_jou.start(0) == m_kou.start(0):
#                         d.dprint("matchTaJouKou")
#                         d.dprint(m_kou)
                        kakou_list.append(
                                self.kakou_bun[
                                index:m_kou.start(0)])
                        kakou_list.append('[')
                        kakou_list.append(m_kou.group(0))
                        kakou_list.append('](')
                        (link, ref_pair_tuple) = \
                                self.translate_ta_jou_kou(
                                m_kou)
                        kakou_list.append(link)
                        kakou_list.append(')')
                        if ref_pair_tuple != None:
                            ref_pair_list.append(
                                    ref_pair_tuple)
                        index = m_kou.end(0)
                        continue
                kakou_list.append(
                        self.kakou_bun[
                        index:m_jou.start(0)])
                kakou_list.append('[')
                kakou_list.append(m_jou.group(0))
                kakou_list.append('](')
                (link, ref_pair_tuple) = \
                        self.translate_ta_jou(m_jou)
                kakou_list.append(link)
                kakou_list.append(')')
                if ref_pair_tuple != None:
                    ref_pair_list.append(
                            ref_pair_tuple)
                index = m_jou.end(0)
                continue
            break
        kakou_list.append(self.kakou_bun[index:])
        self.kakou_bun = ''.join(kakou_list)
        del kakou_list
#         d.dprint(ref_pair_list)
        d.dprint_method_end()
        return ref_pair_list


    def translate_ta_jou(self, m):
        '''
        第Ｘ条でも、第Ｘ条第１項とみなして処理する
        ('消費税法', kubunHou,
        '＿',
         (30 , 1, None))を返す。
        '''
        d.dprint_method_start()
        file_list = [ self.zeihou_mei ]
        if m.group(1) == "法":
            file_list.append("法＿＿＿＿")
            ref_kubun = Md.kubunHou
        elif m.group(1) == "施行令":
            file_list.append("法施行＿令")
            ref_kubun = Md.kubunRei
        else:
            e.eprint("translate_ta_jou 法令以外")
            assert(False)
        # 他の法令については、本則に限定
        file_list.append("＿")
        file_list.append('第')
        (han, zen) = TransNum.k2a_double(m.group(5))
        file_list.append(zen)
        file_list.append('条')
        i_han = int(han)
        ref_tuple = ((i_han, ), 1, None)
        if m.group(7) != None:
            file_list.append('の')
            (han2, zen2) = TransNum.k2a_double(
                    m.group(7))
            file_list.append(zen2)
            i_han2 = int(han2)
            ref_tuple = ((i_han, i_han2), 1, None)
            if m.group(9) != None:
                file_list.append('の')
                (han3, zen3) = \
                        TransNum.k2a_double(m.group(9))
                file_list.append(zen3)
                i_han3 = int(han3)
                ref_tuple = ((i_han, i_han2, i_han3),
                         1, None)
        file_list.append('第１項')
        file_name = ''.join(file_list)
        del file_list
        m_niKiteisuru = Bun.matchTaJouNiKiteisuru.search(
                self.kakou_bun, m.start())
        if m_niKiteisuru != None:
            # self.soku が正しく機能するかは未確認
            ref_pair_tuple = (self.zeihou_mei, ref_kubun,
                    '＿',
                    ref_tuple)
        else:
            ref_pair_tuple = None
#         d.dprint(file_name)
#         d.dprint(ref_pair_tuple)
        d.dprint_method_end()
        return (file_name, ref_pair_tuple)


    def translate_ta_jou_kou(self, m):
        '''
        ('消費税法', kubunHou, (30 , 1, None))を返す。
        '''
        d.dprint_method_start()
#         d.dprint(m.groups())
        file_list = [ self.zeihou_mei ]
        if m.group(1) == "法":
            file_list.append("法＿＿＿＿")
            ref_kubun = Md.kubunHou
        elif m.group(1) == "施行令":
            file_list.append("法施行＿令")
            ref_kubun = Md.kubunRei
        else:
            e.eprint("translate_ta_jou_kou 法令以外")
            assert(False)
        # 他の法令については、本則に限定
        file_list.append("＿")
        file_list.append('第')
        (han, zen) = TransNum.k2a_double(m.group(5))
        file_list.append(zen)
        file_list.append('条')
        i_han = int(han)
        ref_tuple = ((i_han, ), None, None)
        if m.group(7) != None:
            file_list.append('の')
            (han2, zen2) = TransNum.k2a_double(
                    m.group(7))
            file_list.append(zen2)
            i_han2 = int(han2)
            ref_tuple = ((i_han, i_han2), None, None)
            if m.group(9) != None:
                file_list.append('の')
                (han3, zen3) = \
                        TransNum.k2a_double(m.group(9))
                file_list.append(zen3)
                i_han3 = int(han3)
                ref_tuple = ((i_han, i_han2, i_han3),
                         None, None)
        file_list.append('第')
        (han, zen) = TransNum.k2a_double(m.group(10))
        file_list.append(zen)
        file_list.append('項')
        i_han = int(han)
        ref_tuple = (ref_tuple[0], i_han, None)
        file_name = ''.join(file_list)
        del file_list
        m_niKiteisuru = Bun.matchTaJouKouNiKiteisuru. \
                search(self.kakou_bun, m.start())
        if m_niKiteisuru != None:
            ref_pair_tuple = (self.zeihou_mei,
                    ref_kubun,
                    '＿',
                    ref_tuple)
        else:
            ref_pair_tuple = None
#         d.dprint(file_name)
#         d.dprint(ref_pair_tuple)
        d.dprint_method_end()
        return (file_name, ref_pair_tuple)


    def translate_ta_jou_kou_gou(self, m):
        d.dprint_method_start()
        file_list = [ self.zeihou_mei ]
        if m.group(1) == "法":
            file_list.append("法＿＿＿＿")
            ref_kubun = Md.kubunHou
        elif m.group(1) == "施行令":
            file_list.append("法施行＿令")
            ref_kubun = Md.kubunRei
        else:
            e.eprint("translate_ta_jou_kou_gou 法令以外")
            assert(False)
        # 他の法令については、本則に限定
        file_list.append("＿")
        file_list.append('第')
        (han, zen) = TransNum.k2a_double(m.group(5))
        file_list.append(zen)
        file_list.append('条')
        i_han = int(han)
        ref_tuple = ((i_han, ), None, None)
        if m.group(7) != None:
            file_list.append('の')
            (han2, zen2) = TransNum.k2a_double(
                    m.group(7))
            file_list.append(zen2)
            i_han2 = int(han2)
            ref_tuple = ((i_han, i_han2), None, None)
            if m.group(9) != None:
                file_list.append('の')
                (han3, zen3) = \
                        TransNum.k2a_double(m.group(9))
                file_list.append(zen3)
                i_han3 = int(han3)
                ref_tuple = ((i_han, i_han2, i_han3),
                         None, None)
        file_list.append('第')
        (han, zen) = TransNum.k2a_double(m.group(10))
        file_list.append(zen)
        file_list.append('項')
        i_kou = int(han)
#         ref_tuple = (ref_tuple[1], i_han, None)
        file_list.append('第')
        (han, zen) = TransNum.k2a_double(m.group(12))
        file_list.append(zen)
        file_list.append('号')
        i_han = int(han)
        ref_tuple = (ref_tuple[0], i_kou,
                (i_han,))
        if m.group(14) != None:
            file_list.append('の')
            (han2, zen2) = TransNum.k2a_double(
                    m.group(14))
            file_list.append(zen2)
            i_han2 = int(han2)
            ref_tuple = (ref_tuple[0], i_kou,
                    (i_han, i_han2))
            if m.group(16) != None:
                file_list.append('の')
                (han3, zen3) = \
                        TransNum.k2a_double(m.group(16))
                file_list.append(zen3)
                i_han3 = int(han3)
                ref_tuple = (ref_tuple[0], i_kou,
                        '＿',
                        (i_han, i_han2, i_han3))
        file_name = ''.join(file_list)
        del file_list
        m_niKiteisuru = Bun.matchTaJouKouGouNiKiteisuru. \
                search(self.kakou_bun, m.start())
        if m_niKiteisuru != None:
            ref_pair_tuple = (self.zeihou_mei, ref_kubun,
                    '＿',
                    ref_tuple)
        else:
            ref_pair_tuple = None
#         d.dprint(file_name)
#         d.dprint(ref_pair_tuple)
        d.dprint_method_end()
        return (file_name, ref_pair_tuple)


    def kakou2_rei(self, zeihou_mei, rei_list):
        '''
        加工文のうち「～政令に定める」を解析して
        加工文を作る。
        rei_list:
            [ (1,2,3,4) , (1,3,4,0) ]
            [政令](消費税法施行令第１条第２項第３号二)に定める
            [政令](消費税法施行令第１条第３項第４号)に定める
        '''
        d.dprint_method_start()
#         d.dprint(rei_list)
        list_msg = self.kakou_sadameru_rei(zeihou_mei,
                rei_list)
        d.dprint_method_end()
        return list_msg


    def kakou2_ki(self, zeihou_mei, ki_list):
        '''
        加工文のうち「～省令に定める」を解析して
        加工文を作る。
        '''
        d.dprint_method_start()
#         d.dprint(ki_list)
        list_msg = self.kakou_sadameru_ki(zeihou_mei,
                ki_list)
        d.dprint_method_end()
        return list_msg


    def kakou_sadameru_rei(self, zeihou_mei, rei_list):
        d.dprint_method_start()
#         d.dprint(zeihou_mei)
#         d.dprint(rei_list)
        iter_m = Bun.matchReiSadameru.finditer(
                self.kakou_bun)
        list_m = list(iter_m)
        l =  len(list_m)
        if len(rei_list) < l:
            list_msg = [ "政令が探し足りない " \
                    "必要数={}, 見つかった数={}\n". \
                    format(l, len(rei_list)) ]
            return list_msg
        if len(rei_list) > l:
            list_msg = [ "見つかった政令が多すぎる " \
                    "必要数={}, 見つかった数={}\n". \
                    format(l, len(rei_list)) ]
            return list_msg

        kakou_list = []
        index = 0
        for (m, rei) in zip(list_m, rei_list):
            kakou_list.append(
                    self.kakou_bun[index:m.start(0)])
            kakou_list.append('[')
            kakou_list.append(m.group(1))
            kakou_list.append('](')
            kakou_list.append(rei[0]) # TODO
            kakou_list.append(')')
            kakou_list.append('で定める')
            index = m.end(0)
        kakou_list.append(self.kakou_bun[index:])
        self.kakou_bun = ''.join(kakou_list)
        del kakou_list
#         d.dprint(self.kakou_bun)
        d.dprint_method_end()
        return None


    def kakou_sadameru_ki(self, zeihou_mei, ki_list):
        d.dprint_method_start()
#         d.dprint(ki_list)
        iter_m = Bun.matchKiSadameru.finditer(
                self.kakou_bun)
        list_m = list(iter_m)
        l =  len(list_m)
        if len(ki_list) < l:
            list_msg = [ "省令が探し足りない " \
                    "必要数={}, 見つかった数={}\n". \
                    format(l, len(ki_list)) ]
            return list_msg
        if len(ki_list) > l:
            list_msg = [ "見つかった省令が多すぎる " \
                    "必要数={}, 見つかった数={}\n". \
                    format(l, len(ki_list)) ]
            return list_msg

        kakou_list = []
        index = 0
        for (m, ki) in zip(list_m, ki_list):
            kakou_list.append(
                    self.kakou_bun[index:m.start(0)])
            kakou_list.append('[')
            kakou_list.append(m.group(1))
            kakou_list.append('](')
            kakou_list.append(ki[0])
            kakou_list.append(')')
            kakou_list.append('で定める')
            index = m.end(0)
        kakou_list.append(self.kakou_bun[index:])
#         d.dprint(kakou_list)
        self.kakou_bun = ''.join(kakou_list)
        del kakou_list
#         d.dprint(self.kakou_bun)
        d.dprint_method_end()
        return None


    def get_kakou_bun(self):
        return self.kakou_bun


#"他の者から受けた第七十条の九第二項第一号に掲げる課税資産の譲渡等に係る課税仕入れ")
#             "[法第三十条第一項](消費税法第３０条第１項)に規定する政令で定めるところにより計算した金額は、次の各号に掲げる課税仕入れ（特定課税仕入れに該当するものを除く。以下この章において同じ。）の区分に応じ当該各号に定める金額の合計額に百分の七十八を乗じて算出した金額とする。"
# ただし、当該適格請求書発行事業者が行う事業の性質上、適格請求書を交付することが困難な課税資産の譲渡等として[政令](消費税法施行令第７０条の９第２項)で定めるものを行う場合は、この限りでない。

if __name__ == '__main__':
    text_ = '法第六十九条の四第一項に' \
            '規定する被相続人等の宅地等のうち' \
            '政令で定めるものは、相続の開始の直前において、'\
            '当該被相続人等の同項に規定する事業の用'
    matchTaJouKou = re.compile(
            r'(?<!\[)((法)|(施行令))' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '第([一二三四五六七八九十百千]+)項' )
    matchTaJouKouNiKiteisuru = re.compile(
            r'(?<!\[)([法令])' \
            '(第([一二三四五六七八九十百千]+)条' \
            '(の([一二三四五六七八九十百千]+)' \
            '(の([一二三四五六七八九十百千]+))?)?)' \
            '第([一二三四五六七八九十百千]+)項' \
            '(ただし書)?に規定する' \
            '.*' \
            '((政令)|(\w+省令))で定める' )
    m = matchTaJouKou.search(text_)
    d.dprint(m)
    d.dprint(m.groups())
    m = matchTaJouKouNiKiteisuru.search(text_)
    d.dprint(m)
    d.dprint(m.groups())
