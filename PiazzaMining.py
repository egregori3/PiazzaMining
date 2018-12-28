"""
    -p piazza_credentials: piazza_credentials.json
    -t thread_string:
    -f filter_string:
"""
import sys
import getopt
import json
from piazza_api import Piazza


class PiazzaError(Exception):
    def __init__(self, message):
        self.message = message


class PiazzaInterface:

    def __init__(self, piazza_credentials):
        _piazza = Piazza()
        _piazza.user_login( email=piazza_credentials['piazza_email'], 
                            password=piazza_credentials['piazza_password'])
        self._myclass = _piazza.network(piazza_credentials['piazza_network'])
        # Get list of cid's from feed
        self._feed = self._myclass.get_feed(limit=999999, offset=0)['feed']
        self._instructor_ids = [user['id'] for user in self._myclass.get_all_users() if user['admin'] == True]

    def get_post_by_subject(self, subject):
        for _post in self._feed:
            if _post['subject'] == subject:
                return self._myclass.get_post(_post['id'])
        raise PiazzaError("Could not get post '{0}'".format(subject))

    def get_followups(self, thread):
        if thread:
            for followup in thread['children']:
                if followup['type'] != 'followup':
                    continue

                print(str(followup))

    def get_all_posts(self):
        _ids = [_post['id'] for _post in self._feed]
        _posts = []
        for _id in _ids:
            _post = self._myclass.get_post(_id)
            _posts.append(_post)
        return _posts

    def parsePost(self, post):
        _parsePost = {}
        if post['type'] == "question":
            _id = post['id']
            _domains = post['folders'] 
            _subject = post['history'][-1]['subject']
            _content = post['history'][-1]['content']
            _instructor_answer = ""
            for _child in post['children']:
                if _child['type'] == "i_answer":
                   _instructor_answer = _child['history'][-1]['content']
                break
            _parsePost = self._postData(_id, _domains, _subject, _content, _instructor_answer)
        return _parsePost


def _parse_thread_string(thread_string):
    _list_of_thread_names = thread_string.split(',')
    return _list_of_thread_names


def main(argv):

    _parameters = {
                    'piazza_credentials': "piazza_credentials.json",
                    'thread_string': "",
                    'filter_string': "",
                    'backup_file': ""
                  }

    print(__doc__)
    try:
        _opts, _args = getopt.getopt(argv, "p:t:f:b:")
    except getopt.GetoptError:
        sys.exit(1)
    for _opt, _arg in _opts:
        if _opt in ("-p"):
            _parameters['piazza_credentials'] = _arg
        elif _opt in ("-t"):
            _parameters['thread_string'] = _arg
        elif _opt in ("-f"):
            _parameters['filter_string'] = _arg
        elif _opt in ("-b"):
            _parameters['backup_file'] = _arg

    # Load config file
    try:
        with open(_parameters['piazza_credentials'], encoding='utf-8') as _json_data:
                _piazza_credentials = json.load(_json_data)
    except Exception as _err:
        print("Failure opening or reading piazza credentials filename: " + str(_err))
        return -1

    # Open connection to Piazza
    try:
        _piazza_interface = PiazzaInterface(_piazza_credentials)
    except Exception as _err:
        print("Failure connecting to Piazza: " + str(_err))
        return -1

    try:
        _list_of_thread_names = _parse_thread_string(_parameters['thread_string'])
    except Exception as _err:
        print("Failure parsing thread parameter: " + str(_err))
        return -1

    print("Getting threads: "+str(_list_of_thread_names))

    if _list_of_thread_names[0]:
        try:
            _posts = [_piazza_interface.get_post_by_subject(thread) for thread in _list_of_thread_names]
        except Exception as _err:
            print("Failure getting posts by thread: " + str(_err))
            return -1
    else:
        try:
            _posts = _piazza_interface.get_all_posts()
        except Exception as _err:
            print("Failure getting all posts: " + str(_err))
            return -1


    if _parameters['backup_file']:
        try:
            with open(_parameters['backup_file'], 'w') as outfile:
                json.dump(_posts, outfile)
        except Exception as _err:
            print("Failure writing to bckup JSON file: " + str(_err))
            return -1

#    _followup_threads = [_piazza_interface.get_followups(thread) for thread in _threads]

#    for _thread in _threads:
#        print(str(_thread))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))