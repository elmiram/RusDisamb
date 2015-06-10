# -*- coding = utf-8 -*-
from __future__ import division
__author__ = 'elmira'

import pymorphy2
import codecs
import re
from collections import defaultdict



regParts = re.compile(u'lex="(.*?)" gr="(.*?)"></ana>(.*?)</w>', flags=re.U | re.DOTALL)
morph = pymorphy2.MorphAnalyzer()


class Struct:
    def __init__(self, **values):
        vars(self).update(values)


def op_file(fname):

    words = 0
    d = {}
    f = codecs.open(fname, 'r', 'utf-8')
    out = codecs.open('full_final.txt', 'w', 'utf-8')
    for line in f:
        if line.startswith(u'<w>'):
            words += 1
            m = regParts.search(line)
            lex, gr, wf = m.group(1), m.group(2).replace(u'=', u','), m.group(3).replace(u'`', '')
            if wf in d:
                if (lex, gr) in d[wf][0]:
                    d[wf][0][(lex, gr)] += 1
                else:
                    d[wf][0][(lex, gr)] = 1
            else:
                p = morph.parse(wf)[0]
                d[wf] = [{(lex, gr): 1}, p.normal_form, unicode(p.tag)]

            # print wf + '\t' + lex + '\t' + gr + '\t' + d[wf][1] + '\t', d[wf][2][0]
            # print wf + '\t' + lex + '\t' + gr + '\t' + d[wf][1] + '\t', unicode(p.tag)
            s = wf + '\t' + lex + '\t' + gr + '\t' + d[wf][1] + '\t' + d[wf][2] + '\r\n'
            out.write(s)

    f.close()

    print 'words', words
    # print 'normal_form_G', normal_form_G/words
    # print 'normal_form_B', normal_form_B/words
    # print 'ana_G', ana_G/words
    # print 'ana_B', ana_B/words
    return d


def convert_py(tag):
    pos_dic = {u'NOUN': u'S',
                u'ADJF': u'A,plen',
                u'ADJS': u'A,brev',
                u'COMP': u'comp',
                u'VERB': u'V',
                u'INFN': u'V,inf',
                u'PRTF': u'V,partcp,plen',
                u'PRTS': u'V,partcp,brev',
                u'GRND': u'V,ger',
                u'NUMR': u'NUM',
                u'ADVB': u'ADV',
                u'NPRO': u'S-PRO',
                u'PRED': u'PRAEDIC',
                u'PREP': u'PR',
                u'CONJ': u'CONJ',
                u'PRCL': u'PART',
                u'INTJ': u'INTJ',
                u'nomn': u'nom',
                u'gent': u'gen',
                u'datv': u'dat',
                u'accs': u'acc',
                u'ablt': u'ins',
                u'loct': u'loc',
                u'voct': u'voc',
                u'gen2': u'gen2',
                u'acc2': u'acc2',
                u'loc2': u'loc2',
                u'sing': u'sg',
                u'plur': u'pl',
                u'LATN': u'NONLEX',
                u'PNCT': u'PNCT',
                u'NUMB': u'NUM',
                u'intg': u'ciph',
                u'real': u'ciph',
                u'ROMN': u'ciph',
                u'UNKN': u'UNKN',
                u'anim': u'anim',
                u'inan': u'inan',
                u'masc': u'm',
                u'femn': u'f',
                u'neut': u'n',
                u'Ms-f': u'm-f',
                u'Sgtm': u'sg',
                u'Pltm': u'pl',
                u'Fixd': u'0',
                u'Abbr': u'abbr',
                u'Name': u'persn',
                u'Surn': u'famn',
                u'Patr': u'patrn',
                u'Geox': u'topon',
                u'Supr': u'supr',
                u'Apro': u'A-PRO',
                u'Anum': u'ANUM',
                u'Poss': u'poss',
                u'V-ey': u'',
                u'V-oy': u'',
                u'Cmp2': u'comp2',
                u'V-ej': u'',
                u'perf': u'pf',
                u'impf': u'ipf',
                u'tran': u'',
                u'intr': u'',
                u'Refl': u'',
                u'1per': u'1p',
                u'2per': u'2p',
                u'3per': u'3p',
                u'pres': u'praes',
                u'past': u'praet',
                u'futr': u'fut',
                u'indc': u'indic',
                u'impr': u'imper',
                u'incl': u'incl',
                u'excl': u'excl',
                u'actv': u'act',
                u'pssv': u'pass',
                u'Prnt': u'PARENTH',
                u'V-be': u'',
                u'V-en': u'',
                u'V-ie': u'',
                u'V-bi': u'',
                u'Fimp': u'ger,ipf',
                u'Coun': u'adnum',
                u'V-sh': u'',
                u'Af-p': u'',
                u'Vpre': u'',
                u'Qual': u''
               }
    tag = tag.replace(u' ', ',').split(',')
    new_tag = []
    for i in tag:
        if i in pos_dic:
            if ',' in pos_dic[i]:
                new_tag += pos_dic[i].split(',')
            else: new_tag.append(pos_dic[i])
        else:
            new_tag.append(i)
    new_tag = [i for i in new_tag if i != '']
    return ','.join(new_tag), set(new_tag)

def convert_my(tag):
    new_tag = set(tag.split(','))
    return new_tag


if __name__ == "__main__":
    d = op_file(u'gold_corpus2.xhtml')

    # n = codecs.open('other.txt', 'r', 'utf-8')
    # normal_form_G = 0
    # normal_form_B = 0
    # ana_G = 0
    # ana_B = 0
    # words = 8126
    # for line in n:
    #     wf, lex, gr, norm, pym = [i.strip() for i in line.split('\t')]
    #     l, s = convert_py(pym)
    #     print wf,
    #     if norm == lex:
    #         normal_form_G += 1
    #     else:
    #         normal_form_B += 1
    #         print lex, norm,
    #     if convert_my(gr) in s:
    #         ana_G += 1
    #     else:
    #         ana_B += 1
    #     print gr, l
    #
    # n.close()
    #
    # print 'normal_form_G', normal_form_G/words
    # print 'normal_form_B', normal_form_B/words
    # print 'ana_G', ana_G/words
    # print 'ana_B', ana_B/words
