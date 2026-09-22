# 导入工具包
from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# 用来存数据的小仓库（假装是数据库），程序重启就清空啦
DATABASE_FILE = "data.json"


# 初始化数据
def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ------------------------------------------------------------
# 第一个功能：签到
# 访问地址示例：http://127.0.0.1:5000/sign?name=张三
# ------------------------------------------------------------
@app.route('/sign')
def sign_in():
    # 1. 从请求里拿到名字
    name = request.args.get('name')

    # 2. 校验：没传名字就报错
    if not name:
        return jsonify({"code": 400, "msg": "请告诉我你的名字！"})

    # 3. 读取数据
    data = load_data()

    # 4. 业务逻辑：记录签到时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[name] = now
    save_data(data)

    # 5. 返回成功结果
    return jsonify({
        "code": 0,
        "msg": f"签到成功！",
        "data": {
            "name": name,
            "sign_time": now,
            "total": len(data)
        }
    })


# ------------------------------------------------------------
# 第二个功能：查询签到记录
# 访问地址示例：http://127.0.0.1:5000/list
# ------------------------------------------------------------
@app.route('/list')
def list_all():
    data = load_data()
    return jsonify({
        "code": 0,
        "data": data
    })


# ------------------------------------------------------------
# 启动服务（运行这个脚本后，服务就一直在后台等着了）
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    print("服务已启动！访问 http://127.0.0.1:5000")