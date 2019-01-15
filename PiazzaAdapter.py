"""
Connect Piazza to application
"""
import sys
import json
from piazza_api import Piazza


class PiazzaError(Exception):
    def __init__(self, message):
        self.message = message


class PiazzaBackup:
    """
        Save Piazza network to json file
        File is a list of dictionaries.
        Each dictionary is a post.
        dict [-2] is feed
        dict [-1] is instructors
    """

    def __init__(self, filename, piazza_credentials):
        print("Connecting to Piazza")
        try:
            self._connect_to_piazza(piazza_credentials)
        except Exception as _err:
            raise PiazzaError("Failure connecting to Piazza: " + str(_err))
        print("Getting posts")
        try:
            _posts = self._get_all_posts()
        except Exception as _err:
            raise PiazzaError("Failure getting all posts: " + str(_err))

        self.posts = _posts
        print("Writing posts to file: "+filename)
        try:
            with open(filename, 'w') as outfile:
                json.dump(_posts, outfile)
        except Exception as _err:
            raise PiazzaError("Failure writing to file: " + str(_err))
        print("Done")

    def get_posts(self):
        return self.posts

    def _connect_to_piazza(self, piazza_credentials):
        """Connect to Piazza"""
        _piazza = Piazza()
        _piazza.user_login( email=piazza_credentials['piazza_email'], 
                            password=piazza_credentials['piazza_password'])
        self._myclass = _piazza.network(piazza_credentials['piazza_network'])
        # Get list of cid's from feed
        self._feed = self._myclass.get_feed(limit=999999, offset=0)
        self._instructor_ids = [user['id'] for user in self._myclass.get_all_users() if user['admin'] == True]

    def _get_all_posts(self):
        """Get all posts"""
        _ids = [_post['id'] for _post in self._feed['feed']]
        _posts = []
        for _id in _ids:
            print("-", end='')
            sys.stdout.flush()
            _post = self._myclass.get_post(_id)
            _posts.append(_post)
        _posts.append({'mining_feed':self._feed})
        _posts.append({'mining_instructors':self._instructor_ids})
        print()
        return _posts


class PiazzaMine:
    """Extract data from Piazza json file"""

    def __init__(self, filename):
        try:
            with open(filename, encoding='utf-8') as _json_data:
                self.piazza = json.load(_json_data)
        except Exception as _err:
            raise PiazzaError("Failure opening or reading piazza file: " + str(_err))
        self.instructor_ids = None
        for _post in self.piazza:
            if 'mining_instructors' in _post:
                self.instructor_ids = _post['mining_instructors']
        if not self.instructor_ids:
            raise PiazzaError("Instructor ID Not Found Error")

    def get_posts(self):
        return self.piazza

    def get_instructor_ids(self):
        """Get list of instructor id's"""
        return self.instructor_ids

    def get_thread_by_subject(self, thread_subject):
        """
            Walk through list looking for a specific dictionary based on subject.
            Returns dictionary if thread found.
        """
        for _post in self.piazza:
            if 'history' in _post:
                _subject = _post['history'][0]['subject']
                if thread_subject == _subject:
                    return _post
        raise PiazzaError("Thread Not Found Error")

