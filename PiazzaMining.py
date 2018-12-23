"""
    -p piazza_credentials: piazza_credentials.json
    -t thread_string:
    -f filter_string:
"""
import sys
import getopt
import json
from piazza_api import Piazza


class PiazzaInterface:

    def __init__(self, piazza_credentials):
        _piazza = Piazza()
        _piazza.user_login(email=email, password=password)
        self._myclass = _piazza.network(network)
        self._debug = debug
        self._question_field = question_field

    def getPosts(self):
        # Get list of cid's from feed
        _feed = self._myclass.get_feed(limit=999999, offset=0)
        _ids = [_post['id'] for _post in _feed["feed"]]

        if self._debug:
            with open('feed.json', 'w') as _outfile:
                json.dump(_feed, _outfile)

        _posts = []
        for _id in _ids:
            _post = self._myclass.get_post(_id)
            _posts.append(_post)

        if self._debug:
            with open('posts.json', 'w') as _outfile:
                json.dump(_posts, _outfile)

        return _posts

    def getID(self, postData):
        return postData['id']

    def getQuestion(self, postData):
        return postData[self._question_field]

    def getInstructorResponse(self, postData):
        return postData['instructor_answer']

    def _postData(self, _id, domains, subject, content, instructor_answer):
        return {'id':_id, 
                'domains':domains, 
                'subject':subject, 
                'content':content, 
                'instructor_answer':instructor_answer}

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


def _parse_thread_string():

def main(argv):

    _parameters = {
                    'piazza_credentials': "piazza_credentials.json",
                    'thread_string': ""
                    'filter_string': ""
                  }

    print(__doc__)
    try:
        _opts, _args = getopt.getopt(argv, "p:t:f:")
    except getopt.GetoptError:
        sys.exit(1)
    for _opt, _arg in _opts:
        if _opt in ("-p"):
            _parameters['piazza_credentials'] = _arg
        elif _opt in ("-t"):
            _parameters['thread_string'] = _arg
        elif _opt in ("-f"):
            _parameters['filter_string'] = _arg

    # Load config file
    try:
        with open(_parameters['piazza_credentials'], encoding='utf-8') as _json_data:
                _piazza_credentials = json.load(_json_data)
    except FileNotFoundError as _err:
        print("Failure opening or reading piazza credentials filename: " + str(_err))
        return -1

    # Open connection to Piazza
    try:
        _piazza_interface = PiazzaInterface()
    except Exception as _err:
        print("Failure connecting to Piazza: " + str(_err))
        return -1




 _threads = [_piazza_interface.get_post_by_subject(thread) for thread in _list_of_thread_names]

    return Piazza(parameters)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))