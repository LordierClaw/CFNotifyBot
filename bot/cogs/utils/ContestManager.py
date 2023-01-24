import datetime, pytz

class ContestManager():
    __contests = {}
    __isContestsUpdated = 0

    def __init__(self) -> None:
        pass

    @staticmethod
    def getContests():
        import requests
        response = requests.api.get("https://codeforces.com/api/contest.list")
        if response.status_code == 200:
            ContestManager.__contests = response.json()
            ContestManager.__isContestsUpdated = 1
        return response.status_code

    @property
    def isContestsUpdated():
        return ContestManager.__isContestsUpdated

    @staticmethod
    def filter():
        if (ContestManager.__isContestsUpdated == 0): return
        for i in range(len(ContestManager.__contests["result"])-1, -1, -1):
            if (ContestManager.__contests["result"][i]["phase"] != "BEFORE"):
                ContestManager.__contests["result"].pop(i)
    
    @staticmethod
    def parseData(contest:list()):
        id = contest["id"]
        name = contest["name"]
        duration = str(datetime.timedelta(seconds=contest["durationSeconds"]))
        startTime = datetime.datetime.fromtimestamp(contest["startTimeSeconds"], tz=pytz.timezone("Asia/Ho_Chi_Minh"))
        relativeTime = contest["relativeTimeSeconds"]
        return id, name, duration, startTime, relativeTime
    
    @staticmethod
    def saveLocal():
        if (ContestManager.__isContestsUpdated == 0): return
        import json
        data = open("./database.json", "w")
        json.dump(ContestManager.__contests, data, indent=2)
        data.close()
    
    @staticmethod
    def loadLocal():
        import json
        data = open("./database.json", "r")
        ContestManager.__contests = json.load(data)
        ContestManager.filter()

    @staticmethod
    def setup():
        ContestManager.getContests()
        ContestManager.filter()

    @staticmethod
    def getUpcomingInfor():
        return ContestManager.parseData(ContestManager.__contests["result"][-1])

    @staticmethod
    def contestsToday():
        contests = []
        currentTime = datetime.datetime.now(tz=pytz.timezone("Asia/Ho_Chi_Minh"))
        for i in range(len(ContestManager.__contests["result"])):
            contest = ContestManager.__contests["result"][i]
            startTime = datetime.datetime.fromtimestamp(contest["startTimeSeconds"], tz=pytz.timezone("Asia/Ho_Chi_Minh"))
            if startTime.date() == currentTime.date():
                contests.append(contest)
        return contests