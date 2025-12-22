import config
from utils.ui import clear_screen
from utils.localization import Localization
from modules.verb_trainer import VerbTrainer
from modules.noun_trainer import NounTrainer
from modules.case_trainer import CaseTrainer
from utils.file_handler import load_json, save_json
from modules.modal_verb_trainer import ModalVerbTrainer
from modules.vocabulary_trainer import VocabularyTrainer

def main():
    """Main function to run the application."""
    lang_code = select_language()
    loc = Localization(lang_code)

    stats = load_json(config.STATS_FILE)
    if stats is None:
        stats = get_default_stats()

    default_stats = get_default_stats()
    for category in default_stats:
        if category not in stats:
            stats[category] = default_stats[category]

    while True:
        clear_screen()
        print(loc.get('app_title'))
        print(loc.get('current_score', score=stats['total_score']))
        print("\n" + loc.get('choose_mode'))
        
        print(loc.get('menu_verbs'))
        print(loc.get('menu_nouns'))
        print(loc.get('menu_cases'))
        print(loc.get('menu_modals'))
        print(loc.get('menu_w_fragen'))
        print(loc.get('menu_conjunctions'))

        print(loc.get('menu_stats'))
        print(loc.get('menu_exit'))
        
        choice = input(loc.get('enter_number'))
        
        trainer = None

        try:
            if choice == '1':
                trainer = VerbTrainer(loc)
            elif choice == '2':
                trainer = NounTrainer(loc)
            elif choice == '3':
                trainer = CaseTrainer(loc)
            elif choice == '4':
                trainer = ModalVerbTrainer(loc)
            elif choice == '5':
                trainer = VocabularyTrainer(
                    loc, 
                    data_file=config.W_FRAGEN_FILE, 
                    category_key='w_fragen', 
                    title_key='mode_w_fragen_title'
                )
            elif choice == '6':
             trainer = VocabularyTrainer(
                loc, 
                data_file=config.CONJUNCTIONS_FILE, 
                category_key='conjunctions', 
                title_key='mode_conjunctions_title'
            )
            elif choice == '7':
                display_stats(stats, loc)
                continue
            elif choice == '8':
                print(loc.get('goodbye'))
                break
            else:
                print(loc.get('invalid_input'))
                input(loc.get('press_enter'))
                continue

            if trainer:
                trainer.run(stats)
                save_json(config.STATS_FILE, stats)

        except FileNotFoundError as e:
            print(f"Error: {e}")
            input(loc.get('press_enter'))
        except Exception as e:
             print(f"An unexpected error occurred: {e}")
             input(loc.get('press_enter'))

def select_language():
    """Prompts the user to select a language."""
    while True:
        clear_screen()
        print("--- Language Selection / Выбор языка ---")
        print("1. English")
        print("2. Русский")
        choice = input("\nChoose your language / Выберите язык (1-2): ")
        if choice == '1':
            return 'en'
        if choice == '2':
            return 'ru'

def get_default_stats():
    """Returns a default stats structure."""
    pronoun_rules = load_json(config.PRONOUN_RULES_FILE) or []
    pronoun_groups = {rule['group']: rule['ending'] for rule in pronoun_rules}
    articles = load_json(config.ARTICLES_FILE) or {}
    article_keys = {f"{gender}-{case}": {"correct": 0, "incorrect": 0} 
                    for gender in articles for case in articles[gender]}

    pronouns = load_json(config.PERSONAL_PRONOUNS_FILE) or {}
    pronoun_keys = {f"{pronoun}-{case}": {"correct": 0, "incorrect": 0}
                    for case in pronouns for pronoun in pronouns[case]}

    
    return {
        "total_score": 0,
        "endings": {e: {"correct": 0, "incorrect": 0} for e in pronoun_groups.values()},
        "pronoun_groups": {g: {"correct": 0, "incorrect": 0} for g in pronoun_groups.keys()},
        "articles": {
            "der": {"correct": 0, "incorrect": 0},
            "die": {"correct": 0, "incorrect": 0},
            "das": {"correct": 0, "incorrect": 0}
        },
        "singular_plural": {
            "main": {"correct": 0, "incorrect": 0}
        },
        "article_declension": article_keys,
        "pronoun_declension": pronoun_keys,
        "modal_verbs": {}
    }

def display_stats(stats, loc):
    """Displays user statistics."""
    clear_screen()
    print(loc.get('stats_title'))
    print(loc.get('total_score', score=stats['total_score']))
    
    print(loc.get('stats_endings_title'))
    for ending, data in stats['endings'].items():
        correct, incorrect = data['correct'], data['incorrect']
        total = correct + incorrect
        percentage = correct / total if total > 0 else 0
        bar = '█' * int(percentage * 20)
        print(f"{ending.ljust(4)} [{bar.ljust(20)}] {percentage:.0%}")

    print(loc.get('stats_pronouns_title'))
    for group, data in stats['pronoun_groups'].items():
        correct, incorrect = data['correct'], data['incorrect']
        total = correct + incorrect
        percentage = correct / total if total > 0 else 0
        bar = '█' * int(percentage * 20)
        print(f"{group.ljust(20)} [{bar.ljust(20)}] {percentage:.0%}")

    print(loc.get('stats_articles_title'))
    for article, data in stats.get('articles', {}).items():
        correct, incorrect = data['correct'], data['incorrect']
        total = correct + incorrect
        percentage = correct / total if total > 0 else 0
        bar = '█' * int(percentage * 20)
        print(f"{article.ljust(4)} [{bar.ljust(20)}] {percentage:.0%}")
    
    print(loc.get('stats_plurals_title'))
    sp_data = stats.get('singular_plural', {}).get('main', {"correct": 0, "incorrect": 0})
    correct, incorrect = sp_data['correct'], sp_data['incorrect']
    total = correct + incorrect
    percentage = correct / total if total > 0 else 0
    bar = '█' * int(percentage * 20)
    print(f"{'Singular/Plural'.ljust(20)} [{bar.ljust(20)}] {percentage:.0%}")

    if 'article_declension' in stats and any(v['correct'] or v['incorrect'] for v in stats['article_declension'].values()):
        print(loc.get('stats_article_decl_title'))
        for key, data in sorted(stats['article_declension'].items()):
            correct, incorrect = data['correct'], data['incorrect']
            total = correct + incorrect
            if total > 0:
                percentage = correct / total
                bar = '█' * int(percentage * 20)
                print(f"{key.ljust(20)} [{bar.ljust(20)}] {percentage:.0%}")
    
    if 'pronoun_declension' in stats and any(v['correct'] or v['incorrect'] for v in stats['pronoun_declension'].values()):
        print(loc.get('stats_pronoun_decl_title'))
        for key, data in sorted(stats['pronoun_declension'].items()):
            correct, incorrect = data['correct'], data['incorrect']
            total = correct + incorrect
            if total > 0:
                percentage = correct / total
                bar = '█' * int(percentage * 20)
                print(f"{key.ljust(20)} [{bar.ljust(20)}] {percentage:.0%}")

    if 'modal_verbs' in stats and any(v['correct'] or v['incorrect'] for v in stats['modal_verbs'].values()):
        print(loc.get('stats_modals_title'))
        for key, data in sorted(stats['modal_verbs'].items()):
            correct, incorrect = data['correct'], data['incorrect']
            total = correct + incorrect
            if total > 0:
                percentage = correct / total
                bar = '█' * int(percentage * 20)
                print(f"{key.ljust(20)} [{bar.ljust(20)}] {percentage:.0%}")
    
    input(f"\n{loc.get('press_enter')}")

if __name__ == "__main__":
    main()