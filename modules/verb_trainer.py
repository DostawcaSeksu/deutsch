import random
import re
from utils.file_handler import load_json
from utils.ui import clear_screen
import config

class VerbTrainer:
    def __init__(self, loc):
        self.loc = loc
        self.regular_verbs = load_json(config.REGULAR_VERBS_FILE)
        self.irregular_verbs = load_json(config.IRREGULAR_VERBS_FILE)
        self.pronoun_rules = load_json(config.PRONOUN_RULES_FILE)
        
        if not all([self.regular_verbs, self.irregular_verbs, self.pronoun_rules]):
            raise FileNotFoundError("Could not load one or more data files for the verb trainer.")

        self._prepare_data()

    def _prepare_data(self):
        """Pre-processes loaded data for easier use."""
        self.pronoun_groups = {rule['group']: rule['ending'] for rule in self.pronoun_rules}
        
        self.group_to_pronouns_set = {group: set() for group in self.pronoun_groups}
        for rule in self.pronoun_rules:
            base_pronoun = re.sub(r' \(.*\)', '', rule['pronoun'])
            self.group_to_pronouns_set[rule['group']].add(base_pronoun)

    def run(self, stats):
        """Main entry point for the verb trainer module."""
        while True:
            clear_screen()
            print(self.loc.get('choose_verb_mode'))
            print(self.loc.get('verb_mode_1'))
            print(self.loc.get('verb_mode_2'))
            choice = input(self.loc.get('enter_number'))
            
            if choice == '1':
                difficulty = self._choose_difficulty()
                self._run_mode_1(stats, difficulty)
                break
            elif choice == '2':
                difficulty = self._choose_difficulty()
                self._run_mode_2(stats, difficulty)
                break
            else:
                print(self.loc.get('invalid_input'))
                input(self.loc.get('press_enter'))

    def _choose_difficulty(self):
        """Menu for selecting difficulty."""
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
    
    def _run_mode_1(self, stats, difficulty):
        """Mode 1: Guess the ending."""
        clear_screen()
        print(self.loc.get('mode_title', mode=1, title=self.loc.get('mode_1_title'), difficulty=difficulty.upper()))
        print(self.loc.get('exit_to_menu_prompt'))

        while True:
            target_ending = self._get_weighted_choice(stats, 'endings')
            possible_rules = [r for r in self.pronoun_rules if r['ending'] == target_ending]
            chosen_rule = random.choice(possible_rules)
            pronoun, stat_group = chosen_rule['pronoun'], chosen_rule['group']
            
            use_irregular = difficulty in ['medium', 'hard'] and random.choice([True, False])
            if use_irregular and chosen_rule['pronoun'] in ['du', 'er', 'sie (она)', 'es']:
                verb_data = random.choice(self.irregular_verbs)
                verb_stem = verb_data['change'].get(stat_group.split(' ')[0], verb_data['stem'])
            else:
                verb_stem = random.choice(self.regular_verbs)[:-2]

            pronoun_display = chosen_rule['pronoun']
            if 'key' in chosen_rule:
                pronoun_display += f" {self.loc.get(chosen_rule['key'])}"

            print(self.loc.get('current_score', score=stats['total_score']))
            print(self.loc.get('question_ending', pronoun=pronoun_display, stem=verb_stem))

            
            
            if difficulty in ['easy', 'medium']:
                options = list(self.pronoun_groups.values())
                random.shuffle(options)
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                
                user_choice = input(f"\n{self.loc.get('your_choice', options='1-4')} ").lower()
                if user_choice == 'm': break

                try:
                    user_answer = options[int(user_choice) - 1]
                except (ValueError, IndexError):
                    print(f"\n⚠️ {self.loc.get('invalid_input')}\n")
                    continue
            else: # hard
                user_answer = input(self.loc.get('enter_ending_prompt')).strip().lower()
                if user_answer == 'm': break
                if not user_answer.startswith('-'):
                    user_answer = '-' + user_answer
            
            if user_answer == target_ending:
                print(self.loc.get('correct'))
                self._update_stats(stats, 'endings', target_ending, True)
            else:
                print(self.loc.get('incorrect', answer=target_ending))
                print(self.loc.get('incorrect_example', pronoun=pronoun, stem=verb_stem, ending=target_ending.replace('-', '')))
                self._update_stats(stats, 'endings', target_ending, False)
            
            print("-" * 20)

    def _run_mode_2(self, stats, difficulty):
        """Mode 2: Guess the pronoun."""
        clear_screen()
        print(self.loc.get('mode_title', mode=2, title=self.loc.get('mode_2_title'), difficulty=difficulty.upper()))
        print(self.loc.get('exit_to_menu_prompt'))
        
        while True:
            target_group = self._get_weighted_choice(stats, 'pronoun_groups')
            correct_ending = self.pronoun_groups[target_group]
            
            verb_stem = ''
            use_irregular = difficulty in ['medium', 'hard'] and random.choice([True, False])
            if use_irregular and target_group in ['du', 'er / sie / es / ihr']:
                verb_data = random.choice(self.irregular_verbs)
                # Find the irregular stem for du or er/sie/es
                base_pronoun_for_change = target_group.split(' ')[0]
                verb_stem = verb_data['change'].get(base_pronoun_for_change, verb_data['stem'])
            else:
                verb_stem = random.choice(self.regular_verbs)[:-2]
                
            conjugated_verb = verb_stem + correct_ending.replace('-', '')

            print(self.loc.get('current_score', score=stats['total_score']))
            print(self.loc.get('question_pronoun', verb=conjugated_verb))

            is_correct = False
            if difficulty in ['easy', 'medium']:
                options = list(self.pronoun_groups.keys())
                random.shuffle(options)
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                
                user_choice = input(f"\n{self.loc.get('your_choice', options='1-4')} ").lower()
                if user_choice == 'm': break

                try:
                    user_answer_group = options[int(user_choice) - 1]
                    if user_answer_group == target_group:
                        is_correct = True
                except (ValueError, IndexError):
                    print(f"\n⚠️ {self.loc.get('invalid_input')}\n")
                    continue
            else: # hard
                user_input = input(self.loc.get('enter_pronouns_prompt'))
                if user_input.lower() == 'm': break
                
                user_pronouns_set = set(user_input.split())
                correct_pronouns_set = self.group_to_pronouns_set[target_group]
                
                if user_pronouns_set == correct_pronouns_set:
                    is_correct = True

            if is_correct:
                print(self.loc.get('correct'))
                self._update_stats(stats, 'pronoun_groups', target_group, True)
            else:
                print(self.loc.get('incorrect', answer=target_group))
                if difficulty == 'hard':
                    correct_string = " ".join(sorted(list(self.group_to_pronouns_set[target_group])))
                    print(self.loc.get('incorrect_hard_pronoun', answer=correct_string))
                self._update_stats(stats, 'pronoun_groups', target_group, False)
            
            print("-" * 20)

    def _update_stats(self, stats, category, key, is_correct):
        if is_correct:
            stats['total_score'] += 1
            stats[category][key]['correct'] += 1
        else:
            stats['total_score'] = max(0, stats['total_score'] - 1) # Prevents negative score
            stats[category][key]['incorrect'] += 1