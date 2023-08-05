# -*- coding: utf-8 -*-
"""
All unit tests for the scraper Article should be contained in this file.
"""

import spacy
from scraper.text import get_stopwords
from scraper.named_entity_recognition import TextRank4Keyword
from scraper import Article, Configuration


def validate(url, language, translate):
    config = Configuration()
    config.follow_meta_refresh = True
    # BUG was that website reported language as zh-Hant-TW when it really was en!
    config.use_meta_language = False
    config.set_language(language)
    config.translate = translate
    config.http_success_only = False
    article = Article(url, config=config)
    article.download()
    article.parse()
    assert len(article.text)
    article.nlp()
    return article


def test_methods():
    nlp = spacy.load("en_core_web_sm")
    # use spacy language specific STOP WORDS
    stopwords = get_stopwords("en")
    tr4w = TextRank4Keyword(nlp)
    text = "Alan Cooper\nTemple University\nB.A.\nemail:\tcooper@pobox.com\nmobile:+1555.555.5555"
    tr4w.analyze(text, candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False, stopwords=stopwords)
    education = tr4w.get_education()
    assert education == ["BA"]
    persons = tr4w.get_persons()
    assert len(persons) == 1
    assert "Alan Cooper" in persons


def test_power_projects_english():
    url = "https://www.power-technology.com/projects/dai-nanh/"
    validate(url, 'en', False)

def test_chinese():
    url = "http://news.sohu.com/20050601/n225789219.shtml"
    article = validate(url, 'zh', False)
    assert article
