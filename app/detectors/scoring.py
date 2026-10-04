def score_signals(signals, weights):
    score = sum(weights.get(name, 0) for name, fired in signals.items() if fired)
    score = min(100, score)
    if score >= 70: level="Critical"
    elif score >= 40: level="Warning"
    else: level="Normal"
    return score, level
