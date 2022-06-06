def getScore(myInfo, myIdeal, myHobby, userInfo, userIdeal, userHobby):
    idealDelta = 0
    hobbyDelta = 0
    for i, prop in enumerate(myInfo):
        idealDelta += abs(prop - userIdeal[i])
    for i, prop in enumerate(userInfo):
        idealDelta += abs(prop - myIdeal[i])
    for i, prop in enumerate(myHobby):
        hobbyDelta += abs(prop - userHobby[i])

    totalScore = 0.7 * idealDelta + 0.3 * hobbyDelta
    print(0.7 * idealDelta + 0.3 * hobbyDelta)
    return totalScore
