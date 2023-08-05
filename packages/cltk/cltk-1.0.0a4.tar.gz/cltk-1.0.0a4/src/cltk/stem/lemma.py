"""Lemmatize Latin words."""

__author__ = ["Kyle P. Johnson <kyle@kyle-p-johnson.com>"]
__license__ = "MIT License. See LICENSE."

import importlib.machinery
import os
import warnings

from nltk.tokenize.punkt import PunktLanguageVars

from cltk.core.cltk_logger import logger
from cltk.utils import CLTK_DATA_DIR

AVAILABLE_LANGUAGES = ["grc", "lat"]

# Deprecated; remove from future release?
class LemmaReplacer(object):  # pylint: disable=too-few-public-methods
    """Lemmatize Latin words by replacing input words with corresponding
    values from a replacement list.
    """

    def __init__(self, language):
        """Import replacement patterns into a list."""
        self.language = language.lower()
        assert (
            self.language in AVAILABLE_LANGUAGES
        ), "\n\nLemmatizer not available for language '{0}'.".format(self.language)
        self.lemmata = self._load_replacement_patterns()

    def _load_replacement_patterns(self):
        """Check for availability of lemmatizer for a language."""
        if self.language == "lat":
            warnings.warn(
                "LemmaReplacer is deprecated and will soon be removed from CLTK. Please use the BackoffLatinLemmatizer at cltk.lemmatize.lat.backoff.",
                DeprecationWarning,
                stacklevel=2,
            )
            rel_path = os.path.join(
                CLTK_DATA_DIR,
                self.language,
                "model",
                "lat_models_cltk",
                "lemmata",
                "latin_lemmata_cltk.py",
            )
            path = os.path.expanduser(rel_path)
            # logger.info('Loading lemmata. This may take a minute.')
            loader = importlib.machinery.SourceFileLoader("lat_lemmata_cltk", path)

        elif self.language == "grc":
            rel_path = os.path.join(
                CLTK_DATA_DIR,
                self.language,
                "model",
                "grc_models_cltk",
                "lemmata",
                "greek_lemmata_cltk.py",
            )
            path = os.path.expanduser(rel_path)
            # logger.info('Loading lemmata. This may take a minute.')
            loader = importlib.machinery.SourceFileLoader("grc_lemmata_cltk", path)
        module = loader.load_module()
        lemmata = module.LEMMATA
        return lemmata

    def lemmatize(self, input_text, return_raw=False, return_string=False):
        """Take incoming string or list of tokens. Lookup done against a
        key-value list of lemmata-headword. If a string, tokenize with
        ``PunktLanguageVars()``. If a final period appears on a token, remove
        it, then re-add once replacement done.
        TODO: rm check for final period, change PunktLanguageVars()
        """
        assert type(input_text) in [list, str], logger.error(
            "Input must be a list or string."
        )
        if type(input_text) is str:
            punkt = PunktLanguageVars()
            tokens = punkt.word_tokenize(input_text)
        else:
            tokens = input_text

        lemmatized_tokens = []
        for token in tokens:
            # check for final period
            final_period = False
            if token[-1] == ".":
                final_period = True
                token = token[:-1]

            # look for token in lemma dict keys
            if token.lower() in self.lemmata.keys():
                headword = self.lemmata[token.lower()]

                # re-add final period if rm'd
                if final_period:
                    headword += "."

                # append to return list
                if not return_raw:
                    lemmatized_tokens.append(headword)
                else:
                    lemmatized_tokens.append(token + "/" + headword)
            # if token not found in lemma-headword list
            else:
                # re-add final period if rm'd
                if final_period:
                    token += "."

                if not return_raw:
                    lemmatized_tokens.append(token)
                else:
                    lemmatized_tokens.append(token + "/" + token)
        if not return_string:
            return lemmatized_tokens
        elif return_string:
            return " ".join(lemmatized_tokens)


if __name__ == "__main__":
    REPLACER = LemmaReplacer("lat")
    PUNKT = PunktLanguageVars()
    # STRING = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum. Maiores nostri sic habuerunt et ita in legibus posiuerunt: furem dupli condemnari, foeneratorem quadrupli. Quanto peiorem ciuem existimarint foeneratorem quam furem, hinc licet existimare. Et uirum bonum quom laudabant, ita laudabant: bonum agricolam bonumque colonum; amplissime laudari existimabatur qui ita laudabatur. Mercatorem autem strenuum studiosumque rei quaerendae existimo, uerum, ut supra dixi, periculosum et calamitosum. At ex agricolis et uiri fortissimi et milites strenuissimi gignuntur, maximeque pius quaestus stabilissimusque consequitur minimeque inuidiosus, minimeque male cogitantes sunt qui in eo studio occupati sunt. Nunc, ut ad rem redeam, quod promisi institutum principium hoc erit.'  # pylint: disable=line-too-long
    STRING = "hominum divomque voluptas"
    # EX_TOKENS = PUNKT.word_tokenize(UMLEMMATIZED)
    # UMLEMMATIZED = ['τὴν', 'διάγνωσιν', 'αὐτῶν', 'ἔρχεσθαι']
    # LEMMATIZED = REPLACER.lemmatize(UMLEMMATIZED, return_raw=False, return_string=True)
    LEMMATIZED = REPLACER.lemmatize(
        STRING.split(), return_raw=False, return_string=True
    )
    print(LEMMATIZED)
