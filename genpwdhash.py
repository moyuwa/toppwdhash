#!/usr/bin/env python3
# coding=utf-8
# python version 3.7 by 6time
# 生成密码的各种哈希

import hashlib, binascii, sqlite3, base64
import config1
from gmssl import sm3, func

"""
各种哈希算法
"""


def pwdbase64(password, encode='utf-8'):
    b64_byt = base64.b64encode(password.encode(encoding=encode))
    b64_str = b64_byt.decode(encoding=encode)
    return b64_str


def pwdmd5(password, encode='utf-8'):
    m = hashlib.md5()
    m.update(password.encode(encoding=encode))
    return m.hexdigest()


def pwdsha1(password, encode='utf-8'):
    s1 = hashlib.sha1()
    s1.update(password.encode(encoding=encode))
    return s1.hexdigest()


def pwdsha256(password, encode='utf-8'):
    s1 = hashlib.sha256()
    s1.update(password.encode(encoding=encode))
    return s1.hexdigest()


def pwdntlm(password, encode='utf-8'):
    # n = hashlib.new('md4', text.encode('utf-16le'))
    n = hashlib.new('md4')
    n.update(password.encode('utf-16le'))
    return binascii.hexlify(n.digest()).decode()


def pwdmysql(password, encode='utf-8'):
    nr = 1345345333
    add = 7
    nr2 = 0x12345671

    for c in (ord(x) for x in password if x not in (' ', '\t')):
        nr ^= (((nr & 63) + add) * c) + (nr << 8) & 0xFFFFFFFF
        nr2 = (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF
        add = (add + c) & 0xFFFFFFFF

    return "%08x%08x" % (nr & 0x7FFFFFFF, nr2 & 0x7FFFFFFF)


def pwdmysql5(password, encode='utf-8'):
    """
    用SHA1散列字符串两次并返回大写十六进制摘要
    """
    pass1 = hashlib.sha1(password.encode(encoding=encode)).digest()
    pass2 = hashlib.sha1(pass1).hexdigest()
    return pass2


def pwdmd5_middle(password, encode='utf-8'):
    m = hashlib.md5()
    m.update(password.encode(encoding=encode))
    m = m.hexdigest()
    m16 = m[8:]
    m16 = m16[:-8]
    return m16


def pwdsm3(password, encode='utf-8'):
    # 数据和加密后数据为bytes类型
    m = sm3.sm3_hash(func.bytes_to_list(password.encode(encoding=encode)))
    return m


def pwdhashdata(password, encode='utf-8'):
    """
    算法调用、组合 生成密码哈希字典，字段有更改时这里也需要改
    """
    encode1 = 'utf-8'
    ph = {}
    ph['password'] = password
    ph['md5'] = pwdmd5(password, encode1)
    ph['md5x2'] = pwdmd5(pwdmd5(password, encode1), encode1)
    ph['md5x3'] = pwdmd5(pwdmd5(pwdmd5(password, encode1), encode1), encode1)
    ph['sha1'] = pwdsha1(password, encode1)
    ph['ntlm'] = pwdntlm(password, encode1)
    ph['mysql'] = pwdmysql(password, encode1)
    ph['mysql5'] = pwdmysql5(password, encode1)
    ph['md5_sha1'] = pwdmd5(pwdsha1(password, encode1), encode1)
    ph['sha1_sha1'] = pwdsha1(pwdsha1(password, encode1), encode1)
    ph['sha1_md5'] = pwdsha1(pwdmd5(password, encode1), encode1)
    ph['md5_base64'] = pwdmd5(pwdbase64(password, encode1), encode1)
    ph['md5_middle'] = pwdmd5_middle(password, encode1)
    ph['base64_md5'] = pwdbase64(pwdmd5(password, encode1), encode1)
    ph['md5_sha256'] = pwdmd5(pwdsha256(password, encode1), encode1)
    ph['sha256'] = pwdsha256(password, encode1)
    ph['sm3'] = pwdsm3(password, encode1)
    return ph


def generatehash(password):
    ph = pwdhashdata(password)
    print('-' * 86)
    print("{:^24}{:<12}{:^24}".format('password', 'encrypt', 'hash'))
    print('-' * 86)
    for i in range(len(config1.hashlist)):
        # for row in rows:
        print("{:<24}{:<12}{}".format(password, config1.hashlist[i], ph[config1.hashlist[i]]))


def pwdsqlite3(path):
    """
    读取txt密码文件，生成哈希，存储到sqlite3数据库
    """
    conn = sqlite3.connect(config1.db_name)
    # IF NOT EXISTS如果表不存在就创建
    # qy = """CREATE TABLE IF NOT EXISTS "%s"(
    #            password TEXT,md5 TEXT,md5x2 TEXT,md5x3 TEXT,
    #            sha1 TEXT,ntlm TEXT,mysql TEXT,mysql5 TEXT,
    #            md5_sha1 TEXT,sha1_sha1 TEXT,sha1_md5 TEXT);"""
    qy = 'CREATE TABLE IF NOT EXISTS "%s"('
    for com in config1.hashlist:
        qy += "{} TEXT,".format(com)
    qy += "num int);"  # 通过添加一个查询次数统计字段 避免bug
    conn.execute(qy % config1.table)

    cur = conn.cursor()  # 数据库游标

    # qy = "INSERT OR REPLACE INTO '%s'(password,md5,md5x2,md5x3,sha1,ntlm,mysql,mysql5,md5_sha1,sha1_sha1,sha1_md5)VALUES(?,?,?,?,?,?,?,?,?,?,?);" % pwdconfig.table
    qy = "INSERT OR REPLACE INTO '%s'(" % config1.table
    v = "VALUES("
    for com in config1.hashlist:
        qy += com + ","
        v += "?,"
    v += "?);"
    qy += "num)" + v
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            ph = pwdhashdata(line.replace('\n', ''))
            # 插入数据库，字段有更改时这里也需要改
            v = (ph['password'], ph['md5'], ph['md5x2'], ph['md5x3'],
                 ph['sha1'], ph['ntlm'], ph['mysql'], ph['mysql5'],
                 ph['md5_sha1'], ph['sha1_sha1'], ph['sha1_md5'], ph['md5_base64'],
                 ph['md5_middle'],
                 ph['base64_md5'], ph['md5_sha256'], ph['sha256'],
                 ph['sm3'],
                 0)
            cur.execute(qy, v)  # 插入新添的数据

    conn.commit()
    conn.close()


if __name__ == '__main__':
    password = '123456'
    d = pwdhashdata(password)
    print(d.values())

    generatehash('123456')

    # pwdsqlite3('pwdtop7w.txt')
