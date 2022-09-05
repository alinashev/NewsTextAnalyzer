import unittest
from typing import Any

from nltk.corpus import stopwords

from project.transformation.configurator import TransformationConfigurator
from project.transformation.textanalyzer import TextAnalyzer


class TestTextAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        TransformationConfigurator.nltk_setup()
        self.analyzer_word: TextAnalyzer = TextAnalyzer("word")
        self.analyzer_part: TextAnalyzer = TextAnalyzer("part")

        self.sentence: str = "‘Abject Failure’: Texas Public Safety Director" \
                             + " Blames Police For Violating Protocol During" \
                             + " Uvalde Shooting"
        self.chars: set = set('-:;)(?,')
        self.stops: set = set(stopwords.words('english'))
        self.complex_list: list = [
            ["Texas", "Public"],
            ["Safety", "Director", "Blames"]
        ]
        self.positive_word: str = "happy"
        self.negative_word: str = "hate"

    def test_analyzer_word(self) -> None:
        words: list = self.analyzer_word.analyze(self.sentence)
        self.assertNotEqual(len(words), 0)

    def test_analyzer_part(self) -> None:
        part: list = self.analyzer_part.analyze(self.sentence)
        self.assertNotEqual(len(part), 0)

    def test_preprocess(self) -> None:
        preprocessed: list = self.analyzer_word.preprocess(self.sentence)
        if len(self.sentence) != 0:
            self.assertNotEqual(
                len(preprocessed), 0
            )
        else:
            self.assertEqual(len(preprocessed), 0)

    def test_remove_characters(self) -> None:
        cleaned_string: Any = self.analyzer_word \
            .remove_characters(self.sentence)
        result: bool = any((c in self.chars) for c in cleaned_string)
        self.assertEqual(result, False)

    def test_tokenize(self) -> None:
        tokenized: list = self.analyzer_word.tokenize(self.sentence)
        if len(self.sentence) != 0:
            self.assertNotEqual(
                len(tokenized), 0
            )
        else:
            self.assertEqual(len(tokenized), 0)

    def test_clean_stopwords(self) -> None:
        preprocessed: list = self.analyzer_part.preprocess(self.sentence)
        cleaned: list = self.analyzer_word.clean_stopwords(preprocessed)
        result: bool = any((w in self.stops) for w in cleaned)
        self.assertEqual(result, False)

    def test_mark_parts(self) -> None:
        preprocessed: list = self.analyzer_part.preprocess(self.sentence)
        parts: list = self.analyzer_part.mark_parts(preprocessed)
        self.assertEqual(len(preprocessed), len(parts))

    def test_merge_list(self) -> None:
        complex_count: int = 0
        for i in self.complex_list:
            complex_count += len(i)
        merged_list: list = self.analyzer_word.merge_lists(self.complex_list)
        self.assertEqual(complex_count, len(merged_list))


if __name__ == '__main__':
    unittest.main()
