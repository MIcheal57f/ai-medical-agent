def analyze_symptom(text):

    mapping = {
        "头痛": "可能与疲劳、偏头痛或感冒有关",
        "咳嗽": "可能是感冒或支气管炎",
        "发烧": "可能存在感染（病毒或细菌）",
        "腹痛": "可能与胃肠道问题有关",
        "胸痛": "可能涉及心血管或呼吸系统",
        "头晕": "可能与低血压或疲劳有关",
        "乏力": "可能与睡眠不足或感染有关",
        "恶心": "可能与消化系统问题有关",
    }

    results = []

    for key in mapping:
        if key in text:
            results.append(mapping[key])

    if results:
        return "；".join(results)

    return "症状信息不足，建议补充描述"