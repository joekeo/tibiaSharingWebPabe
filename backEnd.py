# import libraries
import urllib2
import json

#retrieve the information of a character an parse it into an character object name.data
def getCharacter(name):
    Char = []
    name = name.replace(' ', '+')
    charUrl = 'https://api.tibiadata.com/v2/characters/' + name + '.json'
    charPage = urllib2.urlopen(charUrl)
    html = charPage.read()
    j = json.loads(html)
    #retreive the character info and try to get the guild if any
    Char.append(j['characters']['data']['name'])
    Char.append(j['characters']['data']['level'])
    Char.append(j['characters']['data']['vocation'])
    Char.append(j['characters']['data']['world'])
    try:
        Char.append(j['characters']['data']['guild']['name'])
    except:
        pass
    return Char

#the argument in item specifies the column to sort the matrix of characters
def getKey(item):
    return item[1]

def getHuntingPals(name):
    Char = getCharacter(name)
    level = Char[1]
    voc = Char[2]
    world = Char[3]
    if len(Char) == 5:
        guild = Char[4]
    else:
        guild = ' '
    #get the world players
    worldUrl = 'https://api.tibiadata.com/v2/world/' + world + '.json'
    worldPage = urllib2.urlopen(worldUrl)
    html = worldPage.read()
    j = json.loads(html)

    #get the number of players
    cOnline = len(j['world']['players_online'])
    #create a matrix to temporarily store the online players information
    #and sorth the players by vocation
    w, h = 4, cOnline;
    charactersOnline = [[0 for x in range(w)] for y in range(h)]
    knights = []
    sorcerers = []
    druids = []
    paladins = []
    print str(cOnline), 'Players online'
    getGuild = 0
    for i in range(0, cOnline):
        #print j['world']['players_online'][i]['name'], j['world']['players_online'][i]['level'], j['world']['players_online'][i]['vocation']
        charactersOnline[i][0] = j['world']['players_online'][i]['name']
        charactersOnline[i][1] = j['world']['players_online'][i]['level']
        charactersOnline[i][2] = j['world']['players_online'][i]['vocation']
        #sort by vocation jus tthe characters with sharing level min of your char (2/3) and max (3/2) or yours
        if ( int(charactersOnline[i][1]) >= (int(level)*2/3) and int(charactersOnline[i][1]) <= (int(level)*3/2)):

            #check if they have a guild or not
            if getGuild == 1:
                try:
                    charactersOnline[i][3] = getCharacter(charactersOnline[i][0])[4]
                except:
                    charactersOnline[i][3] = ' '
            else:
                charactersOnline[i][3] = ' '


            if (charactersOnline[i][2] == 'Elite Knight' or charactersOnline[i][2] == 'Knight'):
                knights.append([charactersOnline[i][0],charactersOnline[i][1],charactersOnline[i][3]])

            elif (charactersOnline[i][2] == 'Master Sorcerer' or charactersOnline[i][2] == 'Sorcerer'):
                sorcerers.append([charactersOnline[i][0],charactersOnline[i][1],charactersOnline[i][3]])

            elif (charactersOnline[i][2] == 'Elder Druid' or charactersOnline[i][2] == 'Druid'):
                druids.append([charactersOnline[i][0],charactersOnline[i][1],charactersOnline[i][3]])

            elif (charactersOnline[i][2] == 'Royal Paladin' or charactersOnline[i][2] == 'paladin'):
                paladins.append([charactersOnline[i][0],charactersOnline[i][1],charactersOnline[i][3]])

    return charactersOnline, knights,sorcerers,paladins,druids


def main():
    doIt = getHuntingPals('General Direction')
    print 'Knights:',sorted(doIt[1],key=getKey)
    print 'Sorcerers:',sorted(doIt[2],key=getKey)
    print 'Paladins',sorted(doIt[3],key=getKey)
    print 'Druids:',sorted(doIt[4],key=getKey)


if __name__ == "__main__":
    main()
