# -*- coding: utf-8 -*-

import datetime
import logging
import os
import time
import argparse
import logging.config
from subprocess import PIPE, Popen

HOST = '172.26.9.18'
PORT = '3306'
USER_NAME = 'competitor_test'
PASSWORD = '123456'
DATABASE = 'ai_test'

TIME_FORMAT = '%Y_%m_%d'
BACKUP_DIR = '/Users/yyinc/data'
BACKUP_FILE_PATH = '{}/{}_{}.sql'.format(BACKUP_DIR, DATABASE, datetime.datetime.now().strftime(TIME_FORMAT))
IGNORE_ERRO = 'Using a password on the command line interface can be insecure.'


def get_logger():
    logger = logging.getLogger("database_backup")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(filename='database_backup.log')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s',
        datefmt='%a %d %b %Y %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def dump_bk_sql(host, port, user_name, pwd, database_name, bk_path):
    start_time = time.time()
    logger = get_logger()
    try:
        cmd = "mysqldump -h{} -u{} -p{} -P {} {} > {}".format(host,
                                                                                   user_name,
                                                                                   pwd,
                                                                                   port,
                                                                                   database_name,
                                                                                   bk_path)
        logger.info('Start to backup database: {} to {}'.format(database_name, bk_path))
        out, err = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        if len(err.strip()) > 0 and IGNORE_ERRO not in err:
            raise RuntimeError(err)
        logger.info('Backup succeed! File size: {} bytes, costs {} seconds'.format(os.path.getsize(bk_path),
                                                                                  time.time() - start_time))
    except Exception, e:
        logger.error('Backup failed cause {}'.format(e))


def main():
    parser = argparse.ArgumentParser('Description')
    parser.add_argument('-backup_dir')
    args = parser.parse_args()
    if args.backup_dir:
         BACKUP_DIR = args.backup_dir

    dump_bk_sql(HOST, PORT, USER_NAME, PASSWORD, DATABASE, BACKUP_FILE_PATH)

    bk_files = sorted(os.listdir(BACKUP_DIR))
    if len(bk_files) > 10:
        os.remove(os.path.join(BACKUP_DIR, bk_files[0]))


if __name__ == '__main__':
    main()
