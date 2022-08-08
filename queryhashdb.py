#!/usr/bin/env python3
# coding=utf-8
# python version 3.7 by 6time
# 哈希查询sqlite3数据库

import sqlite3
import config1


def querystr(hash=str):
    """单个哈希查询"""
    print('-' * 86)
    print("{:^24}{:<12}{:^24}".format('password', 'encrypt', 'hash'))
    print('-' * 86)
    conn = sqlite3.connect(config1.db_name)

    for i in range(1, len(config1.hashlist)):
        # SELECT password FROM pwdhash WHERE md5='e10adc3949ba59abbe56e057f20f883e'
        qy = "SELECT password FROM '%s' WHERE %s='%s'" % (config1.table, config1.hashlist[i], hash)
        rows = conn.execute(qy)
        for row in rows:
            print("{:<24}{:<12}{}".format(row[0], config1.hashlist[i], hash))

    conn.close()


def querylist(hash=[]):
    """从文件读取多个哈希查询"""
    print('-' * 86)
    print("{:^24}{:<12}{:^24}".format('password', 'encrypt', 'hash'))
    print('-' * 86)
    conn = sqlite3.connect(config1.db_name)

    for h in hash:
        for i in range(1, len(config1.hashlist)):
            # SELECT password FROM pwdhash WHERE md5='e10adc3949ba59abbe56e057f20f883e'
            qy = "SELECT password FROM '%s' WHERE %s='%s'" % (
                config1.table, config1.hashlist[i], h)
            rows = conn.execute(qy)
            for row in rows:
                print("{:<24}{:<12}{}".format(row[0], config1.hashlist[i], h))

    conn.close()


def querypassword(pwd):
    """查询密码是否存在数据库中"""
    print('-' * 86)
    print("{:^24}{:<12}{:^24}".format('password', 'encrypt', 'hash'))
    print('-' * 86)
    conn = sqlite3.connect(config1.db_name)

    qy = "SELECT * FROM '%s' WHERE password='%s'" % (config1.table, pwd)
    rows = conn.execute(qy)
    for row in rows:
        for i in range(len(config1.hashlist)):
            # for row in rows:
            print("{:<24}{:<12}{}".format(pwd, config1.hashlist[i], row[i]))

    conn.close()


def pwdlike(hash=str):
    """单个哈希模糊查询"""
    print('-' * 86)
    print("{:^24}{:<12}{:^24}".format('password', 'encrypt', 'hash'))
    print('-' * 86)
    conn = sqlite3.connect(config1.db_name)

    for i in range(len(config1.hashlist)):
        qy = "SELECT password FROM '{}' WHERE {} like '%{}%'".format(config1.table, config1.hashlist[i], hash)
        rows = conn.execute(qy)
        for row in rows:
            print("{:<24}{:<12}{}".format(row[0], config1.hashlist[i], hash))

    conn.close()


if __name__ == '__main__':

    querystr('e10adc3949ba59abbe56e057f20f883e')
    querystr('10470c3b4b1fed12c3baac014be15fac67c6e815')

    querylist(['10470c3b4b1fed12c3baac014be15fac67c6e815',
               'e10adc3949ba59abbe56e057f20f883e',
               '6bb4837eb74329105ee4568dda7dc67ed2ca2ad9'])

    querypassword('123456')

    pwdlike('ba59abbe56')
