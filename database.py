# ==========================================
# 文件：database.py
# 功能：全局数据存储中心
# ==========================================
import datetime

# 1. 商品数据库 (包含销量，用于推荐算法)
products = [
    {"id": 1, "name": "机械键盘", "category": "电子产品", "price": 299.0, "sales": 150},
    {"id": 2, "name": "降噪耳机", "category": "电子产品", "price": 599.0, "sales": 320},
    {"id": 3, "name": "Python编程书", "category": "图书", "price": 89.0, "sales": 800},
    {"id": 4, "name": "洗发水", "category": "生活用品", "price": 45.0, "sales": 2000},
    {"id": 5, "name": "智能手表", "category": "电子产品", "price": 899.0, "sales": 85}
]

# 2. 用户数据库 (字典结构，存储用户信息)
user_db = {}

# 3. 订单数据库 (列表结构，存储历史订单)
order_db = []

# 4. 系统操作日志
logs = []

def add_log(action_text):
    """记录系统操作日志，附带当前时间戳"""
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    logs.append(f"[{time_now}] {action_text}")
