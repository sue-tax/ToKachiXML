'''
Created on 2023/05/13

@author: sue-t
'''

import c
import d
import e

from jou_jou import Jou_jou
from jou_kou import Jou_kou
from jou_gou import Jou_gou
from jou_koumoku import Jou_koumoku

from ToKachi import save_file

from TransNum import TransNum

import os
from lxml import etree
# import xml.etree.ElementTree as ET
# from xml import etree

__version__ = '0.4.8'


class Jou_xml(object):

    def __init__(self, file):
        tree = etree.parse(file)
        root = tree.getroot()
        jou_list = []
        # 本則
        articles = tree.xpath('//MainProvision//Article')
        self.proc_article("本則", jou_list, articles)
        # 附則
        fusokus = tree.xpath('//SupplProvision')
        for fusoku in fusokus:
            fusoku_name = fusoku.attrib.get("AmendLawNum")
            if fusoku_name == None:
                str_fusoku = "附則"
            else:
                index = fusoku_name.find("日")
                # 漢数字を全角アラビア数字に
                str_hizuke = fusoku_name[:index+1] \
                        .replace('元', '一')
                str_ara = TransNum.k2a(
                        str_hizuke, True)
                str_fusoku = "附則" + str_ara
            articles = fusoku.xpath(".//Article")
            if len(articles) != 0:
                self.proc_article(str_fusoku,
                        jou_list, articles)
            else:
                # 附則の中には、第Ｘ条がなく、
                # 項のみの場合あり
                self.proc_jou_nashi(str_fusoku,
                        jou_list, fusoku)
        self.tree = tree
        self.jou_list = jou_list

    def proc_jou_nashi(self, soku, jou_list, fusoku):
        '''
        条（article）がないfusokuで示される附則を
        仮の条として、各項を処理して
        jou_listに条文データを設定する。
        sokuは、附則名を示す。
        '''
        paragraphs = fusoku.xpath('Paragraph')
        kou = self.create_kou(soku, midashi=None,
                jou_bangou_tuple=(0,),
                paragraph=paragraphs[0])
        jou = Jou_jou(bangou_tuple=(0,), kou=kou)
        for paragraph in paragraphs[1:]:
            kou = self.create_kou(soku,
                    midashi=None,
                    jou_bangou_tuple=(0,),
                    paragraph=paragraph)
            jou.tsuika_kou(kou)
        jou.set_kubun((None, None,
                None, None, None))
        jou.set_soku(soku)
#         jou.set_midashi(midashi)
        jou_list.append(jou)


    def proc_article(self, soku, jou_list, articles):
        '''
        articlesで示される本則、附則内の全条文を処理し、
        jou_listに条文データを設定する。
        sokuは、本則か附則（附則名）を示す。
        '''
        for article in articles:
            num = article.get('Num')
            if ':' in num:
                # '29:30' 削除のパターン
                continue
            jou_bangou_tuple = self.num2tuple(num)
            # 編の名前
            part = article.xpath('./ancestor::Part')
            if len(part) != 0:
                part_title = part[0].xpath(
                        './PartTitle')
                if len(part_title) != 0:
                    part_str = part_title[0]. \
                            text.replace('　', '')
                    part_str = TransNum.k2a(
                            part_str, True)
                else:
                    part_str = None
            else:
                part_str = None
            # 章の名前
            chapter = article.xpath(
                    './ancestor::Chapter')
            if len(chapter) != 0:
                chapter_title = chapter[0].xpath(
                        './ChapterTitle')
                if len(chapter_title) != 0:
                    chapter_str = chapter_title[0]. \
                            text.replace('　', '')
                    chapter_str = TransNum.k2a(
                            chapter_str, True)
                else:
                    chapter_str = None
            else:
                chapter_str = None
            # 節の名前
            section = article.xpath(
                    './ancestor::Section')
            if len(section) != 0:
                section_title = section[0].xpath(
                        './SectionTitle')
                if len(section_title) != 0:
                    section_str = section_title[0]. \
                            text.replace('　', '')
                    section_str = TransNum.k2a(
                            section_str, True)
                else:
                    section_str = None
            else:
                section_str = None
            # 款の名前
            subsection = article.xpath(
                    './ancestor::Subsection')
            if len(subsection) != 0:
                subsection_title = subsection[0].xpath(
                        './SubsectionTitle')
                if len(subsection_title) != 0:
                    subsection_str = subsection_title[0]. \
                            text.replace('　', '')
                    subsection_str = TransNum.k2a(
                            subsection_str, True)
                else:
                    subsection_str = None
            else:
                subsection_str = None
            # 目の名前
            division = article.xpath(
                    './ancestor::Division')
            if len(division) != 0:
                division_title = division[0].xpath(
                        './DivisionTitle')
                if len(division_title) != 0:
                    division_str = division_title[0]. \
                            text.replace('　', '')
                    division_str = TransNum.k2a(
                            division_str, True)
                else:
                    division_str = None
            else:
                division_str = None
            # 見出し
            title = article.xpath("ArticleCaption")
            if len(title) != 0:
                midashi = title[0].text
            else:
                midashi = ""

            paragraphs = article.xpath('Paragraph')
            kou = self.create_kou(soku, midashi,
                    jou_bangou_tuple,
                    paragraphs[0])
            jou = Jou_jou(jou_bangou_tuple, kou)
#             jou = Jou_jou((jou_bangou_tuple,), kou)
            for paragraph in paragraphs[1:]:
                kou = self.create_kou(soku, midashi,
                        jou_bangou_tuple,
                        paragraph)
                jou.tsuika_kou(kou)
            jou.set_kubun((part_str, chapter_str,
                    section_str, subsection_str,
                    division_str))
            jou.set_soku(soku)
            jou.set_midashi(midashi)
            jou_list.append(jou)

    def create_kou(self, soku, midashi,
            jou_bangou_tuple, paragraph):
        num = paragraph.get('Num')
        kou_bangou = int(num)
#         d.dprint(jou_bangou_tuple)
#         d.dprint(kou_bangou)

        sentences = paragraph.xpath(
                './ParagraphSentence/Sentence')
        honbun_list = []
        for sentence in sentences:
            # 本文がないことがある
            # 例　相続税法附則平成一二年五月三一日
            # 　　　第３７条第１項
            if sentence.text != None:
                honbun_list.append(sentence.text)
        # 表
        tables = paragraph.xpath('.//Table')
        table_text = self.create_table(tables)
        honbun_list.append(table_text)

        gou_list = []
        items = paragraph.xpath('.//Item')
        for item in items:
            gou = self.create_gou(
                    soku, midashi,
                    jou_bangou_tuple, kou_bangou,
                    item)
            if gou != None:
                gou_list.append(gou)

        honbun = ''.join(honbun_list)
        kou = Jou_kou(jou_bangou_tuple, kou_bangou,
                      honbun, gou_list)
        kou.set_soku(soku)
        kou.set_midashi(midashi)
        item_title = paragraph.xpath('./ParagraphNum')
        kou.set_item_title(item_title[0].text)
        return kou

    def create_gou(self, soku, midashi,
            jou_bangou_tuple, kou_bangou,
            item):
        # d.dprint_method_start()
        num = item.get('Num')
        if ':' in num:  # 略や削除のときに、ある
            return None
        gou_bangou_tuple = self.num2tuple(num)
        # 文、項目列記、表があるようだ
        # TODO 本来は順番を考慮して処理すべき
        sentences = item.xpath(
                './ItemSentence/Sentence')
        honbun_list = []
        for sentence in sentences:
            if sentence.text != None:
                honbun_list.append(sentence.text)
        # 項目列記
        columns = item.xpath(
                './ItemSentence/Column')
        if len(columns) != 0:
            text_column = []
            for column in columns:
                sentences = column.xpath(
                        './Sentence')
                text_sentence = ''
                for sentence in sentences:
                    if sentence.text != None:
                        text_sentence = \
                                text_sentence + \
                                sentence.text
                text_column.append(text_sentence)
            text_columns = '　'.join(text_column)
            honbun_list.append(text_columns)
        # 表
        tables = item.xpath('.//Table')
        table_text = self.create_table(tables)
        honbun_list.append(table_text)

        koumoku_list = []
        subitem1s = item.xpath('./Subitem1')
        for subitem1 in subitem1s:
            koumoku = self.create_koumoku(
                    soku, midashi,
                    jou_bangou_tuple, kou_bangou,
                    gou_bangou_tuple,
                    subitem1)
            koumoku_list.append(koumoku)

        honbun = ''.join(honbun_list)
        gou = Jou_gou(jou_bangou_tuple, kou_bangou,
                gou_bangou_tuple,
                honbun, koumoku_list)
        gou.set_soku(soku)
        gou.set_midashi(midashi)
        item_title = item.xpath('./ItemTitle')
        gou.set_item_title(item_title[0].text)
        # d.dprint_method_end()
        return gou

    def create_koumoku(self, soku, midashi,
            jou_bangou_tuple, kou_bangou,
            gou_bangou_tuple, subitem1):
        # イ、ロ、ハ
        titles = subitem1.xpath('./Subitem1Title')
        koumoku_tuple = (titles[0].text,)

        sentences = subitem1.xpath(
                './Subitem1Sentence/Sentence')
        honbun_list = []
        for sentence in sentences:
            if sentence.text != None:
                honbun_list.append(sentence.text)
        columns = subitem1.xpath(
                './ItemSentence/Column')
        for column in columns:
            sentences = column.xpath('./Sentence')
            for sentence in sentences:
                honbun_list.append(sentence.text)
        tables = subitem1.xpath('.//Table')
        table_text = self.create_table(tables)
        honbun_list.append(table_text)

        koumoku2_list = []
        subitem2s = subitem1.xpath('./Subitem2')
        for subitem2 in subitem2s:
            koumoku2 = self.create_koumoku2(
                    soku, midashi,
                    jou_bangou_tuple, kou_bangou,
                    gou_bangou_tuple, koumoku_tuple,
                    subitem2)
            koumoku2_list.append(koumoku2)

        honbun = ''.join(honbun_list)
        koumoku = Jou_koumoku(jou_bangou_tuple, kou_bangou,
                gou_bangou_tuple, koumoku_tuple,
                honbun, koumoku2_list)
        # ToKachiでは号までなので、不要だが
        koumoku.set_soku(soku)
        koumoku.set_midashi(midashi)
        return koumoku

    def create_koumoku2(self, soku, midashi,
            jou_bangou_tuple, kou_bangou,
            gou_bangou_tuple, koumoku_tuple, subitem2):
        # （２）
        titles = subitem2.xpath(
                './Subitem2Title')
        koumoku2_tuple = koumoku_tuple \
                + (titles[0].text,)

        sentences = subitem2.xpath(
                './Subitem2Sentence/Sentence')
        # TODO honbun_list
        honbun = ''
        for sentence in sentences:
            if sentence.text != None:
                honbun = honbun + sentence.text
        columns = subitem2.xpath(
                './ItemSentence/Column')
        for column in columns:
            sentences = column.xpath('./Sentence')
            for sentence in sentences:
                honbun = honbun + sentence.text
        tables = subitem2.xpath('.//Table')
        table_text = self.create_table(tables)
        honbun = honbun + table_text

        koumoku3_list = []
        subitem3s = subitem2.xpath('./Subitem3')
        for subitem3 in subitem3s:
            koumoku3 = self.create_koumoku3(
                    soku, midashi,
                    jou_bangou_tuple, kou_bangou,
                    gou_bangou_tuple, koumoku2_tuple,
                    subitem3)
            koumoku3_list.append(koumoku3)

        koumoku = Jou_koumoku(
                jou_bangou_tuple, kou_bangou,
                gou_bangou_tuple, koumoku2_tuple,
                honbun, koumoku3_list)
        koumoku.set_soku(soku)
        koumoku.set_midashi(midashi)
        return koumoku

    def create_koumoku3(self, soku, midashi,
            jou_bangou_tuple, kou_bangou,
            gou_bangou_tuple, koumoku_tuple, subitem3):
        # ⅰ ?
        titles = subitem3.xpath('./Subitem3Title')
        koumoku3_tuple = koumoku_tuple \
                + (titles[0].text,)

        sentences = subitem3.xpath(
                './Subitem3Sentence/Sentence')
        honbun = ''
        for sentence in sentences:
            if sentence.text != None:
                honbun = honbun + sentence.text
        columns = subitem3.xpath(
                './ItemSentence/Column')
        for column in columns:
            sentences = column.xpath('./Sentence')
            for sentence in sentences:
                honbun = honbun + sentence.text
        tables = subitem3.xpath('.//Table')
        table_text = self.create_table(tables)
        honbun = honbun + table_text
        koumoku4_list = []
        subitem4s = subitem3.xpath('./Subitem4')
        for subitem4 in subitem4s:
            # TODO これでは対応できない
            # Sbuitem10まで一応ある
            koumoku4 = self.create_koumoku3(
                    jou_bangou_tuple, kou_bangou,
                    gou_bangou_tuple, koumoku3_tuple,
                    subitem4)
            koumoku4_list.append(koumoku4)

        koumoku = Jou_koumoku(
                jou_bangou_tuple, kou_bangou,
                gou_bangou_tuple, koumoku3_tuple,
                honbun, koumoku4_list)
        koumoku.set_soku(soku)
        koumoku.set_midashi(midashi)
        return koumoku

    def create_table(self, tables):
        text_list = []
        for table in tables:
            tableRows = table.xpath('TableRow')
            topRow = tableRows[0]
            topColumns = topRow.xpath('TableColumn')
            # 最初の１行だけ表示が異なるので
            # 意図的に追加した
            # 要検討
            if len(topColumns) == 2:
                text_list.append('\n\n| 上段 | 下段 |\n' \
                        + '| ---- | ---- |\n')
            elif len(topColumns) == 3:
                text_list.append(
                    '\n\n| 上段 | 中段 | 下段 |\n' \
                    + '| ---- | ---- | ---- |\n')
            else:
                text_list.append(
                    '\n\n| 上段 | 　　 | 　　 | 下段 |\n' \
                    + '| ---- | ---- | ---- | ---- |\n')
            for tableRow in tableRows:
                tableColumns = tableRow.xpath(
                        'TableColumn')
                text_list.append('|')
                for tableColumn in tableColumns:
                    sentences = tableColumn.xpath(
                            './Sentence')
                    for sentence in sentences:
                        if sentence.text != None:
                            text_list.append(
                                    ' ' \
                                    + sentence.text \
                                    + ' |' )
                        else:
                            text_list.append(
                                    '    |')
                text_list.append('\n')
        text = ''.join(text_list)
        return text

    def create_appdxTable(self):
        # 別表はmdファイルを作るだけ

        # TODO 所得税法別表３，５などが対応できない
        # colspan, rawspanなどの解析が必要

        appdxTables = self.tree.xpath('//AppdxTable')
        appdx_list = []
        for appdxTable in appdxTables:
            appd_titles = appdxTable.xpath(
                    "./AppdxTableTitle")
            str_title = TransNum.k2a(
                    appd_titles[0].text, True)
            text_list = [str_title, '\n']

            # TODO 順番を考慮する必要あり
            table_structs = appdxTable.xpath(
                    './TableStruct')
            if (len(table_structs) == 1):
                text_list.append(table_structs[0].text)
                tables = table_structs[0].xpath(
                        './Table')
                for table in tables:
                    tableRows = table.xpath('TableRow')
                    topRow = tableRows[0]
                    topColumns = topRow.xpath(
                            'TableColumn')
                    if len(topColumns) == 2:
                        table_list = [
                                '\n\n| 上段 | 下段 |\n' \
                                + '| ---- | ---- |\n' ]
                    elif len(topColumns) == 3:
                        table_list = [
                            '\n\n| 上段 | 中段 | 下段 |\n' \
                            + '| ---- | ---- | ---- |\n' ]
                    else:
                        table_list = [
                            '\n\n| 上段 | 　　 | 　　 | 下段 |\n' \
                            + '| ---- | ---- | ---- | ---- |\n' ]
                    for tableRow in tableRows:
                        tableColumns = tableRow.xpath('TableColumn')
                        table_list.append('|')
                        for tableColumn in tableColumns:
                            sentences = tableColumn.xpath(
                                    './Sentence')
                            for sentence in sentences:
                                if sentence.text != None:
                                    table_list.append(' ')
                                    table_list.append(
                                            sentence.text)
                                    table_list.append(' |')
                                else:
                                    # 上段が２つ合わせて、下段が1つ
                                    table_list.append('    |')
                        table_list.append('\n')
                    text_list.extend(table_list)
            items = appdxTable.xpath('.//Item')
            for item in items:
                titles = item.xpath('./ItemTitle')
                if (len(titles) != 0) and \
                         (titles[0].text != None):
                    text_list.append(titles[0].text)
                    text_list.append('　')
                sentences = item.xpath(
                        './ItemSentence/Sentence')
                for sentence in sentences:
                    text_list.append(sentence.text)
                text_list.append('\n')
                subitem1s = item.xpath('./Subitem1')
                for subitem1 in subitem1s:
                    text_list.append('　')
                    titles = subitem1.xpath(
                            './Subitem1Title')
                    if (len(titles) != 0) and \
                            (titles[0].text != None):
                        text_list.append(titles[0].text)
                        text_list.append('　')
                    sentences = subitem1.xpath(
                        './Subitem1Sentence/Sentence')
                    for sentence in sentences:
                        text_list.append(sentence.text)
                    text_list.append('\n')
                    subitem2s = subitem1.xpath(
                            './Subitem2')
                    for subitem2 in subitem2s:
                        text_list.append('　　')
                        titles = subitem2.xpath(
                                './Subitem2Title')
                        if (len(titles) != 0) and \
                                 (titles[0].text != None):
                            text_list.append(
                                    titles[0].text)
                            text_list.append('　')
                        sentences = subitem2.xpath(
                                './Subitem2Sentence/Sentence')
                        for sentence in sentences:
                            text_list.append(
                                    sentence.text)
                        text_list.append('\n')
            text = ''.join(text_list)
            appdx_list.append((str_title, text))
        return appdx_list


    def get_jou_list(self):
        return self.jou_list;

    def num2tuple(self, num):
        list_num = num.split('_')
        if len(list_num) == 1:
            tup = (int(list_num[0]),)
        elif len(list_num) == 2:
            tup = (int(list_num[0]), int(list_num[1]))
        elif len(list_num) == 3:
            tup = (int(list_num[0]), int(list_num[1]),
                   int(list_num[2]))
        elif len(list_num) == 4:
            tup = (int(list_num[0]), int(list_num[1]),
                   int(list_num[2]), int(list_num[3]))
        else:
            return 0
#             eprint("num2tuple over")
        return tup

if __name__ == '__main__':
    folder = '.\\org'

#     folder = '.\\data'


#     jou_xml = Jou_xml('租税特別措置法.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '租税特別措置', 0, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '租税特別措置法＿＿＿＿' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('租税特別措置法施行令.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '租税特別措置', 1, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '租税特別措置法施行＿令' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('租税特別措置法施行規則.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '租税特別措置', 2, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '租税特別措置法施行規則' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)


#     jou_xml = Jou_xml('法人税法.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '法人税', 0, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '法人税法＿＿＿＿' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('法人税法施行令.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '法人税', 1, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '法人税法施行＿令' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('法人税法施行規則.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '法人税', 2, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '法人税法施行規則' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)

#     jou_xml = Jou_xml('新型コロナ特例法.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '新型コロナ特例', 0, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '新型コロナ特例法＿＿＿＿' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('新型コロナ特例法施行令.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '新型コロナ特例', 1, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '新型コロナ特例法施行＿令' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('新型コロナ特例法施行規則.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '新型コロナ特例', 2, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '新型コロナ特例法施行規則' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)

#     jou_xml = Jou_xml('国税通則法.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '国税通則', 0, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '国税通則法＿＿＿＿' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('国税通則法施行令.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '国税通則', 1, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '国税通則法施行＿令' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('国税通則法施行規則.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '国税通則', 2, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '国税通則法施行規則' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)

#     jou_xml = Jou_xml('地方税法.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '地方税', 0, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '地方税法＿＿＿＿' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('地方税法施行令.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '地方税', 1, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '地方税法施行＿令' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('地方税法施行規則.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '地方税', 2, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '地方税法施行規則' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)

#     jou_xml = Jou_xml('相続税法.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '相続税', 0, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '相続税法＿＿＿＿' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('相続税法施行令.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '相続税', 1, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '相続税法施行＿令' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('相続税法施行規則.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '相続税', 2, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '相続税法施行規則' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)

#     jou_xml = Jou_xml('所得税法.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '所得税', 0, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '所得税法＿＿＿＿' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('所得税法施行令.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '所得税', 1, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '所得税法施行＿令' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)
#     jou_xml = Jou_xml('所得税法施行規則.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '所得税', 2, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '所得税法施行規則' + title + '.md'
#         file_name = os.path.join(folder, file_name)
#         with open(file_name,
#             mode='w',
#             encoding='UTF-8') as f:
#             f.write(text)

    jou_xml = Jou_xml('消費税法.xml')
    jou_list = jou_xml.get_jou_list()
    for jou_jou in jou_list:
        save_file( \
                folder, \
                '消費税', 0, jou_jou)
    appdx_list = jou_xml.create_appdxTable()
    for (title, text) in appdx_list:
        file_name = '消費税法＿＿＿' + title + '.md'
        file_name = os.path.join(folder, file_name)
        with open(file_name,
            mode='w',
            encoding='UTF-8') as f:
            f.write(text)
    jou_xml = Jou_xml('消費税法施行令.xml')
    jou_list = jou_xml.get_jou_list()
    for jou_jou in jou_list:
        save_file( \
                folder, \
                '消費税', 1, jou_jou)
    appdx_list = jou_xml.create_appdxTable()
    for (title, text) in appdx_list:
        file_name = '消費税法施行＿令' + title + '.md'
        file_name = os.path.join(folder, file_name)
        with open(file_name,
            mode='w',
            encoding='UTF-8') as f:
            f.write(text)
    jou_xml = Jou_xml('消費税法施行規則.xml')
    jou_list = jou_xml.get_jou_list()
    for jou_jou in jou_list:
        save_file( \
                folder, \
                '消費税', 2, jou_jou)
    appdx_list = jou_xml.create_appdxTable()
    for (title, text) in appdx_list:
        file_name = '消費税法施行規則' + title + '.md'
        file_name = os.path.join(folder, file_name)
        with open(file_name,
            mode='w',
            encoding='UTF-8') as f:
            f.write(text)
