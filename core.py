# ==========================================
# 文件：core.py
# 功能：核心折扣与运费计算
# ==========================================

def calculate_final_total(total, customer_type="adult", member_level="normal", coupon_amount=0, is_holiday=False):
    """
    计算最终应付金额
    参数: 原价, 身份, 会员等级, 优惠券金额, 是否节日
    """
    if total <= 0: return 0.0
    
    # 1. 身份基础折扣
    base_rate = 1.0
    if customer_type == "student": base_rate = 0.90  # 学生9折
    elif customer_type == "child": base_rate = 0.80  # 儿童8折
    elif customer_type == "senior": base_rate = 0.85 # 老人85折
    
    # 2. 会员叠加折扣
    member_rate = 1.0
    if member_level == "silver": member_rate = 0.95  # 白银95折
    elif member_level == "gold": member_rate = 0.90  # 黄金9折
    elif member_level == "vip": member_rate = 0.80   # 钻石8折
    
    # 3. 节日活动折扣 (大促全场额外95折)
    holiday_rate = 0.95 if is_holiday else 1.0
    
    # 4. 总折扣率计算与底线保护 (防止折扣叠加过低，最低5折)
    final_rate = base_rate * member_rate * holiday_rate
    if final_rate < 0.5: final_rate = 0.5
    
    # 计算折后价格
    discounted_total = total * final_rate

    # 5. 优惠券抵扣与防负数保护
    if coupon_amount > 0: 
        discounted_total -= coupon_amount
    if discounted_total < 0: 
        discounted_total = 0

    # 6. 运费计算：满 99 包邮，否则收 10 元
    shipping_fee = 0.0
    if 0 < discounted_total < 99: 
        shipping_fee = 10.0
    
    return round(discounted_total + shipping_fee, 2)
