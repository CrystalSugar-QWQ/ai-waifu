

def sport_chosse(text):
    sport = 0
    if "看右下方" in text:
        sport = 1
        print("动作" + sport)
    elif "看左下方" in text:
        sport = 2
        print("动作" + sport)
    elif "看右上方" in text:
        sport = 3
        print("动作" + sport)
    elif "看左上方" in text:
        sport = 4
        print("动作" + sport)
    elif "看向下方" in text:
        sport = 5
        print("动作" + sport)
    elif "看向上方" in text:
        sport = 6
        print("动作" + sport)
    elif "看向右侧" in text:
        sport = 7
        print("动作" + sport)
    elif "看向左侧" in text:
        sport = 8
        print("动作" + sport)
    elif "皱起眉头" in text:
        sport = 9
        print("动作" + sport)
    elif "向左歪头" in text:
        sport = 10
        print("动作" + sport)
    elif "向右歪头" in text:
        sport = 11
        print("动作" + sport)
    elif "左右摇头" in text:
        sport = 12
        print("动作" + sport)
    return sport
