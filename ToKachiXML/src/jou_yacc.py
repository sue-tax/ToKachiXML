# -*- encoding: utf-8 -*-
'''
法律の条文を解析するための構文解析
joucutter joubun_yaccより移植
@author: sue-t
'''

import ply.yacc as yacc

from jou_lex import tokens

import c
import d
# import e

from jou_jou import Jou_jou
from jou_kou import Jou_kou
from jou_gou import Jou_gou
from jou_koumoku import Jou_koumoku


def p_hourei_hen(p):
    '''hourei : hen
            | hourei hen'''
#     d.dprint_method_start()
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hourei_shou(p):
    '''hourei : shou
            | hourei shou
    '''
    # 編がなく、章がくるパターン（ないかもしれないが）
#     d.dprint_method_start()
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hourei_setsu(p):
    '''hourei : setsu
            | hourei setsu
    '''
    # 編、章がなく、節がくるパターン（ないかもしれないが）
#     d.dprint_method_start()
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hourei_kan(p):
    '''hourei : kan
            | hourei kan
    '''
    # 編、章、節がなく、款がくるパターン（ないかもしれないが）
#     d.dprint_method_start()
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hourei_moku(p):
    '''hourei : moku
            | hourei moku
    '''
    # 編、章、節、款がなく、目がくるパターン（ないかもしれないが）
#     d.dprint_method_start()
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hourei_jou(p):
    '''hourei : jou
            | hourei jou
    '''
    if len(p) == 2:
        p[0] = [ p[1] ]
    else:
        p[1].append(p[2])
        p[0] = p[1]
#     # 編、章、節、款、目がなく、条がくるパターン


def p_hen_shou(p):
    '''hen : DAI_X_HEN_GYOUTOU ZENKAKU_KUHAKU bun_maru_nashi shou
            | hen shou'''
#     d.dprint_method_start()
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hen_setsu(p):
    '''hen : DAI_X_HEN_GYOUTOU ZENKAKU_KUHAKU bun_maru_nashi setsu
            | hen setsu'''
    # 編の後に、章がなく、節がくるパターン（ないかもしれないが）
#     d.dprint_method_start()
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hen_kan(p):
    '''hen : DAI_X_HEN_GYOUTOU ZENKAKU_KUHAKU bun_maru_nashi kan
            | hen kan'''
    # 編の後に、章・節がなく、款がくるパターン（ないかもしれないが）
#     d.dprint_method_start()
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hen_moku(p):
    '''hen : DAI_X_HEN_GYOUTOU ZENKAKU_KUHAKU bun_maru_nashi moku
            | hen moku'''
    # 編の後に、章・節・款がなく、目がくるパターン（ないかもしれないが）
#     d.dprint_method_start()
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_hen_jou(p):
    '''hen : DAI_X_HEN_GYOUTOU ZENKAKU_KUHAKU bun_maru_nashi jou
            | hen jou'''
    # 編の後に、章・節・款・目がなく、条がくるパターン
#     d.dprint_method_start()
    if len(p) == 5:
        p[0] = [p[4]]
    else:
        p[1].append(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()


def p_shou_and_shou_no_1(p):
    '''shou_and_shou_no : DAI_X_SHOU_GYOUTOU'''
    p[0] = None #p[1][1:-1]

def p_shou_and_shou_no_2(p):
    '''shou_and_shou_no : DAI_X_SHOU_NO_GYOUTOU'''
    p[0] = None #tuple(shou_no_list)

def p_shou_setsu(p):
    '''shou : shou_and_shou_no ZENKAKU_KUHAKU bun_maru_nashi setsu
            | shou setsu'''
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]

def p_shou_kan(p):
    '''shou : shou_and_shou_no ZENKAKU_KUHAKU bun_maru_nashi kan
            | shou kan'''
    # 章の後に、節がなく、款がくるパターン（ないかもしれないが）
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]

def p_shou_moku(p):
    '''shou : shou_and_shou_no ZENKAKU_KUHAKU bun_maru_nashi moku
            | shou moku'''
    # 章の後に、節・款がなく、目がくるパターン（ないかもしれないが）
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]

def p_shou_jou(p):
    '''shou : shou_and_shou_no ZENKAKU_KUHAKU bun_maru_nashi jou
            | shou jou'''
#     d.dprint_method_start()
    # 章の後に、節・款・目がなく、条がくるパターン
    if len(p) == 5:
        p[0] = [p[4]]
    else:
        p[1].append(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()


def p_setsu_and_setsu_no_1(p):
    '''setsu_and_setsu_no : DAI_X_SETSU_GYOUTOU'''
    p[0] = None #p[1][1:-1]

def p_setsu_and_setsu_no_2(p):
    '''setsu_and_setsu_no : DAI_X_SETSU_NO_GYOUTOU'''
    p[0] = None #tuple(setsu_no_list)

def p_setsu_kan(p):
    '''setsu : setsu_and_setsu_no ZENKAKU_KUHAKU bun_maru_nashi kan
            | setsu kan'''
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]

def p_setsu_moku(p):
    '''setsu : setsu_and_setsu_no ZENKAKU_KUHAKU bun_maru_nashi moku
            | setsu moku'''
    # 節の後に、款がなく、目がくるパターン（ないかもしれないが）
    if len(p) == 5:
        p[0] = p[4]
    else:
        p[1].extend(p[2])
        p[0] = p[1]

def p_setsu_jou(p):
    '''setsu : setsu_and_setsu_no ZENKAKU_KUHAKU bun_maru_nashi jou
            | setsu jou'''
    # 節の後に、款・目がなく、条がくるパターン（ないかもしれないが）
    if len(p) == 5:
        p[0] = [p[4]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_kan_and_kan_no_1(p):
    '''kan_and_kan_no : DAI_X_KAN_GYOUTOU'''
    p[0] = None #p[1][1:-1]

def p_kan_and_kan_no(p):
    '''kan_and_kan_no : DAI_X_KAN_NO_GYOUTOU'''
    p[0] = None #tuple(kan_no_list)

def p_kan_moku(p):
    '''kan : kan_and_kan_no ZENKAKU_KUHAKU bun_maru_nashi moku
            | kan moku'''
    if len(p) == 5:
        p[0] = p[4] # (p[1], p[3][0], [p[4]])
    else:
        p[1].extend(p[2])
        p[0] = p[1]

def p_kan_jou(p):
    '''kan : kan_and_kan_no ZENKAKU_KUHAKU bun_maru_nashi jou
            | kan jou'''
    # 款の後に、目がなく、条がくるパターン
    if len(p) == 5:
        p[0] = [p[4]] # (p[1], p[3][0], [(None, None, [ p[4] ])])
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_moku_and_moku_no_1(p):
    '''moku_and_moku_no : DAI_X_MOKU_GYOUTOU'''
    p[0] = None # p[1][1:-1]

def p_moku_and_moku_no(p):
    '''moku_and_moku_no : DAI_X_MOKU_NO_GYOUTOU'''
    p[0] = None # tuple(moku_no_list)


def p_moku(p):
    '''moku : moku_and_moku_no ZENKAKU_KUHAKU bun_maru_nashi jou
            | moku jou'''
    if len(p) == 5:
        p[0] = [p[4]]
    else:
        p[1].append(p[2])
        p[0] = p[1]


# 税務六法
# def p_jou(p):
#     '''jou : HIDARI_KAKKO_GYOUTOU bun_maru_nashi MIGI_KAKKO jou
#             | jou_midashi_nashi'''

def p_jou(p):
    '''jou : HIDARI_KAKKO_GYOUTOU bun_maru_nashi MIGI_KAKKO jou_midashi_nashi
            | jou_midashi_nashi'''
#     d.dprint_method_start()
    if len(p) == 5:
        # Jou_jou
        p[4].set_midashi(p[2][0])
        p[0] = p[4]
    else:
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_jou_midashi_nashi(p):
    '''jou_midashi_nashi : jou_1_kou
            | jou_midashi_nashi kou'''
#     d.dprint_method_start()
    if len(p) == 2:
        p[0] = Jou_jou(p[1][0], p[1][1])
    else:
        p[2].set_jou_bangou_tuple(p[1].get_bangou_tuple())
        p[1].tsuika_kou(p[2])
        p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_jou_1_kou1(p):
    '''
    jou_1_kou : DAI_X_JOU_GYOUTOU ZENKAKU_KUHAKU honbun
    '''
#     d.dprint_method_start()
    jou_bangou_tuple = (p[1][1:-1],)
    kou = Jou_kou(jou_bangou_tuple, 1, p[3][0], [])
    p[0] = (jou_bangou_tuple, kou)
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_jou_1_kou1_2(p):
    '''
    jou_1_kou : DAI_X_JOU_GYOUTOU ZENKAKU_KUHAKU SAKUJO
    '''
#     d.dprint_method_start()
    jou_bangou_tuple = (p[1][1:-1],)
    kou = Jou_kou(jou_bangou_tuple, 1, p[3], [])
    p[0] = (jou_bangou_tuple, kou)
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_jou_1_kou1_3(p):
    '''
    jou_1_kou : DAI_X_JOU_NO_GYOUTOU ZENKAKU_KUHAKU SAKUJO
    '''
#     d.dprint_method_start()
    jou_no_list = p[1].split(sep="の")
    jou_no_list[0] = jou_no_list[0][1:-1]
    kou = Jou_kou(tuple(jou_no_list), 1, p[3], [])
    p[0] = (tuple(jou_no_list), kou)
#     d.dprint_method_end()

 # TODO Ｘ条及びＹ条　削除
 # TODO Ｘ条からＹ条まで　削除

def p_jou_1_kou2(p):
    '''
    jou_1_kou : DAI_X_JOU_NO_GYOUTOU ZENKAKU_KUHAKU honbun
    '''
#     d.dprint_method_start()
    jou_no_list = p[1].split(sep="の")
    jou_no_list[0] = jou_no_list[0][1:-1]
    kou = Jou_kou(tuple(jou_no_list), 1, p[3][0], [])
    p[0] = (tuple(jou_no_list), kou)
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_jou_1_kou3(p):
    '''
    jou_1_kou : jou_1_kou gou
    '''
#     d.dprint_method_start()
    p[2].set_jou_bangou_tuple(p[1][1].get_jou_bangou_tuple())
    p[2].set_kou_bangou(p[1][1].get_kou_bangou())
    p[1][1].tsuika_gou(p[2])
    p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_kou1(p):
    '''
    kou : BANGOU_KOU ZENKAKU_KUHAKU honbun
    '''
#     d.dprint_method_start()
    kou = Jou_kou(None, int(p[1]), p[3][0], [])
    p[0] = kou
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_kou2(p):
    '''
    kou : kou gou
    '''
#     d.dprint_method_start()
    p[2].set_jou_bangou_tuple(p[1].get_jou_bangou_tuple())
    p[2].set_kou_bangou(p[1].get_kou_bangou())
    p[1].tsuika_gou(p[2])
    p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_gou0(p):
    '''
    gou : BANGOU_GOU ZENKAKU_KUHAKU honbun
    '''
#     d.dprint_method_start()
    gou = Jou_gou(None, None, p[1], p[3][0], [])
    p[0] = gou
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_gou1(p):
    '''
    gou : BANGOU_GOU ZENKAKU_KUHAKU bun_maru_nashi
        | BANGOU_GOU ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU bun
        | BANGOU_GOU ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU bun_maru_nashi
        | BANGOU_GOU ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU honbun
        | BANGOU_GOU ZENKAKU_KUHAKU bun ZENKAKU_KUHAKU honbun
        | BANGOU_GOU ZENKAKU_KUHAKU bun ZENKAKU_KUHAKU bun
        | BANGOU_GOU ZENKAKU_KUHAKU bun ZENKAKU_KUHAKU bun_maru_nashi
    '''
    d.dprint_method_start()
    if len(p) == 4:
        gou = Jou_gou(None, None, p[1], p[3][0], [])
        p[0] = gou
    else:
        gou = Jou_gou(None, None, p[1],
                p[3][0] + "　" + p[5][0], [])
        p[0] = gou
    d.dprint(p[0])
    d.dprint_method_end()

# def p_gou1_2(p):
#     '''
#     gou : BANGOU_GOU ZENKAKU_KUHAKU bun bun_maru_nashi
#     '''
#     d.dprint_method_start()
#     gou = Jou_gou(None, None, p[1],
#             p[3][0] + p[4][0], p[3][0] + p[4][0],
#                 (p[3][1], p[4][1]), [])
#     p[0] = gou
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_gou2(p):
    '''
    gou : gou koumoku_iroha
    '''
    d.dprint_method_start()
    p[2].set_gou_bangou_tuple(p[1].get_gou_bangou_tuple())
    p[1].tsuika_koumoku(p[2])
    p[0] = p[1]
    d.dprint(p[0])
    d.dprint_method_end()

def p_iroha0(p):
    '''
    koumoku_iroha : KOUMOKU_IROHA ZENKAKU_KUHAKU honbun
    '''
    d.dprint_method_start()
#     koumoku = Jou_koumoku(None, None, None,
#             p[1], p[3][0], [])
    koumoku = Jou_koumoku(None, None, None,
            (p[1],), p[3][0], [])
    p[0] = koumoku
#     d.dprint(p[0])
    d.dprint_method_end()

def p_koumoku_iroha1(p):
    '''
    koumoku_iroha : KOUMOKU_IROHA ZENKAKU_KUHAKU bun_maru_nashi
            | KOUMOKU_IROHA ZENKAKU_KUHAKU bun_fukusu
            | KOUMOKU_IROHA ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU bun_maru_nashi
            | KOUMOKU_IROHA ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU bun_fukusu
            | KOUMOKU_IROHA ZENKAKU_KUHAKU bun ZENKAKU_KUHAKU bun_maru_nashi
            | KOUMOKU_IROHA ZENKAKU_KUHAKU bun ZENKAKU_KUHAKU bun
    '''
    d.dprint_method_start()
    if len(p) == 4:
        naiyou = p[3][0]
    else:
        naiyou = p[3][0] + "　" + p[5][0]
#     koumoku = Jou_koumoku(None, None, None,
#             (p[1]),
#             naiyou, [])
    koumoku = Jou_koumoku(None, None, None,
            (p[1],),
            naiyou, [])
    p[0] = koumoku
#     d.dprint(p[0])
    d.dprint_method_end()

def p_koumoku_iroha2(p):
    '''
    koumoku_iroha : koumoku_iroha koumoku_kakko_suji
    '''
    d.dprint_method_start()
    p[2].shusei_koumoku_tuple(p[1])
#     p[2].shusei_koumoku_tuple((p[1],))
    p[1].tsuika_koumoku(p[2])
    p[0] = p[1]
#     d.dprint(p[0])
    d.dprint_method_end()

def p_koumoku_kakko_suji1(p):
    '''
    koumoku_kakko_suji : KOUMOKU_KAKKO_SUJI_SENTOU ZENKAKU_KUHAKU bun_maru_nashi
            | KOUMOKU_KAKKO_SUJI_SENTOU ZENKAKU_KUHAKU bun
            | KOUMOKU_KAKKO_SUJI_SENTOU ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU bun_maru_nashi
            | KOUMOKU_KAKKO_SUJI_SENTOU ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU bun
    '''
    d.dprint_method_start()
    if len(p) == 4:
        naiyou = p[3][0]
    else:
        naiyou = p[3][0] + "　" + p[5][0]
    koumoku = Jou_koumoku(None, None, None,
            (p[1],),
            naiyou, [])
    p[0] = koumoku
#     d.dprint(p[0])
    d.dprint_method_end()

    d.dprint_method_start()
#     koumoku = Jou_koumoku(None, None, None,
#             (p[1][:-1],), p[2][0], p[2][0], (p[2][1],), [])
#     p[0] = koumoku
    d.dprint_method_end()

def p_koumoku_kakko_suji2(p):
    '''
    koumoku_kakko_suji : koumoku_kakko_suji koumoku_kakko_roma_suji
    '''
    p[2].shusei_koumoku_tuple(p[1])
#     p[2].shusei_koumoku_tuple((p[1],))
    p[1].tsuika_koumoku(p[2])
    p[0] = p[1]

def p_koumoku_kakko_roma_suji1(p):
    '''
    koumoku_kakko_roma_suji : KOUMOKU_KAKKO_ROMA_SUJI_SENTOU ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU bun_maru_nashi
            | KOUMOKU_KAKKO_ROMA_SUJI_SENTOU ZENKAKU_KUHAKU bun_maru_nashi ZENKAKU_KUHAKU bun
    '''
    d.dprint_method_start()
    naiyou = p[3][0] + "　" + p[5][0]
#     koumoku = Jou_koumoku(None, None, None,
#             (p[1]),
#             naiyou, [])
    koumoku = Jou_koumoku(None, None, None,
            (p[1],),
            naiyou, [])
    p[0] = koumoku

def p_koumoku_kakko_roma_suji2(p):
    '''
    koumoku_kakko_roma_suji : KOUMOKU_KAKKO_ROMA_SUJI_SENTOU ZENKAKU_KUHAKU bun_maru_nashi
            | KOUMOKU_KAKKO_ROMA_SUJI_SENTOU ZENKAKU_KUHAKU bun
    '''
    d.dprint_method_start()
    naiyou = p[3][0]
#     koumoku = Jou_koumoku(None, None, None,
#             (p[1]),
#             naiyou, [])
    koumoku = Jou_koumoku(None, None, None,
            (p[1],),
            naiyou, [])
    p[0] = koumoku


def p_honbun(p):
    '''honbun : bun_fukusu'''
#     d.dprint_method_start()
    p[0] = p[1]
#     d.dprint_method_end()

def p_bun_fukusu(p):
    '''bun_fukusu : bun
            | bun_fukusu bun
            | bun_fukusu bun_maru_nashi
    '''
    # 20210530 追加    bun_fukusu bun_maru_nashi
#     d.dprint_method_start()
    if len(p) == 2:
        p[0] = p[1]
    else:
#         d.dprint(p[1])
#         d.dprint(p[2])
#         p[0] = (p[1][0] + p[2][0], p[1][1]+p[2][1])
        # ver.0.22 2021/10/09
        p[0] = (p[1][0] + p[2][0], (p[1][1], p[2][1]))
#     d.dprint_method_end()

def p_bun(p):
    '''bun : bun_maru_nashi KUTOUTEN_MARU'''
#     d.dprint_method_start()
    p[0] = (p[1][0] + p[2], (p[1][1], p[2]))    # , 'BUN')
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_bun_maru_nashi(p):   # 最後に読点の付かない文
    '''bun_maru_nashi : doredemo
            | bun_maru_nashi KUTOUTEN_TEN doredemo'''
#     d.dprint_method_start()
    if len(p) == 2:
#         print("、なし")
        p[0] = p[1]
    else:
#         print("、あり")
        p[0] = (p[1][0] + p[2] + p[3][0],
                (p[1][1], p[2], p[3][1]))   # , 'BUN_MARU_NASHI')
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_doredemo(p):
    '''doredemo : kandemo
                | doredemo kandemo'''
#     d.dprint_method_start()
    if len(p) == 2:
        p[0] = p[1]
    else:
        if (p[1][2] == 'NANDEMO') and (p[2][2] == 'NANDEMO'):
            p[0] = (p[1][0] + p[2][0], p[1][1] + p[2][1], 'NANDEMO')
        else:
            p[0] = (p[1][0] + p[2][0],
                    (p[1][1], p[2][1]), p[1][2] + p[2][2])
            # ver.0.22 2021/10/09
#             p[0] = (p[1][0] + p[2][0],
#                     p[1][1] + p[2][1], p[1][2] + p[2][2])
#     d.dprint_method_end()

def p_kandemo(p):
    '''kandemo : kandemo_sub
                | kakko
                | kagi_kakko
    '''
#     d.dprint_method_start()
#     d.dprint(p[1])
    p[0] = p[1]
#     d.dprint_method_end()
# def p_kandemo(p):
#     '''kandemo : kandemo_sub
#                 | kakko
#     '''
# #     d.dprint_method_start()
# #     d.dprint(p[1])
#     p[0] = p[1]
# #     d.dprint_method_end()


def p_kandemo_sub1(p):
    '''kandemo_sub : NANDEMO
    '''
#     d.dprint_method_start()
#     d.dprint(p[1])
    p[0] = (p[1], p[1], 'NANDEMO')
#     d.dprint_method_end()

# def p_kandemo_sub2(p):
#     '''kandemo_sub : NUMBER_KANSUJI
#                 | KOUMOKU_KAKKO_SUJI_TOCHU
#                 | SAKUJO
#     '''
#     d.dprint_method_start()
# #     d.dprint(p[1])
#     p[0] = (p[1], p[1], p[1])
#     d.dprint_method_end()
# ver0.22 2021/10/08
def p_kandemo_sub2(p):
    '''kandemo_sub : NUMBER_KANSUJI
                | NUMBER_ZENKAKU
                | KOUMOKU_KAKKO_SUJI_TOCHU
                | SAKUJO
    '''
#     d.dprint_method_start()
#     d.dprint(p[1])
    p[0] = (p[1], p[1], p[1])
#     d.dprint_method_end()

def p_kakko(p):
    '''kakko : HIDARI_KAKKO kakko_nai MIGI_KAKKO'''
    d.dprint_method_start()
#     d.dprint(p[1])
#     d.dprint(p[2])
#     d.dprint(p[3])
    p[0] = (p[1] + p[2][0] + p[3], (p[1], p[2][1], p[3]), 'KAKKO')
#     d.dprint(p[0])
    d.dprint_method_end()

def p_kakko_nai1(p):
    '''kakko_nai : bun_maru_nashi'''
#     d.dprint_method_start()
    p[0] = (p[1][0], (p[1][1],))
#     d.dprint(p[0])
#     d.dprint_method_end()

def p_kakko_nai2(p):
    '''kakko_nai : bun_fukusu'''
#     d.dprint_method_start()
    p[0] = p[1]
#     d.dprint(p[0])
#     d.dprint_method_end()

# # ver0.22 20211008
# def p_kakko_nai3(p):
#     '''kakko_nai : bun'''
#     d.dprint_method_start()
#     p[0] = (p[1][0], (p[1][1],))
# #     d.dprint(p[0])
#     d.dprint_method_end()

def p_kagi_kakko(p):
    '''kagi_kakko : KAGIKAKKONAI'''
    p[0] = (p[1], p[1], 'KAGI_KAKKO')

# def p_kagi_kakko(p):
#     '''kagi_kakko : HIDARI_KAGI_KAKKO kagi_kakko_nai MIGI_KAGI_KAKKO'''
#     d.dprint_method_start()
#     p[0] = (p[1] + p[2] + p[3], (p[1], p[2], p[3]), 'KAGI_KAKKO')
# #     d.dprint(p[0])
# #     d.dprint(p[0])
#     d.dprint_method_end()
#
# def p_kagi_kakko_nai(p):
#     '''kagi_kakko_nai : kagi_kakko_nai_kandemo
#                 | kagi_kakko_nai kagi_kakko_nai_kandemo
#     '''
#     d.dprint_method_start()
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         p[0] = p[1] + p[2]
# #     d.dprint(p[0])
#     d.dprint_method_end()
#
# def p_kagi_kakko_nai_kandemo1(p):
#     '''kagi_kakko_nai_kandemo : kandemo_sub
#     '''
#     d.dprint_method_start()
#     p[0] = p[1][0]
# #     d.dprint(p[0])
#     d.dprint_method_end()
#
# def p_kagi_kakko_nai_kandemo2(p):
#     '''kagi_kakko_nai_kandemo : HIDARI_KAKKO
#             | MIGI_KAKKO
#             | KUTOUTEN_TEN
#             | KUTOUTEN_MARU
#             | NUMBER_ZENKAKU
#     '''
#     d.dprint_method_start()
#     p[0] = p[1]
# #     d.dprint(p[0])
#     d.dprint_method_end()
#
# def p_kagi_kakko_nai_kandemo3(p):
#     '''kagi_kakko_nai_kandemo : kagi_kakko
#     '''
#     d.dprint_method_start()
#     p[0] = p[1][0]
# #     d.dprint(p[0])
#     d.dprint_method_end()

def jou_init():
    global parser
    parser = yacc.yacc()

def jou_parse(text):
    global parser
    # 最初が、編とか章とかを確認する
#     global parser
#     parser = yacc.yacc(start='shou')

    result = parser.parse(text)
    return result


if __name__ == '__main__':
    pass