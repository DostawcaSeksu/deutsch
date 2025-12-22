import random
from utils.file_handler import load_json
from utils.ui import clear_screen
import config

class VocabularyTrainer:
    def __init__(self, loc, data_file, category_key, title_key):
        """
        :param loc: объект локализации
        :param data_file: путь к json файлу (например, config.W_FRAGEN_FILE)
        :param category_key: ключ для сохранения статистики (например, 'w_fragen')
        :param title_key: ключ заголовка для UI
        """
        self.loc = loc
        self.items = load_json(data_file)
        self.category_key = category_key
        self.title_key = title_key
        
        if not self.items:
            raise FileNotFoundError(f"Could not load data from {data_file}")

    def run(self, stats):
        difficulty = self._choose_difficulty()
        self._run_training(stats, difficulty)

    def _run_training(self, stats, difficulty):
        clear_screen()
        title = self.loc.get(self.title_key) 
        print(f"--- {title} (Level: {difficulty.upper()}) ---")
        print(self.loc.get('exit_to_menu_prompt'))

        while True:
            item = self._get_weighted_choice(stats, self.category_key)
            
            question_sentence = item['sentence']
            correct_answer = item['answer']
            translation = item['translation'].get(self.loc.language, "???")

            print(self.loc.get('current_score', score=stats['total_score']))
            print(f"\n{self.loc.get('question_fill_blank')}")
            print(f"  {question_sentence}")
            print(f"  ({self.loc.get('translation_hint', text=translation)})")

            user_answer = ""

            if difficulty == 'easy':
                options = {correct_answer}
                while len(options) < min(4, len(self.items)):
                    distractor = random.choice(self.items)['answer']
                    options.add(distractor)
                
                shuffled_options = list(options)
                random.shuffle(shuffled_options)

                for i, option in enumerate(shuffled_options, 1):
                    print(f"{i}. {option}")
                
                user_choice = input(f"\n{self.loc.get('your_choice', options=f'1-{len(options)}')} ").lower()
                if user_choice == 'm': break
                
                try:
                    user_answer = shuffled_options[int(user_choice) - 1]
                except (ValueError, IndexError):
                    print(f"\n⚠️ {self.loc.get('invalid_input')}\n")
                    continue

            elif difficulty == 'medium':
                hint = correct_answer[0] + "_" * (len(correct_answer) - 1)
                user_answer = input(f"\n{self.loc.get('enter_answer_prompt')} ({hint}): ").strip()
                if user_answer.lower() == 'm': break

            else: # hard
                user_answer = input(f"\n{self.loc.get('enter_answer_prompt')} ").strip()
                if user_answer.lower() == 'm': break

            if user_answer.lower() == correct_answer.lower():
                print(self.loc.get('correct'))
                self._update_stats(stats, self.category_key, item['word'], True)
            else:
                print(self.loc.get('incorrect', answer=correct_answer))
                self._update_stats(stats, self.category_key, item['word'], False)
            
            print("-" * 20)

    def _choose_difficulty(self):
        while True:
            print(self.loc.get('choose_difficulty'))
            print(self.loc.get('difficulty_easy'))
            print(self.loc.get('difficulty_medium'))
            print(self.loc.get('difficulty_hard'))
            choice = input(self.loc.get('your_choice', options="1-3") + " ")
            if choice == '1': return 'easy'
            if choice == '2': return 'medium'
            if choice == '3': return 'hard'
            print(self.loc.get('invalid_input'))

    def _get_weighted_choice(self, stats, category):
        if category not in stats:
            stats[category] = {}
        
        items_list = self.items
        weights = []
        
        for item in items_list:
            key = item['word']
            if key not in stats[category]:
                stats[category][key] = {"correct": 0, "incorrect": 0}
            
            data = stats[category][key]
            weight = 1 + (data['incorrect'] * 2) - (data['correct'] * 0.5)
            weights.append(max(0.1, weight))
            
        return random.choices(items_list, weights=weights, k=1)[0]

    def _update_stats(self, stats, category, key, is_correct):
        if is_correct:
            stats['total_score'] += 1
            stats[category][key]['correct'] += 1
        else:
            stats['total_score'] = max(0, stats['total_score'] - 1)
            stats[category][key]['incorrect'] += 1