'''
Created on 2023/06/10

@author: sue-t
'''

import c
import d
import e

# import config
#
# from md import Md
#
# from jou_jou import Jou_jou
# from jou_kou import Jou_kou
# from jou_gou import Jou_gou
# from jou_koumoku import Jou_koumoku
#
# from ToKachi import save_file
#
# from TransNum import TransNum
#
# import os
from lxml import etree


class Table_struct_xml(object):
    '''
    e-GOV法令検索のXMLデータのうち、
    表を示すTableStructの処理
    '''


    def __init__(self, node_table_struct):
        self.node_table_struct = node_table_struct
        titles = self.node_table_struct.xpath(
                './TableStructTitle')
        d.dprint(titles)
        if len(titles) != 0:
            self.title = titles[0].text
        else:
            self.title = ""
        d.dprint(self.title)

    def create_str_md(self):
        '''
        XMLデータからマークダウン用の文字列を
        作成する
        '''
        tables = self.node_table_struct.xpath(
                './Table')
        table = tables[0]
        row_num = int(table.xpath('count(./TableRow)'))
        table_rows = table.xpath('./TableRow')
        table_columns = table_rows[0]. \
                xpath('./TableColumn')
        column_num = 0
        for table_column in table_columns:
            column_span = table_column.attrib. \
                    get("colspan")
            if column_span == None:
                column_num += 1
            else:
                column_num += int(column_span)
        cell_array = [[None] * column_num
                for i in range(row_num)]

        row_count = 0
        for table_row in table_rows:
#             d.dprint_name("row_count", row_count)
            table_columns = table_row. \
                    xpath('./TableColumn')
            column_count = 0
            for table_column in table_columns:
                while cell_array[row_count] \
                        [column_count] != None:
                    column_count += 1
                row_span = table_column.attrib. \
                        get("rowspan")
                if row_span != None:
                    int_row_span = int(row_span)
                else:
                    int_row_span = 1
                column_span = table_column.attrib. \
                            get("colspan")
                if column_span != None:
                    int_column_span = int(column_span)
                else:
                    int_column_span = 1
                if int_row_span != 1:
                    if int_column_span != 1:
                        for row in range(row_count,
                                row_count + int_row_span):
                            for column in range(column_count,
                                    column_count + int_column_span):
                                cell_array[row][column] \
                                        = "同左上"
                    else:
                        for row in range(row_count,
                                row_count + int_row_span):
                            cell_array[row][column_count] \
                                    = "同上"
                else:
                    if int_column_span != 1:
                        for column in range(column_count,
                                column_count + int_column_span):
                            cell_array[row_count][column] \
                                    = "同左"
                sentences = table_column. \
                        xpath('./Sentence')
                cell_array[row_count][column_count] = \
                            sentences[0].text
                column_count += 1
            row_count += 1
        d.dprint(cell_array)

        text_list = [ self.title, '\n\n', '| ']
        line_list = ['| ']
        for cell in cell_array[0]:
            if cell != None:
                text_list.append(cell)
            else:
                text_list.append(" ")
            text_list.append(" |")
            line_list.append("--- |")
        text_list.append("\n")
        text_list.extend(line_list)
        text_list.append("\n")
        del line_list
        for row in cell_array[1:]:
            text_list.append("| ")
            for cell in row:
                if cell != None:
                    text_list.append(cell)
                else:
                    text_list.append(" ")
                text_list.append(" |")
            text_list.append("\n")
        text_list.append("\n\n")

        remarks = self.node_table_struct.xpath(
                './Remarks')
        for remark in remarks:
            remarks_labels = remark.xpath(
                    './RemaksLabel')
            for label in remarks_labels:
                d.dprint(label.text)
                text_list.append(label.text)
                text_list.append("\n")
            items = remark.xpath('./Item')
            for item in items:
                item_titles = item.xpath('./ItemTitle')
                for item_title in item_titles:
                    d.dprint(item_title.text)
                    if item_title.text != None:
                        text_list.append(item_title.text)
                        text_list.append('　')
#                     text_list.append("\n")
                item_sentences = item.xpath(
                        './ItemSentence')
                for item_sentence in item_sentences:
                    sentences = item_sentence.xpath(
                            './Sentence')
                    for sentence in sentences:
                        text_list.append(sentence.text)
                        d.dprint(sentence.text)
                        text_list.append("\n")
                sub_items = item.xpath(
                        './Subitem1')
                for sub_item in sub_items:
                    sub_item_titles = sub_item.xpath(
                            './Subitem1Title')
                    for sub_item_title in sub_item_titles:
                        if sub_item_title.text != None:
                            text_list.append(
                                    sub_item_title.text)
                            text_list.append('　')
                    sub_item_sentences = sub_item.xpath(
                            './Subitem1Sentence')
                    for sub_item_sentence in \
                            sub_item_sentences:
                        sentences = sub_item_sentence. \
                                xpath('./Sentence')
                        for sentence in sentences:
                            text_list.append(
                                 sentence.text)
                            text_list.append('\n')
        text_list.append('\n\n')

        d.dprint(text_list)
        str_table_md = ''.join(text_list)
        del text_list
        d.dprint(str_table_md)
        return str_table_md




if __name__ == '__main__':
#     tree = etree.parse('所得税法.xml')
    tree = etree.parse('消費税_令和５年６月_法.xml')
    appdx_tables = tree.xpath('//AppdxTable')
#     for appdx_table in appdx_tables:
    for appdx_table in appdx_tables:
        appdx_table_titles = appdx_table. \
                xpath('./AppdxTableTitle')

        title = appdx_table_titles[0].text
        d.dprint(title)
        table_structs = appdx_table. \
                xpath('./TableStruct')
        for table_struct in table_structs:
            table_struct_xml = Table_struct_xml(
                    table_struct)
            str_table_md = table_struct_xml. \
                    create_str_md()
    suppl_provision_appdx_tables = \
            tree.xpath('//SupplProvisionAppdxTable')
    for suppl_provision_appdx_table in \
            suppl_provision_appdx_tables:
        appdx_table_titles = suppl_provision_appdx_table. \
                xpath('./SuppleProvisionAppdxTableTitle')
        if len(appdx_table_titles) != 0:
            title = appdx_table_titles[0].text
        else:
            title = ""
        d.dprint(title)
        table_structs = suppl_provision_appdx_table. \
                xpath('./TableStruct')
        for table_struct in table_structs:
            table_struct_xml = Table_struct_xml(
                    table_struct)
            str_table_md = table_struct_xml. \
                    create_str_md()

