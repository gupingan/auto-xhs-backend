"""
@File: manage.py
@Author: 秦宇
"""
import functools
import json
from typing import Tuple
from flask import Flask, request, jsonify
from pathlib import Path
from loguru import logger
from utils.auth import *
from utils.sqlor import *
from utils.timer import *
from utils.searcher import *
from config import *
from xhsAPI import *

app = Flask(__name__)
app.secret_key = SECRET_KEY
sql.setParam(DATABASE_CONFIG)
Token.setValidTime(LOGIN_VALID_TIME)


def setup_logging():
    logger.remove()
    log_path = Path("logs")
    log_path.mkdir(parents=True, exist_ok=True)  # 确保日志目录存在
    log_file_path = log_path / "{time:YYYY-MM-DD}.log"
    logger.add(
        sink=log_file_path,
        rotation=LOGURU_CONFIG["rotation"],
        retention=LOGURU_CONFIG["retention"],
        compression=LOGURU_CONFIG["compression"],
        level=LOGURU_CONFIG["level"],
        enqueue=LOGURU_CONFIG["enqueue"],
        serialize=LOGURU_CONFIG["serialize"]
    )


setup_logging()


@app.before_request
def before_request():
    logger.info(f"\n\tTarget：{request.method} {request.path}\n\tHost：{request.remote_addr}")


@app.after_request
def after_request(response):
    logger.info(f"\n\tForm：{request.form.to_dict()}\n\tStatus: {response.status}\n")
    return response


def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'msg': 'An error occurred.',
                'data': {}
            }), 500

    return wrapper


def auth(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith("Bearer "):
            token = authorization_header.split(" ")[1]
            if Token.isValid(token, SECRET_KEY):
                user = Token.unravel(token, SECRET_KEY)
                uname = user["uname"]
                tokenId = user['tokenId']
                db_user = sql.select('users', ['is_disabled', 'token'], f'uname={uname!r}', count=1)
                if not db_user:
                    return jsonify({'success': False, 'msg': '用户不存在', 'data': {}}), 404
                if db_user[0]:
                    return jsonify({'success': False, 'msg': '用户已被禁止登录', 'data': {}}), 403
                if tokenId != db_user[1]:
                    return jsonify({'success': False, 'msg': '令牌无效', 'data': {}}), 401
                return func(user, *args, **kwargs)
            return jsonify({'success': False, 'msg': '令牌无效', 'data': {}}), 401
        return jsonify({'success': False, 'msg': '令牌不合法', 'data': {}}), 401

    return decorated


def gpa_verify(api_path):
    def gpa(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            gpa_t = request.form.get('gpa_t', type=int)
            gpa_s = request.form.get('gpa_s')
            if not verifyGPAValues(GPA_KEY, api_path, gpa_s, gpa_t):
                return jsonify({'success': False, 'msg': 'Forbidden.', 'data': {}}), 403
            res = func(*args, **kwargs)
            return res

        return decorated

    return gpa


def loginer(is_admin=False):
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            uname = request.form.get('uname')
            upwd = request.form.get('upwd')
            if not uname or not upwd:
                return jsonify({'success': False, 'msg': '用户名或者密码不能为空', 'data': {}}), 401
            find_user = sql.select('users', USER_FIELDS, f'uname={uname!r}', count=1)
            if not find_user:
                return jsonify({'success': False, 'msg': '用户名不存在', 'data': {}}), 404
            if find_user[4]:
                return jsonify({'success': False, 'msg': '该用户已被禁止登录', 'data': {}}), 403
            if find_user[5]:
                if current() < find_user[6]:
                    return jsonify(
                        {'success': False, 'msg': f'登录请求频繁，请在{remainSeconds(find_user[6])}秒后再试',
                         'data': {}}), 429
                sql.update('users', {'error': 0, 'is_wait': 0, 'update_time': current()}, f'uname={uname!r}')
                find_user = sql.select('users', USER_FIELDS, f'uname={uname!r}', count=1)
            if not Password.verify(upwd, find_user[1], find_user[8]):
                if find_user[7] >= LOGIN_LIMIT - 1:
                    sql.update('users', {'is_wait': 1, 'wait_time': after(WAIT_TIME), 'update_time': current()},
                               condition=f'uname={uname!r}')
                else:
                    new_count = find_user[7] + 1
                    sql.update('users', {'error': new_count, 'update_time': current()}, f'uname={uname!r}')
                logger.info(f'用户 [账号：{uname} 密码：{upwd}] 因密码错误而登录失败')
                return jsonify(
                    {'success': False, 'msg': f'登录失败，你还有 {LOGIN_LIMIT - find_user[7] - 1} 次机会',
                     'data': LOGIN_LIMIT - find_user[7] - 1}), 401
            if is_admin and not find_user[3]:
                logger.info(f'用户 [账号：{uname}] 尝试访问管理员API')
                return jsonify({'success': False, 'msg': '该用户非管理员身份', 'data': {}}), 403
            token = Token.create(uname, upwd, secret_key=SECRET_KEY)
            tokenId = Token.unravel(token, secret_key=SECRET_KEY)['tokenId']
            sql.update('users', {'is_wait': 0, 'error': 0, 'token': tokenId, 'update_time': current()},
                       f'uname={uname!r}')
            logger.info(f'用户 [账号：{uname}] 登录成功')
            return func(token, *args, **kwargs)

        return decorated

    return decorator


def register_user(uname: str, upwd: str, is_admin: int = 0, max_limit: int = 0) -> Tuple[bool, str]:
    if not uname or not upwd:
        return False, "用户名或者密码不能为空"

    find_user = sql.select("users", USER_FIELDS, f"uname={uname!r}", count=1)
    if find_user:
        return False, "注册失败，用户名已存在"

    upwd, salt = Password.encrypt(upwd)
    new_user = {
        "uname": uname,
        "upwd": upwd,
        "max_limit": max_limit,
        "is_admin": is_admin,
        "is_disabled": 0,
        "is_wait": 0,
        "wait_time": current(),
        "error": 0,
        "salt": salt,
        "create_time": current(),
        "update_time": current(),
    }
    sql.insert("users", new_user)

    return True, "注册成功"


@app.route('/api/test', methods=['GET'])
@trace
def test_get():
    time.sleep(5)
    return jsonify({'success': True, 'msg': '获取成功', 'data': {'time': current('timestamp')}}), 200


@app.route('/api/user/login', methods=['POST'])
@trace
@loginer()
def user_login(token):
    return jsonify({'success': True, 'msg': '登录成功', 'token': token, 'data': {}}), 200


@app.route('/api/admin/login', methods=['POST'])
@trace
@loginer(is_admin=True)
def admin_login(token):
    return jsonify({'success': True, 'msg': '登录成功', 'token': token, 'data': {}}), 200


@app.route("/api/user/register", methods=["POST"])
@trace
def user_register():
    uname = request.form.get("uname").replace(" ", "")
    upwd = request.form.get("upwd").replace(" ", "")
    max_limit = request.form.get("max_limit", 0)

    success, msg = register_user(uname, upwd, max_limit=max_limit)
    status_code = 200 if success else 401
    logger.info(f'注册用户 [账号：{uname}，密码：{upwd}]{"成功" if success else "失败"}')
    return jsonify({"success": success, "msg": msg, "data": {}}), status_code


@app.route("/api/admin/init", methods=["POST"])
@trace
def init_admin():
    success, msg = register_user("adminer", "123456", is_admin=1, max_limit=100)
    status_code = 200 if success else 401
    logger.info(f'初始化管理员账号 {"成功" if success else "失败"}')
    return jsonify({"success": success, "msg": msg, "data": {}}), status_code


@app.route('/api/user/password', methods=['POST'])
@trace
@auth
def modify_user_pwd(user):
    uname = request.form.get('uname')
    upwd = request.form.get('upwd')
    if not uname or not upwd:
        return jsonify({'success': False, 'msg': '用户名或者密码不能为空', 'data': {}}), 401
    if user['uname'] != uname:
        return jsonify({'success': False, 'msg': f'无权限修改密码', 'data': {}}), 403
    user = sql.select('users', ('uname',), f'uname={uname!r}', count=1)
    if not user:
        return jsonify({'success': False, 'msg': f'用户 {uname} 不存在', 'data': {}}), 404
    new_upwd, new_salt = Password.encrypt(upwd)
    user_data = {'upwd': new_upwd, 'salt': new_salt, 'update_time': current()}
    sql.update('users', user_data, f'uname={user[0]!r}')
    return jsonify({'success': True, 'msg': f"用户 {user[0]} 的密码更改为 {upwd}", 'data': {}}), 200


@app.route('/api/admin/password', methods=['POST'])
@trace
@auth
def modify_admin_pwd(user):
    uname, upwd = request.form.get('uname'), request.form.get('upwd')
    if not uname or not upwd:
        return jsonify({'success': False, 'msg': '用户名或者密码不能为空', 'data': {}}), 401
    admin = sql.select('users', ('is_admin',), f'uname={user["uname"]!r}', count=1)
    if not admin:
        return jsonify({'success': False, 'msg': '当前管理员不存在', 'data': {}}), 404
    if not admin[0]:
        return jsonify({'success': False, 'msg': '无权限修改密码', 'data': {}}), 403
    user = sql.select('users', ('uname',), f'uname={uname!r}', count=1)
    if not user:
        return jsonify({'success': False, 'msg': f'用户 {uname} 不存在', 'data': {}}), 404
    new_upwd, new_salt = Password.encrypt(upwd)
    sql.update('users', {'upwd': new_upwd, 'salt': new_salt, 'update_time': current()}, f'uname={user[0]!r}')
    return jsonify({'success': True, 'msg': f"用户 {user[0]} 的密码更改为 {upwd}", 'data': {}}), 200


@app.route('/api/admin/json', methods=['GET'])
@trace
@auth
def admin_json_folder(user):
    admin = sql.select('users', ('is_admin',), f'uname={user["uname"]!r}', count=1)
    if not admin or not admin[0]:
        return jsonify({'success': False, 'msg': '无权限查看日志', 'data': {}}), 403
    folder = Path('./配置/')
    if not folder.exists():
        return jsonify({'success': False, 'msg': '配置不存在', 'data': {}}), 404
    subfolders = [subfolder.name for subfolder in folder.iterdir() if subfolder.is_dir()]
    return jsonify({'success': True, 'msg': '获取成功', 'data': subfolders}), 200


@app.route('/api/admin/json', methods=['POST'])
@trace
@auth
def admin_json_subfile(user):
    admin = sql.select('users', ('is_admin',), f'uname={user["uname"]!r}', count=1)
    if not admin or not admin[0]:
        return jsonify({'success': False, 'msg': '无权限查看日志', 'data': {}}), 403
    uname = request.form.get('uname')
    folder = Path(f'./配置/{uname}/')
    if not folder.exists():
        return jsonify({'success': False, 'msg': f'{uname}的配置文件夹不存在', 'data': {}}), 404
    subfiles = [subfile.stem for subfile in folder.iterdir() if subfile.is_file()]
    return jsonify({'success': True, 'msg': '获取成功', 'data': subfiles}), 200


@app.route('/api/admin/v/json', methods=['POST'])
@trace
@auth
def admin_json(user):
    admin = sql.select('users', ('is_admin',), f'uname={user["uname"]!r}', count=1)
    if not admin or not admin[0]:
        return jsonify({'success': False, 'msg': '无权限查看日志', 'data': {}}), 403
    uname, spider_name = request.form.get('uname'), request.form.get('spider_name')
    spider_json = Path(f'./配置/{uname}/{spider_name}.json')
    if not spider_json.exists():
        return jsonify({'success': False, 'msg': f'{spider_name}的配置文件不存在', 'data': {}}), 404
    with spider_json.open('r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    if isinstance(json_data, dict):
        json_data.setdefault('创建时间', timeText(spider_json.stat().st_ctime))
    return jsonify({'success': True, 'msg': '获取成功', 'data': json_data}), 200


@app.route('/api/user/locate', methods=['GET'])
@trace
@auth
def user_locate(user):
    ip = request.remote_addr
    data = {'ip': ip}
    return jsonify({'success': True, 'msg': '获取成功', 'data': data}), 200


@app.route('/api/user/limit', methods=['GET'])
@trace
@auth
def user_limit(user):
    username = user['uname']
    max_limit = sql.select('users', ['max_limit'], f'uname={username!r}', count=1)
    if not max_limit:
        return jsonify({'success': False, 'msg': '获取失败', 'data': 0})
    return jsonify({'success': True, 'msg': '获取成功', 'data': max_limit[0]})


@app.route('/api/spider/create', methods=['POST'])
@trace
@auth
@gpa_verify('/api/spider/create')
def create(user):
    post_count = request.form.get('count', type=int)
    spider_info = json.loads(request.form.get('info'))
    spider_info.setdefault('创建时间', current('str'))
    spider_info.setdefault('创建地址', request.remote_addr)
    username = user['uname']
    spider_name = spider_info['名称']
    Path(f'./配置/{username}').mkdir(parents=True, exist_ok=True)
    with open(f'./配置/{username}/{spider_name}.json', 'w', encoding='utf-8') as f:
        json.dump(spider_info, f, ensure_ascii=False, indent=4)
    max_limit = sql.select('users', ['max_limit'], f'uname={username!r}', count=1)
    if post_count >= max_limit[0]:
        return jsonify({'success': False, 'msg': '创建失败，你的进程数量余额不足', 'data': {}}), 403
    return jsonify({'success': True, 'msg': f'进程 {spider_name} 创建成功', 'data': {}}), 200


@app.route('/api/qrcode/info', methods=['GET'])
@trace
@auth
def qrcode(user):
    loginAPI = Login(DEFAULT_COOKIES)
    qrcode_data = loginAPI.createQrcode()['data']
    return jsonify({
        'success': True,
        'msg': '获取成功',
        'data': qrcode_data,
    })


@app.route('/api/qrcode/state', methods=['GET'])
@trace
@auth
def qrcode_state(user):
    qr_id = request.args.get('qrId')
    code = request.args.get('code')
    loginAPI = Login(DEFAULT_COOKIES)
    data = loginAPI.qrcodeStatus(qr_id, code)['data']
    if not data or data.get('code_status', -1) == 0 or data.get('code_status', -1) == 1:
        return jsonify({
            'success': True,
            'msg': '等待扫码',
            'data': data.get('login_info'),
        })
    elif data.get('code_status', -1) == 2:
        return jsonify({
            'success': True,
            'msg': '登录成功',
            'data': data.get('login_info'),
        })
    elif data.get('code_status', -1) == 3:
        return jsonify({
            'success': False,
            'msg': '二维码已过期',
            'data': {},
        })
    else:
        return jsonify({
            'success': False,
            'msg': '未知错误',
            'data': data.get('code_status', -1),
        })


@app.route('/api/note/search', methods=['POST'])
@trace
@auth
def search_note(user):
    urls = []
    keywords = request.form.getlist('keywords')
    sort_type = request.form.get('sort_type')
    note_type = request.form.get('note_type')
    needs = request.form.get('needs', type=int)
    cookies = request.headers.get('Cookies')
    searcher = Search(cookies)
    for keyword in keywords:
        if note_type == '3':
            urls.extend(get_desired_items(searcher, keyword, 1, needs // 2, sort_type, 2))
            urls.extend(get_desired_items(searcher, keyword, 1, needs - needs // 2, sort_type, 1))
        else:
            urls.extend(get_desired_items(searcher, keyword, 1, needs, sort_type, note_type))
    return jsonify({'success': True, 'msg': '获取成功', 'data': urls}), 200


@app.route('/api/note/uncollect', methods=['POST'])
@trace
@auth
def uncollect(user):
    cookies = request.headers.get('Cookies')
    noteId = request.form.get('noteId')
    response = Note(cookies).uncollect(noteId)
    return jsonify({
        'success': response['code'] == 0,
        'msg': '操作成功',
        'data': {},
    }), 200 if response['code'] == 0 else 401


@app.route('/api/note/collected', methods=['POST'])
@trace
@auth
def check_collected(user):
    cookies = request.headers.get('Cookies')
    noteId = request.form.get('noteId')
    response = Note(cookies).feed(noteId)
    if not response['data']:
        return jsonify({
            'success': False,
            'msg': '操作频繁',
            'data': False,
        }), 404
    collected = response['data']['items'][0]['note_card']['interact_info']['collected']
    return jsonify({
        'success': True,
        'msg': '操作成功',
        'data': collected,
    })


@app.route('/api/note/comment', methods=['POST'])
@trace
@auth
def comment_note(user):
    logger.info(f'用户 [账号：{user["uname"]}] 正在评论中')
    cookies = request.headers.get('Cookies')
    noteId = request.form.get('noteId')
    comment = request.form.get('comment')
    userId = request.form.get('userId')
    commenter = Comment(cookies)
    response = commenter.post(noteId, comment)  # -9119 表示只允许好友评论
    if response['code'] != 0:
        return jsonify({
            'success': False,
            'msg': '操作失败',
            'data': False,
        }), 401
    else:
        time.sleep(3)
        posted_comments = commenter.showAll(noteId)['data']['comments']
        for posted_comment in posted_comments:
            if posted_comment['content'] == comment and posted_comment['user_info']['user_id'] == userId:
                if posted_comment['status'] in (0, 2):
                    return jsonify({
                        'success': True,
                        'msg': '操作成功',
                        'data': True,
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'msg': '操作失败',
                        'data': False,
                    }), 401
        else:
            return jsonify({
                'success': False,
                'msg': '操作失败',
                'data': False,
            }), 401


@app.route('/api/note/collect', methods=['POST'])
@trace
@auth
def collect(user):
    cookies = request.headers.get('Cookies')
    noteId = request.form.get('noteId')
    response = Note(cookies).collect(noteId)
    return jsonify({
        'success': response['code'] == 0,
        'msg': '操作成功',
        'data': {},
    }), 200 if response['code'] == 0 else 401


@app.route('/api/note/like', methods=['POST'])
@trace
@auth
def like(user):
    cookies = request.headers.get('Cookies')
    noteId = request.form.get('noteId')
    response = Note(cookies).like(noteId)
    return jsonify({
        'success': response['code'] == 0,
        'msg': '操作成功',
        'data': {},
    }), 200 if response['code'] == 0 else 401


@app.route('/api/note/follow', methods=['POST'])
@trace
@auth
def follow(user):
    cookies = request.headers.get('Cookies')
    noteId = request.form.get('noteId')
    response = Note(cookies).feed(noteId)
    if not response['data']:
        return jsonify({
            'success': False,
            'msg': '操作频繁',
            'data': False,
        }), 404
    author_id = response['data']['items'][0]['note_card']['user']['user_id']
    response = User(cookies).follow(author_id)
    return jsonify({
        'success': response['code'] == 0,
        'msg': '操作成功',
        'data': {'authorId': author_id},
    }), 200 if response['code'] == 0 else 401


if __name__ == '__main__':
    app.run(debug=DEBUG)
