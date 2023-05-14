'''
Created on 2022/10/05

@author: sue-t
'''

import os
import re
from tkinter import messagebox

import c
import d
import e
from TransNum import TransNum
# from bun import Bun


class Md(object):
    '''
    条文の項・号ごとの
    マークダウンファイルの内容を
    管理する
    '''

    kubunHou = 0    # ～税法
    kubunRei = 1    # ～税法施行令
    kubunKi = 2     # ～税法施行規則

    matchFileName = re.compile(
            r'(?![._])([^法令規]+)' \
            '(法＿＿＿＿|法施行＿令|法施行規則)' \
            '(第([１２３４５６７８９０]+)条' \
            '(の([１２３４５６７８９０]+)' \
            '(の([１２３４５６７８９０]+))?)?)' \
            '(第([１２３４５６７８９０]+)項' \
            '((第([１２３４５６７８９０]+)号' \
            '(の([１２３４５６７８９０]+)' \
            '(の([１２３４５６７８９０]+))?)?))?)?' \
            '\..*'
            )


    def __init__(self, zeihou_mei, kubun,
                joubun_bangou, honbun,
                file_name=None, file_bun=None):
        '''
        zeihou_mei:
            税法名を示す文字列
            ex. "消費税"
        kubun:
            法、令、規則を区分するデータ
        joubun_bangou:
            条文の番号を示すタプル
            ex. ((1,),2,(3,)) 第１条第２項第３号
        honbun:
            条文の本文（加工文）を示す文字列
            （先頭の全角空白なし）
            ただし、ヘッダ・フッタ付きの
            文字列の場合あり
        file_name:
            ファイル名（パス名、拡張子付き）
        file_bun:
            ヘッダ・フッタ付きの加工文を示す文字列
        '''
        self.zeihou_mei = zeihou_mei
        self.kubun = kubun
        self.joubun_bangou = joubun_bangou
        self.honbun = honbun
        self.file_name = file_name
        self.file_bun = file_bun


    def set_file_bun(self, kakou_bun):
        self.file_bun = kakou_bun
        return


    @classmethod
    def create_file_name(cls, zeihou_mei, kubun,
            joubun_bangou):
        '''
        ファイル名を生成する
        '''
#         d.dprint_method_start()
#         d.dprint(zeihou_mei)
#         d.dprint(kubun)
#         d.dprint(joubun_bangou)
        if kubun == Md.kubunHou:
            kubun_mei = '法＿＿＿＿'
        elif kubun == Md.kubunRei:
            kubun_mei = '法施行＿令'
        else:
            assert(kubun == Md.kubunKi)
            kubun_mei = '法施行規則'
        list_name = [zeihou_mei, kubun_mei]

        jou_list = TransNum.bangou_tuple2str(
                joubun_bangou)
        list_name.extend(jou_list)
        list_name.append('.md')
        file_name = ''.join(list_name)
        del list_name
#         d.dprint(file_name)
#         d.dprint_method_end()
        return file_name


    def set_part(self, part):
        #         self.kubun = (None, None, None, None, None)
        # 編、章、節、款、目
        self.part = part

    def sakusei_file(self, folder):
        '''
        ファイルの内容(file_name,file_bun)を
        作成する
        '''
        d.dprint_method_end()
        d.dprint(folder)
        if self.kubun == self.kubunHou:
            kubun_mei = '法'
            kubun_file_mei = '法＿＿＿＿'
        elif self.kubun == self.kubunRei:
            kubun_mei = '法施行令'
            kubun_file_mei = '法施行＿令'
        else:
            assert(self.kubun == self.kubunKi)
            kubun_mei = '法施行規則'
            kubun_file_mei = '法施行規則'
        list_name = [self.zeihou_mei, kubun_file_mei]

        jou_list = TransNum.bangou_tuple2str(
                self.joubun_bangou)
        list_name.extend(jou_list)
        # jou_bangouが項か号の前提イロハは想定していない
        # 前提として項、号以下であり、条のことはない
        assert(jou_list[0] != '')
        assert(jou_list[1] != '')
        if jou_list[2] == '':
            # 項
            list_bun = [self.zeihou_mei, kubun_mei]
            list_bun.extend(jou_list)
            # [消費税法第三十条](消費税法第三十条)第一項
            # とは、しない。
        else:
            # 号
            list_bun = ['[' ,self.zeihou_mei, kubun_mei]
            list_bun.append(jou_list[0])
            list_bun.append(jou_list[1])
            list_bun.append('](')
            list_bun.append(self.zeihou_mei)
            list_bun.append(kubun_file_mei)
            list_bun.append(jou_list[0])
            list_bun.append(jou_list[1])
            list_bun.append(')')
            list_bun.append(jou_list[2])
        list_name.append('.md')
        file_name = ''.join(list_name)
        self.file_name = os.path.join(folder, file_name)
        del list_name

#         list_bun.append('\n\n　')
        list_bun.append('\n\n')
        list_bun.append(self.honbun)
        list_bun.append('\n\n')

        list_tag = ['#', self.zeihou_mei, kubun_mei]
        list_bun.extend(list_tag)
        list_bun.append('\n')

        if self.part != None:
            list_tag_kubun = list_tag.copy()
            list_tag_kubun.append('/')
            if self.part[0] != None:
                list_tag_kubun.append(self.part[0])
                list_bun.extend(list_tag_kubun)
                list_bun.append('\n')
                list_tag_kubun.append('/')
            if self.part[1] != None:
                list_tag_kubun.append(self.part[1])
                list_bun.extend(list_tag_kubun)
                list_bun.append('\n')
                list_tag_kubun.append('/')
            if self.part[2] != None:
                list_tag_kubun.append(self.part[2])
                list_bun.extend(list_tag_kubun)
                list_bun.append('\n')
                list_tag_kubun.append('/')
            if self.part[3] != None:
                list_tag_kubun.append(self.part[3])
                list_bun.extend(list_tag_kubun)
                list_bun.append('\n')
                list_tag_kubun.append('/')
            if self.part[4] != None:
                list_tag_kubun.append(self.part[4])
                list_bun.extend(list_tag_kubun)
                list_bun.append('\n')
                list_tag_kubun.append('/')

        list_tag.append('/')
        list_tag.append(jou_list[0])
        list_bun.extend(list_tag)
        list_bun.append('\n')
        list_tag.append('/')
        list_tag.append(jou_list[1])
        list_bun.extend(list_tag)
        list_bun.append('\n')
        if jou_list[2] != '':
            list_tag.append('/')
            list_tag.append(jou_list[2])
            list_bun.extend(list_tag)
            list_bun.append('\n')
        del list_tag
        del jou_list

        self.file_bun = ''.join(list_bun)
        del list_bun

        d.dprint(self.file_name)
        d.dprint(self.file_bun)
        d.dprint_method_end()
        return


    def save(self):
        d.dprint_method_start()
        d.dprint(self.file_name)
        with open(self.file_name,
            mode='w',
            encoding='UTF-8') as f:
            f.write(self.file_bun)
        d.dprint_method_end()
        return


    @classmethod
    def load(cls, folder_name, file_name):
        '''
        指定されたフォルダ・ファイル名のファイルを
        読込み、Mdデータを作成する。
        folder_name:
            フォルダ名
        file_name:
            ファイル名（拡張子付き）
        '''
        d.dprint_method_start()
        m = Md.matchFileName.match(file_name)
# ('消費税', '法施行令',
# '第４条の５', '４', 'の５', '５', None, None,
#  '第２項第９４号の３の２１', '２',
# '第９４号の３の２１', '第９４号の３の２１',
# '９４', 'の３の２１', '３', 'の２１', '２１')
        if m == None:
            d.dprint_method_end()
            return None
        full_name = os.path.join(folder_name, file_name)
        try:
            f = open(full_name,
                    "r",
                    encoding="UTF-8")
            read_list = f.readlines()
            f.close()
        except OSError as e:
#             messagebox.showwarning(
#                     'ファイル読込失敗', e)
            return None
        if m.group(2) == '法＿＿＿＿':
            kubun = Md.kubunHou
        elif m.group(2) == '法施行＿令':
            kubun = Md.kubunRei
        else:
            assert(m.group(2) == '法施行規則')
            kubun = Md.kubunKi
        if m.group(6) == None:
            jou_tuple = (int(m.group(4)),)
        elif m.group(8) == None:
            jou_tuple = (int(m.group(4)), int(m.group(6)))
        else:
            # 第１条の２の３の４ は、ない前提
            jou_tuple = (int(m.group(4)), int(m.group(6)),
                    int(m.group(8)))
        if m.group(10) == None:
            kou = None
        else:
            kou = int(m.group(10))
        if m.group(13) == None:
            gou_tuple = None
        elif m.group(15) == None:
            gou_tuple = (int(m.group(13)),)
        elif m.group(17) == None:
            gou_tuple = (int(m.group(13)),
                    int(m.group(15)))
        else:
            gou_tuple = (int(m.group(13)),
                    int(m.group(15)), int(m.group(17)))
        read_text = ''.join(read_list)
        del read_list
        md = Md(m.group(1), kubun,
                (jou_tuple, kou, gou_tuple),
                read_text)

        # TODO

        md.file_name = full_name
        md.file_bun = read_text
        d.dprint(md)
        d.dprint_method_end()
        return md


if __name__ == '__main__':
    md = Md.load(
            r'C:\Users\sue-t\Documents\000_保管庫\インボイス登録',
            '消費税法施行規則第２６条の３第１項第２号.md')
    exit(0)
