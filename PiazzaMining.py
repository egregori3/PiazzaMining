import sys
import getopt
import json
from piazza_api import Piazza


class PiazzaInterface:

    def __init__(self, piazza_credentials, filters, debug=False):
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


def main(argv):

    parameters = {
                    'verbose': False,
                    'frames': "ExampleQuestions.json",
                    'log': "results"
                 }

    print(__doc__)
    try:
        opts, args = getopt.getopt(argv, "vf:l:")
    except getopt.GetoptError:
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-v"):  # -v verbose
            parameters['verbose'] = True
        elif opt in ("-f"):  # -f <json containing dictionary frames>
            parameters['frames'] = arg
        elif opt in ("-l"):  # -l <path/filename to log file>
            parameters['log'] = arg

    return AgentAutograder(parameters)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))