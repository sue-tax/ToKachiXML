'''
Created on 2022/10/22

@author: sue-t
'''

from tkinter import Toplevel, Button, Text, Label, Entry, \
        W, N, IntVar, Spinbox
from tkinter.ttk import Combobox

import c
import d
import e
import config
from TransNum import TransNum


class DialogLink1(object):
    '''
    前条第二項などのハイパーリンクを
    自分で設定するための入力するダイアログ
    '''

    def __init__(self):
        self.dialog = Toplevel()
        self.dialog.title("ハイパーリンクの入力")
        self.dialog.geometry("750x360")
        self.dialog.grab_set()
        self.dialog.grid()
        self.dialog.protocol("WM_DELETE_WINDOW",
                self.cancel)
        Label(self.dialog, text="") \
                .grid(row=0, column=0)
        row = self.set_format(1)
        Label(self.dialog, text="") \
                .grid(row=row, column=0)
        self.set_button(row+1)


    def set_format(self, row):
        Label(self.dialog, text="参照元") \
                .grid(row=row, column=0)
        Label(self.dialog, text="（前条第二項etc）") \
                .grid(row=row+1, column=0)
        Label(self.dialog, text="税法名") \
                .grid(row=row, column=1)
        self.entry_zeihou_mei_moto = Entry(
                self.dialog, width=50)
        self.entry_zeihou_mei_moto.configure(
                font=("MS ゴシック", 12))
        self.entry_zeihou_mei_moto.grid(row=row, column=2,
                columnspan=6, sticky=W)

        Label(self.dialog, text="区分") \
                .grid(row=row+1, column=1, sticky=W)
        self.combo_kubun_moto = Combobox(self.dialog,
                values=["法", "法施行令", "法施行規則"],
                width=10)
        self.combo_kubun_moto.grid(row=row+1, column=2,
                columnspan=3)
        self.combo_kubun_moto.set("法")

        Label(self.dialog, text="第") \
                .grid(row=row+2, column=2, sticky=N)
        self.var_jou1_moto = IntVar(self.dialog)
        self.var_jou1_moto.set(1)
        self.spin_jou1_moto = Spinbox(self.dialog,
                textvariable=self.var_jou1_moto,
                from_=1, to=999, increment=1)
        self.spin_jou1_moto.grid(row=row+2, column=3,
                sticky=W)
        Label(self.dialog, text="条の") \
                .grid(row=row+2, column=4, sticky=N)
        self.var_jou2_moto = IntVar(self.dialog)
        self.var_jou2_moto.set(0)
        self.spin_jou2_moto = Spinbox(self.dialog,
                textvariable=self.var_jou2_moto,
                from_=0, to=999, increment=1)
        self.spin_jou2_moto.grid(row=row+2, column=5,
                sticky=W)
        Label(self.dialog, text="の") \
                .grid(row=row+2, column=6, sticky=N)
        self.var_jou3_moto = IntVar(self.dialog)
        self.var_jou3_moto.set(0)
        self.spin_jou3_moto = Spinbox(self.dialog,
                textvariable=self.var_jou3_moto,
                from_=0, to=999, increment=1)
        self.spin_jou3_moto.grid(row=row+2, column=7,
                sticky=W)

        Label(self.dialog, text="第") \
                .grid(row=row+3, column=2, sticky=N)
        self.var_kou_moto = IntVar(self.dialog)
        self.var_kou_moto.set(1)
        self.spin_kou_moto = Spinbox(self.dialog,
                textvariable=self.var_kou_moto,
                from_=1, to=999, increment=1)
        self.spin_kou_moto.grid(row=row+3, column=3,
                sticky=W)
        Label(self.dialog, text="項") \
                .grid(row=row+3, column=4, sticky=N)

        Label(self.dialog, text="第") \
                .grid(row=row+4, column=2, sticky=N)
        self.var_gou1_moto = IntVar(self.dialog)
        self.var_gou1_moto.set(0)
        self.spin_gou1_moto = Spinbox(self.dialog,
                textvariable=self.var_gou1_moto,
                from_=0, to=999, increment=1)
        self.spin_gou1_moto.grid(row=row+4, column=3,
                sticky=W)
        Label(self.dialog, text="号の") \
                .grid(row=row+4, column=4, sticky=N)
        self.var_gou2_moto = IntVar(self.dialog)
        self.var_gou2_moto.set(0)
        self.spin_gou2_moto = Spinbox(self.dialog,
                textvariable=self.var_gou2_moto,
                from_=0, to=999, increment=1)
        self.spin_gou2_moto.grid(row=row+4, column=5,
                sticky=W)
        Label(self.dialog, text="の") \
                .grid(row=row+4, column=6, sticky=N)
        self.var_gou3_moto = IntVar(self.dialog)
        self.var_gou3_moto.set(0)
        self.spin_gou3_moto = Spinbox(self.dialog,
                textvariable=self.var_gou3_moto,
                from_=0, to=999, increment=1)
        self.spin_gou3_moto.grid(row=row+4, column=7,
                sticky=W)

        Label(self.dialog, text="参照文言") \
                .grid(row=row+6, column=0, sticky=N)
        self.entry_koumoku = Entry(
                self.dialog, width=50)
        self.entry_koumoku.grid(row=row+6, column=2,
                columnspan=6, sticky=W)

        Label(self.dialog, text="") \
                .grid(row=row+7, column=2, sticky=N)
        row += 8

        Label(self.dialog, text="参照先") \
                .grid(row=row, column=0)

        Label(self.dialog, text="税法名") \
                .grid(row=row, column=1)
        self.entry_zeihou_mei_saki = Entry(
                self.dialog, width=50)
        self.entry_zeihou_mei_saki.configure(
                font=("MS ゴシック", 12))
        self.entry_zeihou_mei_saki.grid(row=row, column=2,
                columnspan=6, sticky=W)

        Label(self.dialog, text="区分") \
                .grid(row=row+1, column=1, sticky=W)
        self.combo_kubun_saki = Combobox(self.dialog,
                values=["法", "法施行令", "法施行規則"],
                width=10)
        self.combo_kubun_saki.grid(row=row+1, column=2,
                columnspan=3)
        self.combo_kubun_saki.set("法")

        Label(self.dialog, text="第") \
                .grid(row=row+2, column=2, sticky=N)
        self.var_jou1_saki = IntVar(self.dialog)
        self.var_jou1_saki.set(1)
        self.spin_jou1_saki = Spinbox(self.dialog,
                textvariable=self.var_jou1_saki,
                from_=1, to=999, increment=1)
        self.spin_jou1_saki.grid(row=row+2, column=3,
                sticky=W)
        Label(self.dialog, text="条の") \
                .grid(row=row+2, column=4, sticky=N)
        self.var_jou2_saki = IntVar(self.dialog)
        self.var_jou2_saki.set(0)
        self.spin_jou2_saki = Spinbox(self.dialog,
                textvariable=self.var_jou2_saki,
                from_=0, to=999, increment=1)
        self.spin_jou2_saki.grid(row=row+2, column=5,
                sticky=W)
        Label(self.dialog, text="の") \
                .grid(row=row+2, column=6, sticky=N)
        self.var_jou3_saki = IntVar(self.dialog)
        self.var_jou3_saki.set(0)
        self.spin_jou3_saki = Spinbox(self.dialog,
                textvariable=self.var_jou3_saki,
                from_=0, to=999, increment=1)
        self.spin_jou3_saki.grid(row=row+2, column=7,
                sticky=W)

        Label(self.dialog, text="第") \
                .grid(row=row+3, column=2, sticky=N)
        self.var_kou_saki = IntVar(self.dialog)
        self.var_kou_saki.set(1)
        self.spin_kou_saki = Spinbox(self.dialog,
                textvariable=self.var_kou_saki,
                from_=1, to=999, increment=1)
        self.spin_kou_saki.grid(row=row+3, column=3,
                sticky=W)
        Label(self.dialog, text="項") \
                .grid(row=row+3, column=4, sticky=N)

        Label(self.dialog, text="第") \
                .grid(row=row+4, column=2, sticky=N)
        self.var_gou1_saki = IntVar(self.dialog)
        self.var_gou1_saki.set(0)
        self.spin_gou1_saki = Spinbox(self.dialog,
                textvariable=self.var_gou1_saki,
                from_=0, to=999, increment=1)
        self.spin_gou1_saki.grid(row=row+4, column=3,
                sticky=W)
        Label(self.dialog, text="号の") \
                .grid(row=row+4, column=4, sticky=N)
        self.var_gou2_saki = IntVar(self.dialog)
        self.var_gou2_saki.set(0)
        self.spin_gou2_saki = Spinbox(self.dialog,
                textvariable=self.var_gou2_saki,
                from_=0, to=999, increment=1)
        self.spin_gou2_saki.grid(row=row+4, column=5,
                sticky=W)
        Label(self.dialog, text="の") \
                .grid(row=row+4, column=6, sticky=N)
        self.var_gou3_saki = IntVar(self.dialog)
        self.var_gou3_saki.set(0)
        self.spin_gou3_saki = Spinbox(self.dialog,
                textvariable=self.var_gou3_saki,
                from_=0, to=999, increment=1)
        self.spin_gou3_saki.grid(row=row+4, column=7,
                sticky=W)

        return row + 8


    def set_button(self, row):
        btCancel = Button(
                self.dialog,
                text='Cancel',
                command=lambda : self.cancel())
        btCancel.grid(row=row, column=7, pady=6)
        btOK = Button(
                self.dialog,
                text='OK',
                command=lambda : self.ok())
        btOK.grid(row=row, column=5, pady=5)


    def ok(self):
        zeihou_mei_moto = self.entry_zeihou_mei_moto. \
                get()
#         d.dprint(zeihou_mei_moto)
        kubun_moto = self.combo_kubun_moto.get()
        jou1_moto = self.var_jou1_moto.get()
        jou2_moto = self.var_jou2_moto.get()
        jou3_moto = self.var_jou3_moto.get()
        kou_moto = self.var_kou_moto.get()
        gou1_moto = self.var_gou1_moto.get()
        gou2_moto = self.var_gou2_moto.get()
        gou3_moto = self.var_gou3_moto.get()
        koumoku = self.entry_koumoku.get()

        zeihou_mei_saki = self.entry_zeihou_mei_saki. \
                get()
        kubun_saki = self.combo_kubun_saki.get()
        jou1_saki = self.var_jou1_saki.get()
        jou2_saki = self.var_jou2_saki.get()
        jou3_saki = self.var_jou3_saki.get()
        kou_saki = self.var_kou_saki.get()
        gou1_saki = self.var_gou1_saki.get()
        gou2_saki = self.var_gou2_saki.get()
        gou3_saki = self.var_gou3_saki.get()

        if jou2_moto == 0:
            jou_moto = (jou1_moto,)
        elif jou3_moto == 0:
            jou_moto = (jou1_moto, jou2_moto)
        else:
            jou_moto = (jou1_moto, jou2_moto, jou3_moto)
        if gou1_moto == 0:
            gou_moto = None
        elif gou2_moto == 0:
            gou_moto = (gou1_moto,)
        elif gou3_moto == 0:
            gou_moto = (gou1_moto, gou2_moto)
        else:
            gou_moto = (gou1_moto, gou2_moto, gou3_moto)
        moto_tuple = (jou_moto, kou_moto, gou_moto)
#         moto_link = TransNum.create_link_name(
#                 zeihou_mei_moto, kubun_moto, moto_tuple)

        if jou2_saki == 0:
            jou_saki = (jou1_saki,)
        elif jou3_saki == 0:
            jou_saki = (jou1_saki, jou2_saki)
        else:
            jou_saki = (jou1_saki, jou2_saki, jou3_saki)
        if gou1_saki == 0:
            gou_saki = None
        elif gou2_saki == 0:
            gou_saki = (gou1_saki,)
        elif gou3_saki == 0:
            gou_saki = (gou1_saki, gou2_saki)
        else:
            gou_saki = (gou1_saki, gou2_saki, gou3_saki)
        saki_tuple = (jou_saki, kou_saki, gou_saki)
        saki_link = TransNum.create_link_name(
                zeihou_mei_saki, kubun_saki, saki_tuple)
        d.dprint(saki_link)

# ('法', '法施行令', 措置', ((69, 4), 1, None)) :
# [ (3, ('措置法施行＿令第４０条の２第１項', ((40, 2), 1, None))),
#   (5, ('措置法施行＿令第４０条の２第４項', ((40, 2), 4, None)) ]
# ('法', '法施行規則', '措置', ((2,), 1, (16,))):
# [(1, ('措置法施行＿令第４０条の２第４項', ((40, 2), 4, None)))]
#         key = (kubun_moto, kubun_saki,
#                zeihou_mei_moto, moto_tuple)
#         item = (koumoku, (saki_link, saki_tuple))
        key = (kubun_moto, zeihou_mei_moto, moto_tuple)
        item = (kubun_saki, zeihou_mei_saki,
                koumoku, (saki_link, saki_tuple))

        if key in config.jiko1_dict:
            value = config.jiko1_dict[key]
            value.append(item)
            config.jiko1_dict[key] = value
        else:
            config.jiko1_dict[key] = [item]

        import ToKachi
        ToKachi.save_tokachi_file()
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()

