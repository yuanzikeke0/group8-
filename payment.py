# ==========================================
# 文件：payment.py
# 功能：极尽详细的支付路由与渠道专属优惠
# ==========================================
import random # 导入随机数模块，用于模拟QQ钱包随机立减

def process_payment(method, amount):
    """处理各种支付方式的扣款与优惠"""
    print("\n========================================")
    print("       💳 正在接入支付网关")
    print("========================================")
    
    actual_amount = amount # 初始化实际扣款金额
    msg = "" # 初始化提示信息
    
    # 1. 支付宝
    if method == "alipay":
        print("💙 正在跳转至支付宝安全支付页面...")
        msg = "💙 支付宝支付成功"
        
    # 2. 微信支付
    elif method == "wechat":
        print("💚 正在唤起微信支付...")
        msg = "💚 微信支付成功"
        
    # 3. 银行卡支付
    elif method == "bank_card":
        print("💳 正在校验您的银行卡信息...")
        if actual_amount >= 100: # 满减活动
            actual_amount = actual_amount - 5
            msg = "💳 银行卡支付成功 (触发满100立减5元优惠)"
            print("🎉 恭喜！已为您立减 5 元！")
        else:
            msg = "💳 银行卡支付成功"
            
    # 4. QQ钱包
    elif method == "qq":
        print("🐧 正在连接QQ钱包...")
        cut = round(random.uniform(0.5, 3.0), 2) # 随机生成 0.5 到 3 元
        actual_amount = actual_amount - cut
        msg = f"🐧 QQ钱包支付成功 (触发随机立减 {cut} 元)"
        print(f"🎉 恭喜！随机立减了 {cut} 元！")
        
    # 5. 银联支付
    elif method == "unionpay":
        print("🏦 正在接入银联云闪付...")
        actual_amount = actual_amount * 0.98 # 打 98 折
        msg = "🏦 银联支付成功 (享受全场98折专属优惠)"
        print("🎉 已为您应用银联专属 98 折优惠！")
        
    # 6. 分期付款
    elif method == "installment":
        print("📅 正在为您办理信用卡分期业务...")
        actual_amount = actual_amount * 0.99 # 打 99 折
        msg = "📅 分期付款成功 (享受免息99折)"
        print("🎉 已为您办理3期免息，并享受 99 折优惠！")
        
    # 7. 未知方式
    else:
        print("⚠️ 未知的支付方式，正在尝试默认扣款...")
        msg = "默认支付成功"
        
    # 打印账单明细
    print(f"\n💵 原始应付: ￥{amount}")
    print(f"💵 优惠后实付: ￥{round(actual_amount, 2)}")
    
    # 返回结果字典
    return {"success": True, "actual": round(actual_amount, 2), "msg": msg}
