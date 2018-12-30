"""
Backup or Mine Piazza for data.

Use the -b option to backup a Piazza network.
Use the -m option to mine the backup file for data.
    -b backup Piazza network to file
        - e = Piazza user email
        - p = Piazza user password
        - n = Piazza network

    -m mine data from Pizza backup file
        - t mine a specific thread
"""
import sys
import getopt
import json
from piazza_api import Piazza


class Error(Exception):
   """Base class for other exceptions"""
   pass

class ThreadNotFoundError(Error):
    """Thread not found"""
    pass

class InstructorIDNotFoundError(Error):
    """Instructor ID's not found"""
    pass


class PiazzaInterface:

    def __init__(self, piazza_credentials):
        """Connect to Piazza"""
        _piazza = Piazza()
        _piazza.user_login( email=piazza_credentials['piazza_email'], 
                            password=piazza_credentials['piazza_password'])
        self._myclass = _piazza.network(piazza_credentials['piazza_network'])
        # Get list of cid's from feed
        self._feed = self._myclass.get_feed(limit=999999, offset=0)
        self._instructor_ids = [user['id'] for user in self._myclass.get_all_users() if user['admin'] == True]

    def get_all_posts(self):
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


def error_message(message):
    """Error message"""
    print("!ERROR! - "+message)

def get_instructor_ids(piazza):
    """Get list of instructor id's"""
    for _post in piazza:
        if 'mining_instructors' in _post:
            return _post['mining_instructors']
    raise InstructorIDNotFoundError()

def get_thread_by_subject(piazza,thread_subject):
    """Look for thread with specified subject"""
    for _post in piazza:
        if 'history' in _post:
            _subject = _post['history'][0]['subject']
            if thread_subject == _subject:
                return _post
    raise ThreadNotFoundError()

def process_change_log(change_log,instructor_ids):
    """Get most recent change log in each post"""
    for _entry in change_log:
        print(_entry)
        if _entry['uid'] in instructor_ids:
            print("instructor")
        else:
            print("student")


def main(argv):
    """
        -b backup Piazza network to file
        - e = Piazza user email
        - p = Piazza user password
        - n = Piazza network

        -m mine data from Pizza backup file
        - t mine a specific thread
    """
    _parameters = dict()
    print(__doc__)
    try:
        _opts, _args = getopt.getopt(argv, "b:m:e:p:n:t:")
    except getopt.GetoptError:
        sys.exit(1)
    for _opt, _arg in _opts:
        if _opt in ("-b"):
            _parameters['option_b'] = _arg
        elif _opt in ("-m"):
            _parameters['option_m'] = _arg
        elif _opt in ("-e"):
            _parameters['option_e'] = _arg
        elif _opt in ("-p"):
            _parameters['option_p'] = _arg
        elif _opt in ("-n"):
            _parameters['option_n'] = _arg
        elif _opt in ("-t"):
            _parameters['option_t'] = _arg

    if 'option_b' in _parameters:
        _filename = _parameters['option_b']
        _piazza_credentials = dict()
        try:
            _piazza_credentials['piazza_email'] = _parameters['option_e']
            _piazza_credentials['piazza_password'] = _parameters['option_p']
            _piazza_credentials['piazza_network']  = _parameters['option_n']
        except Exception as _err:
            error_message("Invalid Piazza credentials: " + str(_err))
            return -1

        print("Connecting to Piazza")
        try:
            _piazza_interface = PiazzaInterface(_piazza_credentials)
        except Exception as _err:
            error_message("Failure connecting to Piazza: " + str(_err))
            return -1

        print("Getting posts")
        try:
            _posts = _piazza_interface.get_all_posts()
        except Exception as _err:
            error_message("Failure getting all posts: " + str(_err))
            return -1

        print("Writing posts to file: "+_filename)
        try:
            with open(_filename, 'w') as outfile:
                json.dump(_posts, outfile)
        except Exception as _err:
            error_message("Failure writing to file: " + str(_err))
            return -1
        print("Done")
        return 0

    # option b not set
    try:
        _filename = _parameters['option_m']
    except:
        error_message("option -b or -m MUST be set")
        return -1

    print("Mining: "+_filename)
    try:
        with open(_filename, encoding='utf-8') as _json_data:
            _piazza = json.load(_json_data)
    except Exception as _err:
        error_message("Failure opening or reading piazza file: " + str(_err))
        return -1

    print("Piazza file loaded")
    if 'option_t' in _parameters:
        _thread_subject = _parameters['option_t']
        print("Looking for thread: "+_thread_subject)
        try:
            _post = get_thread_by_subject(_piazza,_thread_subject)
        except ThreadNotFoundError:
            print("Thread not found")
            return -1
        print("Thread found")
        _instructor_ids = get_instructor_ids(_piazza)
        if 'change_log' in _post:
            process_change_log(_post['change_log'], _instructor_ids)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))