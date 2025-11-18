import random
from utils.file_handler import load_json
from utils.ui import clear_screen
import config

class CaseTrainer:
    def __init__(self, loc):
        self.loc = loc
        self.articles = load_json(config.ARTICLES_FILE)
        self.pronouns = load_json(config.PERSONAL_PRONOUNS_FILE)
        self.sentences = load_json(config.CASE_SENTENCES_FILE)
        
        if not all([self.articles, self.pronouns, self.sentences]):
            raise FileNotFoundError("Could not load one or more data files for the case trainer.")

    def run(self, stats):
        """Main entry point for the case trainer module."""
        while True:
            clear_screen()
            print(self.loc.get('choose_case_mode'))
            print(self.loc.get('case_mode_1'))
            print(self.loc.get('case_mode_2'))
            choice = input(self.loc.get('enter_number'))
            
            if choice == '1':
                self._run_article_declension(stats)
                break
            elif choice == '2':
                self._run_pronoun_declension(stats)
                break
            else:
                print(self.loc.get('invalid_input'))
                input(self.loc.get('press_enter'))
    
    def _run_article_declension(self, stats):
        difficulty = self._choose_difficulty()
        clear_screen()
        print(self.loc.get('mode_title', mode=5, title=self.loc.get('mode_5_title'), difficulty=difficulty.upper()))
        print(self.loc.get('exit_to_menu_prompt'))

        while True:
            task = random.choice(self.sentences['articles'])
            sentence_template = task['sentence']
            gender = task['gender']
            case = task['case']
            noun = task['noun']
            correct_answer = self.articles[gender][case]['bestimmter']
            
            print(self.loc.get('current_score', score=stats['total_score']))
            print(self.loc.get('question_fill_blank'))
            
            print(f"  {sentence_template.format(blank='___')}")
            if 'translation' in task and self.loc.language in task['translation']:
                translation_text = task['translation'][self.loc.language]
                print(f"  {self.loc.get('translation_hint', text=translation_text)}")
            
            gender_article = self.articles[gender]['nominativ']['bestimmter']
            print(self.loc.get('prompt_details_article', case=case.capitalize(), gender_article=gender_article, noun=noun))

            user_answer = ""
            if difficulty == 'easy':
                options = list({
                    correct_answer, 
                    self.articles[gender]['nominativ']['bestimmter'],
                    self.articles[gender]['dativ']['bestimmter'] if case != 'dativ' else self.articles[gender]['akkusativ']['bestimmter']
                })
                random.shuffle(options)
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                user_choice = input(f"\n{self.loc.get('your_choice', options=f'1-{len(options)}')} ").lower()
                if user_choice == 'm': break
                try:
                    user_answer = options[int(user_choice) - 1]
                except (ValueError, IndexError):
                    print(f"\n⚠️ {self.loc.get('invalid_input')}\n")
                    continue
            elif difficulty == 'medium':
                 hint = correct_answer[0] + "_" * (len(correct_answer) - 1)
                 user_answer = input(f"\n{self.loc.get('enter_answer_prompt')} ({hint}): ").strip().lower()
                 if user_answer == 'm': break
            else: # hard
                user_answer = input(f"\n{self.loc.get('enter_answer_prompt')}").strip().lower()
                if user_answer == 'm': break

            stat_key = f"{gender}-{case}"
            if user_answer == correct_answer:
                print(self.loc.get('correct'))
                self._update_stats(stats, 'article_declension', stat_key, True)
            else:
                print(self.loc.get('incorrect', answer=correct_answer))
                self._update_stats(stats, 'article_declension', stat_key, False)
            
            print("-" * 20)

    def _run_pronoun_declension(self, stats):
        difficulty = self._choose_difficulty()
        clear_screen()
        print(self.loc.get('mode_title', mode=6, title=self.loc.get('mode_6_title'), difficulty=difficulty.upper()))
        print(self.loc.get('exit_to_menu_prompt'))

        while True:
            task = random.choice(self.sentences['pronouns'])
            sentence_template = task['sentence']
            pronoun_nom = task['pronoun_nom']
            case = task['case']
            correct_answer = self.pronouns[case][pronoun_nom]

            print(self.loc.get('current_score', score=stats['total_score']))
            print(self.loc.get('question_fill_blank'))

            pronoun_display = pronoun_nom
            if 'key' in task:
                 pronoun_display += f" {self.loc.get(task['key'])}"
            print(f"  {sentence_template.format(blank=f'___ ({pronoun_display})')}")
            if 'translation' in task and self.loc.language in task['translation']:
                translation_text = task['translation'][self.loc.language]
                print(f"  {self.loc.get('translation_hint', text=translation_text)}")

            user_answer = ""
            if difficulty == 'easy':
                other_case = 'dativ' if case == 'akkusativ' else 'akkusativ'
                options = [correct_answer, self.pronouns[other_case][pronoun_nom]]
                random.shuffle(options)
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                user_choice = input(f"\n{self.loc.get('your_choice', options='1-2')} ").lower()
                if user_choice == 'm': break
                try:
                    user_answer = options[int(user_choice) - 1]
                except (ValueError, IndexError):
                    user_answer = ""
                    print(f"\n⚠️ {self.loc.get('invalid_input')}\n")
                    continue
            elif difficulty == 'medium':
                hint = correct_answer[0] + "_" * (len(correct_answer) - 1)
                user_answer = input(f"\n{self.loc.get('enter_answer_prompt')} ({hint}): ").strip().lower()
                if user_answer == 'm': break
            else: # hard
                user_answer = input(f"\n{self.loc.get('enter_answer_prompt')}").strip().lower()
                if user_answer == 'm': break
            
            stat_key = f"{pronoun_nom}-{case}"
            if user_answer == correct_answer:
                print(self.loc.get('correct'))
                self._update_stats(stats, 'pronoun_declension', stat_key, True)
            else:
                print(self.loc.get('incorrect', answer=correct_answer))
                self._update_stats(stats, 'pronoun_declension', stat_key, False)

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

    def _update_stats(self, stats, category, key, is_correct):
        if key not in stats[category]:
             stats[category][key] = {"correct": 0, "incorrect": 0}

        if is_correct:
            stats['total_score'] += 2
            stats[category][key]['correct'] += 1
        else:
            stats['total_score'] = max(0, stats['total_score'] - 1)
            stats[category][key]['incorrect'] += 1