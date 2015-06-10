# coding=utf-8
__author__ = 'Admin'

import codecs
from pymorphy_test import *

class Line:
    dic = ['nom', 'gen', 'dat', 'acc', 'gen2', 'loc', 'loc2', 'voc', 'acc2', 'ins','anim', 'inan','1p', '2p', '3p','m', 'f', 'n', 'm-f','sg', 'pl','brev', 'plen','tran', 'intr','pf', 'ipf','act', 'pass','praet', 'praes','indic', 'imper', 'inf','comp', 'supr', 'ger', 'anum', 'abbr', 'anom', 'distort']
    pos = {'S': ['nom', 'gen', 'dat', 'acc', 'gen2', 'loc', 'loc2', 'voc', 'acc2', 'ins','anim', 'inan', 'm', 'f', 'n', 'm-f','sg', 'pl'],
           'A': ['nom', 'gen', 'dat', 'acc', 'gen2', 'loc', 'loc2', 'voc', 'acc2', 'ins','anim', 'inan', 'm', 'f', 'n', 'm-f','sg', 'pl', 'brev', 'plen', 'comp', 'supr'],
           'V': ['1p', '2p', '3p', 'm', 'f', 'n','sg', 'pl', 'tran', 'intr','pf', 'ipf','act', 'pass','praet', 'praes','indic', 'imper', 'inf',  'ger'],
           'NUM': ['abbr', 'a1m', 'distort'],
           'ADV': ['comp', 'supr'],
           'S-PRO': ['1p', '2p', '3p', 'sg', 'pl'],
           'PRAEDIC': ['abbr', 'a1m', 'distort'],
           'CONJ': ['abbr', 'a1m', 'distort'],
           'PR': ['abbr', 'a1m', 'distort'],
           'PART': ['abbr', 'a1m', 'distort'],
           'INTJ': ['abbr', 'a1m', 'distort'],
           'APRO': ['abbr', 'a1m', 'distort'],
           'ANUM': ['abbr', 'a1m', 'distort'],
           'PARENTH': ['abbr', 'a1m', 'distort'],
           '': dic,
           'ADV-PRO': dic,
           'A-PRO': dic,
           'INIT': dic,}


    def __init__(self, wf, lex, gr, norm, pym, l, s):
        self.wordform = wf
        self.gold_caps = 1 if lex[0].isupper() else 0
        self.tagger_caps = 1 if norm[0].isupper() else 0
        self.lemma_gold = lex.lower()
        self.lemma_tagger = norm.lower()
        self.correct_lemma = '1' if self.lemma_tagger.replace(u'ё', u'е') == self.lemma_gold.replace(u'ё', u'е') else '0'
        self.tag_gold = gr
        self.tag_tagger = l
        g = set(self.tag_gold.split(','))
        if 'tran' in g:
            tr = g.remove('tran')
        elif 'intr' in g:
            tr = g.remove('intr')
        else:
            tr = g
        self.correct_tag = '1' if tr == set(self.tag_tagger.split(',')) else '0'
        self.tag_original = pym
        self.pos_gold = ''
        self.pos_tagger = ''
        self.check_other(s)

    def check_other(self, s):
        gold = self.tag_gold.split(',')
        self.check(gold, s)

    def check(self, gold, s):
        for i in self.pos:
            if i in gold: self.pos_gold = i
            if i in s: self.pos_tagger = i
        self.correct_pos = '1' if self.pos_tagger == self.pos_gold else '0'
        for i in self.dic:
            if i in self.pos[self.pos_tagger] or i in self.pos[self.pos_gold]:
                if i in s:
                    if i in ['1p', '2p', '3p', 'pass']:
                        i = '_' + i
                    elif i == 'm-f': i = 'm_f'
                    vars(self)[i] = '1'
                    if i in gold:
                        vars(self)[i+'_match'] = '1'
                    else:
                        vars(self)[i+'_match'] = '0'
                else:
                    if i in ['1p', '2p', '3p', 'pass']:
                        i = '_' + i
                    elif i == 'm-f': i = 'm_f'
                    vars(self)[i] = '0'
                    if i in gold:
                        vars(self)[i+'_match'] = '0'
                    else:
                        vars(self)[i+'_match'] = '1'
            else:
                if i in ['1p', '2p', '3p', 'pass']:
                        i = '_' + i
                elif i == 'm-f': i = 'm_f'
                vars(self)[i] = 'NA'
                vars(self)[i+'_match'] = 'NA'

    def unicode(self):
        return '\t'.join([self.wordform, self.lemma_gold, self.lemma_tagger, self.correct_lemma, self.pos_gold, self.pos_tagger, self.correct_pos, self.tag_gold, self.tag_tagger, self.tag_original, self.correct_tag, self.nom, self.nom_match, self.gen, self.gen_match, self.dat, self.dat_match, self.acc, self.acc_match, self.ins, self.ins_match, self.loc, self.loc_match, self.gen2, self.gen2_match, self.loc2, self.loc2_match, self.voc, self.voc_match, self.sg, self.sg_match, self.pl, self.pl_match, self.f, self.f_match, self.m, self.m_match, self.n, self.n_match, self.m_f, self.m_f_match, self.anim, self.anim_match, self.inan, self.inan_match, self.anom, self.anom_match, self.distort, self.distort_match, self.anum, self.anum_match, self.abbr, self.abbr_match, self.indic, self.indic_match, self.imper, self.imper_match, self.inf, self.inf_match, self.ger, self.ger_match, self.praes, self.praes_match, self.praet, self.praet_match, self._1p, self._1p_match, self._2p, self._2p_match, self._3p, self._3p_match, self.pf, self.pf_match, self.ipf, self.ipf_match, self.inf, self.inf_match, self.act, self.act_match, self._pass, self._pass_match, self.tran, self.tran_match, self.intr, self.intr_match, self.brev, self.brev_match, self.plen, self.plen_match, self.supr, self.supr_match, self.comp, self.comp_match])



if __name__ == '__main__':
    s = u'wordform\tlemma_gold\tlemma_pymorphy\tmatch\tpos_gold\tpos_pymorphy\tmatch\ttag_gold\ttag_pymorphy\ttag_original\tmatch\tnom\tnom_match\tgen\tgen_match\tdat\tdat_match\tacc\tacc_match\tins\tins_match\tloc\tloc_match\tgen2\tgen2_match\tloc2\tloc2_match\tvoc\tvoc2_match\tsg\tsg_match\tpl\tpl_match\tf\tf_match\tm\tm_match\tn\tn_match\tm-f\tmf_match\tanim\tanim_match\tinan\tinan_match\tanom\tanom_match\tdistort\tdist_match\tanum\tanum_match\tabbr\tabbr_match\tindic\tindic_match\timper\timper_match\tinf\tinf_match\tger\tger_match\tpraes\tpraes_match\tpraet\tpraet_match\t1p\t1p_match\t2p\t2p_match\t3p\t3p_match\tpf\tpf_match\tipf\tipf_match\tinf\tinf_match\tact\tact_match\tpass\tpass_match\ttran\ttran_match\tintr\tintr_match\tbrev\tbrev_match\tplen\tpren_match\tsupr\tsupr_match\tcomp\tcomp_match\r\n'

    with codecs.open(u'diff_pymorphy3.csv', 'w', 'utf-8') as dif:
        dif.write(s)
        n = codecs.open('full_final.txt', 'r', 'utf-8')
        for line in n:
            example = ''
            wf, lex, gr, norm, pym = [i.strip() for i in line.split('\t')]
            example += wf + '\t' + lex + '\t' + norm + '\t'
            l, s = convert_py(pym)
            A = Line(wf, lex, gr, norm, pym, l, s)
            dif.write(A.unicode())
            dif.write('\r\n')

        n.close()
