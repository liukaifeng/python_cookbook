__author__ = 'dell'


dic={'APPEND_STDOUT_LOGFILE=/OPT/PAAS/TALAS/LOGS/COLLECTING/COLL_FILE.LOG': 1, 'APPEND_[PROGRAM:COLL_LOGSTASH]': 1, 'APPEND_/OPT/PAAS/TALAS/DEV/COLLECTING/COLLECTING_SMGLOGS.PY': 1, 'APPEND_[PROGRAM:COLL_SMGLOGS]': 1, 'APPEND_/OPT/PAAS/TALAS/DEV/COLLECTING/COLLECTING_FILESERVER.PY': 1, 'APPEND_[PROGRAM:COLL_GENCOTT]': 1, 'APPEND_STDOUT_LOGFILE=/OPT/PAAS/TALAS/LOGS/COLLECTING/COLL_NONE.LOG': 1, 'APPEND_/OPT/PAAS/TALAS/DEV/COLLECTING/COLLECTING_FILE.PY': 1, 'APPEND_STDOUT_LOGFILE=/OPT/PAAS/TALAS/LOGS/COLLECTING/COLL_SMGLOGS.LOG': 1, 'APPEND_STDOUT_LOGFILE=/OPT/PAAS/TALAS/LOGS/COLLECTING/LOGSTASH_CONSOLE.LOG': 1, 'APPEND_DIRECTORY=/OPT/PAAS/TALAS/LIB/LOGSTASH': 1, 'APPEND_/OPT/PAAS/TALAS/DEV/COLLECTING/COLLECTING_ZMQ.PY': 1, 'APPEND_DIRECTORY=/OPT/PAAS/TALAS/DEV/COLLECTING': 6, 'APPEND_REDIRECT_STDERR=TRUE': 7, 'APPEND_[PROGRAM:COLL_FILESERVER]': 1, 'APPEND_-F': 1, 'APPEND_-L': 1, 'APPEND_STARTSECS=0': 7, 'APPEND_STDOUT_LOGFILE=/OPT/PAAS/TALAS/LOGS/COLLECTING/COLL_FILESERVER.LOG': 1, 'APPEND_STDOUT_LOGFILE=/OPT/PAAS/TALAS/LOGS/COLLECTING/COLL_ZMQ.LOG': 1, 'APPEND_COMMAND=PYTHON': 6, 'APPEND_COMMAND=/OPT/PAAS/TALAS/LIB/LOGSTASH/BIN/LOGSTASH': 1, 'APPEND_[PROGRAM:COLL_ZMQ]': 1, 'APPEND_[PROGRAM:COLL_FILE]': 1, 'APPEND_/OPT/PAAS/TALAS/DEV/COLLECTING/COLLECTING_NONE.PY': 1, 'APPEND_STDOUT_LOGFILE=/OPT/PAAS/TALAS/LOGS/COLLECTING/COLL_GENCOTT.LOG': 1, 'APPEND_AGENT': 1, 'APPEND_/OPT/PAAS/TALAS/LOGS/COLLECTING/LOGSTASH.LOG': 1, 'APPEND_/OPT/PAAS/TALAS/DEV/COLLECTING/COLLECTING_GENCOTT.PY': 1, 'APPEND_/OPT/PAAS/TALAS/LIB/LOGSTASH/XCOTT': 1, 'APPEND_[PROGRAM:COLL_NONE]': 1}

def iterator_map():
    for (k,v) in dic.items():
        print k,v

iterator_map()