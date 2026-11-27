# ==========================================
# 文件：auth.py
# 功能：用户认证与账号管理
# ==========================================
import database

def register_account():
    """注册新账号，包含密码、身份和初始偏好"""
    print("\n--- 📝 注册新账号 ---")
    uid = input("请输入账号ID: ").strip()
    if not uid or uid in database.user_db: 
        return print("❌ 账号无效或已存在！")
    
    pwd = input("设置密码: ").strip()
    identity = input("身份(student/child/adult): ").strip() or "adult"
    
    # 存入数据库，preferences 为初始空列表
    database.user_db[uid] = {
        "password": pwd, 
        "identity": identity, 
        "member": "normal", 
        "preferences": [] 
    }
    print("✅ 注册成功！")

def login():
    """账号登录验证"""
    print("\n--- 🔐 账号登录 ---")
    uid = input("账号ID: ").strip()
    if uid not in database.user_db: 
        return print("❌ 账号不存在"), None
    pwd = input("密码: ").strip()
    
    if database.user_db[uid]["password"] == pwd:
        return uid
    return print("❌ 密码错误"), None

def set_preferences(uid):
    """首次登录后触发：设置商品偏好（用于首页推荐）"""
    print("\n✨ 请选择偏好(用逗号隔开，如:电子产品,图书)，直接回车跳过：")
    c = input("👉 选择: ").strip()
    if c: 
        database.user_db[uid]["preferences"] = c.split(",")
        print("✅ 偏好设置成功！")
