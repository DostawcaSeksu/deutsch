import json
import random
import os
import re

STATS_FILE = 'german_stats.json'

REGULAR_VERBS = [
    'machen', 'wohnen', 'lernen', 'sagen', 'fragen', 'spielen', 
    'kaufen', 'suchen', 'kochen', 'leben', 'lieben', 'hören',
    'arbeiten', 'brauchen', 'glauben', 'hoffen', 'tanzen', 'reisen',
    'zeigen', 'malen', 'antworten', 'bezahlen', 'öffnen'
]

IRREGULAR_VERBS = [
    {'infinitive': 'fahren', 'stem': 'fahr', 'change': {'du': 'fähr', 'er/sie/es': 'fähr'}},
    {'infinitive': 'sprechen', 'stem': 'sprech', 'change': {'du': 'sprich', 'er/sie/es': 'sprich'}},
    {'infinitive': 'geben', 'stem': 'geb', 'change': {'du': 'gib', 'er/sie/es': 'gib'}},
    {'infinitive': 'sehen', 'stem': 'seh', 'change': {'du': 'sieh', 'er/sie/es': 'sieh'}},
    {'infinitive': 'lesen', 'stem': 'les', 'change': {'du': 'lies', 'er/sie/es': 'lies'}},
    {'infinitive': 'helfen', 'stem': 'helf', 'change': {'du': 'hilf', 'er/sie/es': 'hilf'}},
    {'infinitive': 'nehmen', 'stem': 'nehm', 'change': {'du': 'nimm', 'er/sie/es': 'nimm'}},
    {'infinitive': 'treffen', 'stem': 'treff', 'change': {'du': 'triff', 'er/sie/es': 'triff'}},
    {'infinitive': 'essen', 'stem': 'ess', 'change': {'du': 'iss', 'er/sie/es': 'iss'}},
    {'infinitive': 'schlafen', 'stem': 'schlaf', 'change': {'du': 'schläf', 'er/sie/es': 'schläf'}},
    {'infinitive': 'laufen', 'stem': 'lauf', 'change': {'du': 'läuf', 'er/sie/es': 'läuf'}},
    {'infinitive': 'tragen', 'stem': 'trag', 'change': {'du': 'träg', 'er/sie/es': 'träg'}},
]

PRONOUN_RULES = [
    {'pronoun': 'ich', 'ending': '-e', 'group': 'ich'},
    {'pronoun': 'du', 'ending': '-st', 'group': 'du'},
    {'pronoun': 'er', 'ending': '-t', 'group': 'er / sie / es / ihr'},
    {'pronoun': 'sie (она)', 'ending': '-t', 'group': 'er / sie / es / ihr'},
    {'pronoun': 'es', 'ending': '-t', 'group': 'er / sie / es / ihr'},
    {'pronoun': 'ihr', 'ending': '-t', 'group': 'er / sie / es / ihr'},
    {'pronoun': 'wir', 'ending': '-en', 'group': 'wir / sie / Sie'},
    {'pronoun': 'sie (они)', 'ending': '-en', 'group': 'wir / sie / Sie'},
    {'pronoun': 'Sie (вежл.)', 'ending': '-en', 'group': 'wir / sie / Sie'},
]

PRONOUN_GROUPS = {
    'ich': '-e',
    'du': '-st',
    'er / sie / es / ihr': '-t',
    'wir / sie / Sie': '-en'
}

GROUP_TO_PRONOUNS_SET = {group: set() for group in PRONOUN_GROUPS}
for rule in PRONOUN_RULES:
    base_pronoun = re.sub(r' \(.*\)', '', rule['pronoun'])
    GROUP_TO_PRONOUNS_SET[rule['group']].add(base_pronoun)

def main_menu():
    stats = load_stats()
    while True:
        clear_screen()
        stats = load_stats()
        print("--- Тренажер спряжения немецких глаголов ---")
        print(f"\nВаш текущий счет: {stats['total_score']}\n")
        print("Выберите режим:")
        print("1. Угадай окончание (ich wohn__ -> -e)")
        print("2. Угадай местоимение (wohnst -> du)")
        print("3. Показать статистику")
        print("4. Выход")
        
        choice = input("\nВведите номер: ")
        
        if choice in ['1', '2']:
            difficulty = choose_difficulty()
            if choice == '1':
                run_mode_1(stats, difficulty)
            else:
                run_mode_2(stats, difficulty)
        elif choice == '3':
            display_stats(stats)
        elif choice == '4':
            print("Auf Wiedersehen!")
            break
        else:
            print("Неверный ввод. Попробуйте еще раз.")
            input("Нажмите Enter для продолжения...")

def load_stats():
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "total_score": 0,
            "endings": { e: {"correct": 0, "incorrect": 0} for e in PRONOUN_GROUPS.values() },
            "pronoun_groups": { g: {"correct": 0, "incorrect": 0} for g in PRONOUN_GROUPS.keys() }
        }

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

def update_stats(stats, category, key, is_correct):
    if is_correct:
        stats['total_score'] += 1
        stats[category][key]['correct'] += 1
    else:
        stats['total_score'] -= 1
        stats[category][key]['incorrect'] += 1
    return stats

def get_weighted_choice(stats, category):
    items = list(stats[category].keys())
    weights = [stats[category][item]['incorrect'] + 1 for item in items]
    return random.choices(items, weights=weights, k=1)[0]

def display_stats(stats):
    clear_screen()
    print("--- ВАША СТАТИСТИКА ---")
    print(f"\nОбщий счет: {stats['total_score']}\n")
    print("--- Успешность по ОКОНЧАНИЯМ ---")
    for ending, data in stats['endings'].items():
        correct, incorrect = data['correct'], data['incorrect']
        total = correct + incorrect
        percentage = correct / total if total > 0 else 0
        bar = '█' * int(percentage * 20)
        print(f"{ending.ljust(4)} [{bar.ljust(20)}] {percentage:.0%}")

    print("\n--- Успешность по МЕСТОИМЕНИЯМ ---")
    for group, data in stats['pronoun_groups'].items():
        correct, incorrect = data['correct'], data['incorrect']
        total = correct + incorrect
        percentage = correct / total if total > 0 else 0
        bar = '█' * int(percentage * 20)
        print(f"{group.ljust(20)} [{bar.ljust(20)}] {percentage:.0%}")
    input("\nНажмите Enter, чтобы вернуться в меню...")

def choose_difficulty():
    """Меню выбора сложности."""
    while True:
        print("\nВыберите уровень сложности:")
        print("1. Легкий (только правильные глаголы, выбор по номеру)")
        print("2. Средний (правильные и неправильные глаголы, выбор по номеру)")
        print("3. Сложный (ввод ответа вручную)")
        choice = input("Ваш выбор (1-3): ")
        if choice == '1': return 'easy'
        if choice == '2': return 'medium'
        if choice == '3': return 'hard'
        print("Неверный ввод, попробуйте снова.")

def run_mode_1(stats, difficulty):
    """Режим 1: Угадай окончание."""
    clear_screen()
    print(f"--- РЕЖИМ 1: Угадай окончание (Уровень: {difficulty.upper()}) ---")
    print("Введите 'm' для выхода в меню.\n")

    while True:
        target_ending = get_weighted_choice(stats, 'endings')
        possible_rules = [r for r in PRONOUN_RULES if r['ending'] == target_ending]
        chosen_rule = random.choice(possible_rules)
        pronoun, stat_group = chosen_rule['pronoun'], chosen_rule['group']
        
        use_irregular = difficulty in ['medium', 'hard'] and random.choice([True, False])
        if use_irregular and chosen_rule['pronoun'] in ['du', 'er', 'sie (она)', 'es']:
            verb_data = random.choice(IRREGULAR_VERBS)
            verb_stem = verb_data['change'].get(stat_group.split(' ')[0], verb_data['stem'])
        else:
            verb_stem = random.choice(REGULAR_VERBS)[:-2]

        print(f"Текущий счет: {stats['total_score']}")
        print(f"\nКакое окончание у глагола: {pronoun} {verb_stem}__\n")
        
        if difficulty in ['easy', 'medium']:
            options = list(PRONOUN_GROUPS.values())
            random.shuffle(options)
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            
            user_choice = input("\nВаш выбор (1-4): ").lower()
            if user_choice == 'm': break

            try:
                user_answer = options[int(user_choice) - 1]
            except (ValueError, IndexError):
                print("\n⚠️ Неверный ввод.\n")
                continue
        else:
            user_answer = input("Введите окончание (например, -st): ").strip().lower()
            if user_answer == 'm': break
            if not user_answer.startswith('-'):
                user_answer = '-' + user_answer
        
        if user_answer == target_ending:
            print("\n✅ Правильно!\n")
            stats = update_stats(stats, 'endings', target_ending, True)
        else:
            print(f"\n❌ Неправильно! Правильный ответ: {target_ending}")
            print(f"Пример: {pronoun} {verb_stem}{target_ending.replace('-', '')}\n")
            stats = update_stats(stats, 'endings', target_ending, False)
        
        save_stats(stats)
        print("-" * 20)


def run_mode_2(stats, difficulty):
    """Режим 2: Угадай местоимение."""
    clear_screen()
    print(f"--- РЕЖИМ 2: Угадай местоимение (Уровень: {difficulty.upper()}) ---")
    print("Введите 'm' для выхода в меню.\n")
    
    while True:
        target_group = get_weighted_choice(stats, 'pronoun_groups')
        correct_ending = PRONOUN_GROUPS[target_group]
        
        verb_stem = ''
        use_irregular = difficulty in ['medium', 'hard'] and random.choice([True, False])
        if use_irregular and target_group in ['du', 'er / sie / es / ihr']:
            verb_data = random.choice(IRREGULAR_VERBS)
            verb_stem = verb_data['change'].get(target_group.split(' ')[0], verb_data['stem'])
        else:
            verb_stem = random.choice(REGULAR_VERBS)[:-2]
            
        conjugated_verb = verb_stem + correct_ending.replace('-', '')

        print(f"Текущий счет: {stats['total_score']}")
        print(f"\nКакая группа местоимений подходит к глаголу '{conjugated_verb}'?\n")

        is_correct = False
        if difficulty in ['easy', 'medium']:
            options = list(PRONOUN_GROUPS.keys())
            random.shuffle(options)
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            
            user_choice = input("\nВаш выбор (1-4): ").lower()
            if user_choice == 'm': break

            try:
                user_answer_group = options[int(user_choice) - 1]
                if user_answer_group == target_group:
                    is_correct = True
            except (ValueError, IndexError):
                print("\n⚠️ Неверный ввод.\n")
                continue
        else:
            prompt = "Введите все подходящие местоимения через пробел: "
            user_input = input(prompt)
            if user_input.lower() == 'm': break
            
            user_pronouns_set = set(user_input.split())
            correct_pronouns_set = GROUP_TO_PRONOUNS_SET[target_group]
            
            if user_pronouns_set == correct_pronouns_set:
                is_correct = True

        if is_correct:
            print("\n✅ Правильно!\n")
            stats = update_stats(stats, 'pronoun_groups', target_group, True)
        else:
            print(f"\n❌ Неправильно! Правильный ответ: {target_group}")
            if difficulty == 'hard':
                correct_string = " ".join(sorted(list(GROUP_TO_PRONOUNS_SET[target_group])))
                print(f"Нужно было ввести: {correct_string}\n")
            stats = update_stats(stats, 'pronoun_groups', target_group, False)
        
        save_stats(stats)
        print("-" * 20)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main_menu()