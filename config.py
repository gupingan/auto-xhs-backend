"""
@File: config.py
@Author: 秦宇
@Created: 2023/11/5 13:56
@Description: Created in 咸鱼-自动化-AutoXhs.
"""
import pymysql

SECRET_KEY = '4&erxibr_&farf#h#lne7$4yuiv&4e@l^%drvk6a+767ug27wm'

GPA_KEY = '&71)26eb3h5j%6n*fk9%w*zvimf0ccl-2p9$ifo()n$pq!xyu9'

DATABASE_CONFIG = {
    'creator': pymysql,
    'mincached': 2,
    'maxconnections': 8,
    'blocking': True,
    'ping': 0,
    'host': 'localhost',
    'port': 3306,
    'user': '<your user>',
    'password': '<your password>',
    'database': 'auto_xhs_db',
    'charset': 'utf8mb4',
}

USER_FIELDS = ('uname', 'upwd', 'max_limit', 'is_admin', 'is_disabled', 'is_wait', 'wait_time', 'error', 'salt')

LOGIN_LIMIT = 3
WAIT_TIME = 5

LOGIN_VALID_TIME = 60 * 60 * 24 * 7

DEFAULT_COOKIES = ("abRequestId=b3a24d97-e349-553f-866c-7fba9239ccaa; "
                   "a1=18b287fe0af9atg98uvl7aoprycn0jsa7sc9ov2z750000374905; "
                   "webId=037a83ee1baebf147894c93a32bf9802; "
                   "gid=yYDJYWifdKWdyYDJYWid8MhJ0ij09kjY7h1WSuW0lUFvSj28I8VM0l888qW4j8280q00WSKf; "
                   "webBuild=3.13.6; "
                   "acw_tc=3c07e4257dfae1f514f0a9f187905bff9ad44213b56f4642a68b85b2fefb1259; "
                   "xsecappid=xhs-pc-web; "
                   "websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467; "
                   "sec_poison_id=35ae2fea-e006-494c-b7cd-fc479d1a16f6; "
                   "web_session=040069b4589c75f8cc96b64d77374bf590e845; "
                   "unread={%22ub%22:%22651be29b000000001d038221%22%2C%22ue%22:%22653a31b7000000001e02ed04%22%2C"
                   "%22uc%22:15}")

DEBUG = False

# 日志
LOGURU_CONFIG = {
    "rotation": "1 day",  # 每天滚动日志文件
    "retention": "7 days",  # 保留7天的日志文件
    "compression": "zip",  # 压缩日志文件
    "level": "INFO",  # 日志级别
    "enqueue": True,  # 异步写入
    "serialize": False  # 如果需要序列化为JSON格式，设置为True
}

try:
    from config_prod import *
except ImportError:
    pass

try:
    from config_dev import *
except ImportError:
    pass
