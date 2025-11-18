import os
from pathlib import Path

STATS_FILE = 'german_stats.json'
DATA_DIR = 'data'
I18N_DIR = 'i18n'


REGULAR_VERBS_FILE = os.path.join(DATA_DIR, 'regular_verbs.json')
IRREGULAR_VERBS_FILE = os.path.join(DATA_DIR, 'irregular_verbs.json')
PRONOUN_RULES_FILE = os.path.join(DATA_DIR, 'pronoun_rules.json')
NOUNS_FILE = os.path.join(DATA_DIR, 'nouns.json')