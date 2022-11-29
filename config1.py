#!/usr/bin/env python3
# coding=utf-8
# python version 3.7 by 6time
# 需要计算的hash字段与数据库表配置

# 密码字典文件，需要utf8格式保存
# pwdtop7w.txt 集合了各种top100、top3000、默认密码、后台口令、内网密码、域控密码、装机密码等合并去重，只保留4位及其以上的字典
pwdfile = 'pwdtop7w.txt'
# 数据库文件名
db_name = 'pwdtop7w.db'
# 数据库表名
table = 'pwdhash'
# 数据库字段，代码里末尾添加查询次数统计字段，顺序不能变，添加或删除字段后需要重新生成数据库
hashlist = [
    'password', 'md5', 'md5x2', 'md5x3',
    'sha1', 'ntlm', 'mysql', 'mysql5',
    'md5_sha1', 'sha1_sha1', 'sha1_md5', 'md5_base64',
    'md5_middle',
    'base64_md5', 'md5_sha256', 'sha256',
    'sm3'
]
