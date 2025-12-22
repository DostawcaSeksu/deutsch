from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

STATS_FILE = BASE_DIR / 'german_stats.json'
DATA_DIR = BASE_DIR / 'data'
I18N_DIR = BASE_DIR / 'i18n'

REGULAR_VERBS_FILE = DATA_DIR / 'regular_verbs.json'
IRREGULAR_VERBS_FILE = DATA_DIR / 'irregular_verbs.json'
PRONOUN_RULES_FILE = DATA_DIR / 'pronoun_rules.json'
NOUNS_FILE = DATA_DIR / 'nouns.json'
ARTICLES_FILE = DATA_DIR / 'articles.json'
PERSONAL_PRONOUNS_FILE = DATA_DIR / 'personal_pronouns.json'
CASE_SENTENCES_FILE = DATA_DIR / 'case_sentences.json'
MODAL_VERBS_FILE = DATA_DIR / 'modal_verbs.json'
W_FRAGEN_FILE = DATA_DIR / 'w_fragen.json'
CONJUNCTIONS_FILE = DATA_DIR / 'conjunctions.json'