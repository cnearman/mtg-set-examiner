'''
Created on Jul 16, 2012

@author: Everybody
'''

from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy

COLORED_MANA_COEF = 1.0/1.7

def main():
    book = open_workbook('Magic2013.xls')
    card_list = book.sheet_by_index(0)
    workbook = copy(book)
    blocksheet = workbook.add_sheet('Block List')
    
    creature_list = build_creature_list(card_list)
    build_blocks(creature_list,blocksheet)
    
    workbook.save('new2.xls')
    
    book = open_workbook('new2.xls')
    blocksheet = book.sheet_by_name('Block List')
    workbook = copy(book)
    combatsheet = workbook.add_sheet('Combat Exchanges')
    combat_numbers(blocksheet, creature_list, combatsheet)
    workbook.save('new3.xls')
                  
def combat_numbers(blocks, clist, combatsheet):
    for col_index in range(blocks.ncols):
        if col_index != 0:
            combatsheet.write(0, col_index,clist[col_index - 1][0])
        
        combatsheet.write(col_index, 0, clist[col_index - 1][0])
        for row_index in range(blocks.nrows):
            if blocks.cell(row_index, col_index).value == 'X':
                creature1 = clist[row_index - 1]
                creature2 = clist[col_index - 1]
                
                'Pro-Black'
                if creature2[9] == 1 and creature1[4] == 'B':
                    if creature2[1] >= creature1[2]:
                        combatsheet.write(row_index, col_index, 'C')
                    else:
                        combatsheet.write(row_index, col_index, 'D')
                    'Pro-White'        
                elif creature2[10] == 1 and creature1[4] == 'U':
                    if creature2[1] >= creature1[2]:
                        combatsheet.write(row_index, col_index, 'C')
                    else:
                        combatsheet.write(row_index, col_index, 'D')
                
                    'Stuffy Doll'
                elif creature2[0] == 218:
                    combatsheet.write(row_index, col_index, 'D')
                        
                    'Attacker kills blocker'
                elif creature1[1] >= creature2[2] and creature2[1] < creature1[2]: 
                    combatsheet.write(row_index, col_index,'A')
                    
                    'Attacker and Blocker die'
                elif creature1[1] >= creature2[2] and creature2[1] >= creature1[2]:
                    combatsheet.write(row_index, col_index,'B')
                    
                    'Attacker only dies'
                elif creature1[1] < creature2[2] and creature2[1] >= creature1[2]:
                    combatsheet.write(row_index, col_index,'C')
                    
                    'Neither die'
                else:
                    combatsheet.write(row_index, col_index,'D')
                      
def build_blocks(clist,sheet):
    column = 1
    for creature in clist:
        sheet.write(0, column, creature[0])
        sheet.write(column, 0, creature[0])
        row = 1
        for creature2 in clist:
            sheet.write(column, row, can_block(creature, creature2))
            row += 1
        column += 1
        
def can_block(creature, creature2):
    indexes = [4,5,6,7,8,9,10,11]
    color, flying, reach, unblock, cant_block, prot_black, prot_white, defender = (creature[i] for i in indexes)            
    color2, flying2, reach2, unblock2, cant_block2, prot_black2, prot_white2, defender2 = (creature2[i] for i in indexes)
    intimidate = creature[12]
    if defender == 1:
        return 'N'
    elif intimidate == 1 and (color2 != 'N/A') and (color != color2):
        return 'E'
    elif (flying == 1 and (flying2 == 0 and reach2 == 0)):
        return 'E'
    elif cant_block2 == 1:
        return 'E'
    elif prot_black == 1 and color2 == 'B':
        return 'E'
    elif prot_white == 1 and color2 == 'W':
        return 'E'
    elif unblock == 1:
        return 'E'
    else: 
        return 'X'
    
def build_creature_list(sheet):
    creatures = []
    for row_index in range(sheet.nrows):
        current = sheet.row_values(row_index,0)
        if 'Creature' in current[2]:
            num = int(current[0])
            power = set_pow_tough(current[3])
            tough = set_pow_tough(current[4])
            cost = set_altered_cost(current[5])
            color = current[7]
            flying = 1 if 'Flying.' in current[8] else 0
            reach = 1 if 'Reach.' in current[8] else 0
            unblock = 1 if 'Unblockable.' in current[8] else 0
            cant_block = 1 if 'Can\'t Block.' in current [8] else 0
            prot_black = 1 if 'Protection from black' in current[8] else 0
            prot_white = 1 if 'Protection from white' in current[8] else 0
            defender = 1 if 'Defender' in current[8] else 0
            intimidate = 1 if 'Intimidate' in current[8] else 0
                
            t = num, power, tough, cost, color, flying, reach, unblock, cant_block, prot_black, prot_white, defender, intimidate
            creatures.append(t)
    return creatures
            
def set_pow_tough(curr):
    if curr == '*':
        return '*'
    else:
        return int(curr)

def set_altered_cost(cost):
    cmc = 0
    try:
        cmc = int(cost)
    except ValueError:
        color = 0
        for char in cost:
            if char.isdigit():
                cmc += int(char)
            else:
                cmc += 1
                color += 1
        if cmc < 7:
            cmc += round(color * COLORED_MANA_COEF,2)
    finally:
        return cmc 
            
if __name__ == "__main__":
    main()