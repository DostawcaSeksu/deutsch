import random
from utils.file_handler import load_json
from utils.ui import clear_screen
import config

class ModalVerbTrainer:
    def __init__(self, loc):
        self.loc = loc
        self.modal_verbs = load_json(config.MODAL_VERBS_FILE)
        self.pronoun_rules = load_json(config.PRONOUN_RULES_FILE)
        
        if not self.modal_verbs or not self.pronoun_rules:
            raise FileNotFoundError("Could not load modal verbs or pronoun rules data.")

    def run(self, stats):
        """Main entry point for the modal verb trainer module."""
        difficulty = self._choose_difficulty()
        self._run_conjugation(stats, difficulty)

    def _get_correct_form(self, verb_data, pronoun_rule):
        """Determines the correct conjugated form of a modal verb."""
        pronoun = pronoun_rule['pronoun']
        key = pronoun_rule.get('key')
        
        if pronoun in ['ich', 'er', 'es'] or key == 'she':
            return verb_data['forms']['ich/er/sie/es']
        if pronoun == 'du':
            return verb_data['forms']['du']
        if pronoun == 'ihr':
            return verb_data['forms']['ihr']
        # Default for wir, sie (they), Sie (formal)
        return verb_data['forms']['wir/sie_plural/Sie']

    def _run_conjugation(self, stats, difficulty):
        clear_screen()
        print(self.loc.get('mode_title', mode=7, title=self.loc.get('mode_7_title'), difficulty=difficulty.upper()))
        print(self.loc.get('exit_to_menu_prompt'))

        while True:
            verb_data = random.choice(self.modal_verbs)
            pronoun_rule = random.choice(self.pronoun_rules)
            
            infinitive = verb_data['infinitive']
            correct_answer = self._get_correct_form(verb_data, pronoun_rule)

            pronoun_display = pronoun_rule['pronoun']
            if 'key' in pronoun_rule:
                pronoun_display += f" {self.loc.get(pronoun_rule['key'])}"
            
            print(self.loc.get('current_score', score=stats['total_score']))
            print(self.loc.get('question_modal', pronoun=pronoun_display, infinitive=infinitive))
            
            verb_translation = verb_data['translation'][self.loc.language]
            print(f"  ({self.loc.get('translation_hint', text=verb_translation)})")

            user_answer = ""
            if difficulty == 'easy':
                options = {correct_answer, infinitive}
                # Add one more incorrect option
                all_forms = list(verb_data['forms'].values())
                random.shuffle(all_forms)
                for form in all_forms:
                    if form not in options:
                        options.add(form)
                        break
                
                shuffled_options = list(options)
                random.shuffle(shuffled_options)

                for i, option in enumerate(shuffled_options):
                    print(f"{i+1}. {option}")
                
                user_choice = input(f"\n{self.loc.get('your_choice', options=f'1-{len(shuffled_options)}')} ").lower()
                if user_choice == 'm': break
                try:
                    user_answer = shuffled_options[int(user_choice) - 1]
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

            stat_key = f"{infinitive}-{pronoun_display.split(' ')[0]}"
            if user_answer == correct_answer:
                print(self.loc.get('correct'))
                self._update_stats(stats, 'modal_verbs', stat_key, True)
            else:
                print(self.loc.get('incorrect', answer=correct_answer))
                self._update_stats(stats, 'modal_verbs', stat_key, False)
            
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
            stats['total_score'] += 1
            stats[category][key]['correct'] += 1
        else:
            stats['total_score'] = max(0, stats['total_score'] - 1)
            stats[category][key]['incorrect'] += 1