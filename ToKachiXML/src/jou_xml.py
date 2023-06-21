'''
Created on 2023/05/13

@author: sue-t
'''

import c
import d
import e

import config

from md import Md

from jou_jou import Jou_jou
from jou_kou import Jou_kou
from jou_gou import Jou_gou
from jou_koumoku import Jou_koumoku

from table_struct_xml import Table_struct_xml

from ToKachi import save_file

from TransNum import TransNum

import os
from lxml import etree
# import xml.etree.ElementTree as ET
# from xml import etree

__version__ = '0.6.4'



class Jou_xml(object):

    def __init__(self, file, mei, kubun):
        '''
        file 消費税法.xml
        mei 消費税
        kubun 0,1,2
        '''
        tree = etree.parse(file)
#         root = tree.getroot()
        jou_list = []
        # 本則
        articles = tree.xpath('//MainProvision//Article')
        self.proc_article("＿",  # "本則",
                 jou_list, articles)
        index_list = []
        if kubun != 0:
            index_list.append('[')
            index_list.append(mei)
            index_list.append('法　　　　目次](index')
            index_list.append(mei)
            index_list.append('法＿＿＿＿.md)\n\n')
        if kubun != 1:
            index_list.append('[')
            index_list.append(mei)
            index_list.append('法施行令　目次](index')
            index_list.append(mei)
            index_list.append('法施行＿令.md)\n\n')
        if kubun != 2:
            index_list.append('[')
            index_list.append(mei)
            index_list.append('法施行規則目次](index')
            index_list.append(mei)
            index_list.append('法施行規則.md)\n\n')
        index_list.append('[TOC]\n\n# 本則\n\n' )
        main_provision = tree.xpath('//MainProvision')
        self.proc_index(main_provision[0],
                "＿", index_list, mei, kubun)
        d.dprint(index_list)
        # 附則
        fusokus = tree.xpath('//SupplProvision')
        if len(fusokus) != 0:
            index_list.append('# 附則\n\n')
        for fusoku in fusokus:
            fusoku_name = fusoku.attrib.get( \
                    "AmendLawNum")
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
            index_list.append(
                    '## ' + str_fusoku + '\n\n')
            articles = fusoku.xpath(".//Article")
            if len(articles) != 0:
                self.proc_article(str_fusoku,
                        jou_list, articles)
                self.proc_index_article(articles,
                        str_fusoku, index_list,
                        mei, kubun)
            else:
                # 附則の中には、第Ｘ条がなく、
                # 項のみの場合あり
                self.proc_jou_nashi(str_fusoku,
                        jou_list, fusoku,
                        index_list, mei, kubun)
        self.tree = tree
        self.jou_list = jou_list
        self.index_list = index_list

    def proc_index(self, provision, soku,
            index_list, mei, kubun):
        '''
        provision 本則、附則の先頭ノード
        soku 本則、附則名
        index_list 目次用のmdファイルの作成用
        mei 法律名　消費税 など
        kubun 0 法、1 施行令、2 施行規則
        '''
        childs = provision.xpath('*')
        if len(childs) != 0:
            if childs[0].tag == "Part":
                self.proc_index_part(childs, soku,
                        index_list, mei, kubun)
            elif childs[0].tag == "Chapter":
                self.proc_index_chapter(childs, soku,
                        index_list, mei, kubun)
            elif childs[0].tag == "Section":
                self.proc_index_section(childs, soku,
                        index_list, mei, kubun)
            elif childs[0].tag == "Subsection":
                self.proc_index_subsection(childs, soku,
                        index_list, mei, kubun)
            elif childs[0].tag == "Division":
                self.proc_index_division(childs, soku,
                        index_list, mei, kubun)
            elif childs[0].tag == "Article":
                self.proc_index_article(childs, soku,
                        index_list, mei, kubun)
            else:
                print(childs[0].tag)
                assert(False)
        else:
            print(provision.text)
            print(provision)
            assert(False)

    def proc_index_part(self, parts, soku,
            index_list, mei, kubun):
        for part in parts:
            titles = part.xpath('PartTitle')
            index_list.append(
                    "## " + titles[0].text + '\n\n')
            childs = part.xpath('./*')
            if len(childs) > 1:
                if childs[1].tag == "Chapter":
                    self.proc_index_chapter(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Section":
                    self.proc_index_section(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Subsection":
                    self.proc_index_subsection(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Division":
                    self.proc_index_division(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Article":
                    self.proc_index_article(childs[1:],
                            soku,
                            index_list, mei, kubun)
                else:
                    print(childs[0].tag)
                    assert(False)
            else:
                print(part.tag)
                print(part)
                assert(False)

    def proc_index_chapter(self, chapters, soku,
            index_list, mei, kubun):
        for chapter in chapters:
            titles = chapter.xpath('ChapterTitle')
            index_list.append(
                    "### " + titles[0].text + '\n\n')
            childs = chapter.xpath('./*')
            if len(childs) > 1:
                if childs[1].tag == "Section":
                    self.proc_index_section(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Subsection":
                    self.proc_index_subsection(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Division":
                    self.proc_index_division(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Article":
                    self.proc_index_article(childs[1:],
                            soku,
                            index_list, mei, kubun)
                else:
                    print(childs[1].tag)
                    assert(False)
            else:
                print(chapter.text)
                print(chapter)
                assert(False)

    def proc_index_section(self, sections, soku,
            index_list, mei, kubun):
        for section in sections:
            titles = section.xpath('SectionTitle')
            index_list.append(
                    "#### " + titles[0].text + '\n\n')
            childs = section.xpath('./*')
            if len(childs) > 1:
                if childs[1].tag == "Subsection":
                    self.proc_index_subsection(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Division":
                    self.proc_index_division(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Article":
                    self.proc_index_article(childs[1:],
                            soku,
                            index_list, mei, kubun)
                else:
                    print(childs[1].tag)
                    assert(False)
            else:
                print(section.text)
                print(section)
                assert(False)

    def proc_index_subsection(self, subsections, soku,
            index_list, mei, kubun):
        for subsection in subsections:
            titles = subsection.xpath('SubsectionTitle')
            index_list.append(
                    "##### " + titles[0].text + '\n\n')
            childs = subsection.xpath('./*')
            if len(childs) > 1:
                if childs[1].tag == "Division":
                    self.proc_index_division(childs[1:],
                            soku,
                            index_list, mei, kubun)
                elif childs[1].tag == "Article":
                    self.proc_index_article(childs[1:],
                            soku,
                            index_list, mei, kubun)
                else:
                    print(childs[1].tag)
                    assert(False)
            else:
                print(subsection.text)
                print(subsection)
                assert(False)

    def proc_index_division(self, divisions, soku,
            index_list, mei, kubun):
        for division in divisions:
            titles = division.xpath('DivisionTitle')
            index_list.append(
                    "###### " + titles[0].text + '\n\n')
            childs = division.xpath('./*')
            if len(childs) > 1:
                if childs[1].tag == "Article":
                    self.proc_index_article(childs[1:],
                            soku,
                            index_list, mei, kubun)
                else:
                    print(childs[1].tag)
                    assert(False)
            else:
                print(division.text)
                print(division)
                assert(False)

    def proc_index_article(self, articles, str_fusoku,
            index_list, mei, kubun):
        for article in articles:
            num = article.get('Num')
            if ':' in num:
                # '29:30' 削除のパターン
                continue
            jou_bangou_tuple = self.num2tuple(num)
            d.dprint(jou_bangou_tuple)
            # 見出し
            title = article.xpath("ArticleCaption")
            if len(title) != 0:
                midashi = title[0].text
            else:
                midashi = ""
            jou_str = TransNum.bangou_tuple2str(
                    (jou_bangou_tuple, None, None))
            d.dprint(jou_str)
            str_text = '[' + jou_str[0] + midashi + ']('
            d.dprint(str_text)
            index_list.append(str_text)
            (file_name, _str_title, _kubun_mei, _jou_list) = \
                    Md.sakusei_title('',
                    mei, kubun,
                    str_fusoku,
                    (jou_bangou_tuple, None, None),
                    '', '')
            index_list.append(file_name[:-3] \
                    + '_.md)\n\n')
            d.dprint(index_list)


    def proc_jou_nashi(self, str_fusoku,
            jou_list, fusoku, index_list, mei, kubun):
        '''
        条（article）がないfusokuで示される附則を
        仮の条として、各項を処理して
        jou_listに条文データを設定する。
        str_fusokuは、附則名を示す。
        '''
#         index_list.append('##' + str_fusoku + '\n\n')
        paragraphs = fusoku.xpath('Paragraph')
        kou = self.create_kou(str_fusoku, midashi=None,
                jou_bangou_tuple=(0,),
                paragraph=paragraphs[0])
        jou = Jou_jou(bangou_tuple=(0,), kou=kou)
        for paragraph in paragraphs[1:]:
            kou = self.create_kou(str_fusoku,
                    midashi=None,
                    jou_bangou_tuple=(0,),
                    paragraph=paragraph)
            jou.tsuika_kou(kou)
        jou.set_kubun((None, None,
                None, None, None))
        jou.set_soku(str_fusoku)
#         jou.set_midashi(midashi)
        jou_list.append(jou)
        jou_str = TransNum.bangou_tuple2str(
                ((0,),None,None))
        midashi = jou.get_midashi()
        if midashi != None:
            index_list.append(
                    '[' + jou_str[0] + midashi + '](')
        else:
            index_list.append(
                    '[' + jou_str[0] + '](')
        (file_name, _str_title, _kubun_mei, _jou_list) = \
                Md.sakusei_title('',
                mei, kubun,
                str_fusoku,
                ((0,),None,None), '', '')
        index_list.append(file_name + ')\n\n')
        d.dprint(index_list)


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
            # 本則、附則を超えてしまう
#             zenjou = article.xpath(
#                     'preceding::Article[position()=last()]')
            # 目などの範囲に限定されてしまう
            zenjou = article.xpath(
#                     'preceding-sibling::Article[position()=last()]')
                    'preceding-sibling::Article[position()=1]')
            if len(zenjou) == 1:
                zenjou_num = zenjou[0].get('Num')
                if not ':' in zenjou_num:
                    zenjou_bangou_tuple \
                            = self.num2tuple(zenjou_num)
                    jou.set_zenjou(zenjou_bangou_tuple)
            jijou = article.xpath(
                    'following-sibling::Article[position()=1]')
            if len(jijou) == 1:
                jijou_num = jijou[0].get('Num')
                if not ':' in jijou_num:
                    jijou_bangou_tuple \
                            = self.num2tuple(jijou_num)
                    jou.set_jijou(jijou_bangou_tuple)
#             d.dprint("========")
#             d.dprint(jou_bangou_tuple)
#             d.dprint(zenjou)
#             d.dprint("========")
            jou_list.append(jou)

    def create_kou(self, soku, midashi,
            jou_bangou_tuple, paragraph):
#         d.dprint_method_start()
        num = paragraph.get('Num')
        if ':' in num:
            nums = num.split(':')
            num = nums[0]   # 暫定処理
        kou_bangou = int(num)
#         d.dprint(jou_bangou_tuple)
#         d.dprint(kou_bangou)

        sentences = paragraph.xpath(
                './ParagraphSentence/Sentence')
        honbun_list = []
#         for sentence in sentences:
#             # 本文がないことがある
#             # 例　相続税法附則平成一二年五月三一日
#             # 　　　第３７条第１項
#             if sentence.text != None:
#                 honbun_list.append(sentence.text)
        for sentence in sentences:
            # Rubyに対応
            child_nodes = sentence.xpath('./node()')
            for child_node in child_nodes:
                if isinstance(child_node, str):
                    honbun_list.append(child_node)
                else:
                    if child_node.text != None:
                        honbun_list.append(child_node.text)
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
        zenkou = paragraph.xpath( \
                'preceding-sibling::' \
                'Paragraph[position()=1]')
        if len(zenkou) == 1:
            zenkou_num = zenkou[0].get('Num')
            if not ':' in zenkou_num:
                zenkou_bangou \
                        = int(zenkou_num)
                kou.set_zenkou(
                        (jou_bangou_tuple,
                        zenkou_bangou, None))
        jikou = paragraph.xpath( \
                'following-sibling::' \
                'Paragraph[position()=1]')
        if len(jikou) == 1:
            jikou_num = jikou[0].get('Num')
            if not ':' in jikou_num:
                jikou_bangou \
                        = int(jikou_num)
                kou.set_jikou(
                        (jou_bangou_tuple,
                        jikou_bangou, None))
#         d.dprint_method_end()
        return kou

    def create_gou(self, soku, midashi,
            jou_bangou_tuple, kou_bangou,
            item):
#         d.dprint_method_start()
        num = item.get('Num')
        if ':' in num:  # 略や削除のときに、ある
            return None
        gou_bangou_tuple = self.num2tuple(num)
        # 文、項目列記、表があるようだ
        # TODO 本来は順番を考慮して処理すべき
        sentences = item.xpath(
                './ItemSentence/Sentence')
        honbun_list = []
#         d.dprint(jou_bangou_tuple)
#         d.dprint(num)
        for sentence in sentences:
#             d.dprint(sentence)
            # Rubyに対応
            child_nodes = sentence.xpath('./node()')
#             d.dprint(child_nodes)
            for child_node in child_nodes:
#                 d.dprint(child_node)
                if isinstance(child_node, str):
                    honbun_list.append(child_node)
                else:
                    if child_node.text != None:
                        honbun_list.append(child_node.text)
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

        zengou = item.xpath( \
                'preceding-sibling::' \
                'Item[position()=1]')
        if len(zengou) == 1:
            zengou_num = zengou[0].get('Num')
            if not ':' in zengou_num:
#                 print(gou_bangou_tuple)
#                 print(zengou)
                zengou_bangou_tuple \
                        = self.num2tuple(zengou_num)
#                 print(zengou_bangou_tuple)
                gou.set_zengou(
                        (jou_bangou_tuple,
                        kou_bangou,
                        zengou_bangou_tuple))
        jigou = item.xpath( \
                'following-sibling::' \
                'Item[position()=1]')
        if len(jigou) == 1:
            jigou_num = jigou[0].get('Num')
            if not ':' in jigou_num:
                jigou_bangou_tuple \
                        = self.num2tuple(jigou_num)
                gou.set_jigou(
                        (jou_bangou_tuple,
                        kou_bangou,
                        jigou_bangou_tuple))
#         d.dprint_method_end()
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
            # Rubyに対応
            child_nodes = sentence.xpath('./node()')
            for child_node in child_nodes:
                if isinstance(child_node, str):
                    honbun_list.append(child_node)
                else:
                    if child_node.text != None:
                        honbun_list.append(child_node.text)
        columns = subitem1.xpath(
                './Subitem1Sentence/Column')
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
        honbun_list = []
        for sentence in sentences:
            # Rubyに対応
            child_nodes = sentence.xpath('./node()')
            for child_node in child_nodes:
                if isinstance(child_node, str):
                    honbun_list.append(child_node)
                else:
                    if child_node.text != None:
                        honbun_list.append(child_node.text)

        columns = subitem2.xpath(
                './Subitem2Sentence/Column')
        for column in columns:
            sentences = column.xpath('./Sentence')
            for sentence in sentences:
                honbun_list.append(sentence.text)
        tables = subitem2.xpath('.//Table')
        table_text = self.create_table(tables)
        honbun_list.append(table_text)
        honbun = ''.join(honbun_list)
        del honbun_list

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
        del koumoku3_list
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
        honbun_list = []
        for sentence in sentences:
            # Rubyに対応
            child_nodes = sentence.xpath('./node()')
            for child_node in child_nodes:
                if isinstance(child_node, str):
                    honbun_list.append(child_node)
                else:
                    if child_node.text != None:
                        honbun_list.append(child_node.text)
        columns = subitem3.xpath(
                './Subitem3Sentence/Column')
        for column in columns:
            sentences = column.xpath('./Sentence')
            for sentence in sentences:
                honbun_list.append(sentence.text)
        tables = subitem3.xpath('.//Table')
        table_text = self.create_table(tables)
        honbun_list.append(table_text)
        honbun = ''.join(honbun_list)
        del honbun_list
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
        del koumoku4_list
        koumoku.set_soku(soku)
        koumoku.set_midashi(midashi)
        return koumoku

    def create_table(self, tables):
        text_list = []
        for table in tables:
            tableRows = table.xpath('TableRow')
            topRow = tableRows[0]
            topColumns = topRow.xpath('TableColumn')
            tableRow = tableRows[0]
            tableColumns = tableRow.xpath(
                    'TableColumn')
            text_list.append('\n\n|')
            row_list = [ '|' ]
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
                    row_list.append(' ---- |')
            text_list.append('\n')
            row_list.append('\n')
            text_list.extend(row_list)
            del row_list
            for tableRow in tableRows[1:]:
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

    def create_appdxTable(self,
            index_list, mei, kubun):
        # 別表はmdファイルを作るだけ
        d.dprint_method_start()
        appdx_tables = self.tree.xpath('//AppdxTable')
        d.dprint(appdx_tables)
        appdx_list = []
#         text_list = []
        if len(appdx_tables) != 0:
            index_list.append('# 別表\n\n')
        for appdx_table in appdx_tables:
            appd_titles = appdx_table.xpath(
                    "./AppdxTableTitle")
            str_title = TransNum.k2a(
                    appd_titles[0].text, True)
            d.dprint(str_title)
            file_title = str_title. \
                    replace('　', '_')
            related_article_nums = appdx_table.xpath(
                    "./RelatedArticleNum")
            if len(related_article_nums) != 0:
                related = related_article_nums[0].text
            else:
                related = ''
            text_list = [str_title, related, '\n']
            if kubun == 0:
                file_name2 = mei + '法＿＿＿＿' \
                        + '＿' \
                        + file_title + '.md'
#                         + appd_titles[0].text + '.md'
            elif kubun == 1:
                file_name2 = mei + '法施行＿令' \
                        + '＿' \
                        + file_title + '.md'
#                         + appd_titles[0].text + '.md'
            else:
                file_name2 = mei + '法施行規則' \
                        + '＿' \
                        + file_title + '.md'
#                         + appd_titles[0].text + '.md'
            file_name = '＿' + file_title
#             file_name = '＿' + appd_titles[0].text
            str_index = '[' + appd_titles[0].text \
                    + '](' + file_name2 + ')\n\n'
            index_list.append(str_index)
            table_structs = appdx_table. \
                    xpath('./TableStruct')
            for table_struct in table_structs:
                table_struct_xml = Table_struct_xml(
                        table_struct)
                str_table_md = table_struct_xml. \
                        create_str_md()
                text_list.append(str_table_md)

            items = appdx_table.xpath('.//Item')
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
            appdx_list.append((file_name, text))

        suppl_provision_appdx_tables = \
                self.tree.xpath(
                        '//SupplProvisionAppdxTable')
        for suppl_provision_appdx_table in \
                suppl_provision_appdx_tables:
            appd_titles = suppl_provision_appdx_table.xpath(
                    "./SupplProvisionAppdxTableTitle")
            if len(appd_titles) != 0:
                title = appd_titles[0].text
                str_title = TransNum.k2a(
                        title, True)
                file_title = str_title. \
                        replace('　', '_')
                related_article_nums = \
                        suppl_provision_appdx_table. \
                        xpath("./RelatedArticleNum")
                if len(related_article_nums) != 0:
                    related = related_article_nums[0].text
                else:
                    related = ''
                text_list = [str_title, related, '\n']
            else:
                title = "_"
                str_title = " "
                file_title = "_"
                text_list = ['\n']
            suppl_provisions = suppl_provision_appdx_table.xpath(
                    './ancestor::SupplProvision')
            # ================================
#             print(suppl_provision_appdx_table)
#             print(appd_titles)
#             print(suppl_provisions)
            # ================================
            fusoku_name = suppl_provisions[0].attrib. \
                    get("AmendLawNum")
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
            if kubun == 0:
                file_name2 = mei + '法＿＿＿＿' \
                        + str_fusoku \
                        + file_title + '.md'
#                         + title + '.md'
            elif kubun == 1:
                file_name2 = mei + '法施行＿令' \
                        + str_fusoku \
                        + file_title + '.md'
#                         + title + '.md'
            else:
                file_name2 = mei + '法施行規則' \
                        + str_fusoku \
                        + file_title + '.md'
#                         + title + '.md'
            file_name = str_fusoku + file_title
#             file_name = str_fusoku + title
#             str_index = '[' + appd_titles[0].text \
#                     + '](' + file_name + ')\n\n'
            str_index = '[' + str_fusoku + str_title \
                    + '](' + file_name2 + ')\n\n'
            index_list.append(str_index)
            table_structs = suppl_provision_appdx_table. \
                    xpath('./TableStruct')
#             print(table_structs)
            for table_struct in table_structs:
                table_struct_xml = Table_struct_xml(
                        table_struct)
                str_table_md = table_struct_xml. \
                        create_str_md()
#                 print(str_table_md)
                text_list.append(str_table_md)
            items = suppl_provision_appdx_table. \
                    xpath('.//Item')
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
            appdx_list.append((file_name, text))
        d.dprint_method_end()
        return appdx_list


    def get_jou_list(self):
        return self.jou_list

    def get_index_list(self):
        return self.index_list

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

    @classmethod
    def main_main(cls, mei, file):
        folder = '.\\org'
    #     folder = '.\\data'
        config.folder_name = folder

#         from ToKachi import kakou1_ji
#         jou_xml = Jou_xml('会社計算規則.xml')
#         jou_list = jou_xml.get_jou_list()
#         for jou_jou in jou_list:
#             save_file( \
#                     folder, \
#                     '会社計算規則', 0, jou_jou)
#         from ToKachi import kakou1_ji
#         kakou1_ji()

#         from ToKachi import kakou1_ji
#         jou_xml = Jou_xml(
#             '小規模企業共済法の一部を改正する法律の施行に伴う経過措置に関する政令.xml',
#             '小規模企業共済_経過措置',1)
#         jou_list = jou_xml.get_jou_list()
#         for jou_jou in jou_list:
#             save_file( \
#                     folder, \
#                     '小規模企業共済法の一部を改正する法律の施行に伴う経過措置に関する政令', 1, jou_jou)
#         jou_xml = Jou_xml(
#             '小規模企業共済法の一部を改正する法律の施行に伴う経過措置に関する省令.xml',
#             '小規模企業共済_経過措置',2)
#         jou_list = jou_xml.get_jou_list()
#         for jou_jou in jou_list:
#             save_file( \
#                     folder, \
#                     '小規模企業共済法の一部を改正する法律の施行に伴う経過措置に関する省令',
#                      2, jou_jou)

        jou_xml = Jou_xml(file + '法.xml', mei, 0)
        jou_list = jou_xml.get_jou_list()
        index_list = jou_xml.get_index_list()
        for jou_jou in jou_list:
            save_file( \
                    folder, \
                    mei, 0, jou_jou)
        appdx_list = jou_xml.create_appdxTable(
                index_list, mei, 0)
        for (title, text) in appdx_list:
#             file_name = file + '法＿＿＿＿' + title + '.md'
            file_name = mei + '法＿＿＿＿' + title + '.md'
            file_name = os.path.join(folder, file_name)
            with open(file_name,
                mode='w',
                encoding='UTF-8') as f:
                f.write(text)
        str_index = ''.join(index_list)
        file_name = 'index' + mei + '法＿＿＿＿.md'
        file_name = os.path.join(folder, file_name)
        with open(file_name,
            mode='w',
            encoding='UTF-8') as f:
            f.write(str_index)

        jou_xml = Jou_xml(file + '法施行令.xml', mei, 1)
        jou_list = jou_xml.get_jou_list()
        index_list = jou_xml.get_index_list()
        for jou_jou in jou_list:
            save_file( \
                    folder, \
                    mei, 1, jou_jou)
        appdx_list = jou_xml.create_appdxTable(
                index_list, mei, 1)
        for (title, text) in appdx_list:
#             file_name = file + '法施行＿令' + title + '.md'
            file_name = mei + '法施行＿令' + title + '.md'
            file_name = os.path.join(folder, file_name)
            with open(file_name,
                mode='w',
                encoding='UTF-8') as f:
                f.write(text)
        str_index = ''.join(index_list)
        file_name = 'index' + mei + '法施行＿令.md'
        file_name = os.path.join(folder, file_name)
        with open(file_name,
            mode='w',
            encoding='UTF-8') as f:
            f.write(str_index)

        jou_xml = Jou_xml(file + '法施行規則.xml', mei, 2)
        jou_list = jou_xml.get_jou_list()
        index_list = jou_xml.get_index_list()
        for jou_jou in jou_list:
            save_file( \
                    folder, \
                    mei, 2, jou_jou)
        appdx_list = jou_xml.create_appdxTable(
                index_list, mei, 2)
        for (title, text) in appdx_list:
#             file_name = file + '法施行規則' + title + '.md'
            file_name = mei + '法施行規則' + title + '.md'
            file_name = os.path.join(folder, file_name)
            with open(file_name,
                mode='w',
                encoding='UTF-8') as f:
                f.write(text)
        str_index = ''.join(index_list)
        file_name = 'index' + mei + '法施行規則.md'
        file_name = os.path.join(folder, file_name)
        with open(file_name,
            mode='w',
            encoding='UTF-8') as f:
            f.write(str_index)

        from ToKachi import kakou1_ji, \
                kakou1_hou_rei, kakou2_hou_rei, \
                kakou1_hou_ki, kakou2_hou_ki, \
                kakou1_rei_ki, kakou2_rei_ki

        kakou1_ji()
        kakou1_hou_rei()
        kakou2_hou_rei()
        kakou1_hou_ki()
        kakou2_hou_ki()
        kakou1_rei_ki()
        kakou2_rei_ki()




