# encoding: utf-8
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz

@version: 1.0
@license: Apache Licence
@file: test_embeddings.py
@time: 2019-01-27 13:05

"""
import os
import unittest
import logging
import kashgari.macros as k
from kashgari.embeddings import WordEmbeddings, BERTEmbedding, CustomEmbedding, BaseEmbedding, TwoHeadEmbedding
from kashgari.utils.logger import init_logger
init_logger()

SEQUENCE_LENGTH = 30
TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestWordEmbeddings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.embedding = WordEmbeddings('sgns.weibo.bigram-char',
                                       sequence_length=SEQUENCE_LENGTH,
                                       limit=1000)

    def test_build(self):
        # self.setup()
        assert self.embedding.idx2token[0] == k.PAD
        assert self.embedding.idx2token[1] == k.BOS
        assert self.embedding.idx2token[2] == k.EOS
        assert self.embedding.idx2token[3] == k.UNK

    def test_tokenize(self):
        sentence = ['我', '想', '看', '电影', '%%##!$#%']
        tokens = self.embedding.tokenize(sentence)

        logging.info('tokenize test: {} -> {}'.format(sentence, tokens))
        assert len(tokens) == len(tokens)
        assert tokens[-2] == self.embedding.token2idx[k.UNK]

        token_list = self.embedding.tokenize([sentence])
        assert len(token_list[0]) == len(sentence) + 2

    def test_embed(self):
        sentence = ['我', '想', '看', '电影', '%%##!$#%']
        embedded_sentence = self.embedding.embed(sentence)
        embedded_sentences = self.embedding.embed([sentence])
        logging.info('embed test: {} -> {}'.format(sentence, embedded_sentence))
        assert embedded_sentence.shape == (SEQUENCE_LENGTH, self.embedding.embedding_size)
        assert embedded_sentences.shape == (1, SEQUENCE_LENGTH, self.embedding.embedding_size)


class TestBERTEmbedding(TestWordEmbeddings):
    @classmethod
    def setUpClass(cls):
        bert_path = 'chinese_L-12_H-768_A-12'
        cls.embedding = BERTEmbedding(bert_path,
                                      sequence_length=SEQUENCE_LENGTH)

    def test_build(self):
        assert self.embedding.embedding_size > 0
        assert self.embedding.token2idx[k.PAD] == 0
        assert self.embedding.token2idx[k.BOS] > 0
        assert self.embedding.token2idx[k.EOS] > 0
        assert self.embedding.token2idx[k.UNK] > 0


class TestCustomEmbedding(TestWordEmbeddings):
    @classmethod
    def setUpClass(cls):
        cls.embedding = CustomEmbedding('empty_embedding',
                                        sequence_length=SEQUENCE_LENGTH,
                                        embedding_size=100)

        corpus = [['我', '们', '变', '而', '以', '书', '会', '友', '，', '以', '书', '结', '缘', '，',
                   '把', '欧', '美', '、', '港', '台', '流', '行', '的',
                   '食', '品', '类', '图', '谱', '、', '画', '册', '、',
                   '工', '具', '书', '汇', '集', '一', '堂', '。'],
                  ['为', '了', '跟', '踪', '国', '际', '最', '新', '食', '品',
                   '工', '艺', '、', '流', '行', '趋', '势', '，', '大', '量',
                   '搜', '集', '海', '外', '专', '业', '书', '刊', '资', '料',
                   '是', '提', '高', '技', '艺', '的', '捷', '径', '。'],
                  ['其', '中', '线', '装', '古', '籍', '逾', '千', '册',
                   '；', '民', '国', '出', '版', '物', '几', '百', '种',
                   '；', '珍', '本', '四', '册', '、', '稀', '见', '本',
                   '四', '百', '余', '册', '，', '出', '版', '时', '间',
                   '跨', '越', '三', '百', '余', '年', '。'],
                  ['有', '的', '古', '木', '交', '柯', '，',
                   '春', '机', '荣', '欣', '，', '从', '诗',
                   '人', '句', '中', '得', '之', '，', '而',
                   '入', '画', '中', '，', '观', '之', '令', '人', '心', '驰', '。', '我']]
        cls.embedding.build_token2idx_dict(x_data=corpus, min_count=2)

    def test_build(self):
        assert self.embedding.token_count == 33
        super(TestCustomEmbedding, self).test_build()


class TestTwoHeadEmbedding(TestWordEmbeddings):
    @classmethod
    def setUpClass(cls):
        cls.embedding = TwoHeadEmbedding('empty_embedding',
                                         sequence_length=[SEQUENCE_LENGTH, SEQUENCE_LENGTH],
                                         embedding_size=100)
        corpus1 = [['我', '们', '变', '而', '以', '书', '会', '友', '，', '以', '书', '结', '缘', '，',
                   '把', '欧', '美', '、', '港', '台', '流', '行', '的',
                   '食', '品', '类', '图', '谱', '、', '画', '册', '、',
                   '工', '具', '书', '汇', '集', '一', '堂', '。'],
                  ['为', '了', '跟', '踪', '国', '际', '最', '新', '食', '品',
                   '工', '艺', '、', '流', '行', '趋', '势', '，', '大', '量',
                   '搜', '集', '海', '外', '专', '业', '书', '刊', '资', '料',
                   '是', '提', '高', '技', '艺', '的', '捷', '径', '。']]
        corpus2 = [['其', '中', '线', '装', '古', '籍', '逾', '千', '册',
                   '；', '民', '国', '出', '版', '物', '几', '百', '种',
                   '；', '珍', '本', '四', '册', '、', '稀', '见', '本',
                   '四', '百', '余', '册', '，', '出', '版', '时', '间',
                   '跨', '越', '三', '百', '余', '年', '。'],
                  ['有', '的', '古', '木', '交', '柯', '，',
                   '春', '机', '荣', '欣', '，', '从', '诗',
                   '人', '句', '中', '得', '之', '，', '而',
                   '入', '画', '中', '，', '观', '之', '令', '人', '心', '驰', '。', '我']]
        cls.embedding.build_token2idx_dict(x_data=[corpus1, corpus2], min_count=2)

    def test_build(self):
        assert self.embedding.token_count == 33
        super(TestTwoHeadEmbedding, self).test_build()

    def test_embed(self):
        sentence1 = ['我', '想', '看', '电影', '%%##!$#%']
        sentence2 = ['我', '不', '看', '电影', '%%##!$#%']
        sentences = [[sentence1], [sentence2]]
        embedded_sentences = self.embedding.embed(sentences)
        logging.info('embed test: {} -> {}'.format(sentences, embedded_sentences))
        # assert embedded_sentence.shape == (SEQUENCE_LENGTH, self.embedding.embedding_size)
        assert embedded_sentences.shape == (1, SEQUENCE_LENGTH*2, self.embedding.embedding_size)


if __name__ == "__main__":
    unittest.main()
