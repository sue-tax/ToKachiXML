'''
Created on 2022/09/30
指定された税法条文を解析し、
obsidian（黒曜石）ソフトで処理しやすい
条文ファイルを作成するToKachi（十勝石）ソフト
@author: sue-t
'''

'''
TODO
 .md 以外の拡張子を使い、加工の段階を区別する？
それか、.ToKachiファイルに加工の段階を書き込んでおく
'''

'''
条文番号を示すタプルのパターン
第１条 ((1,), None, None)
第１条の２ ((1,2), None, None)
第１条の２の３ ((1,2,3), None, None)
第１条第２項 ((1,), 2, None)　第２項の３などはない
第１条第２項第３号 ((1,), 2, (3,))
第１条第２項第３号の４ ((1,), 2, (3,4))
第１条第２項第３号の４の５ ((1,), 2, (3,4,5))
'''

from tkinter import Tk, Menu, Frame, Label, Text, \
        Scrollbar, Button, \
        NONE, NORMAL, HORIZONTAL, VERTICAL, DISABLED, \
        filedialog, messagebox
import sys
import os
import csv
import shutil
import datetime

import c
import d
import e
import config

from jou_yacc import jou_init, jou_parse
from bun import Bun
from md import Md


# __version__ = '0.6.4'
# 0.6.4 表対応の強化
# __version__ = '0.6.5'
# 別表名に空白が入る場合に対応 別表第一　（第二条、第四条関係）
__version__ = '0.7.0'
# 基本的なリンクの追加、タグの廃止
# 条（全）などの作成、色付け機能を別ソフトへ

if __name__ == '__main__':
    from jou_xml import Jou_xml
#     mei = '国税通則' # '0.7.0'
#     mei = '国税徴収' # '0.7.0'
#     mei = '所得税' # '0.6.5'
#     mei = '法人税' # '0.6.4'
#     mei = '相続税' # '0.7.0'

#     file = '相続税_令和６年１月_' # '0.6.4'
#     mei = '相続税' # '0.6.4'

    mei = '消費税' # '0.6.4'

#     file = '消費税_令和５年６月_' # '0.6.4'
#     mei = '消費税'

#     mei = '地方税' # '0.6.4'
#     mei = '地方法人税' # '0.6.3'
#     mei = '租税特別措置'  # '0.6.5' 0.5.1まではMemoryError
#     mei = '新型コロナ特例' # '0.7.0'
#     mei = '電子帳簿保存' # '0.7.0' 政令なし
#     mei = '会社' # '0.6.4'　計算規則あり
#     mei = '一般社団法人' # '0.7.0'
#     mei = '民' # '0.6.4' 規則なし
#     mei = '小規模企業共済' # '0.6.5' 経過措置あり

    file = mei

    Jou_xml.main_main(mei, file)
    exit(0)




font_name = "MS ゴシック"
font_size = 16
window_yoko = 800
window_tate = 750   # 850
frame_yoko = 70
frame_tate = 30 # 38

SETTEI_FILE_NAME = 'ToKachi.cfg'
TOKACHI_FILE_NAME = '.ToKachi.csv'


def create_window():
    global root
    root = Tk()
#     global app
#     app = Application(master=root)
    global __version__
    root.title(
            "ToKachi (version {:})" \
            .format(__version__))
    global window_yoko, window_tate
    window_size = "{}x{}".format(window_yoko, window_tate)
    root.geometry(window_size)

#     global folder_name
    config.folder_name = os.path.dirname(sys.argv[0])

    create_menu(root)
#     frame_src = create_frame_src(root)
    frame_log = create_frame_log(root)
#     frame_src.grid(row=0, column=0)
#     frame_log.grid(row=0, column=1)
    frame_log.pack()
#     frame_button = create_frame_button(root)
#     frame_button.grid(row=0, column=2, rowspan=2)

#     global form_src
#     form_src.focus_set()

    root.mainloop()
    return root


def create_menu(root):
    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="作業フォルダの選択",
            command=select_folder)
    file_menu.add_command(label="条文ファイルのコピー",
            command=copy_file)
    file_menu.add_separator()
    file_menu.add_command(label="条文ファイルの作成",
            command=create_file)
    file_menu.add_separator()
    file_menu.add_command(label="項号ファイルのインポート",
             command=import_file, state=DISABLED)
    file_menu.add_separator()
    file_menu.add_command(label="終了", command=shuryou)
    menu_bar.add_cascade(label="ファイル", menu=file_menu)
    shori_menu = Menu(menu_bar, tearoff=0)
    shori_menu.add_command(label="項号分割",
            command=divide_kougou)
    shori_menu.add_command(label="加工１", command=kakou1)
    shori_menu.add_command(label="加工２", command=kakou2)
    menu_bar.add_cascade(label="処理", menu=shori_menu)
    tool_menu = Menu(menu_bar, tearoff=0)
    tool_menu.add_command(label="処理済み条文ファイルの戻し",
            command=rename_file)
    tool_menu.add_separator()
    tool_menu.add_command(label="ハイパーリンク自己設定１",
            command=set_link1)
    tool_menu.add_command(label="ハイパーリンク自己設定２",
            command=set_link2)
    tool_menu.add_command(label="ハイパーリンク除外設定",
            command=set_jogai)
    tool_menu.add_separator()
    tool_menu.add_command(label="一括処理",
            command=full_process)
    menu_bar.add_cascade(label="ツール", menu=tool_menu)

    root.config(menu=menu_bar)


# def create_frame_src(root):
#     frame = Frame(root)
#     Label(frame, text="textelテキスト").grid(row=0, column=0)
#     global frame_yoko, frame_tate
#     entry_form = Text(frame,
#             width=frame_yoko, height=frame_tate, wrap=NONE)
#     global font_name, font_size
#     entry_form.configure(font=(font_name, font_size))
#     scrollbar_form_x = Scrollbar(frame, orient=HORIZONTAL,
#             command=entry_form.xview)
#     entry_form.configure(
#             xscrollcommand=scrollbar_form_x.set)
#     scrollbar_form_y = Scrollbar(frame, orient=VERTICAL,
#             command=entry_form.yview)
#     entry_form.configure(
#             yscrollcommand=scrollbar_form_y.set)
#     entry_form.grid(row=1, column=0)
#     scrollbar_form_x.grid(row=2, column=0, sticky='ew')
#     scrollbar_form_y.grid(row=1, column=1, sticky='ns')
# #     entry_form.configure(state=DISABLED)
#     global form_src
#     form_src = entry_form
#     return frame
#
#
def create_frame_log(root):
    frame = Frame(root)
    Label(frame, text="処理ログ").grid(row=0, column=0)
    global frame_yoko, frame_tate
    entry_form = Text(frame,
            width=frame_yoko, height=frame_tate, wrap=NONE)
    global font_name, font_size
    entry_form.configure(font=(font_name, font_size))
    scrollbar_form_x = Scrollbar(frame, orient=HORIZONTAL,
            command=entry_form.xview)
    entry_form.configure(
            xscrollcommand=scrollbar_form_x.set)
    scrollbar_form_y = Scrollbar(frame, orient=VERTICAL,
            command=entry_form.yview)
    entry_form.configure(
            yscrollcommand=scrollbar_form_y.set)
    entry_form.grid(row=1, column=0)
    scrollbar_form_x.grid(row=2, column=0, sticky='ew')
    scrollbar_form_y.grid(row=1, column=1, sticky='ns')
    entry_form.configure(state=DISABLED)
#     global form_log
    config.form_log = entry_form
    return frame


def create_frame_button(root):
    frame = Frame(root)

#     Button(frame, text="作成", padx=4, pady=2,
#             command=click_button_make) \
#             .grid(row=0, column=0, columnspan=1)
#     Label(frame, text="").grid(row=1, column=0)
#     Label(frame, text="").grid(row=2, column=0)
    return frame


# def click_button_make():
#     d.dprint_method_start()
#     global form_src
#     str_src = form_src.get('1.0', 'end -1c')
# #     d.dprint(str_src)
#     lines_list = str_src.split('\n')
#     textel = Textel()
#     f = textel.process(lines_list)
#     if not f:
#         str_msg = textel.get_message()
#     else:
#         str_msg = textel.get_message()
#         str_msg += "\nComplete !"
# #     d.dprint(str_msg)
#     set_log(str_msg)
#     del textel
#     d.dprint_method_end()


def select_folder():
#     global folder_name
    config.folder_name = filedialog.askdirectory(
            title="作業フォルダ名",
            initialdir=config.folder_name
            )
    # 暫定
    # 初期化のタイミング
    # フォルダ変更かも？
    # hou_ki_dict[('消費税法',((2,),1,(8,)))] =
    #    [((2,),1,None)]
    # 消費税法２①八の中の「財務省令で定める」は
    # 消費税法施行規則２①に対応することを示している
    global hou_rei_dict, hou_ki_dict, rei_ki_dict
    hou_rei_dict = {}
    hou_ki_dict = {}
    # hou_ki_dict 法の条文の中の財務省令で定めるを処理するため
    rei_ki_dict = {}
    config.jiko1_list = []
    load_tokachi_file()
    str_log = 'フォルダ【{}】を作業フォルダとして選択しました\n' \
            .format(config.folder_name)
    set_log(str_log)
    return


def copy_file():
    list_log = ['指定されたファイルを条文ファイルとして' \
            '作業フォルダにコピーします。\n']
    # 複数ファイル選択
    file_type = [('テキストファイル', '*.txt'), \
            ('', '*')]
#     global folder_name
    files = filedialog.askopenfilenames(
            filetypes=file_type,
            initialdir=config.folder_name)
    for file in files:
        file_name = os.path.basename(file)
        # ファイル名形式チェック
        if '規' in file_name:
            index = file_name.find('規')
            index2 = file_name.find('法')
            if (index2 != -1) and (index2 < index):
                index = index2
#             kubun = Md.kubunKi
        elif '令' in file_name:
            index = file_name.find('令')
            index2 = file_name.find('法')
            if (index2 != -1) and (index2 < index):
                index = index2
#             kubun = Md.kubunRei
        elif '法' in file_name:
            index = file_name.find('法')
#             kubun = Md.kubunHou
        else:
            list_log.append('\tファイル【{}】の名前に' \
                    '法、令、規のいずれかが必要です。\n')
        new_file_name = file_name
        if new_file_name[0] == '.' \
                or new_file_name[0] == '_':
            new_file_name = new_file_name[1:]
        # 拡張子変更
        split_name = os.path.splitext(new_file_name)
        if (split_name[1] != '.txt'):
            new_file_name = split_name[0] + '.txt'
        new_name = os.path.join(config.folder_name,
                new_file_name)
        try:
            shutil.copy2(file, new_name)
        except Exception as _e:
            list_log.append(
                    '\t既にファイル【{}】がありました。\n' \
                    .format(new_name))
            continue
        list_log.append(
                '\tファイル【{}】を【{}】として' \
                'コピーしました。\n'. \
                format(file, new_name))
    str_log = ''.join(list_log)
    del list_log
    set_log(str_log)
    return


def create_file():
    # ファイル作成
    # 税法名、区分、条文を入力
    from dialogInput import DialogInput
    DialogInput()
    return


def create_file2(dlg):
    dt_now = datetime.datetime.now()
    file_name = ''.join([config.dlg_mei, config.dlg_kubun,
            dt_now.strftime("%Y%m%d%H%M%S"), '.txt'])
    full_name = os.path.join(config.folder_name, file_name)
    with open(full_name,
            mode='w',
            encoding='UTF-8') as f:
        f.write(config.dlg_joubun)
    str_log = 'ファイル【{}】を作成しました。\n'. \
            format(file_name)
    set_log(str_log)
    return


def import_file():
    # 自作マークロウ・ファイル
    # 編集済みマークダウン・ファイル
    pass

def divide_kougou():
    '''
    処理フォルダ内のＸ法（施行令、施行規則）xxx.txtファイルを
    条文ファイルとして構文解析して、
    項・号に分割したmdファイルを
    処理フォルダに作成する。
    元のファイル名は、先頭に_を付けた名前に変更する。
    処理フォルダ内の_や.で始まるファイルは
    処理対象外。
    '''
    d.dprint_method_start()
#     global folder_name
    files = os.listdir(config.folder_name)
    list_file = []
    for file_name in files:
        if os.path.isdir(os.path.join(
                config.folder_name, file_name)):
            continue
        if (file_name[0] == '.') \
                or (file_name[0] == '_'):
            continue
#         if (file_name[-4:] != '.txt'):
        if (os.path.splitext(file_name)[1] != '.txt'):
            continue
        if '規' in file_name:
            index = file_name.find('規')
            index2 = file_name.find('法')
            if (index2 != -1) and (index2 < index):
                index = index2
            list_file.append((file_name[:index],
                    Md.kubunKi,
                    file_name))
#                     os.path.join(folder_name, file_name)))
        elif '令' in file_name:
            index = file_name.find('令')
            index2 = file_name.find('法')
            if (index2 != -1) and (index2 < index):
                index = index2
            list_file.append((file_name[:index],
                    Md.kubunRei,
                    file_name))
#                     os.path.join(folder_name, file_name)))
        elif '法' in file_name:
            index = file_name.find('法')
            list_file.append((file_name[:index],
                    Md.kubunHou,
                    file_name))
#                     os.path.join(folder_name, file_name)))
    del files

    list_log = [ \
            'ファイルを条・項・号ごとに分割しました。\n' ]
    for tuple_file in list_file:
        full_name = os.path.join(config.folder_name,
                tuple_file[2])
        read_text = load_text_file(full_name)
        if read_text == None:
            continue
        result_list = jou_parse(read_text)
        if result_list == None:
            list_log.append('\tファイル【{}】は、' \
                    '法律の条文として' \
                    '解析できませんでした\n' \
                    .format(tuple_file[2]))
            continue
        list_log.append('\t{}\n'.format(tuple_file[2]))
        for result in result_list:
            # Jou_jou
            log = save_file(folder=config.folder_name,
                    zeihou_mei=tuple_file[0],
                    kubun=tuple_file[1],
                    jou_jou=result)
            list_log.extend(log)
            del log
        new_name = os.path.join(config.folder_name,
                '_' + tuple_file[2])
        try:
            os.rename(full_name, new_name)
        except Exception as _e:
            try:
                os.remove(new_name+'.bak')
            except Exception as _e:
                pass
            # '.bak'には上書きする。
            os.rename(new_name, new_name+'.bak')
            os.rename(full_name, new_name)
            list_log.append('\t\tファイル名を変更しました。' \
                    '\t{} -> {}.bak\n'. \
                    format(new_name, new_name))
        list_log.append('\t\tファイル名を変更しました。\t')
        list_log.append(tuple_file[2])
        list_log.append(' -> _')
        list_log.append(tuple_file[2])
        list_log.append('\n')
    list_log.append("次に、加工１を実行してください。\n")
    str_log = ''.join(list_log)
    del list_log
#     set_log(str_log)
    print(str_log)
    return


def load_text_file(file_name):
    try:
        f = open(file_name,
                "r",
                encoding="UTF-8")
        read_list = f.readlines()
        f.close()
    except OSError as e:
        messagebox.showwarning(
                'ファイル読込失敗', e)
        return None
    read_text = ''.join(read_list)
    del read_list
    d.dprint(read_text)
    return read_text


def save_file(folder, zeihou_mei, kubun, jou_jou):
    d.dprint(kubun)
    list_log = []
    for kou in jou_jou.kou_list:
        md_kou = Md(zeihou_mei, kubun,
                (kou.jou_bangou_tuple, kou.kou_bangou, None),
                kou.honbun)
        md_kou.set_part(jou_jou.kubun)
        soku = jou_jou.get_soku()
        md_kou.set_soku(soku)
        midashi = jou_jou.get_midashi()
#         d.dprint(midashi)
        md_kou.set_midashi(midashi)
        md_kou.set_kou(kou)
        md_kou.sakusei_file(folder)
        md_kou.save()
        list_log.append('\t\t{}\n'.format(
                os.path.basename(md_kou.file_name)))
#         if len(kou.gou_list) != 0:
        (file_name, file_bun) = \
                md_kou.sakusei_file_full_kou(
                folder, kou, kou.gou_list)
#         d.dprint(file_name)
#         d.dprint(file_bun)
        with open(file_name,
            mode='w',
            encoding='UTF-8') as f:
            f.write(file_bun)
        del md_kou
        for gou in kou.gou_list:
            # 号の処理
            honbun = gou.get_honbun()   # イ、ロ、ハ付き
#             print(honbun)
            md = Md(zeihou_mei, kubun,
                    (gou.jou_bangou_tuple, gou.kou_bangou,
                    gou.gou_bangou_tuple),
                    honbun)
#                     honbun, None, None, gou)
            md.set_part(jou_jou.kubun)
            md.set_soku(soku)
            md.set_midashi(midashi)
            md.set_gou(gou)
            md.sakusei_file(folder)
            md.save()
            list_log.append('\t\t{}\n'.format(
                    os.path.basename(md.file_name)))
#     d.dprint(jou_jou.bangou_tuple)
    (file_name, file_bun) = \
            Md.sakusei_file_full_jou(
            folder, zeihou_mei, kubun, jou_jou)
    with open(file_name,
        mode='w',
        encoding='UTF-8') as f:
        f.write(file_bun)
    return list_log


def kakou1():
    '''
    処理フォルダ内のxxx.mdファイルを
    加工１して上書き保存する。
    '''
    d.dprint_method_start()
#     global folder_name
    files = os.listdir(config.folder_name)
    global hou_rei_dict, hou_ki_dict, rei_ki_dict
    hou_rei_dict = {}
    hou_ki_dict = {}
    rei_ki_dict = {}
    if len(files):
        list_log = [ '加工１を行ないました。\n' ]
    else:
        list_log = [ '加工１を行なうファイルが' \
                'ありませんでした。\n' ]
    src_list_full = []
    for file_name in files:
        if os.path.isdir(os.path.join(
                config.folder_name, file_name)):
            continue
        if (file_name[0] == '.') \
                or (file_name[0] == '_'):
            continue
        if (file_name[-3:] != '.md'):
            continue
        if (file_name[-4:] == '_.md'):
            # "所得税法第９条_.md"などは
            # 加工対象外とする
            continue
        md = Md.load(config.folder_name, file_name)
        if md == None:
            continue
        bun = Bun.md_to_bun(md)
        dict_key = (bun.kubun_mei, bun.zeihou_mei,
                md.soku,
                bun.joubun_bangou)
        # d.dprint(bun.joubun_bangou)
        # d.dprint(dict_key)
        # d.dprint(config.jiko1_dict)
        if dict_key in config.jiko1_dict:
            # 既に、jiko1_dictにデータあり
            dict_value = config.jiko1_dict[dict_key]
        else:
            dict_value = []
        if dict_key in config.jogai_dict:
            jogai_list = config.jogai_dict[dict_key]
        else:
            jogai_list = []
        (ref_pair_list, src_list) = bun.kakou1(
                dict_value,
                jogai_list)
#         d.dprint_name("bun.kakou_bun", bun.kakou_bun)
        src_list_full.extend(src_list)
        del src_list
        md.set_file_bun(bun.get_kakou_bun())
#         d.dprint_name("md.file_bun", md.file_bun)
        md.save()

        joubun_mei = Bun.create_joubun_file_name(
                bun.zeihou_mei, bun.kubun,
                bun.soku,
                bun.joubun_bangou)
        if bun.kubun == Bun.kubunRei:
            for ref_pair in ref_pair_list:
                # ref_pair = (
                #    "消費税", bun.kubunHou,
                #    "＿", 条文番号タプル)
#                 d.dprint(ref_pair)
                if ref_pair[1] == bun.kubunHou:
                    if (ref_pair[0], ref_pair[2], ref_pair[3]) \
                            in hou_rei_dict:
                        value = hou_rei_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]]
                        value.append((joubun_mei,
                                bun.joubun_bangou))
                        hou_rei_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]] \
                                = value
                    else:
                        hou_rei_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]] \
                                = [(joubun_mei,
                                bun.joubun_bangou)]
                else:
                    d.dprint(ref_pair)
                    d.dprint("===================")
                    continue
#                     assert(False)
        elif bun.kubun == Bun.kubunKi:
            for ref_pair in ref_pair_list:
                if ref_pair[1] == bun.kubunHou:
                    if (ref_pair[0], ref_pair[2], ref_pair[3]) \
                            in hou_ki_dict:
                        value = hou_ki_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]]
                        value.append((joubun_mei,
                                bun.joubun_bangou))
                        hou_ki_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]] \
                                = value
                    else:
                        hou_ki_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]] \
                                = [(joubun_mei,
                                bun.joubun_bangou)]
                elif ref_pair[1] == bun.kubunRei:
                    if (ref_pair[0], ref_pair[2], ref_pair[3]) \
                            in rei_ki_dict:
                        value = rei_ki_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]]
                        value.append((joubun_mei,
                                bun.joubun_bangou))
                        rei_ki_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]] \
                                = value
                    else:
                        rei_ki_dict[
                                ref_pair[0], ref_pair[2], ref_pair[3]] \
                                = [(joubun_mei,
                                bun.joubun_bangou)]
                else:
                    d.dprint(ref_pair)
                    d.dprint("===================")
                    continue
#                     assert(False)
        else:
            # 消費税法第３８条第３項
            #　新消費税法第三十条第七項に規定する請求書等の
            pass
#             d.dprint(ref_pair_list)
#             if len(ref_pair_list) != 0:
#                 assert(False)
        list_log.append('\t{}\n'.format(file_name))
    src_set = set(src_list_full)
    del src_list_full
    if len(src_set) != 0:
        list_log.append(
                '\t見つからない参照ファイル\n')
        flag = False
        for src_file in src_set:
#             d.dprint(src_file)
            full_name = os.path.join(config.folder_name,
                    src_file+'.md')
            if not os.path.isfile(full_name):
                # 参照元のファイルがない
                list_log.append('\t\t{}\n' \
                        .format(src_file))
                flag = True
        if not flag:
            list_log.append(
                    '\t\tはありませんでした。\n')
    del src_set
    if (len(hou_rei_dict) > 0) or (len(hou_ki_dict) > 0) \
            or (len(rei_ki_dict) > 0):
        list_log.append(
                '続けて、加工２を実行してください。\n')
    str_log = ''.join(list_log)
#     set_log(str_log)
    print(str_log)
    d.dprint_name("hou_rei_dict", hou_rei_dict)
    d.dprint_name("hou_ki_dict", hou_ki_dict)
    d.dprint_name("rei_ki_dict", rei_ki_dict)
    d.dprint_method_end()
    return


def kakou1_ji():
    '''
    加工１処理のうち、各法令内部の処理
    '''
    d.dprint_method_start()
    files = os.listdir(config.folder_name)
#     src_list_full = []
    for file_name in files:
        if os.path.isdir(os.path.join(
                config.folder_name, file_name)):
            continue
        if (file_name[0] == '.') \
                or (file_name[0] == '_'):
            continue
        if (file_name[-3:] != '.md'):
            continue
        if (file_name[-4:] == '_.md'):
            # "所得税法第９条_.md"などは
            # 加工対象外とする
            continue
        md = Md.load(config.folder_name, file_name)
        if md == None:
            continue
        bun = Bun.md_to_bun(md)
        dict_key = (bun.kubun_mei, bun.zeihou_mei,
                md.soku,
                bun.joubun_bangou)
        if dict_key in config.jiko1_dict:
            # 既に、jiko1_dictにデータあり
            dict_value = config.jiko1_dict[dict_key]
        else:
            dict_value = []
        if dict_key in config.jogai_dict:
            jogai_list = config.jogai_dict[dict_key]
        else:
            jogai_list = []
#         src_list = bun.kakou1_ji(
        bun.kakou1_ji(
                dict_value,
                jogai_list)
#         src_list_full.extend(src_list)
#         del src_list
        md.set_file_bun(bun.get_kakou_bun())
        md.save()
#     del src_list_full
    d.dprint_method_end()
    return

def kakou1_hou_rei():
    '''
    加工１処理のうち、法と施行令のリンクの処理
    '''
    d.dprint_method_start()
#     global folder_name
    files = os.listdir(config.folder_name)
    global hou_rei_dict #, hou_ki_dict, rei_ki_dict
    hou_rei_dict = {}
#     hou_ki_dict = {}
#     rei_ki_dict = {}
    if len(files):
        list_log = [ '加工１を行ないました。\n' ]
    else:
        list_log = [ '加工１を行なうファイルが' \
                'ありませんでした。\n' ]
    for file_name in files:
        if os.path.isdir(os.path.join(
                config.folder_name, file_name)):
            continue
        if (file_name[0] == '.') \
                or (file_name[0] == '_'):
            continue
        if (file_name[-3:] != '.md'):
            continue
        if (file_name[-4:] == '_.md'):
            # "所得税法第９条_.md"などは
            # 加工対象外とする
            continue
        md = Md.load(config.folder_name, file_name)
        if md == None:
            continue
        if md.kubun != Md.kubunRei:
            continue
        bun = Bun.md_to_bun(md)
        dict_key = (bun.kubun_mei, bun.zeihou_mei,
                md.soku,
                bun.joubun_bangou)
        if dict_key in config.jiko1_dict:
            # 既に、jiko1_dictにデータあり
            dict_value = config.jiko1_dict[dict_key]
        else:
            dict_value = []
        if dict_key in config.jogai_dict:
            jogai_list = config.jogai_dict[dict_key]
        else:
            jogai_list = []
        ref_pair_list = bun.kakou1_hou_rei(
                dict_value,
                jogai_list)
        md.set_file_bun(bun.get_kakou_bun())
#         d.dprint_name("md.file_bun", md.file_bun)
        md.save()

        joubun_mei = Bun.create_joubun_file_name(
                bun.zeihou_mei, bun.kubun,
                bun.soku,
                bun.joubun_bangou)
        for ref_pair in ref_pair_list:
            # ref_pair = (
            #    "消費税", bun.kubunHou,
            #    "＿", 条文番号タプル)
#                 d.dprint(ref_pair)
            if ref_pair[1] == bun.kubunHou:
                if (ref_pair[0], ref_pair[2],
                            ref_pair[3]) \
                        in hou_rei_dict:
                    value = hou_rei_dict[ref_pair[0],
                            ref_pair[2], ref_pair[3]]
                    value.append((joubun_mei,
                            bun.joubun_bangou))
                    hou_rei_dict[ref_pair[0],
                            ref_pair[2], ref_pair[3]] \
                            = value
                else:
                    hou_rei_dict[ref_pair[0],
                            ref_pair[2], ref_pair[3]] \
                            = [(joubun_mei,
                            bun.joubun_bangou)]
            else:
                d.dprint(ref_pair)
                d.dprint("===================")
                continue
#                     assert(False)
        list_log.append('\t{}\n'.format(file_name))
    str_log = ''.join(list_log)
    del list_log
#     set_log(str_log)
    print(str_log)
    d.dprint_name("hou_rei_dict", hou_rei_dict)
#     d.dprint_name("hou_ki_dict", hou_ki_dict)
#     d.dprint_name("rei_ki_dict", rei_ki_dict)
    d.dprint_method_end()
    return

def kakou1_hou_ki():
    '''
    加工１処理のうち、法と施行規則のリンクの処理
    '''
    d.dprint_method_start()
#     global folder_name
    files = os.listdir(config.folder_name)
    global hou_ki_dict
    hou_ki_dict = {}
    if len(files):
        list_log = [ '加工１を行ないました。\n' ]
    else:
        list_log = [ '加工１を行なうファイルが' \
                'ありませんでした。\n' ]
    for file_name in files:
        if os.path.isdir(os.path.join(
                config.folder_name, file_name)):
            continue
        if (file_name[0] == '.') \
                or (file_name[0] == '_'):
            continue
        if (file_name[-3:] != '.md'):
            continue
        if (file_name[-4:] == '_.md'):
            # "所得税法第９条_.md"などは
            # 加工対象外とする
            continue
        md = Md.load(config.folder_name, file_name)
        if md == None:
            continue
        if md.kubun != Md.kubunKi:
            continue
        bun = Bun.md_to_bun(md)
        dict_key = (bun.kubun_mei, bun.zeihou_mei,
                md.soku,
                bun.joubun_bangou)
        if dict_key in config.jiko1_dict:
            # 既に、jiko1_dictにデータあり
            dict_value = config.jiko1_dict[dict_key]
        else:
            dict_value = []
        if dict_key in config.jogai_dict:
            jogai_list = config.jogai_dict[dict_key]
        else:
            jogai_list = []
        ref_pair_list = bun.kakou1_hou_ki(
                dict_value,
                jogai_list)
        md.set_file_bun(bun.get_kakou_bun())
#         d.dprint_name("md.file_bun", md.file_bun)
        md.save()

        joubun_mei = Bun.create_joubun_file_name(
                bun.zeihou_mei, bun.kubun,
                bun.soku,
                bun.joubun_bangou)
        for ref_pair in ref_pair_list:
            if ref_pair[1] == bun.kubunHou:
                if (ref_pair[0], ref_pair[2], ref_pair[3]) \
                        in hou_ki_dict:
                    value = hou_ki_dict[
                            ref_pair[0], ref_pair[2], ref_pair[3]]
                    value.append((joubun_mei,
                            bun.joubun_bangou))
                    hou_ki_dict[
                            ref_pair[0], ref_pair[2], ref_pair[3]] \
                            = value
                else:
                    hou_ki_dict[
                            ref_pair[0], ref_pair[2], ref_pair[3]] \
                            = [(joubun_mei,
                            bun.joubun_bangou)]
#             elif ref_pair[1] == bun.kubunRei:
#                 if (ref_pair[0], ref_pair[2], ref_pair[3]) \
#                         in rei_ki_dict:
#                     value = rei_ki_dict[
#                             ref_pair[0], ref_pair[2], ref_pair[3]]
#                     value.append((joubun_mei,
#                             bun.joubun_bangou))
#                     rei_ki_dict[
#                             ref_pair[0], ref_pair[2], ref_pair[3]] \
#                             = value
#                 else:
#                     rei_ki_dict[
#                             ref_pair[0], ref_pair[2], ref_pair[3]] \
#                             = [(joubun_mei,
#                             bun.joubun_bangou)]
#             else:
#                 d.dprint(ref_pair)
#                 d.dprint("===================")
#                 continue
#                     assert(False)
        list_log.append('\t{}\n'.format(file_name))
    str_log = ''.join(list_log)
    del list_log
#     set_log(str_log)
    print(str_log)
    d.dprint_name("hou_ki_dict", hou_ki_dict)
#     d.dprint_name("rei_ki_dict", rei_ki_dict)
    d.dprint_method_end()
    return

def kakou1_rei_ki():
    '''
    加工１処理のうち、法と施行規則のリンクの処理
    '''
    d.dprint_method_start()
#     global folder_name
    files = os.listdir(config.folder_name)
    global rei_ki_dict
    rei_ki_dict = {}
    if len(files):
        list_log = [ '加工１を行ないました。\n' ]
    else:
        list_log = [ '加工１を行なうファイルが' \
                'ありませんでした。\n' ]
    for file_name in files:
        if os.path.isdir(os.path.join(
                config.folder_name, file_name)):
            continue
        if (file_name[0] == '.') \
                or (file_name[0] == '_'):
            continue
        if (file_name[-3:] != '.md'):
            continue
        if (file_name[-4:] == '_.md'):
            # "所得税法第９条_.md"などは
            # 加工対象外とする
            continue
        md = Md.load(config.folder_name, file_name)
        if md == None:
            continue
        if md.kubun != Md.kubunKi:
            continue
        bun = Bun.md_to_bun(md)
        dict_key = (bun.kubun_mei, bun.zeihou_mei,
                md.soku,
                bun.joubun_bangou)
        if dict_key in config.jiko1_dict:
            # 既に、jiko1_dictにデータあり
            dict_value = config.jiko1_dict[dict_key]
        else:
            dict_value = []
        if dict_key in config.jogai_dict:
            jogai_list = config.jogai_dict[dict_key]
        else:
            jogai_list = []
        ref_pair_list = bun.kakou1_rei_ki(
                dict_value,
                jogai_list)
        md.set_file_bun(bun.get_kakou_bun())
#         d.dprint_name("md.file_bun", md.file_bun)
        md.save()

        joubun_mei = Bun.create_joubun_file_name(
                bun.zeihou_mei, bun.kubun,
                bun.soku,
                bun.joubun_bangou)
        for ref_pair in ref_pair_list:
            if ref_pair[1] == bun.kubunRei:
                if (ref_pair[0], ref_pair[2], ref_pair[3]) \
                        in rei_ki_dict:
                    value = rei_ki_dict[
                            ref_pair[0], ref_pair[2], ref_pair[3]]
                    value.append((joubun_mei,
                            bun.joubun_bangou))
                    rei_ki_dict[
                            ref_pair[0], ref_pair[2], ref_pair[3]] \
                            = value
                else:
                    rei_ki_dict[
                            ref_pair[0], ref_pair[2], ref_pair[3]] \
                            = [(joubun_mei,
                            bun.joubun_bangou)]
        list_log.append('\t{}\n'.format(file_name))
    str_log = ''.join(list_log)
    del list_log
#     set_log(str_log)
    print(str_log)
    d.dprint_name("rei_ki_dict", rei_ki_dict)
    d.dprint_method_end()
    return

def kakou2():
    # 除外リスト処理を検討
    d.dprint_method_start()
#     global folder_name
    global hou_rei_dict, hou_ki_dict, rei_ki_dict
#     d.dprint(hou_rei_dict)
    # hou_ki_dict[('消費税法',((2,),1,(8,)))] =
    #    ["消費税法施行規則第２条第１項",
    #    (((2,),1,None))]
    # 消費税法２①八の中の「財務省令で定める」は
    # 消費税法施行規則２①に対応することを示している

# ('法', '法施行令', 措置', ((69, 4), 1, None)) :
# [ (3, ('措置法施行＿令第４０条の２第１項', ((40, 2), 1, None))),
#   (5, ('措置法施行＿令第４０条の２第４項', ((40, 2), 4, None)) ]
# ('法', '法施行規則', '措置', ((2,), 1, (16,))):
# [(1, ('措置法施行＿令第４０条の２第４項', ((40, 2), 4, None)))]

    list_log = [ '加工２を行ないました。\n' ]

    # TODO hou_rei_dict が空で、自己設定のみの場合が
    # 処理できない

        # dict_key = (bun.kubun_mei, bun.zeihou_mei,
        #         md.soku,
        #         bun.joubun_bangou)

    for key_tuple, value_list in hou_rei_dict.items():
#         d.dprint(key_tuple)
#         d.dprint(value_list)
        file_name = Md.create_file_name(
                zeihou_mei=key_tuple[0],
                kubun=Md.kubunHou,
                soku=key_tuple[1],
                joubun_bangou=key_tuple[2])
        md = Md.load(config.folder_name, file_name)
        if md == None:
#             list_log.append("\t【{}】などに対応する" \
#                     "\n\t\tファイル【{}】" \
#                     "が見つかりません、または、" \
#                     "オープンに失敗しました。\n" \
#                     "\t\t違う法令の可能性があります。\n". \
#                     format(value_list[0][0], file_name))
            continue
#         list_log.append("\t{}\n".format(file_name))
        bun = Bun.md_to_bun(md)
        # key のソートがNoneでエラー
        zero_list = []  # 号のNoneを省く
        for value in value_list:
            if value[1][2] != None:
                zero_list.append(value)
            else:
                zero_list.append(
                        (value[0],
                        (value[1][0], value[1][1])))
        # del value_list
        sort_list = sorted(zero_list,
                reverse=False, key=lambda x:x[1])
        del zero_list
        jiko2_key = ('法', '法施行令',
                key_tuple[0], key_tuple[1])
        if jiko2_key in config.jiko2_dict:
            values = config.jiko2_dict[jiko2_key]
            value_list = sorted(values, reverse=True,
                    key=lambda x:x[0])
            for value in value_list:
                data = (value[1][0], value[1][1])
                sort_list.insert(value[0] - 1, data)
        log_msg = bun.kakou2_rei(key_tuple[0],
                sort_list)
        if log_msg == None:
            md.set_file_bun(bun.kakou_bun)
            md.save()
            list_log.append('\t成功　')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
        else:
            list_log.append('\t失敗　')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
            list_log.append('\t\t')
            list_log.extend(log_msg)
            del log_msg
            for value in sort_list:
                list_log.append('\t\t\t{}\n'. \
                        format(value[0]))
        del sort_list
    for key_tuple, value_list in hou_ki_dict.items():
#         d.dprint(key_tuple)
#         d.dprint(value_list)
        file_name = Md.create_file_name(
                zeihou_mei=key_tuple[0],
                kubun=Md.kubunHou,
                soku=key_tuple[1],
                joubun_bangou=key_tuple[2])
        md = Md.load(config.folder_name, file_name)
        if md == None:
            list_log.append("\t【{}】などに対応する" \
                    "\n\t\tファイル【{}】" \
                    "が見つかりません、または、" \
                    "オープンに失敗しました。\n" \
                    "\t\t違う法令の可能性があります。\n". \
                    format(value_list[0][0], file_name))
            continue
#         list_log.append("\t{}\n".format(file_name))
        bun = Bun.md_to_bun(md)
        zero_list = []  # 号のNoneを省く
        for value in value_list:
            if value[1][2] != None:
                zero_list.append(value)
            else:
                zero_list.append(
                        (value[0],
                        (value[1][0], value[1][1])))
        # del value_list
        sort_list = sorted(zero_list,
                reverse=False, key=lambda x:x[1])
        del zero_list
        jiko2_key = ('法', '法施行規則',
                key_tuple[0], key_tuple[1])
        if jiko2_key in config.jiko2_dict:
            values = config.jiko2_dict[jiko2_key]
            value_list = sorted(values, reverse=True,
                    key=lambda x:x[0])
            for value in value_list:
                data = (value[1][0], value[1][1])
                sort_list.insert(value[0], data)
        log_msg = bun.kakou2_ki(key_tuple[0], sort_list)
        if log_msg == None:
            md.set_file_bun(bun.kakou_bun)
            md.save()
            list_log.append('\t成功　')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
        else:
            list_log.append('\t失敗　')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
            list_log.append('\t\t')
            list_log.extend(log_msg)
            del log_msg
            for value in sort_list:
                list_log.append('\t\t\t{}\n'. \
                        format(value[0]))
        del sort_list
    for key_tuple, value_list in rei_ki_dict.items():
#         d.dprint(key_tuple)
#         d.dprint(value_list)
        file_name = Md.create_file_name(
                zeihou_mei=key_tuple[0],
                kubun=Md.kubunRei,
                soku=key_tuple[1],
                joubun_bangou=key_tuple[2])
        md = Md.load(config.folder_name, file_name)
        if md == None:
            list_log.append("\t【{}】などに対応する" \
                    "\n\t\tファイル【{}】" \
                    "が見つかりません、または、" \
                    "オープンに失敗しました。\n" \
                    "\t\t違う法令の可能性があります。\n". \
                    format(value_list[0][0], file_name))
            continue
#         list_log.append("\t{}\n".format(file_name))
        bun = Bun.md_to_bun(md)
        zero_list = []  # 号のNoneを省く
        for value in value_list:
            if value[1][2] != None:
                zero_list.append(value)
            else:
                zero_list.append(
                        (value[0],
                        (value[1][0], value[1][1])))
        # del value_list
        sort_list = sorted(zero_list,
                reverse=False, key=lambda x:x[1])
        del zero_list
        jiko2_key = ('法施行令', '法施行規則',
                key_tuple[0], key_tuple[1])
        if jiko2_key in config.jiko2_dict:
            values = config.jiko2_dict[jiko2_key]
            value_list = sorted(values, reverse=True,
                    key=lambda x:x[0])
            for value in value_list:
                data = (value[1][0], value[1][1])
                sort_list.insert(value[0], data)
        log_msg = bun.kakou2_ki(key_tuple[0], sort_list)
        if log_msg == None:
            md.set_file_bun(bun.kakou_bun)
            md.save()
            list_log.append('\t成功')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
        else:
            list_log.append('\t失敗')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
            list_log.append('\t\t')
            list_log.extend(log_msg)
            del log_msg
            for value in sort_list:
                list_log.append('\t\t\t{}\n'. \
                        format(value[0]))
        del sort_list
    str_log = ''.join(list_log)
    del list_log
#     set_log(str_log)
    print(str_log)
    d.dprint_method_end()
    return


def kakou2_hou_rei():
    # 除外リスト処理を検討
    d.dprint_method_start()
    global hou_rei_dict #, hou_ki_dict, rei_ki_dict
    # hou_ki_dict[('消費税法',((2,),1,(8,)))] =
    #    ["消費税法施行規則第２条第１項",
    #    (((2,),1,None))]
    # 消費税法２①八の中の「財務省令で定める」は
    # 消費税法施行規則２①に対応することを示している

    list_log = [ '加工２を行ないました。\n' ]

        # dict_key = (bun.kubun_mei, bun.zeihou_mei,
        #         md.soku,
        #         bun.joubun_bangou)

    for key_tuple, value_list in hou_rei_dict.items():
        file_name = Md.create_file_name(
                zeihou_mei=key_tuple[0],
                kubun=Md.kubunHou,
                soku=key_tuple[1],
                joubun_bangou=key_tuple[2])
        md = Md.load(config.folder_name, file_name)
        if md == None:
            list_log.append("\t【{}】などに対応する" \
                    "\n\t\tファイル【{}】" \
                    "が見つかりません、または、" \
                    "オープンに失敗しました。\n" \
                    "\t\t違う法令の可能性があります。\n". \
                    format(value_list[0][0], file_name))
            continue
        bun = Bun.md_to_bun(md)
        # key のソートがNoneでエラー
        zero_list = []  # 号のNoneを省く
        for value in value_list:
            if value[1][2] != None:
                zero_list.append(value)
            else:
                zero_list.append(
                        (value[0],
                        (value[1][0], value[1][1])))
        # del value_list
        sort_list = sorted(zero_list,
                reverse=False, key=lambda x:x[1])
        del zero_list
        jiko2_key = ('法', '法施行令',
                key_tuple[0], key_tuple[1])
        if jiko2_key in config.jiko2_dict:
            values = config.jiko2_dict[jiko2_key]
            value_list = sorted(values, reverse=True,
                    key=lambda x:x[0])
            for value in value_list:
                data = (value[1][0], value[1][1])
                sort_list.insert(value[0] - 1, data)
        log_msg = bun.kakou2_rei(key_tuple[0],
                sort_list)
        if log_msg == None:
            md.set_file_bun(bun.kakou_bun)
            md.save()
            list_log.append('\t成功　')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
        else:
            list_log.append('\t失敗　')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
            list_log.append('\t\t')
            list_log.extend(log_msg)
            del log_msg
            for value in sort_list:
                list_log.append('\t\t\t{}\n'. \
                        format(value[0]))
        del sort_list
#         del sort_list
    str_log = ''.join(list_log)
    del list_log
#     set_log(str_log)
    print(str_log)
    del hou_rei_dict
    d.dprint_method_end()
    return

def kakou2_hou_ki():
    # 除外リスト処理を検討
    d.dprint_method_start()
    global hou_ki_dict
    list_log = [ '加工２を行ないました。\n' ]
    for key_tuple, value_list in hou_ki_dict.items():
        file_name = Md.create_file_name(
                zeihou_mei=key_tuple[0],
                kubun=Md.kubunHou,
                soku=key_tuple[1],
                joubun_bangou=key_tuple[2])
        md = Md.load(config.folder_name, file_name)
        if md == None:
            list_log.append("\t【{}】などに対応する" \
                    "\n\t\tファイル【{}】" \
                    "が見つかりません、または、" \
                    "オープンに失敗しました。\n" \
                    "\t\t違う法令の可能性があります。\n". \
                    format(value_list[0][0], file_name))
            continue
        list_log.append("\t{}\n".format(file_name))
        bun = Bun.md_to_bun(md)
        zero_list = []  # 号のNoneを省く
        for value in value_list:
            if value[1][2] != None:
                zero_list.append(value)
            else:
                zero_list.append(
                        (value[0],
                        (value[1][0], value[1][1])))
        sort_list = sorted(zero_list,
                reverse=False, key=lambda x:x[1])
        del zero_list
        jiko2_key = ('法', '法施行規則',
                key_tuple[0], key_tuple[1])
        if jiko2_key in config.jiko2_dict:
            values = config.jiko2_dict[jiko2_key]
            value_list = sorted(values, reverse=True,
                    key=lambda x:x[0])
            for value in value_list:
                data = (value[1][0], value[1][1])
                sort_list.insert(value[0], data)
        log_msg = bun.kakou2_ki(key_tuple[0], sort_list)
        if log_msg == None:
            md.set_file_bun(bun.kakou_bun)
            md.save()
            list_log.append('\t成功　')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
        else:
            list_log.append('\t失敗　')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
            list_log.append('\t\t')
            list_log.extend(log_msg)
            del log_msg
            for value in sort_list:
                list_log.append('\t\t\t{}\n'. \
                        format(value[0]))
        del sort_list
    str_log = ''.join(list_log)
    del list_log
#     set_log(str_log)
    print(str_log)
    del hou_ki_dict
    d.dprint_method_end()
    return

def kakou2_rei_ki():
    # 除外リスト処理を検討
    d.dprint_method_start()
    list_log = []
    global rei_ki_dict
    for key_tuple, value_list in rei_ki_dict.items():
        file_name = Md.create_file_name(
                zeihou_mei=key_tuple[0],
                kubun=Md.kubunRei,
                soku=key_tuple[1],
                joubun_bangou=key_tuple[2])
        md = Md.load(config.folder_name, file_name)
        if md == None:
            list_log.append("\t【{}】などに対応する" \
                    "\n\t\tファイル【{}】" \
                    "が見つかりません、または、" \
                    "オープンに失敗しました。\n" \
                    "\t\t違う法令の可能性があります。\n". \
                    format(value_list[0][0], file_name))
            continue
        bun = Bun.md_to_bun(md)
        zero_list = []  # 号のNoneを省く
        for value in value_list:
            if value[1][2] != None:
                zero_list.append(value)
            else:
                zero_list.append(
                        (value[0],
                        (value[1][0], value[1][1])))
        sort_list = sorted(zero_list,
                reverse=False, key=lambda x:x[1])
        del zero_list
        jiko2_key = ('法施行令', '法施行規則',
                key_tuple[0], key_tuple[1])
        if jiko2_key in config.jiko2_dict:
            values = config.jiko2_dict[jiko2_key]
            value_list = sorted(values, reverse=True,
                    key=lambda x:x[0])
            for value in value_list:
                data = (value[1][0], value[1][1])
                sort_list.insert(value[0], data)
        log_msg = bun.kakou2_ki(key_tuple[0], sort_list)
        if log_msg == None:
            md.set_file_bun(bun.kakou_bun)
            md.save()
            list_log.append('\t成功')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
        else:
            list_log.append('\t失敗')
            list_log.append(os.path.basename(md.file_name))
            list_log.append('\n')
            list_log.append('\t\t')
            list_log.extend(log_msg)
            del log_msg
            for value in sort_list:
                list_log.append('\t\t\t{}\n'. \
                        format(value[0]))
        del sort_list
    str_log = ''.join(list_log)
    del list_log
#     set_log(str_log)
    print(str_log)
    del rei_ki_dict
    d.dprint_method_end()
    return


def rename_file():
    '''
    処理フォルダ内の_xxx.txtファイルの名前を
    xxx.txtにする。
    divide_kougouで
    先頭に_を付けた名前に変更されたものを戻す。
    '''
    d.dprint_method_start()
#     global folder_name
    files = os.listdir(config.folder_name)
    list_file = []
    out_file = []
    for file_name in files:
        if os.path.isdir(
                os.path.join(config.folder_name, file_name)):
            continue
        if os.path.splitext(file_name)[1] != '.txt':
            continue
        if file_name[0] != '_':
            out_file.append(file_name)
            continue
        if file_name[:2] == '__':
            # 処理済み条文ファイルの戻しの対象外
            out_file.append(file_name)
            continue
        if ('法' not in file_name) and \
                ('令' not in file_name) and \
                ('規' not in file_name):
            out_file.append(file_name)
            continue
        list_file.append(file_name)
    del files
    d.dprint(list_file)

    if len(list_file):
        list_log = [ 'ファイル名を変更しました。\n']
    else:
        list_log = [ 'ファイル名を変更するファイルが' \
                'ありませんでした。\n']
    for file_name in list_file:
        full_name = os.path.join(config.folder_name,
                file_name)
        new_name = os.path.join(config.folder_name,
                file_name[1:])
        try:
            os.rename(full_name, new_name)
        except Exception as _e:
            list_log.append('\t既にファイル【{}】が' \
                    'ありました。\n' \
                    .format(file_name[1:]))
            continue
        list_log.append('\t{} -> {}\n'.format(
                file_name, file_name[1:]))
    if len(out_file) != 0:
        list_log.append(
                '次のファイルは変更の対象外です。\n')
        for file in out_file:
            list_log.append('\t{}\n'.format(file))
    del list_file
    del out_file
    list_log.append('項号分割を実行してください。\n')
    str_log = ''.join(list_log)
#     set_log(str_log)
    print(str_log)
    return


def set_link1():
    # 前項第１項などを自分で設定する
    from dialogLink1 import DialogLink1
    DialogLink1()
    return


def set_link2():
    # 政令で定めるなどを自分で設定する
    from dialogLink2 import DialogLink2
    DialogLink2()
    return


def set_jogai():
    # ハイバーリンクを設定しない文言を設定する
    from dialogJogai import DialogJogai
    DialogJogai()
    return


def set_link2_2(dlg):
    return


def full_process():
    divide_kougou()
    kakou1()
    kakou2()
    return

def set_log(str_log):
#     config.form_log.configure(state=NORMAL)
#     config.form_log.insert("end", str_log)
#     config.form_log.see("end")
#     config.form_log.configure(state=DISABLED)
    print(str_log)


def shuryou():
    sys.exit()


def load_tokachi_file():
    d.dprint_method_start()
    full_name = os.path.join(config.folder_name,
            TOKACHI_FILE_NAME)
    input_list = []
    try:
        with open(full_name, "r", encoding="ms932",
                newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                input_list.append(row)
    except OSError as e:
        set_log('ファイル【{}】の読込に失敗しました。{}\n' \
                .format(full_name, str(e)))
        return
    d.dprint(input_list)
    for koumoku in input_list:
        d.dprint(koumoku)
        if len(koumoku) == 0:
            break
        if koumoku[0] == '加工１':
            pass
        elif koumoku[0] == '自己１':
            moto_tuple = list2jou_tuple(koumoku[3:10])
            saki_tuple = list2jou_tuple(koumoku[14:21])
            key = (koumoku[1], koumoku[2],
                   moto_tuple)
            item = (koumoku[10], koumoku[11],
                    koumoku[12], (koumoku[13], saki_tuple))
            if key in config.jiko1_dict:
                value = config.jiko1_dict[key]
                value.append(item)
                config.jiko1_dict[key] = value
            else:
                config.jiko1_dict[key] = [item]
            d.dprint(key)
            d.dprint(item)
        elif koumoku[0] == '自己２':
            moto_tuple = list2jou_tuple(koumoku[5:12])
            saki_tuple = list2jou_tuple(koumoku[13:20])
            key = (koumoku[1], koumoku[2],
                   koumoku[3], moto_tuple)
            item = (int(koumoku[4]), (koumoku[12], saki_tuple))
            if key in config.jiko2_dict:
                value = config.jiko2_dict[key]
                value.append(item)
                config.jiko2_dict[key] = value
            else:
                config.jiko2_dict[key] = [item]
            d.dprint(key)
            d.dprint(item)
        elif koumoku[0] == '除外':
            moto_tuple = list2jou_tuple(koumoku[3:10])
            key = (koumoku[1], koumoku[2],
                   moto_tuple)
            item = koumoku[10]
            if key in config.jogai_dict:
                value = config.jogai_dict[key]
                value.append(item)
                config.jogai_dict[key] = value
            else:
                config.jogai_dict[key] = [item]
            d.dprint(key)
            d.dprint(item)
        else:
            str_log = 'データが誤っています。{}\n' \
                    .format(','.join(koumoku))
            set_log(str_log)
    d.dprint_method_end()
    return


def save_tokachi_file():
    full_name = os.path.join(config.folder_name,
            TOKACHI_FILE_NAME)
    try:
        with open(full_name, "w", encoding="ms932",
                newline='') as csvfile:
            writer = csv.writer(csvfile)
#         key = (kubun_moto, zeihou_mei_moto, moto_tuple)
#         item = (kubun_saki, zeihou_mei_saki,
#                 koumoku, (saki_link, saki_tuple))

            for (key, values) in config.jiko1_dict.items():
                for value in values:
                    list_row = kv1row(key, value)
                    list_row.insert(0, '自己１')
                    writer.writerow(list_row)
                    del list_row
# ('法', '法施行令', 措置', (...)) :
# [ (3, ('措置法施行＿令第４０条の２第１項', ((40, 2), 1, None))),
#   (5, ('措置法施行＿令第４０条の２第４項', ((40, 2), 4, None)) ]
# ('法', '法施行規則', '措置', ((2,), 1, (16,))):
# [(1, ('措置法施行＿令第４０条の２第４項', ((40, 2), 4, None)))]
            for (key, values) in config.jiko2_dict.items():
                for value in values:
                    list_row = kv2row(key, value)
                    list_row.insert(0, '自己２')
                    writer.writerow(list_row)
                    del list_row
            for (key, values) in config.jogai_dict.items():
                for value in values:
                    list_row = kv3row(key, value)
                    list_row.insert(0, '除外')
                    writer.writerow(list_row)
                    del list_row
    except OSError as e:
        set_log('ファイル【{}】の書込に失敗しました。{}\n' \
                .format(full_name, str(e)))
        return
    return


def kv1row(key, value):
#         key = (kubun_moto, zeihou_mei_moto, moto_tuple)
#         item = (kubun_saki, zeihou_mei_saki,
#                 koumoku, (saki_link, saki_tuple))
    list_row = [key[0], key[1] ]
    jou_moto_list = jou_tuple2list(key[2])
    list_row.extend(jou_moto_list)
    list_row.append(value[0])
    list_row.append(value[1])
    list_row.append(value[2])
    list_row.append(value[3][0])
    jou_saki_list = jou_tuple2list(value[3][1])
    list_row.extend(jou_saki_list)
    del jou_moto_list, jou_saki_list
    d.dprint(list_row)
    return list_row


def kv2row(key, value):
    list_row = [key[0], key[1], key[2], value[0]]
    jou_moto_list = jou_tuple2list(key[3])
    jou_saki_list = jou_tuple2list(value[1][1])
    list_row.extend(jou_moto_list)
    list_row.append(value[1][0])
    list_row.extend(jou_saki_list)
    del jou_moto_list, jou_saki_list
    d.dprint(list_row)
    return list_row


def kv3row(key, value):
    list_row = [key[0], key[1]]
    jou_moto_list = jou_tuple2list(key[2])
    list_row.extend(jou_moto_list)
    list_row.append(value)
    del jou_moto_list
    d.dprint(list_row)
    return list_row


# def list2jou_tuple(jou_list):
#     if jou_list[1] == 0:
#         jou = (jou_list[0],)
#     elif jou_list[2] == 0:
#         jou = (jou_list[0], jou_list[1])
#     else:
#         jou = (jou_list[0], jou_list[1], jou_list[2])
#     if jou_list[4] == 0:
#         gou = None
#     elif jou_list[5] == 0:
#         gou = (jou_list[4],)
#     elif jou_list[6] == 0:
#         gou = (jou_list[4], jou_list[5])
#     else:
#         gou = (jou_list[4], jou_list[5], jou_list[6])
#     return (jou, jou_list[3], gou)

# ((69, 4), 1, None)) :
def list2jou_tuple(jou_list):
    if jou_list[1] == '0':
        jou = (int(jou_list[0]),)
    elif jou_list[2] == '0':
        jou = (int(jou_list[0]), int(jou_list[1]))
    else:
        jou = (int(jou_list[0]), int(jou_list[1]),
               int(jou_list[2]))
    if jou_list[4] == '0':
        gou = None
    elif jou_list[5] == '0':
        gou = (int(jou_list[4]),)
    elif jou_list[6] == '0':
        gou = (int(jou_list[4]), int(jou_list[5]))
    else:
        gou = (int(jou_list[4]), int(jou_list[5]), int(jou_list[6]))
    return (jou, int(jou_list[3]), gou)


def jou_tuple2list(jou_tuple):
    # ((69, 4), 1, None)
    list_row = [jou_tuple[0][0]]
    if len(jou_tuple[0]) == 1:
        list_row.append(0)
        list_row.append(0)
    elif len(jou_tuple[0]) == 2:
        list_row.append(jou_tuple[0][1])
        list_row.append(0)
    else:
        list_row.append(jou_tuple[0][1])
        list_row.append(jou_tuple[0][2])
    list_row.append(jou_tuple[1])
    if jou_tuple[2] == None:
        list_row.append(0)
        list_row.append(0)
        list_row.append(0)
    elif len(jou_tuple[2]) == 1:
        list_row.append(jou_tuple[2][0])
        list_row.append(0)
        list_row.append(0)
    elif len(jou_tuple[2]) == 2:
        list_row.append(jou_tuple[2][0])
        list_row.append(jou_tuple[2][1])
        list_row.append(0)
    else:
        list_row.append(jou_tuple[2][0])
        list_row.append(jou_tuple[2][1])
        list_row.append(jou_tuple[2][2])
    return list_row


def load_settei_file_if():
    if os.path.isfile(SETTEI_FILE_NAME):
        load_settei_file()


def load_settei_file():
    input_list = []
    file_name = SETTEI_FILE_NAME
    try:
        with open(file_name, "r",
                encoding="ms932", newline='') \
                as csvfile:
            spamreader = csv.reader(csvfile,
                    delimiter=',')
            for row in spamreader:
                input_list.append(row)
    except OSError as e:
        e.eprint(
            'ファイル読込エラー', e)
        return

    for koumoku in input_list:
        if koumoku[0] == 'フォント名':
            global font_name
            font_name = koumoku[1]
        elif koumoku[0] == 'フォントサイズ':
            global font_size
            font_size = koumoku[1]
        elif koumoku[0] == 'ウィンドウ横':
            global window_yoko
            window_yoko = koumoku[1]
        elif koumoku[0] == 'ウィンドウ縦':
            global window_tate
            window_tate = koumoku[1]
        elif koumoku[0] == 'フレーム横':
            global frame_yoko
            frame_yoko = koumoku[1]
        elif koumoku[0] == 'フレーム縦':
            global frame_tate
            frame_tate = koumoku[1]


if __name__ == '__main__':
    load_settei_file_if()
    jou_init()
    create_window()


