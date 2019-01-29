from operator import attrgetter
from itertools import groupby
import numpy as np
from py2neo import authenticate, Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
import wiki_scape
import neoViz
from neoViz import draw

# set up authentication parameters
#authenticate("localhost:7474", "user", "pass")

# connect to authenticated graph database
sgraph = Graph("http://localhost:7474/db/data/")

class Team(GraphObject):
    __primarykey__ = "name"

    def __init__(self, name): self.name = name

    name = Property()
    conference = Property()
    division = Property()

    gave = RelatedTo("Team")
    received = RelatedTo("Team")
    traded = RelatedTo("Team")
    #traded_to = RelatedTo("Team")

teamList = ['Hawks','Celtics','Nets','Hornets','Bulls','Cavaliers','Mavericks','Nuggets','Pistons','Warriors','Rockets','Pacers','Clippers','Lakers','Grizzlies','Heat','Bucks','Timberwolves','Pelicans','Knicks','Thunder','Magic','76ers','Suns','Blazers','Kings','Spurs','Raptors','Jazz','Wizards']
eastList = ['Hawks','Celtics','Nets','Hornets','Bulls','Cavaliers','Pistons','Pacers','Heat','Bucks','Knicks','Magic','76ers','Raptors','Wizards']
southeastList = ['Hawks','Heat','Wizards','Hornets','Magic']
atlanticList = ['Celtics','Nets','Knicks','76ers','Raptors']
centralList = ['Bulls','Cavaliers','Pacers','Bucks','Pistons']
southwestList = ['Mavericks','Spurs','Rockets','Grizzlies','Pelicans']
northwestList = ['Thunder','Blazers','Jazz','Nuggets','Timberwolves']
pacificList = ['Clippers','Lakers','Kings','Suns','Warriors']

matches = []
allDraft = []
tradeMonth = []
for r in wiki_scape.resultNew:
    #matches the index of the team name
    tradeMonth.append(r[0])
    mymatch = [x for x, y in enumerate(teamList) if y in r]
    matches.append(mymatch)
    #determines if a first or second round pick was received
    draft = []
    print(r)
    if len(r) > 3:
        if r[1] == "first" or r[2] == "first" or r[3] == "first":
            draft.append(1)
        else:
            draft.append(0)
        if r[2] == "second" or r[2] == "second" or r[3] == "second":
            draft.append(2)
        else: draft.append(0)
    else:
        if r[1] == 'first':
            draft.append(1)
        else:
            draft.append(0)
        if r[1] == 'second':
            draft.append(2)
        else:
            draft.append(0)
    print(draft)
    allDraft.append(draft)

print(wiki_scape.resultNew)
print(tradeMonth)
print(matches)
print(allDraft)

allTrades = []
for j in range(0,len(matches)):
    allTrades.append(Team(teamList[matches[j][0]]))
    allTrades.append(Team(teamList[matches[j][1]]))

print(allTrades)

for a in allTrades:
    if a.name in eastList: a.conference = "East"
    else: a.conference = "West"

for a in allTrades:
    if a.name in southeastList: a.division = "Southeast"
    elif a.name in atlanticList: a.division = "Atlantic"
    elif a.name in centralList: a.division = "Central"
    elif a.name in southwestList: a.division = "Southwest"
    elif a.name in northwestList: a.division = "Northwest"
    elif a.name in pacificList: a.division = "Pacific"

for j in range(0,len(matches)):
        #allTrades[j * 2].gave.update(allTrades[j * 2 + 1], properties={"month": tradeMonth[j], "year": 2016, "draft": allDraft[j][1]})
        #allTrades[j * 2 + 1].received.update(allTrades[j * 2], properties={"month": tradeMonth[j], "year": 2016, "draft": allDraft[j][0]})
        sgraph.merge(Relationship(allTrades[j * 2].__ogm__.node, "TRADED", allTrades[j * 2 + 1].__ogm__.node, month=tradeMonth[j], year=2016, draft=allDraft[j][1]))
        sgraph.merge(Relationship(allTrades[j * 2 + 1].__ogm__.node, "TRADED", allTrades[j * 2].__ogm__.node, month=tradeMonth[j], year=2016, draft=allDraft[j][0]))

# for t in teams:
#     sgraph.push(t)
options = {"Team": "name"}

draw(sgraph, options, physics=True, limit=100)