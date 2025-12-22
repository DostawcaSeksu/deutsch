import time

class StatsManager:
    def __init__(self, stats_dict):
        self.stats = stats_dict

    def get_due_items(self, category, all_items_keys):
        """
        Возвращает список элементов, которые пора повторять.
        Если SRS данных нет, возвращает все элементы.
        """
        if category not in self.stats:
            return all_items_keys

        current_time = time.time()
        due_items = []
        
        for key in all_items_keys:
            item_data = self.stats[category].get(key, {})
            next_review = item_data.get('next_review', 0)
            
            if current_time >= next_review:
                due_items.append(key)
        
        return due_items if due_items else all_items_keys

    def update_srs(self, category, key, is_correct):
        """
        Простой алгоритм интервального повторения (похож на Leitner box).
        """
        if category not in self.stats:
            self.stats[category] = {}
        if key not in self.stats[category]:
            self.stats[category][key] = {"correct": 0, "incorrect": 0, "level": 0, "next_review": 0}

        data = self.stats[category][key]
        
        if is_correct:
            data['correct'] += 1
            data['level'] = data.get('level', 0) + 1
        else:
            data['incorrect'] += 1
            data['level'] = 1 

        intervals = [0, 60, 600, 86400, 3*86400, 7*86400, 14*86400]
        
        level = min(data['level'], len(intervals) - 1)
        wait_time = intervals[level]
        
        data['next_review'] = time.time() + wait_time
        
        self.stats[category][key] = data