"""
Backup or Mine Piazza for data.

Use the -b option to backup a Piazza network.
Use the -m option to mine the backup file for data.
    [-b <filename>] backup Piazza network to file
        [- e <Piazza user email>]
        [- p <Piazza user password>]
        [- n <Piazza network>]

    [-m <filename>] mine data from Pizza backup file
        [- t <subject>] mine a specific thread
        [- s] statistics
"""
import sys
import getopt
import json
from PiazzaAdapter import PiazzaBackup
from PiazzaAdapter import PiazzaMine
from PiazzaAdapter import PiazzaError
from Statistics import Statistics
from Statistics import StatisticsError


def error_message(message):
    """Error message"""
    print("!ERROR! - "+message)


def main(argv):
    """
        -b backup Piazza network to file
        - e = Piazza user email
        - p = Piazza user password
        - n = Piazza network

        -m mine data from Pizza backup file
        - t mine a specific thread
        - s statistics
    """
    _parameters = dict()
    print(__doc__)
    try:
        _opts, _args = getopt.getopt(argv, "b:m:e:p:n:t:s:")
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
        elif _opt in ("-s"):
            _parameters['option_s'] = True

#
# Option b - Save Piazza network to file
#
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

        try:
            PiazzaBackup(_filename, _piazza_credentials)
        except PiazzaError as _err:
            error_message(str(_err))
        return 0


    # option b not set
    try:
        _filename = _parameters['option_m']
    except:
        error_message("option -b or -m MUST be set")
        return -1

#
# option m - Mine a Piazza backup file
#
    print("Mining: "+_filename)
    try:
        _piazza_mine = PiazzaMine(_filename)
        _instructor_ids = _piazza_mine.get_instructor_ids()
    except PiazzaError as _err:
        print(str(_err))
        return -1
    print("Piazza file loaded")

#
# option t - Extract thread by subject
#
    if 'option_t' in _parameters:
        _thread_subject = _parameters['option_t']
        print("Looking for thread: "+_thread_subject)
        try:
            _post = _piazza_mine.get_thread_by_subject(_thread_subject)
        except PiazzaError as _err:
            print(str(_err))
            return -1
        print("Thread found")

#
# option s - Display statistics
#
    if 'option_s' in _parameters:
        print("Display statistics")
        try:
            _filter = ProcessChangeLog.Filter(_post, _instructor_ids)
        except FilterError as _err:
            print(str(_err))
            return -1

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))