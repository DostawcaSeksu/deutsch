import random
import os
from utils.file_handler import load_json
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
            self._clear_screen()
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
        self._clear_screen()
        print(self.loc.get('mode_title', mode=3, title=self.loc.get('mode_3_title'), difficulty=difficulty.upper()))
        print(self.loc.get('exit_to_menu_prompt'))

        while True:
            # Weighted choice based on incorrect answers for articles
            target_article = self._get_weighted_choice(stats, 'articles')
            possible_nouns = [n for n in self.nouns if n['gender'] == target_article]
            chosen_noun = random.choice(possible_nouns)
            word = chosen_noun['singular']
            correct_answer = chosen_noun['gender']
            
            print(self.loc.get('current_score', score=stats['total_score']))
            print(self.loc.get('question_article', word=word))

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
        self._clear_screen()
        print(self.loc.get('mode_title', mode=4, title=self.loc.get('mode_4_title'), difficulty="HARD"))
        print(self.loc.get('exit_to_menu_prompt'))
        
        while True:
            chosen_noun = random.choice(self.nouns)
            
            # 50/50 chance to ask for plural or singular
            if random.choice([True, False]):
                # Ask for plural
                question_word = f"{chosen_noun['gender']} {chosen_noun['singular']}"
                # Plural nouns almost always use 'die' (with few exceptions)
                correct_answer = f"die {chosen_noun['plural']}"
                print(self.loc.get('question_plural', word=question_word))
            else:
                # Ask for singular
                question_word = f"die {chosen_noun['plural']}"
                correct_answer = f"{chosen_noun['gender']} {chosen_noun['singular']}"
                print(self.loc.get('question_singular', word=question_word))

            print(self.loc.get('current_score', score=stats['total_score']))
            user_answer = input(self.loc.get('enter_answer_prompt')).strip().lower()
            if user_answer == 'm': break

            if user_answer == correct_answer:
                print(self.loc.get('correct'))
                self._update_stats(stats, 'singular_plural', 'main', True)
            else:
                print(self.loc.get('incorrect', answer=correct_answer))
                self._update_stats(stats, 'singular_plural', 'main', False)
            
            print("-" * 20)


    def _choose_difficulty(self):
        """Menu for selecting difficulty (only easy/hard for this module)."""
        while True:
            print(self.loc.get('choose_difficulty'))
            print("1. " + self.loc.get('difficulty_easy').split('(')[1].replace(')', '')) # Simplified prompt
            print("2. " + self.loc.get('difficulty_hard').split('(')[1].replace(')', ''))
            choice = input(self.loc.get('your_choice', options="1-2") + " ")
            if choice == '1': return 'easy'
            if choice == '2': return 'hard'
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

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')