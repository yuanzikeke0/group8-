# ==========================================
# 文件：main.py
# 功能：主控台系统，串联所有模块，处理用户的一切交互
# ==========================================
import os # 导入系统模块用于清屏
import database, auth, core, shop, payment, logistics # 导入自己写的所有模块

def clear_screen():
    """跨平台清屏函数，让控制台界面保持整洁"""
    os.system('cls' if os.name == 'nt' else 'clear')

def run():
    """系统的主循环"""
    current_user = None  # 记录当前登录的用户，默认为None
    
    while True: # 只要没选退出，就一直循环
        clear_screen()  # 每次刷新都清空屏幕
        
        # 动态生成顶部状态栏
        if current_user is None:
            status = "👤 未登录 (游客)"
        else:
            status = f"👤 已登录: {current_user}"
        
        # 打印超级详细的菜单
        print("╔════════════════════════════════════════╗")
        print("║      🛒 第八组智能电商购物系统         ║")
        print(f"║  {status.ljust(36)}║") # ljust用于左对齐填充空格
        print("╠════════════════════════════════════════╣")
        print("║  1. 🛍️  浏览 / 搜索商品                ║")
        print("║  2. 🔍  查看商品资质与评价             ║")
        print("║  3. 💳  收银台 (完整结账流程)          ║")
        print("║  4. 🔐  登录账号                       ║")
        print("║  5. 📝  注册新账号                     ║")
        print("║  6. 🔑  忘记密码/找回密码              ║")
        print("║  7. 📦  我的订单 / 追踪物流            ║")
        print("║  0. 🚪  退出系统                       ║")
        print("╚════════════════════════════════════════╝")
        
        # 接收用户输入
        choice = input("👉 请输入功能编号: ").strip()
        
        # ============ 选项 0: 退出 ============
        if choice == "0":
            print("👋 感谢使用，系统已退出！")
            break # 跳出循环，结束程序
            
        # ============ 选项 1: 浏览商品 ============
        elif choice == "1":
            # 调用 shop 模块展示商品
            shop.browse_products(current_user)
            input("\n按回车键返回主菜单...")
            
        # ============ 选项 2: 查看详情 ============
        elif choice == "2":
            try:
                pid = int(input("\n请输入要查看的商品ID: "))
                shop.view_product_detail(pid)
            except ValueError: # 防止用户输入字母导致崩溃
                print("❌ 输入错误，必须输入数字ID！")
            input("\n按回车键返回主菜单...")
            
        # ============ 选项 3: 结账流程 ============
        elif choice == "3":
            if current_user is None:
                print("❌ 拦截：请先登录账号再结账！")
                input("\n按回车键返回...")
                continue # 直接跳回主菜单
                
            print("\n========================================")
            print("          💳 欢迎使用收银台")
            print("========================================")
            try:
                pid = int(input("请输入要购买的商品ID: "))
                
                # 查找商品
                product = None
                for p in database.products:
                    if p["id"] == pid:
                        product = p
                        break
                        
                if product is None:
                    print("❌ 商品不存在！")
                    input("\n按回车键返回...")
                    continue
                
                # 1. 选择规格
                print(f"\n📏 该商品有以下规格: {', '.join(product['options'])}")
                spec = input("👉 请选择具体规格: ").strip()
                if spec not in product["options"]: # 校验规格输入是否正确
                    print("❌ 规格输入错误！")
                    input("\n按回车键返回...")
                    continue
                
                # 2. 选择数量
                qty = int(input("\n🔢 请输入购买数量: "))
                if qty <= 0:
                    print("❌ 数量必须大于0！")
                    input("\n按回车键返回...")
                    continue
                
                # 计算商品总原价
                total_price = product["price"] * qty
                print(f"💵 商品总原价: ￥{total_price}")
                
                # 3. 获取用户信息
                u_info = database.user_db[current_user]
                
                # 4. 节日活动与优惠券
                is_holiday = input("\n🎉 今天是双11大促吗？全场额外95折 (y/n): ").strip().lower() == 'y'
                coupon = float(input("🎟️ 请输入要使用的优惠券面额 (没有填0): ") or 0)
                
                # 5. 算钱
                base_amount = core.calculate_final_total(
                    total_price, 
                    u_info["identity"], 
                    u_info["member"], 
                    coupon, 
                    is_holiday
                )
                
                # 6. 支付方式选择
                print("\n========================================")
                print("       💳 请选择您的支付方式")
                print("========================================")
                print("1. 💙 支付宝 (无额外优惠)")
                print("2. 💚 微信支付 (无额外优惠)")
                print("3. 💳 银行卡 (满100立减5元)")
                print("4. 🐧 QQ钱包 (随机立减0.5-3元)")
                print("5. 🏦 银联支付 (全场98折)")
                print("6. 📅 信用卡分期 (全场99折)")
                print("========================================")
                
                m_choice = input("👉 请输入支付方式编号 (1-6): ").strip()
                method = "alipay"
                if m_choice == "1": method = "alipay"
                elif m_choice == "2": method = "wechat"
                elif m_choice == "3": method = "bank_card"
                elif m_choice == "4": method = "qq"
                elif m_choice == "5": method = "unionpay"
                elif m_choice == "6": method = "installment"
                
                # 7. 扣款
                pay_result = payment.process_payment(method, base_amount)
                
                # 8. 生成订单
                if pay_result["success"]:
                    order_id = len(database.order_db) + 1001 # 模拟生成订单号
                    database.order_db.append({
                        "id": order_id,
                        "user": current_user,
                        "item": product["name"],
                        "spec": spec,
                        "qty": qty,
                        "amount": pay_result["actual"],
                        "reviewed": False # 初始状态为未评价
                    })
                    database.add_log(f"{current_user} 购买 {product['name']} x{qty}，实付 ￥{pay_result['actual']}")
                    print(f"\n✅ 交易完成！最终实付金额: ￥{pay_result['actual']}")
                    print(f"您的订单号为: {order_id}")
                    
            except ValueError: # 捕捉数字转换异常
                print("❌ 输入格式错误，请输入数字！")
            input("\n按回车键返回主菜单...")

        # ============ 选项 4: 登录 ============
        elif choice == "4":
            if current_user is not None:
                print("✅ 您已经登录了，无需重复登录。")
            else:
                res = auth.login()
                if res is not None: # 如果登录成功
                    current_user = res
                    # 如果是新登录且没设置过偏好，引导设置
                    if len(database.user_db[current_user]["preferences"]) == 0:
                        auth.set_preferences(current_user)
            input("\n按回车键返回主菜单...")

        # ============ 选项 5: 注册 ============
        elif choice == "5":
            auth.register_account()
            input("\n按回车键返回主菜单...")

        # ============ 选项 6: 找回密码 ============
        elif choice == "6":
            auth.forgot_password()
            input("\n按回车键返回主菜单...")

        # ============ 选项 7: 查看订单与物流 ============
        elif choice == "7":
            print("\n--- 📦 我的历史订单 ---")
            if current_user is None:
                print("❌ 请先登录！")
            else:
                # 筛选出当前用户的订单
                my_orders = []
                for o in database.order_db:
                    if o["user"] == current_user:
                        my_orders.append(o)
                        
                if len(my_orders) == 0:
                    print("暂无订单记录，快去逛逛吧！")
                else:
                    for o in my_orders:
                        print(f"\n订单号:{o['id']} | 商品:{o['item']} | 规格:{o['spec']} | 数量:{o['qty']} | 实付:￥{o['amount']}")
                        
                        # 自动查询物流
                        logistics.track_logistics(o["id"])
                        
                        # 评价功能
                        if o["reviewed"] == False: # 如果还没评价
                            ans = input("\n是否现在评价该商品? (y/n): ")
                            if ans.lower() == 'y':
                                rating = int(input("请输入评分 (1-5星): "))
                                text = input("请输入评价内容: ")
                                
                                # 根据商品名称找回商品ID
                                pid = 0
                                for p in database.products:
                                    if p["name"] == o["item"]:
                                        pid = p["id"]
                                        break
                                
                                # 将评价存入评价库
                                if pid not in database.reviews_db:
                                    database.reviews_db[pid] = []
                                    
                                database.reviews_db[pid].append({
                                    "user": current_user, 
                                    "rating": rating, 
                                    "text": text
                                })
                                o["reviewed"] = True # 更新订单评价状态
                                print("✅ 评价提交成功！")
                                database.add_log(f"{current_user} 评价了 {o['item']}")
                        else:
                            print("✅ 该订单已评价。")
            input("\n按回车键返回...")

# 程序的启动入口
if __name__ == "__main__":
    run()
