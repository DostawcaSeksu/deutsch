import os
import config
from utils.file_handler import load_json, save_json
from utils.localization import Localization
from modules.verb_trainer import VerbTrainer
from modules.noun_trainer import NounTrainer

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
        print(loc.get('menu_stats'))
        print(loc.get('menu_exit'))
        
        choice = input(loc.get('enter_number'))
        
        if choice == '1':
            try:
                trainer = VerbTrainer(loc)
                trainer.run(stats)
                save_json(config.STATS_FILE, stats)
            except FileNotFoundError as e:
                print(f"Error: {e}")
                input(loc.get('press_enter'))
        elif choice == '2':
            try:
                trainer = NounTrainer(loc)
                trainer.run(stats)
                save_json(config.STATS_FILE, stats)
            except FileNotFoundError as e:
                print(f"Error: {e}")
                input(loc.get('press_enter'))
        elif choice in '3':
             print("\nThis module is coming soon!")
             input(loc.get('press_enter'))
        elif choice == '4':
            display_stats(stats, loc)
        elif choice == '5':
            print(loc.get('goodbye'))
            break
        else:
            print(loc.get('invalid_input'))
            input(loc.get('press_enter'))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        }
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
    
    input(f"\n{loc.get('press_enter')}")

if __name__ == "__main__":
    main()