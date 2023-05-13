'''
Created on 2022/10/11

@author: sue-t
'''

from tkinter import Toplevel, Button, Text, Label, Entry, \
        Scrollbar, W, N, NONE, HORIZONTAL, VERTICAL
from tkinter.ttk import Combobox

import c
import d
import e
import config


class DialogInput(object):
    '''
    条文テキストファイルを作成するために、
    税法名、区分、条文を入力するダイアログ
    '''

    def __init__(self):
        self.dialog = Toplevel()
        self.dialog.title("条文ファイルのデータ入力")
        self.dialog.geometry("800x500")
        self.dialog.grab_set()
        self.dialog.grid()
        self.dialog.protocol("WM_DELETE_WINDOW",
                self.cancel)
        row = self.set_format(0)
        self.set_button(row)


    def set_format(self, row):
        Label(self.dialog, text="税法名") \
                .grid(row=row, column=0)

        self.entry_zeihou_mei = Entry(
                self.dialog, width=50)
        self.entry_zeihou_mei.configure(
                font=("MS ゴシック", 12))
        self.entry_zeihou_mei.grid(row=row, column=1,
                sticky=W)

        Label(self.dialog, text="区分") \
                .grid(row=row+1, column=0, sticky=W)
        self.combo_kubun = Combobox(self.dialog,
                values=["法", "法施行令", "法施行規則"],
                width=10)
        self.combo_kubun.grid(row=row+1, column=1) #, sticky=W)
        self.combo_kubun.set("法")

        Label(self.dialog, text="条文") \
                .grid(row=row+2, column=0, sticky=N)
        self.entry_joubun = Text(self.dialog,
#                 width=frame_yoko, height=frame_tate,
                wrap=NONE)
        self.entry_joubun.configure(
                font=("MS ゴシック", 12))
        scrollbar_form_x = Scrollbar(self.dialog,
                orient=HORIZONTAL,
                command=self.entry_joubun.xview)
        self.entry_joubun.configure(
                xscrollcommand=scrollbar_form_x.set)
        scrollbar_form_y = Scrollbar(self.dialog,
                orient=VERTICAL,
                command=self.entry_joubun.yview)
        self.entry_joubun.configure(
                yscrollcommand=scrollbar_form_y.set)
        self.entry_joubun.grid(row=row+2, column=1)
        scrollbar_form_x.grid(row=row+3, column=1,
                sticky='ew')
        scrollbar_form_y.grid(row=row+2, column=2,
                sticky='ns')
        return row + 4


    def set_button(self, row):
        btCancel = Button(
                self.dialog,
                text='Cancel',
                command=lambda : self.cancel())
        btCancel.grid(row=row, column=4, pady=6)
        btOK = Button(
                self.dialog,
                text='OK',
                command=lambda : self.ok())
        btOK.grid(row=row, column=3, pady=5)


    def ok(self):
#         self.dlg_mei = self.entry_zeihou_mei.get()
#         self.dlg_kubun = self.combo_kubun.get()
#         self.dlg_joubun = self.entry_joubun.get(
#                 '1.0', 'end -1c')
        config.dlg_mei = self.entry_zeihou_mei.get()
        config.dlg_kubun = self.combo_kubun.get()
        config.dlg_joubun = self.entry_joubun.get(
                '1.0', 'end -1c')
        import ToKachi
        ToKachi.create_file2(self)
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()

