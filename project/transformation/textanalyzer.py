import re

from re import Pattern
from typing import Any
from nltk import pos_tag, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pyspark.ml.feature import HashingTF
from pyspark.sql import DataFrame


class TextAnalyzer:

    def __init__(self, param: str = None) -> None:
        self.param = param

    def analyze(self, sentence: str) -> list:
        words: list = self.preprocess(sentence)
        if self.param == "part":
            return self.mark_parts(words)
        return words

    def preprocess(self, sentence: str) -> list:
        return self.clean_stopwords(
            self.tokenize(self.remove_characters(sentence))
        )

    def remove_characters(self, sentence: str) -> Any:
        pattern: Pattern = re.compile(r'\t|\n|\.|-|:|;|\)|\(|\?|,|"')
        return re.sub(pattern, ' ', str(sentence))

    def tokenize(self, sentence: str) -> list:
        tokenized_word: list = list()
        lemmatizer: WordNetLemmatizer = WordNetLemmatizer()
        for t in word_tokenize(sentence):
            if t.isalpha() and t:
                t = t.lower()
                tokenized_word.append(
                    lemmatizer.lemmatize(t, pos="a")
                )
        return tokenized_word

    def clean_stopwords(self, words_list: list) -> list:
        clear_list: list = list()
        for word in words_list:
            if word not in stopwords.words('english'):
                clear_list.append(word)
        return clear_list

    def mark_parts(self, word_list: list) -> list:
        marked_list: list = pos_tag(word_list)
        parts = list()
        for m in marked_list:
            parts.append(m[-1])
        return parts

    def merge_lists(self, lists: list) -> list:
        general_list: list = list()
        for i in lists:
            general_list.extend(i)
        return general_list

    def preparation(self, df: DataFrame,
                    udf_analyzer: Any, target_col: str) -> DataFrame:
        return self.vectorizer(
            df.withColumn("processed", udf_analyzer(target_col)),
            "processed", "features"
        )

    def vectorizer(self, df: DataFrame,
                   inputCol: str, outputCol: str) -> DataFrame:
        hashTF: HashingTF = HashingTF(inputCol=inputCol, outputCol=outputCol)
        return hashTF.transform(df)
