"""
Process change log
"""


class StatisticsError(Exception):
    def __init__(self, message):
        self.message = message


class Statistics:
    """Filter change log"""

    def __init__(self, post, instructor_ids):
        self.post = post
        self.instructor_ids = instructor_ids
        if 'change_log' in self.post:
            self._get_statistics_from_change_log()

    def _get_statistics_from_change_log(self):
        for _entry in change_log:
            print(_entry)
            if _entry['uid'] in instructor_ids:
                print("instructor")
            else:
                print("student")
