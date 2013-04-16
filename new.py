'''
Created on Dec 23, 2012

@author: Chris Nearman
'''

from sets import Set
import csv

COLORED_MANA_COEF = 1.0/0.7

class Graph():
    allCards =[]
    edges = {}
    blocks = []
    creatures = []
    
    def __init__(self, _filename):
        
        #Constructs list of Each Card in Set
        with open(_filename, 'rb') as cardlist:
            cardBuilder = csv.reader(cardlist)
            for row in cardBuilder:
                if(row[0] != '#'):
                    currentCard = Card(row)
                    self.allCards.insert(currentCard.cardNumber, currentCard)
     
    #Prints AllCards from the set            
    def __str__(self):
        result = ""
        for card in self.allCards:
            result += str(card) + "\n"
        return result
        
class Edge:
    ABlock = '1'
    BBlock = '2'
    CBlock = '3'
    DBlock = '4'
    NullBlock = -1
    
    fromCard = None
    toCard = None
    edgeType = NullBlock
    
    def __init__(self, f, t, edgetype):
        self.fromCard = f
        self.toCard = t
        self.edgeType = edgetype
        f.outdegree += 1
        t.indegree += 1
    
    def __str__(self):
        return '<' + str(self.fromCard) + ', ' + str(self.toCard) + ', ' + self.edgeType + '>'
    
class MetaEdge:
    fromCard = None
    toEdge = None
    
class Card:
    raw = ""
    cardNumber = 0
    cardName = ""
    type = ""
    pt = (0,0)
    cost = ""
    cmc = 0
    alteredCost = 0
    rarity = ""
    color = []
    keywords = ""
    otherAbilities = "" #Separate from evergreen keywords
    evasionPotentials = []
    creatureNumber = -1
    
    indegree = 0 #how many creatures this can block
    outdegree = 0 #how many creatures this can be blocked by
    
    def __str__(self):
        return str(self.cardNumber) + ". " + self.cardName
    
    def __init__(self, row):
        self.raw = row
        self.setCardNumber(row[0])
        self.setCardName(row[1])
        self.setType(row[2])
        self.setPowerToughness(row[3],row[4])
        self.setCost(row[5])
        self.setCMC()
        self.setRarity(row[6])
        self.setKeywords(row[7])
        self.setColor()
    
    def setCardNumber(self, number):
        self.cardNumber = int(number)
    
    def setCardName(self, name):
        self.cardName = name
    
    def setType(self, cType):
        self.type = cType
    
    def setPowerToughness(self, power, tough):
        if(power.isdigit() and tough.isdigit()):
            self.pt = int(power), int(tough)
        else:
            self.pt = power, tough
    
    def setCost(self, cost):
        self.cost = cost
    
    def setRarity(self, rarity):
        self.rarity = rarity
    
    def setCMC(self):
        #Needs to set CMC and AlteredCost
        cmc = 0
        try:
            cmc = int(self.cost)
        except ValueError:
            color = 0
            for char in self.cost:
                if char.isdigit():
                    cmc += int(char)
                else:
                    cmc += 1
                    color += 1
            if cmc < 7:
                cmc += round(color * COLORED_MANA_COEF,2)
        finally:
            self.cmc = cmc
            
    def setColor(self):
        self.color = Set([])
        for char in self.cost:
            if not char.isdigit():   
                if char == 'W':
                    self.color.add('white')
                elif char == 'U':
                    self.color.add('blue')
                elif char == 'B':
                    self.color.add('black')
                elif char == 'R':
                    self.color.add('red')
                else:
                    self.color.add('green')
                    
    def isColor(self, otherColor):
        return otherColor in self.color
        
    def setKeywords(self, keywords):
        self.keywords = keywords
    
    def setOtherAbilities(self, otherAbilities):
        self.otherAbilities = otherAbilities
        
    def hasProtectionFrom(self, otherCard):
        if otherCard.color:
            for color in otherCard.color:
                print 'Protection from ' + color
                print self.keywords
                if 'Protection from ' + color in self.keywords: 
                    return True
            return False
        else:
            if 'Protection from artifact' in self.keywords:
                return True
            else:
                return False
            
    def isFlying(self):
        return 'Flying' in self.keywords
    
    def isDefender(self):
        return 'Defender' in self.keywords
    
    def isUnblockable(self):
        return 'Unblockable' in self.keywords
    
    def cantBlock(self):
        return 'Can\'t Block' in self.keywords
    
    def hasIntimidate(self): 
        return 'Intimidate' in self.keywords
    
    def isIndestructible(self):
        return 'Indestructible' in self.keywords
    
    def isCreature(self):
        return 'Creature' in self.type
    
    def shareColor(self, otherCard):
        for color in self.color:
            for otherColor in otherCard.color:
                if color == otherColor:
                    return True
        return False
    
    def hasReach(self):
        return 'Reach' in self.keywords
    
    def canKill(self, otherCard):
        if self.pt[0] >= otherCard.pt[1]:
            return True
        else:
            return False
        
    def isLegendary(self):
        return 'Legendary' in self.type
    
def main():
    MSet = Graph('Magic2013.csv')
    print MSet
    print MSet.allCards[217].cardName
    print MSet.allCards[217].isIndestructible()
    print MSet.allCards[95].hasProtectionFrom(MSet.allCards[1])
    
if __name__ == '__main__':
    main()