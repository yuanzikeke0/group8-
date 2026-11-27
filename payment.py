# ==========================================
# 文件：payment.py
# 功能：支付渠道处理与专属优惠
# ==========================================
import random

def process_payment(method, amount):
    """根据不同的支付方式给予不同的立减优惠"""
    msg = ""
    
    # 根据支付方式计算优惠后的实际金额
    if method == "bank_card" and amount >= 100: 
        amount -= 5
        msg = "银行卡满100减5"
    elif method == "qq": 
        amount -= random.uniform(0.5, 3)
        msg = "QQ随机立减"
    elif method == "unionpay": 
        amount *= 0.98
        msg = "银联98折"
    else:
        msg = "正常支付"
        
    return {"success": True, "actual": round(amount, 2), "msg": msg}
