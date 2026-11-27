# ==========================================
# 文件：database.py
# 功能：全局数据存储，模拟数据库的增删改查
# ==========================================
import datetime # 导入时间模块，用于生成日志时间戳

# 1. 商品数据库：包含了商品的各种详细属性，如分类、价格、销量、规格和厂商资质
products = [
    {
        "id": 1, 
        "name": "机械键盘", 
        "category": "电子产品", 
        "price": 299.0, 
        "sales": 150, 
        "desc": "探索前沿科技，体验指尖敲击的快感。", # 商品描述
        "options": ["红轴", "青轴", "茶轴"], # 可选规格
        "certs": ["ISO9001认证", "3C强制认证", "正品保障"] # 厂商资质
    },
    {
        "id": 2, 
        "name": "降噪耳机", 
        "category": "电子产品", 
        "price": 599.0, 
        "sales": 320, 
        "desc": "沉浸式音乐体验，隔绝外界喧嚣。", 
        "options": ["曜石黑", "云雾白"], 
        "certs": ["Hi-Res金标认证"]
    },
    {
        "id": 3, 
        "name": "Python编程书", 
        "category": "图书", 
        "price": 89.0, 
        "sales": 800, 
        "desc": "书中自有黄金屋，畅游知识的海洋。", 
        "options": ["平装版", "精装版"], 
        "certs": ["ISBN出版物", "正版授权"]
    },
    {
        "id": 4, 
        "name": "纯棉T恤", 
        "category": "生活用品", 
        "price": 45.0, 
        "sales": 2000, 
        "desc": "精选日常好物，提升您的生活品质。", 
        "options": ["S码", "M码", "L码", "XL码"], 
        "certs": ["A类质检", "环保染料认证"]
    }
]

# 2. 用户数据库：用于存储所有注册用户的信息，格式为 {"账号": {"密码": "...", ...}}
user_db = {}

# 3. 订单数据库：存储所有已生成的订单记录
order_db = []

# 4. 评价数据库：存储用户对商品的评价，格式为 {"商品ID": [{"user": "...", "rating": 5, "text": "..."}]}
reviews_db = {}

# 5. 系统日志库：记录系统运行过程中的所有关键操作
logs = []

def add_log(action_text):
    """将操作记录添加到日志库中，并附带当前时间"""
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 获取当前时间并格式化
    log_message = f"[{time_now}] {action_text}" # 拼接日志内容
    logs.append(log_message) # 存入列表
    print(f"📝 [系统日志] {action_text}") # 在控制台实时打印出来
