"""
Process change log
"""


class StatisticsError(Exception):
    def __init__(self, message):
        self.message = message


class Statistics:
    """Filter change log"""

    def __init__(self, data, instructor_ids):
        """ """
        self.data = data
        self.instructor_ids = instructor_ids
        # create,update,followup,s_answer,s_answer_update,i_answer,i_answer_update
        self.stats = {
                        'create': {'i':0, 's':0},
                        'update': {'i':0, 's':0},
                        'followup': {'i':0, 's':0},
                        's_answer': {'i':0, 's':0},
                        's_answer_update': {'i':0, 's':0},
                        'i_answer': {'i':0, 's':0},
                        'i_answer_update': {'i':0, 's':0},
                        'feedback': {'i':0, 's':0},
                        'dupe': {'i':0, 's':0}
                     }

    def _get_change_log(self, data):
        """
            if data is a list, return empty list
            if data is a dictionary, return 'change_log'
        """
        try:
            _change_log = data['change_log']
        except:
            return list()
        return _change_log

    def _process_data(self):
        """
            if data is a list, iterate through list of dicts to find 'change_log'
            if data is a dictionary, look for 'change_log' directly
        """
        _change_log = self._get_change_log(self.data)
        if _change_log:
            self._get_statistics_from_change_log(_change_log)
        else:
            for _entry in self.data:
                _change_log = self._get_change_log(_entry)
                if _change_log:
                    self._get_statistics_from_change_log(_change_log)

    def _get_statistics_from_change_log(self, change_log):
        """
            "anon": "no",
            "uid": "jl1k6ffwrj24ki",
            "data": "jl9ymzv3ssx3td",
            "type": "create", "update", "followup", "s_answer", "s_answer_update", "i_answer", "i_answer_update"
            "when": "2018-08-25T21:52:02Z"
        """
        for _entry in change_log:
            if 'type' in _entry and 'uid' in _entry:
                if _entry['uid'] in self.instructor_ids:
                    self.stats[_entry['type']]['i'] += 1
                else:
                    self.stats[_entry['type']]['s'] += 1

    def print_statistics(self):
        """ """
        self._process_data()
        for k in self.stats.keys():
            print(str(k)+" : "+str(self.stats[k]))
