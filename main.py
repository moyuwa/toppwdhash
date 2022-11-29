#!/usr/bin/env python3
# coding=utf-8
# python version 3.7 by 6time
# 哈希查询sqlite3数据库

import os, sys
import config1
import genpwdhash
import queryhashdb

import argparse

helptext = """
常见密码哈希离线查询工具 python version 3.7 by 6time 
包含算法类型 
    'password', 'md5', 'md5x2', 'md5x3',
    'sha1', 'ntlm', 'mysql', 'mysql5',
    'md5_sha1', 'sha1_sha1', 'sha1_md5', 'md5_base64',
    'md5_middle',
    'base64_md5', 'md5_sha256', 'sha256',
    'sm3'
        
修改 config1.py 内参数 配置字典与哈希数据库

查询单个哈希 py -3 main.py -s e10adc3949ba59abbe56e057f20f883e
查询多个哈希 py -3 main.py -l test.txt
查询密码是否在库中 py -3 main.py -p 123456
模糊查询单个哈希值 py -3 main.py -k a59abb
生成指定密码的哈希值 py -3 main.py -g 12345667890
"""

print(helptext)

# 初始化参数选项
parser = argparse.ArgumentParser(description='')
parser.add_argument('-s', '--string', type=str, default=None, help='-s e10adc3949ba59abbe56e057f20f883e')
parser.add_argument('-l', '--list-file', type=str, default=None, help='-l hash.txt')
# parser.add_argument('-et', '--entype', type=str, default=None, help='-et md5x2') //指定哈希类型查询多个哈希 py -3 main.py -l test.txt -et md5
parser.add_argument('-p', '--password', type=str, default=None, help='-p 123456')
parser.add_argument('-k', '--like', type=str, default=None, help='-k a59abb')
parser.add_argument('-g', '--generate', type=str, default=None, help='-g 123456')
# parser.add_argument('-rc', '--record', type=int, default=1, help='记录查询次数加 n，默认为 1')
args = parser.parse_args()


def main():
    # 如果数据库不存在就生成
    if os.path.exists(config1.db_name) == False:
        print("\r\n未找到离线数据库，将根据配置生成")
        genpwdhash.pwdsqlite3(config1.pwdfile)
        print("哈希数据库创建完成!!!\r\n")
    # 查询次数加1
    # if args.record != None:
    #     record = int(args.record)
    # 查询哈希值
    if args.string != None:
        # 单个查询
        queryhashdb.querystr(args.string)
    elif args.list_file != None:
        # 加载哈希文件，进行多个查询
        with open(args.list_file, 'r', encoding='utf8') as f:
            hashlist = []
            for line in f.readlines():
                # 有时文本需要一些过滤或处理
                # 删除哈希值的 前后空格，回车换行
                hashlist.append(str(line).rstrip().strip().replace('\r', '').replace('\n', ''))
            # 列表查询
            queryhashdb.querylist(hashlist)
    elif args.password != None:
        # 查询明文密码的哈希值
        queryhashdb.querypassword(args.password)
    elif args.generate != None:
        # 查询明文密码的哈希值
        genpwdhash.generatehash(args.generate)
    elif args.like != None:
        # 查询明文密码的哈希值
        queryhashdb.pwdlike(args.like)
    else:
        print('参数错误\r\n')
        parser.print_help()


if __name__ == '__main__':
    main()
