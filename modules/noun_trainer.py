import random
from utils.file_handler import load_json
from utils.ui import clear_screen
import config

class NounTrainer:
    def __init__(self, loc):
        self.loc = loc
        self.nouns = load_json(config.NOUNS_FILE)
        
        if not self.nouns:
            raise FileNotFoundError("Could not load nouns data file.")

    def run(self, stats):
        """Main entry point for the noun trainer module."""
        while True:
            clear_screen()
            print(self.loc.get('choose_noun_mode'))
            print(self.loc.get('noun_mode_1'))
            print(self.loc.get('noun_mode_2'))
            choice = input(self.loc.get('enter_number'))
            
            if choice == '1':
                self._run_guess_article(stats)
                break
            elif choice == '2':
                self._run_singular_plural(stats)
                break
            else:
                print(self.loc.get('invalid_input'))
                input(self.loc.get('press_enter'))

    def _run_guess_article(self, stats):
        """Mode: Guess the article for a noun."""
        difficulty = self._choose_difficulty()
        clear_screen()
        print(self.loc.get('mode_title', mode=3, title=self.loc.get('mode_3_title'), difficulty=difficulty.upper()))
        print(self.loc.get('exit_to_menu_prompt'))

        while True:
            target_article = self._get_weighted_choice(stats, 'articles')
            possible_nouns = [n for n in self.nouns if n['gender'] == target_article]
            chosen_noun = random.choice(possible_nouns)
            word = chosen_noun['singular']
            correct_answer = chosen_noun['gender']
            
            print(self.loc.get('current_score', score=stats['total_score']))
            print(self.loc.get('question_article', word=word))

            user_answer = ""
            if difficulty == 'easy':
                options = ['der', 'die', 'das']
                random.shuffle(options)
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                user_choice = input(f"\n{self.loc.get('your_choice', options='1-3')} ").lower()
                if user_choice == 'm': break
                try:
                    user_answer = options[int(user_choice) - 1]
                except (ValueError, IndexError):
                    print(f"\n⚠️ {self.loc.get('invalid_input')}\n")
                    continue
            elif difficulty == 'medium':
                hint = correct_answer[0] + "_" * (len(correct_answer) - 1)
                user_answer = input(f"{self.loc.get('enter_article_prompt')} ({hint}): ").strip().lower()
                if user_answer == 'm': break
            else: # hard
                user_answer = input(self.loc.get('enter_article_prompt')).strip().lower()
                if user_answer == 'm': break

            if user_answer == correct_answer:
                print(self.loc.get('correct'))
                self._update_stats(stats, 'articles', correct_answer, True)
            else:
                print(self.loc.get('incorrect', answer=correct_answer))
                self._update_stats(stats, 'articles', correct_answer, False)
            
            print("-" * 20)

    def _run_singular_plural(self, stats):
        """Mode: Convert between singular and plural forms."""
        difficulty = self._choose_difficulty()
        clear_screen()
        print(self.loc.get('mode_title', mode=4, title=self.loc.get('mode_4_title'), difficulty=difficulty.upper()))
        print(self.loc.get('exit_to_menu_prompt'))
        
        while True:
            chosen_noun = random.choice(self.nouns)
            to_plural = random.choice([True, False])

            if to_plural:
                question_word = f"{chosen_noun['gender']} {chosen_noun['singular']}"
                correct_answer_full = f"die {chosen_noun['plural']}"
                correct_answer_medium = chosen_noun['plural']
                print(self.loc.get('question_plural', word=question_word))
            else:
                question_word = f"die {chosen_noun['plural']}"
                correct_answer_full = f"{chosen_noun['gender']} {chosen_noun['singular']}"
                correct_answer_medium = chosen_noun['singular']
                print(self.loc.get('question_singular', word=question_word))

            print(self.loc.get('current_score', score=stats['total_score']))

            user_answer = ""
            is_correct = False

            if difficulty == 'easy':
                options = self._generate_plural_options(correct_answer_full, chosen_noun, to_plural)
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                user_choice = input(f"\n{self.loc.get('your_choice', options='1-3')} ").lower()
                if user_choice == 'm': break
                try:
                    user_answer = options[int(user_choice) - 1]
                    if user_answer == correct_answer_full:
                        is_correct = True
                except (ValueError, IndexError):
                    print(f"\n⚠️ {self.loc.get('invalid_input')}\n")
                    continue
            
            elif difficulty == 'medium':
                user_answer = input(self.loc.get('enter_answer_prompt')).strip().lower()
                if user_answer == 'm': break
                if user_answer == correct_answer_medium:
                    is_correct = True
            
            else: # hard
                user_answer = input(self.loc.get('enter_answer_prompt')).strip().lower()
                if user_answer == 'm': break
                if user_answer == correct_answer_full:
                    is_correct = True
            
            if is_correct:
                print(self.loc.get('correct'))
                self._update_stats(stats, 'singular_plural', 'main', True)
            else:
                print(self.loc.get('incorrect', answer=correct_answer_full))
                self._update_stats(stats, 'singular_plural', 'main', False)
            
            print("-" * 20)

    def _generate_plural_options(self, correct_option, noun, to_plural):
        options = {correct_option}
        base_word = noun['singular']
        
        if to_plural:
            wrong_endings = ['en', 's', 'e', 'er', '']
            while len(options) < 3:
                ending = random.choice(wrong_endings)
                options.add(f"die {base_word}{ending}")
        else:
            wrong_articles = ['der', 'die', 'das']
            while len(options) < 3:
                article = random.choice(wrong_articles)
                options.add(f"{article} {base_word}")
        
        shuffled_options = list(options)
        random.shuffle(shuffled_options)
        return shuffled_options

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
        items = list(stats[category].keys())
        weights = [stats[category][item]['incorrect'] + 1 for item in items]
        return random.choices(items, weights=weights, k=1)[0]
    
    def _update_stats(self, stats, category, key, is_correct):
        if is_correct:
            stats['total_score'] += 1
            stats[category][key]['correct'] += 1
        else:
            stats['total_score'] = max(0, stats['total_score'] - 1)
            stats[category][key]['incorrect'] += 1