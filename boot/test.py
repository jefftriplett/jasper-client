import os
import unittest

import g2p
import vocabcompiler

from mock import patch


if os.environ.get('JASPER_HOME') is None:
    os.environ['JASPER_HOME'] = '/home/pi'


class UnorderedList(list):

    def __eq__(self, other):
        return sorted(self) == sorted(other)


class TestVocabCompiler(unittest.TestCase):

    def testWordExtraction(self):
        sentences = "temp_sentences.txt"
        dictionary = "temp_dictionary.dic"
        languagemodel = "temp_languagemodel.lm"

        words = [
            'HACKER', 'LIFE', 'FACEBOOK', 'THIRD', 'NO', 'JOKE',
            'NOTIFICATION', 'MEANING', 'TIME', 'TODAY', 'SECOND',
            'BIRTHDAY', 'KNOCK KNOCK', 'INBOX', 'OF', 'NEWS', 'YES',
            'TOMORROW', 'EMAIL', 'WEATHER', 'FIRST', 'MUSIC', 'SPOTIFY'
        ]

        with patch.object(g2p, 'translateWords') as translateWords:
            with patch.object(vocabcompiler, 'text2lm') as text2lm:
                vocabcompiler.compile(sentences, dictionary, languagemodel)

                # 'words' is appended with ['MUSIC', 'SPOTIFY']
                # so must be > 2 to have received WORDS from modules
                translateWords.assert_called_once_with(UnorderedList(words))
                self.assertTrue(text2lm.called)
        os.remove(sentences)
        os.remove(dictionary)

if __name__ == '__main__':
    unittest.main()
