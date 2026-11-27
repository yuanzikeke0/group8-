# ==========================================
# 文件：shop.py
# 功能：商品大厅展示、商品详情资质、用户评价查看
# ==========================================
import database # 导入数据库模块

def browse_products(uid):
    """展示商品列表及猜你喜欢推荐"""
    print("\n========================================")
    print("          🛍️ 欢迎来到商品大厅")
    print("========================================")
    
    print("🌟 [猜你喜欢] (基于偏好/热销):")
    
    # 获取当前用户的偏好设置
    prefs = []
    if uid is not None:
        prefs = database.user_db[uid].get("preferences", [])
    
    recs = [] # 存放推荐商品
    if len(prefs) > 0:
        # 如果用户有偏好，筛选出对应分类的商品
        for p in database.products:
            if p["category"] in prefs:
                recs.append(p)
        # 如果筛选后没有商品，按销量降序推荐爆款
        if len(recs) == 0:
            print("  (没有找到符合偏好的商品，为您推荐爆款)")
            recs = sorted(database.products, key=lambda x: x["sales"], reverse=True)
    else:
        # 如果用户没登录或没设置偏好，直接按销量降序推荐
        recs = sorted(database.products, key=lambda x: x["sales"], reverse=True)
        
    # 打印最多前两个推荐商品
    for i in range(min(2, len(recs))):
        r = recs[i]
        print(f" ⭐ [推荐] {r['name']} | ￥{r['price']} (热销:{r['sales']}件)")
    
    print("\n--- 全部商品列表 ---")
    # 遍历打印所有商品基本信息
    for p in database.products:
        print(f"ID:{p['id']} | {p['name']} [{p['category']}] | ￥{p['price']}")

def view_product_detail(pid):
    """查看商品详情，包含资质与历史评价"""
    print(f"\n--- 🔍 正在加载商品 ID:{pid} 的详情 ---")
    product = None
    # 在数据库中查找对应的商品
    for p in database.products:
        if p["id"] == pid:
            product = p
            break
            
    if product is None:
        print("❌ 商品不存在！")
        return
        
    # 打印商品详情
    print(f"📦 商品名称: {product['name']}")
    print(f"📝 分类描述: {product['desc']}")
    print(f"💰 商品价格: ￥{product['price']}")
    
    # 打印厂商资质
    print("\n🛡️ 厂商资质认证:")
    for cert in product["certs"]:
        print(f"  ✓ {cert}")
        
    # 打印可选规格
    print("\n📏 可选规格:")
    for opt in product["options"]:
        print(f"  - {opt}")
        
    # 打印历史评价
    print("\n⭐ 历史用户评价:")
    if pid in database.reviews_db:
        for r in database.reviews_db[pid]:
            print(f"  [{r['rating']}星] 用户{r['user']}: {r['text']}")
    else:
        print("  暂无评价，快来抢首评吧！")
