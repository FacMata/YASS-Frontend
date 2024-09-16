import flask
import requests
import hashlib
from flask import request, redirect
from flask_cors import CORS
from urllib.parse import quote
import socket
from flask_caching import Cache
import time
from functools import wraps
import yaml

# 读取 YAML 配置文件
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# 从配置中获取全局变量
emby_url = config['emby_url']
emby_key = config['emby_key']
local_dir = config['local_dir']
remote_api = config['remote_api']
remote_domain = config['remote_domain']
remote_port = config['remote_port']
remote_token = config['remote_token']

# 从配置中获取 host 和 port
app_host = config['app']['host']
app_port = config['app']['port']

app = flask.Flask(__name__)

# 配置缓存
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = config['cache']['redis_host']
app.config['CACHE_REDIS_PORT'] = config['cache']['redis_port']
app.config['CACHE_KEY_PREFIX'] = config['cache']['key_prefix']

# 创建缓存对象
cache = Cache(app)

# 装饰器函数，用于计算执行时间
def time_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行被装饰的函数
        end_time = time.time()  # 记录结束时间
        execution_time = end_time - start_time  # 计算执行时间
        print(f"Function {func.__name__} took {execution_time:.4f} seconds")
        return result
    return wrapper

def get_ip_from_domain(domain):
    """解析域名并返回 IP 地址。"""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

@time_logger
def generate_redirect_url(emby_path, MediaSourceId):
    """生成重定向的URL"""
    local_path = emby_path.replace(local_dir, "")
    raw_string = f"dir={local_path}&MediaSourceId={MediaSourceId}"
    md5_verify = hashlib.md5(f"{raw_string}&remote_token={remote_token}".encode(encoding='UTF-8')).hexdigest()
    raw_string = f"dir={quote(local_path)}&MediaSourceId={MediaSourceId}"
    raw_ip = get_ip_from_domain(remote_domain)
    return f"http://{remote_domain}:{remote_port}/stream?{raw_string}&key={md5_verify}"

@time_logger
def process_request(item_Id, MediaSourceId, api_key=None):
    """处理请求，生成重定向URL"""
    if api_key is None:
        api_key = emby_key  # Infuse默认使用全局emby_key
    
    item_info_uri = f"{emby_url}/Items/{item_Id}/PlaybackInfo?MediaSourceId={MediaSourceId}&api_key={api_key}"
    emby_path = fetchEmbyFilePath(item_info_uri, MediaSourceId)
    return generate_redirect_url(emby_path, MediaSourceId)

@app.route('/emby/videos/<item_Id>/original.<type>', methods=["GET"])
@app.route('/videos/<item_Id>/original.<type>', methods=["GET"])
@app.route('/emby/videos/<item_Id>/stream.<type>', methods=["GET"])
@app.route('/emby/Videos/<item_Id>/stream.<type>', methods=["GET"])
@app.route('/Videos/<item_Id>/stream', methods=["GET"])
def handle_request(item_Id, type=None):
    MediaSourceId = request.args.get("MediaSourceId")
    api_key = request.args.get("api_key")

    redirect_url = process_request(item_Id, MediaSourceId, api_key)
    return redirect(redirect_url)

@time_logger
@cache.memoize(timeout=3600)
def fetchEmbyFilePath(itemInfoUri, MediaSourceId):
    """获取Emby内文件路径"""
    req = requests.get(itemInfoUri)
    resjson = req.json()
    for media_source in resjson['MediaSources']:
        if media_source['Id'] == MediaSourceId:
            return media_source['Path']
    return None

# 在Flask应用中启用CORS
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(port=app_port, debug=True, host=app_host, threaded=True)
