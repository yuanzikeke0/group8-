# ==========================================
# 文件：auth.py
# 功能：处理用户注册、登录、密码找回与偏好设置
# ==========================================
import database # 导入数据库模块以便操作数据

def register_account():
    """注册新账号，包含详细的密码校验和密保设置"""
    print("\n========================================")
    print("          📝 欢迎注册新账号")
    print("========================================")
    uid = input("请输入您的账号ID: ").strip() # 获取输入并去除首尾空格
    if not uid: # 判断是否为空
        print("❌ 注册失败：账号不能为空！")
        return
    
    if uid in database.user_db: # 判断账号是否已存在
        print("❌ 注册失败：该账号已存在，请换个名字！")
        return
    
    pwd = input("请设置您的密码: ").strip()
    pwd_confirm = input("请再次确认密码: ").strip()
    if pwd != pwd_confirm: # 校验两次密码是否一致
        print("❌ 注册失败：两次密码输入不一致！")
        return
    
    print("\n--- 🔐 安全设置 (用于日后找回密码) ---")
    security_q = input("请设置密保问题 (如:我的小学名字?): ").strip()
    security_a = input("请输入您的密保答案: ").strip()
    
    print("\n--- 👤 属性设置 ---")
    identity = input("请输入身份(student/child/senior/adult): ").strip().lower() # 转换为小写
    if identity == "student":
        print("👨‍🎓 已设定为学生身份")
    elif identity == "child":
        print("👦 已设定为儿童身份")
    elif identity == "senior":
        print("👴 已设定为老人身份")
    else:
        identity = "adult"
        print("🧑 已设定为成人身份")

    member = input("请输入会员等级(normal/silver/gold/vip): ").strip().lower()
    if member not in ["normal", "silver", "gold", "vip"]: # 如果输入不符合规范
        member = "normal"
        print("⚠️ 未识别等级，默认设为 normal (普通会员)")
        
    # 将用户信息打包成字典，存入全局用户数据库
    database.user_db[uid] = {
        "password": pwd, 
        "identity": identity, 
        "member": member,
        "security_q": security_q, 
        "security_a": security_a, 
        "preferences": [] # 初始化偏好为空列表
    }
    database.add_log(f"新用户 {uid} 注册成功")
    print(f"✅ 账号 {uid} 注册成功！欢迎加入！")

def login():
    """账号登录验证"""
    print("\n========================================")
    print("          🔐 账号登录")
    print("========================================")
    uid = input("请输入账号ID: ").strip()
    if uid not in database.user_db: # 判断账号是否存在
        print("❌ 登录失败：账号不存在！")
        return None
        
    pwd = input("请输入密码: ").strip()
    if database.user_db[uid]["password"] == pwd: # 验证密码是否匹配
        print(f"✅ 登录成功！欢迎回来，{uid}")
        database.add_log(f"用户 {uid} 登录系统")
        return uid # 返回账号ID，代表登录成功
    else:
        print("❌ 登录失败：密码错误！")
        return None # 返回None，代表登录失败

def forgot_password():
    """忘记密码找回流程"""
    print("\n========================================")
    print("          🔑 密码找回")
    print("========================================")
    uid = input("请输入您的账号ID: ").strip()
    if uid not in database.user_db:
        print("❌ 该账号不存在！")
        return
        
    # 提示出该用户设置的密保问题
    print(f"\n🔒 密保问题: {database.user_db[uid]['security_q']}")
    answer = input("请输入您的密保答案: ").strip()
    
    if answer == database.user_db[uid]["security_a"]: # 校验密保答案
        print("✅ 验证通过！请设置新密码。")
        new_pwd = input("请输入新密码: ").strip()
        database.user_db[uid]["password"] = new_pwd # 更新数据库中的密码
        database.add_log(f"用户 {uid} 重置了密码")
        print("✅ 密码重置成功，请重新登录！")
    else:
        print("❌ 密保答案错误，无法重置密码！")

def set_preferences(uid):
    """首次登录后，引导用户设置商品偏好用于推荐"""
    print("\n========================================")
    print("          ✨ 商品偏好设置")
    print("========================================")
    print("分类有: 电子产品, 图书, 生活用品")
    print("请输入您喜欢的分类 (用逗号隔开，如: 电子产品,图书)")
    print("如果不想设置，请直接按回车键跳过。")
    
    user_input = input("👉 您的偏好: ").strip()
    
    if user_input == "": # 如果用户直接回车
        print("✅ 已跳过偏好设置，系统将默认推荐全网爆款。")
        return
    
    pref_list = user_input.split(",") # 用逗号切分成列表
    database.user_db[uid]["preferences"] = pref_list # 存入用户信息
    print(f"✅ 偏好设置成功！您关注的分类是: {pref_list}")
    database.add_log(f"用户 {uid} 设置了偏好")
