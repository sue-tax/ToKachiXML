# -*- encoding: utf-8 -*-
'''
法律の条文を解析するための字句解析
Created on 2021/05/15
joucutter joubun_lexより移植
@author: sue-t
'''

# 「「取締役会」とあるのは「「清算人会」と
# の処理で失敗する

import ply.lex as lex


tokens = (
    'NUMBER_KANSUJI',
    'NUMBER_ZENKAKU',

    'DAI_X_HEN_GYOUTOU',
    'DAI_X_SHOU_GYOUTOU',
    'DAI_X_SHOU_NO_GYOUTOU',
    'DAI_X_SETSU_GYOUTOU',
    'DAI_X_SETSU_NO_GYOUTOU',
    'DAI_X_KAN_GYOUTOU',
    'DAI_X_KAN_NO_GYOUTOU',
    'DAI_X_MOKU_GYOUTOU',
    'DAI_X_MOKU_NO_GYOUTOU',

    'DAI_X_JOU_GYOUTOU',
    'DAI_X_JOU_NO_GYOUTOU',

    'BANGOU_KOU',
    'BANGOU_GOU',
    'KOUMOKU_IROHA',
    'KOUMOKU_KAKKO_SUJI_SENTOU',
    'KOUMOKU_KAKKO_SUJI_TOCHU',
    'KOUMOKU_KAKKO_ROMA_SUJI_SENTOU',

    'ZENKAKU_KUHAKU',

    'KUTOUTEN_TEN',
    'KUTOUTEN_MARU',

    'SAKUJO',

    'HIDARI_KAKKO_GYOUTOU',
    'HIDARI_KAKKO',
    'MIGI_KAKKO',

    'NANDEMO',

    'KAGIKAKKONAI'
    )


states = (
    ('kagikakkonai', 'exclusive'),)


t_NUMBER_KANSUJI = r'[一二三四五六七八九十百千]+'
t_NUMBER_ZENKAKU = r'[１２３４５６７８９０]+'

t_DAI_X_HEN_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+編'
t_DAI_X_SHOU_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+章'
t_DAI_X_SHOU_NO_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+章の' \
                            '[一二三四五六七八九十百千の]+'
t_DAI_X_SETSU_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+節'
t_DAI_X_SETSU_NO_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+節' \
                            '[一二三四五六七八九十百千の]+'
t_DAI_X_KAN_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+款'
t_DAI_X_KAN_NO_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+款' \
                            '[一二三四五六七八九十百千の]+'
t_DAI_X_MOKU_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+目'
t_DAI_X_MOKU_NO_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+目' \
                            '[一二三四五六七八九十百千の]+'

t_DAI_X_JOU_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+条'
t_DAI_X_JOU_NO_GYOUTOU = r'(?m)^第[一二三四五六七八九十百千]+条の' \
                            '[一二三四五六七八九十百千の]+'

t_BANGOU_KOU = r'(?m)^[１２３４５６７８９０]+'
t_BANGOU_GOU = r'(?m)^[一二三四五六七八九十百千の]+'
t_KOUMOKU_IROHA = r'(?m)^[イロハニホヘトチリヌルヲワカヨタレソ]'
t_KOUMOKU_KAKKO_SUJI_SENTOU = r'(?m)^（[１２３４５６７８９０]+）'
t_KOUMOKU_KAKKO_SUJI_TOCHU = r'（[１２３４５６７８９０]+）'
t_KOUMOKU_KAKKO_ROMA_SUJI_SENTOU = r'(?m)^（[ｉｖ]+）'

t_ZENKAKU_KUHAKU = r'　'

t_KUTOUTEN_TEN = r'、'
t_KUTOUTEN_MARU = r'。'

t_SAKUJO = r'削除'

t_HIDARI_KAKKO_GYOUTOU = r'(?m)^（'
# t_HIDARI_KAKKO = r'[（|(]'
# t_MIGI_KAKKO = r'[）|)]'
t_HIDARI_KAKKO = r'[（(]'
t_MIGI_KAKKO = r'[）)]'

t_NANDEMO = r'.'    # １回以上繰り返し、最短一致


def t_newline(t):
    r'\n+'
#     t.lexer.lineno += len(t.value)
    t.lexer.lineno += 1

def t_error(t):
    print(r"エラー　'{}'" .format(t.value[0]))
    t.lexer.skip(1)


def t_begin_kagikakkonai(t):
    r'「'
    t.lexer.code_start = t.lexer.lexpos - 1
    t.lexer.level = 1
    t.lexer.begin('kagikakkonai')

# def t_kagikakkonai_hidari_kagi_kakko(t):
#     r'「'
#     t.lexer.level += 1

def t_kagikakkonai_migi_kagi_kakko(t):
    r'」'
    t.lexer.level -= 1
    if t.lexer.level == 0:
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
        t.type = "KAGIKAKKONAI"
        t.lexer.begin('INITIAL')
        return t

# def t_kagikakkonai_NANDEMO(t):
#     r'[^「^」]+'
def t_kagikakkonai_NANDEMO(t):
    r'[^」]+'

def t_kagikakkonai_error(t):
    print(r"「」内　エラー　'{}'" .format(t.value[0]))
    t.lexer.skip(1)
     # TODO 構文解析無視

lexer = lex.lex()

if __name__ == '__main__':
    f = open('末永税法.txt', 'r', encoding='utf-8')
    text = f.read()
    f.close()

    lexer.input(text)
    for tok in lexer:
        print(tok)

