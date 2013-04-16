'''
Created on Dec 24, 2012

@author: Everybody
'''

from new import *
import sys

class M2013(Graph):
    def __init__(self, _filename):
        Graph.__init__(self,_filename)
        
        #Constructs general block and evasion stucture
        ccn = 0
        for fcard in self.allCards:
            if(fcard.isCreature()):
                fcard.creatureNumber = ccn
                ccn += 1
                self.creatures.append(fcard)
                interior = [] 
                for scard in self.allCards:    
                    if(scard.isCreature()):
                        result = self.can_block(fcard, scard)
                        if result == 'X':
                            if not fcard in self.edges:
                                self.edges[fcard] = []
                            self.edges[fcard].append(Edge(fcard,scard,self.combat_result(fcard,scard)))
                        interior.append(result)
                self.blocks.append(interior)
                fcard.evasionPotentials = interior                    
    
    def printOut(self, file):
        for card in self.allCards:
            file.write(str(card.raw) + "\n")
        
        for allblock in self.blocks:
            for block in allblock:
                file.write(block)
            file.write("\n")
        
        for k in self.edges.keys():
            for e in self.edges[k]:
                file.write(str(e) + '\n')
            
    def can_block(self, card1, card2):
        if card1.isDefender():
            return 'N'
        elif card1.isLegendary() and card1 is card2:
            return 'N'
        elif card1.hasIntimidate() and card1.shareColor(card2):
            return 'E'
        elif card1.isFlying() and (not card2.isFlying() and not card2.hasReach()):
            return 'E'
        elif card2.cantBlock():
            return 'E'
        elif card1.hasProtectionFrom(card2):
            return 'E'
        elif card1.isUnblockable() or card1.cardNumber == 70: #Stormtide Leviathan
            return 'E'
        elif card2.cardNumber == 79 and not card1.isFlying(): #Welkin Tern
            return 'E'
        else:
            return 'X'
        
    def combat_result(self, card1, card2): 
        if card2.hasProtectionFrom(card1):
            if card2.canKill(card1):
                return '3'
            else:
                return '4'
        elif card2.isIndestructible(): #Stuffy Doll
            if card2.canKill(card1):
                return '3'
            else:
                return '4'
        elif card1.isIndestructible():
            if card1.canKill(card2):
                return '1'
            else:
                return '4'
        elif card1.canKill(card2) and not card2.canKill(card1):
            return '1'
        elif card1.canKill(card2) and card2.canKill(card1):
            return '2'
        elif not card1.canKill(card2) and card2.canKill(card1):
            return '3'
        else:
            return '4'
        
        
def main():
    file = open('m13.txt', 'w')
    M2013Set = M2013('new3.csv')
    M2013Set.printOut(file)
    with open('m13nodes.csv', 'wb') as csvfile1:
        csvout = csv.writer(csvfile1)
        csvout.writerow(['Id', 'Label', 'power', 'toughness', 'cost', 'keywords'])
        for card in M2013Set.allCards:
            if card.isCreature():
                csvout.writerow([card.cardNumber, card.cardName, card.pt[0], card.pt[1], card.cost, card.keywords])
    with open('m13edges.csv', 'wb') as csvfile2:
        csvout = csv.writer(csvfile2)
        csvout.writerow(['Id','Source', 'Target', 'Weight'])
        i = 0
        for k in M2013Set.edges.keys():
            for v in M2013Set.edges.get(k):
                csvout.writerow([i, k.cardNumber, v.toCard.cardNumber, v.edgeType])
                i += 1
            
if __name__ == '__main__':
    main()