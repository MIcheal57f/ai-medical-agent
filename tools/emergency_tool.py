def is_emergency(text):

    high_risk = [
        "胸痛", "胸闷", "呼吸困难", "窒息感",
        "昏迷", "意识模糊", "抽搐", "失去意识",
        "剧烈头痛", "爆炸性头痛",
        "持续高烧", "高烧不退",
        "呕血", "便血",
        "心跳过快", "心律不齐"
    ]

    medium_risk = [
        "头晕", "乏力", "恶心",
        "咳嗽", "发烧", "腹痛"
    ]

    # 高危 → 直接拦截
    for k in high_risk:
        if k in text:
            return "high"

    # 中风险
    for k in medium_risk:
        if k in text:
            return "medium"

    return "low"