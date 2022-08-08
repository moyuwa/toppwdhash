# toppwdhash
 
常见密码哈希离线查询工具 python version 3.7 by 6time 
包含算法类型 
        'md5', 'md5x2', 'md5x3', 'sha1', 'ntlm', 'mysql', 'mysql5',
        'md5_sha1', 'sha1_sha1', 'sha1_md5', 'md5_base64', 'md5_middle'
        
修改 config1.py 内参数 配置字典与哈希数据库

查询单个哈希 py -3 main.py -s e10adc3949ba59abbe56e057f20f883e
查询多个哈希 py -3 main.py -l test.txt
查询密码是否在库中 py -3 main.py -p 123456
模糊查询单个哈希值 py -3 main.py -k a59abb
生成指定密码的哈希值 py -3 main.py -g 12345667890
