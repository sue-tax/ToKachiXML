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

import os
from lxml import etree
# import xml.etree.ElementTree as ET


__version__ = '0.4.3'


class Jou_xml(object):

    def __init__(self, file):
        tree = etree.parse(file)
        root = tree.getroot()

        # 本則の条文のみ
        jou_list = []
        d.dprint('//MainProvision//Article')
        articles = tree.xpath('//MainProvision//Article')

        for article in articles:
#     def __init__(self, jou_bangou_tuple, kou, sakujo=False):
            num = article.get('Num')
            if ':' in num:
                # '29:30' 削除のパターン
                continue
            jou_bangou_tuple = self.num2tuple(num)

            part = article.xpath('ancestor::Part')
            if len(part) != 0:
#                 d.dprint_data(part[0].text)
                part_title = part[0].xpath('./PartTitle')
#                 d.dprint_data(part_title[0].text)
                part_str = part_title[0].text.replace('　', '')
            else:
                part_str = None
            chapter = article.xpath('ancestor::Chapter')
            if len(chapter) != 0:
#                 d.dprint_data(chapter[0].text)
                chapter_title = chapter[0].xpath('./ChapterTitle')
#                 d.dprint_data(chapter_title[0].text)
                chapter_str = chapter_title[0].text.replace('　', '')
            else:
                chapter_str = None
            section = article.xpath('ancestor::Section')
            if len(section) != 0:
#                 d.dprint_data(section[0].text)
                section_title = section[0].xpath('./SectionTitle')
#                 d.dprint_data(section_title[0].text)
                section_str = section_title[0].text.replace('　', '')
            else:
                section_str = None
            subsection = article.xpath('ancestor::Subsection')
            if len(subsection) != 0:
#                 d.dprint_data(subsection[0].text)
                subsection_title = subsection[0].xpath('./SubsectionTitle')
#                 d.dprint_data(subsection_title[0].text)
                subsection_str = subsection_title[0].text.replace('　', '')
            else:
                subsection_str = None
            division = article.xpath('ancestor::Division')
            if len(division) != 0:
#                 d.dprint_data(division)
                division_title = division[0].xpath('./DivisionTitle')
#                 d.dprint_data(division_title[0].text)
                division_str = division_title[0].text.replace('　', '')
            else:
                division_str = None

            title = article.xpath("ArticleTitle")
            if len(title) != 0:
                midashi = title[0].text
            else:
                midashi = ""
#             print(midashi)

            paragraphs = article.xpath('Paragraph')
            kou = self.create_kou(jou_bangou_tuple,
                    paragraphs[0])
            jou = Jou_jou(jou_bangou_tuple, kou)
            for paragraph in paragraphs[1:]:
                kou = self.create_kou(jou_bangou_tuple,
                        paragraph)
                jou.tsuika_kou(kou)
            jou.set_kubun((part_str, chapter_str,
                    section_str, subsection_str,
                    division_str))

            jou_list.append(jou)
        self.tree = tree
        self.jou_list = jou_list

    def create_appdxTable(self):
        # 別表はmdファイルを作るだけ
        appdxTables = self.tree.xpath('//AppdxTable')
        appdx_list = []
        for appdxTable in appdxTables:
            appd_titles = appdxTable.xpath("./AppdxTableTitle")
            text = appd_titles[0].text + '\n'
            d.dprint(appd_titles[0].text)

            # TODO 順番を考慮する必要あり
            table_structs = appdxTable.xpath('./TableStruct')
            if (len(table_structs) == 1):
                text = text + table_structs[0].text
                tables = table_structs[0].xpath('./Table')
                for table in tables:
                    tableRows = table.xpath('TableRow')
                    topRow = tableRows[0]
                    topColumns = topRow.xpath('TableColumn')
                    if len(topColumns) == 2:
                        table_text = '\n\n| 上段 | 下段 |\n' \
                                + '| ---- | ---- |\n'
                    elif len(topColumns) == 3:
                        table_text = '\n\n| 上段 | 中段 | 下段 |\n' \
                                + '| ---- | ---- | ---- |\n'
                    else:
                        table_text = '\n\n| 上段 | 　　 | 　　 | 下段 |\n' \
                                + '| ---- | ---- | ---- | ---- |\n'
                    d.dprint(table_text)
                    for tableRow in tableRows:
                        tableColumns = tableRow.xpath('TableColumn')
                        table_text = table_text + '|'
                        for tableColumn in tableColumns:
                            sentences = tableColumn.xpath('./Sentence')
                            for sentence in sentences:
                                d.dprint(sentence.text)
                                if sentence.text != None:
                                    table_text = table_text + ' ' \
                                            + sentence.text + ' |'
                                else:
                                    # 上段が２つ合わせて、下段が1つ
                                    table_text = table_text \
                                            + '    |'

                        table_text = table_text + '\n'
                    text = text + table_text

            items = appdxTable.xpath('.//Item')
            for item in items:
                titles = item.xpath('./ItemTitle')
                if (len(titles) != 0) and \
                         (titles[0].text != None):
                    text = text + titles[0].text + '　'
                sentences = item.xpath('./ItemSentence/Sentence')
                for sentence in sentences:
#                     print(sentence.text)
                    text = text + sentence.text
                text = text + '\n'
                subitem1s = item.xpath('./Subitem1')
#                 print(subitems)
                for subitem1 in subitem1s:
#                     print(subitem)
                    text = text + '　'
                    titles = subitem1.xpath('./Subitem1Title')
                    if (len(titles) != 0) and \
                            (titles[0].text != None):
                        text = text + titles[0].text + '　'
                    sentences = subitem1.xpath(
                        './Subitem1Sentence/Sentence')
                    for sentence in sentences:
                        text = text + sentence.text
                    text = text + '\n'
                    subitem2s = subitem1.xpath('./Subitem2')
                    for subitem2 in subitem2s:
                        text = text + '　　'
                        titles = subitem2.xpath('./Subitem2Title')
                        if (len(titles) != 0) and \
                                 (titles[0].text != None):
                            text = text + titles[0].text + '　'
                        sentences = subitem2.xpath(
                            './Subitem2Sentence/Sentence')
                        for sentence in sentences:
                            text = text + sentence.text
                        text = text + '\n'
            appdx_list.append((appd_titles[0].text, text))
        return appdx_list


    def create_kou(self, jou_bangou_tuple, paragraph):
        num = paragraph.get('Num')
        kou_bangou = int(num)

        sentences = paragraph.xpath(
                './ParagraphSentence/Sentence')
        honbun = ''
        for sentence in sentences:
            honbun = honbun + sentence.text

        gou_list = []
        items = paragraph.xpath('.//Item')
        for item in items:
            gou = self.create_gou(
                    jou_bangou_tuple, kou_bangou,
                    item)
            gou_list.append(gou)

        kou = Jou_kou(jou_bangou_tuple, kou_bangou,
                      honbun, gou_list)
        return kou

    def create_gou(self, jou_bangou_tuple, kou_bangou,
            item):
        d.dprint_method_start()
        num = item.get('Num')
        gou_bangou_tuple = self.num2tuple(num)

        sentences = item.xpath('./ItemSentence/Sentence')
        honbun = ''
        for sentence in sentences:
            honbun = honbun + sentence.text
        d.dprint_name('honbun', honbun)

        columns = item.xpath('./ItemSentence/Column')
        if len(columns) != 0:
            text_column = []
            for column in columns:
                sentences = column.xpath('./Sentence')
                text_sentence = ''
                for sentence in sentences:
                    text_sentence = text_sentence + sentence.text
                text_column.append(text_sentence)
            text_columns = '　'.join(text_column)
            honbun = honbun + text_columns

        tables = item.xpath('.//Table')
        for table in tables:
            tableRows = table.xpath('TableRow')
            topRow = tableRows[0]
            topColumns = topRow.xpath('TableColumn')
            if len(topColumns) == 2:
                table_text = '\n\n| 上段 | 下段 |\n' \
                        + '| ---- | ---- |\n'
            elif len(topColumns) == 3:
                table_text = '\n\n| 上段 | 中段 | 下段 |\n' \
                        + '| ---- | ---- | ---- |\n'
            else:
                table_text = '\n\n| 上段 | 　　 | 　　 | 下段 |\n' \
                        + '| ---- | ---- | ---- | ---- |\n'
            for tableRow in tableRows:
                tableColumns = tableRow.xpath('TableColumn')
                table_text = table_text + '|'
                for tableColumn in tableColumns:
                    sentences = tableColumn.xpath('./Sentence')
                    for sentence in sentences:
                        if sentence.text != None:
                            table_text = table_text + ' ' \
                                    + sentence.text + ' |'
                        else:
                            table_text = table_text \
                                    + '    |'
                table_text = table_text + '\n'
            honbun = honbun + table_text

        koumoku_list = []
        subitem1s = item.xpath('./Subitem1')
        for subitem1 in subitem1s:
            koumoku = self.create_koumoku(
                    jou_bangou_tuple, kou_bangou,
                    gou_bangou_tuple,
                    subitem1)
            koumoku_list.append(koumoku)

        gou = Jou_gou(jou_bangou_tuple, kou_bangou,
                gou_bangou_tuple,
                honbun, koumoku_list)
        d.dprint_method_end()
        return gou

    def create_koumoku(self, jou_bangou_tuple, kou_bangou,
            gou_bangou_tuple, subitem1):
        # イ、ロ、ハ
        titles = subitem1.xpath('./Subitem1Title')
        koumoku_tuple = (titles[0].text,)

        sentences = subitem1.xpath('./Subitem1Sentence/Sentence')
        honbun = ''
        for sentence in sentences:
            honbun = honbun + sentence.text

        columns = subitem1.xpath('./ItemSentence/Column')
        for column in columns:
            sentences = column.xpath('./Sentence')
            for sentence in sentences:
                honbun = honbun + sentence.text

        tables = subitem1.xpath('.//Table')
        for table in tables:
            tableRows = table.xpath('TableRow')
            topRow = tableRows[0]
            topColumns = topRow.xpath('TableColumn')
            if len(topColumns) == 2:
                table_text = '\n\n| 上段 | 下段 |\n' \
                        + '| ---- | ---- |\n'
            elif len(topColumns) == 3:
                table_text = '\n\n| 上段 | 中段 | 下段 |\n' \
                        + '| ---- | ---- | ---- |\n'
            else:
                table_text = '\n\n| 上段 | 　　 | 　　 | 下段 |\n' \
                        + '| ---- | ---- | ---- | ---- |\n'
            for tableRow in tableRows:
                tableColumns = tableRow.xpath('TableColumn')
                table_text = table_text + '|'
                for tableColumn in tableColumns:
                    sentences = tableColumn.xpath('./Sentence')
                    for sentence in sentences:
                        table_text = ' ' + table_text \
                                + sentence.text + ' |'
                table_text = table_text + '\n'
            honbun = honbun + table_text


        koumoku2_list = []
        subitem2s = subitem1.xpath('./Subitem2')
        for subitem2 in subitem2s:
            koumoku2 = self.create_koumoku2(
                    jou_bangou_tuple, kou_bangou,
                    gou_bangou_tuple, koumoku_tuple,
                    subitem2)
            koumoku2_list.append(koumoku2)

        koumoku = Jou_koumoku(jou_bangou_tuple, kou_bangou,
                gou_bangou_tuple, koumoku_tuple,
                honbun, koumoku2_list)
        return koumoku

    def create_koumoku2(self, jou_bangou_tuple, kou_bangou,
            gou_bangou_tuple, koumoku_tuple, subitem2):
        # （２）
        titles = subitem2.xpath('./Subitem2Title')
        koumoku2_tuple = koumoku_tuple + (titles[0].text,)

        sentences = subitem2.xpath('./Subitem2Sentence/Sentence')
        honbun = ''
        for sentence in sentences:
            honbun = honbun + sentence.text

        koumoku3_list = []
        subitem3s = subitem2.xpath('./Subitem3')
        for subitem3 in subitem3s:
            koumoku3 = self.create_koumoku3(
                    jou_bangou_tuple, kou_bangou,
                    gou_bangou_tuple, koumoku2_tuple,
                    subitem3)
            koumoku3_list.append(koumoku3)

        koumoku = Jou_koumoku(jou_bangou_tuple, kou_bangou,
                gou_bangou_tuple, koumoku2_tuple,
                honbun, koumoku3_list)
        return koumoku

    def create_koumoku3(self, jou_bangou_tuple, kou_bangou,
            gou_bangou_tuple, koumoku_tuple, subitem3):
        #
        titles = subitem3.xpath('./Subitem3Title')
        koumoku3_tuple = koumoku_tuple + (titles[0].text,)

        sentences = subitem3.xpath('./Subitem3Sentence/Sentence')
        honbun = ''
        for sentence in sentences:
            honbun = honbun + sentence.text

        koumoku4_list = []
        subitem4s = subitem3.xpath('./Subitem4')
        for subitem4 in subitem4s:
            koumoku4 = self.create_koumoku3(
                    jou_bangou_tuple, kou_bangou,
                    gou_bangou_tuple, koumoku3_tuple,
                    subitem4)
            koumoku4_list.append(koumoku4)

        koumoku = Jou_koumoku(jou_bangou_tuple, kou_bangou,
                gou_bangou_tuple, koumoku3_tuple,
                honbun, koumoku4_list)
        return koumoku

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
#     folder = '.'

#     jou_xml = Jou_xml('法人税法.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '法人税', 0, jou_jou)
#     appdx_list = jou_xml.create_appdxTable()
#     for (title, text) in appdx_list:
#         file_name = '法人税法' + title + '.md'
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

#     jou_xml = Jou_xml('法人税法施行規則.xml')
#     jou_list = jou_xml.get_jou_list()
#     for jou_jou in jou_list:
#         save_file( \
#                 folder, \
#                 '法人税', 2, jou_jou)

    folder = '.'

    jou_xml = Jou_xml('消費税法.xml')
    jou_list = jou_xml.get_jou_list()
    for jou_jou in jou_list:
        save_file( \
                folder, \
                '消費税', 0, jou_jou)
    appdx_list = jou_xml.create_appdxTable()
    for (title, text) in appdx_list:
        file_name = '消費税法' + title + '.md'
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

    jou_xml = Jou_xml('消費税法施行規則.xml')
    jou_list = jou_xml.get_jou_list()
    for jou_jou in jou_list:
        save_file( \
                folder, \
                '消費税', 2, jou_jou)
