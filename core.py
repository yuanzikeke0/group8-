# ==========================================
# 文件：core.py
# 功能：详细的折扣、会员、节日、运费计算
# ==========================================

def calculate_final_total(total, customer_type="adult", member_level="normal", coupon_amount=0, is_holiday=False):
    """核心算法：计算商品最终应付金额"""
    print("\n--- 🧮 正在为您计算最终金额 ---")
    if total <= 0: 
        return 0.0 # 防止异常数据
    
    # 1. 身份折扣判断 (使用最基础的 if-elif，绝对不精简)
    base_rate = 1.0
    if customer_type == "student":
        base_rate = 0.90
        print("👨‍🎓 识别为学生身份，享受 9 折优惠。")
    elif customer_type == "child":
        base_rate = 0.80
        print("👦 识别为儿童身份，享受 8 折优惠。")
    elif customer_type == "senior":
        base_rate = 0.85
        print("👴 识别为老人身份，享受 85 折优惠。")
    elif customer_type == "adult":
        base_rate = 1.0
        print("🧑 识别为成人身份，无身份折扣。")
    
    # 2. 会员折扣判断
    member_rate = 1.0
    if member_level == "silver":
        member_rate = 0.95
        print("🥈 白银会员，叠加 95 折优惠。")
    elif member_level == "gold":
        member_rate = 0.90
        print("🥇 黄金会员，叠加 9 折优惠。")
    elif member_level == "vip":
        member_rate = 0.80
        print("💎 钻石会员，叠加 8 折优惠。")
    elif member_level == "normal":
        member_rate = 1.0
        print("普通会员，无叠加折扣。")
    
    # 3. 节日折扣判断
    holiday_rate = 1.0
    if is_holiday == True:
        holiday_rate = 0.95
        print("🎉 双11大促期间，叠加全场 95 折优惠。")
    elif is_holiday == False:
        holiday_rate = 1.0
        print("今日无节日活动。")
    
    # 4. 计算总折扣率并设置 5 折底线
    final_rate = base_rate * member_rate * holiday_rate
    if final_rate < 0.5:
        final_rate = 0.5
        print("⚠️ 折扣力度过大，系统自动触发底线保护（最低 5 折）！")
    
    discounted_total = total * final_rate # 计算折后价
    print(f"💰 折扣后商品金额: ￥{round(discounted_total, 2)}")

    # 5. 优惠券抵扣
    if coupon_amount > 0:
        print(f"🎟️ 使用优惠券抵扣了 ￥{coupon_amount}")
        discounted_total = discounted_total - coupon_amount # 减去优惠券
        
    if discounted_total < 0: 
        print("⚠️ 抵扣后金额为负，系统已自动归零。")
        discounted_total = 0 # 防止出现负数

    # 6. 运费计算 (满 99 包邮)
    shipping_fee = 0.0
    if discounted_total > 0 and discounted_total < 99:
        shipping_fee = 10.0
        print("🚚 订单不满 99 元，需收取 10 元运费。")
    elif discounted_total >= 99:
        shipping_fee = 0.0
        print("🎉 订单满 99 元，已为您免除运费！")
    
    return round(discounted_total + shipping_fee, 2) # 返回最终总价，保留两位小数
