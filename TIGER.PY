# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 12:17:58 2020

@author: SAURAV
"""
class board:
    def __init__(s):
        s.points=Points()
        s.kill=Kills()
        s.tiger=1
        s.goats=3
        s.tiger_pos='A'
        s.goat1_pos='I'
        s.goat2_pos='H'
        s.goat3_pos='J'
        s.current_pos=[s.tiger_pos,s.goat1_pos,s.goat2_pos,s.goat3_pos]
    #def __repr__(s):
        s.original_shape='''            
                            A
                           * *
                          * * *
                         *  *  *
                        *   *   *
                       *    *    *
                      B *** C *** D
                     *             *
                    *               *
                   *                 *
                  *                   *
                 *                     *
                *                       *
               *                         *
              E *********** F *********** G
                            *
                            *
                            *
                            *
                            *
           H ************** I ************** J
        
            '''
        s.current_shape='''            
                            o
                           * *
                          * * *
                         *  *  *
                        *   *   *
                       *    *    *
                      o *** o *** o
                     *             *
                    *               *
                   *                 *
                  *                   *
                 *                     *
                *                       *
               *                         *
              o *********** o *********** o
                            *
                            *
                            *
                            *
                            *
           o ************** o ************** o
        
            '''
            
        s.go_back='''            
                            o
                           * *
                          * * *
                         *  *  *
                        *   *   *
                       *    *    *
                      o *** o *** o
                     *             *
                    *               *
                   *                 *
                  *                   *
                 *                     *
                *                       *
               *                         *
              o *********** o *********** o
                            *
                            *
                            *
                            *
                            *
           o ************** o ************** o
        
            '''

#--------------------------------------------------------------------------------------------------------------------       
def changes_in_goat(s):
    for i in range(len(s.original_shape)):
        if s.original_shape[i] in s.current_pos:
            s.current_shape =s.current_shape[:i]+s.original_shape[i]+s.current_shape[i+1:]
    print("It is reference: ",s.original_shape.ljust(40),"\nIt is Current Position:",s.current_shape.rjust(40))
    s.current_shape=s.go_back
    
#-------------------------------------------------------------------------------------------------------------------

def move_goat(s):
    s.current_pos=[s.tiger_pos,s.goat1_pos,s.goat2_pos,s.goat3_pos]
    print("\n\t\t  Tiger is at ",s.current_pos[0])
    for i in range(1,len(s.current_pos)):
        if(s.current_pos[i]=='o'):
            print('\n\t\tGoat ',i," has been kileed by tiger")
        else:
            print("\n\n\t*****     Goat ",i," at ",s.current_pos[i],"      *******")
    goat=input("\tPlease enter which goat do you want to move(enter position of that goat):")
    while(goat=='o'):
        print('\tThis goat has been killed by tiger....select other goat...')
        goat=input(" ")
    if goat in s.current_pos and goat!=s.tiger_pos:
        print("\tpossible moves available:",end="  ")
        possible_moves=[ i for i in s.points[goat] if i not in s.current_pos]
        if('o' in possible_moves):
            possible_moves=possible_moves.remove('o')
        if not possible_moves:
            print("\nNo options available for this goat:\n Select other goat")
            move_goat(s)
        else: 
            for i in possible_moves:
                print(i,end="\t")
        print("\nEnter your choice(position at which you want to move):")
        i=3
        while(i!=0):
            my_move=input()
            if my_move in possible_moves and my_move not in s.current_pos:
                i=0
                loc=s.current_pos.index(goat)+1
                if (loc==2):
                    s.goat1_pos=my_move
                    s.current_pos[1]=my_move
                elif(loc==3):
                    s.goat2_pos=my_move
                    s.current_pos[2]=my_move
                elif(loc==4):
                    s.goat3_pos=my_move
                    s.current_pos[3]=my_move
                break
            else:
                print("Your input is incorrect....re enter your choice...")
                i-=1
                
    else:
        move_goat(s)


#----------------------------------------------------------------------------------------------------------------------            


def killing_move(s,i,j):
           print('none')
           if(s.goat1_pos==i):
               s.goat1_pos='o'
               print("Goat 1 at position ",i," has been killed by tiger")
           elif(s.goat2_pos==i):
               s.goat2_pos='o'
               print("Goat 2 at position ",i," has been killed by tiger")
           elif(s.goat3_pos==i):
               s.goat3_pos='o'
               print("Goat 3 at position ",i," has been killed by tiger")
           s.tiger_pos=j
           s.current_pos=[s.tiger_pos,s.goat1_pos,s.goat2_pos,s.goat3_pos]
           changes_in_goat(s)


#----------------------------------------------------------------------------------------------------------------------


def moves_for_tiger(s):
    s.possible_tiger_moves=[i for i in s.points[s.tiger_pos] if i not in s.current_pos]
    #print("possible moves available for tiger:",s.possible_tiger_moves)
    s.tiger_neighbours=s.points[s.tiger_pos]
    for i in s.tiger_neighbours:
        if i in s.current_pos and i!='A':
            for j in s.kill[s.tiger_pos]:
                if j not in s.current_pos:
                    if j in s.points[i]:
                        killing_move(s,i,j)
                        return True
    return False

#--------------------------------------------------------------------------------------------------------------------
def cal_heuristic(s,list1):
    hue_val=[]
    for i in list1:
        if i in s.current_pos:
            if(moves_for_tiger(s)):
                hue_val.append(100)
            else:
                hue_val.append(0)
                
        else:
            val=50
            point=i
            for j in range(1,len(s.current_pos)):
                if(s.current_pos[j]!='o'):
                    if point in s.points[s.current_pos[j]]:
                        val=val-10
            hue_val.append(val)
    return hue_val
            

#--------------------------------------------------------------------------------------------------------------------


def AI_Tiger(s):
    s.next_possible_move=s.points[s.tiger_pos]
    #Using HILL CLIMBING ALGORITHM to select next move...........
    n=len(s.next_possible_move)
    heuristic_value=[0 for _ in range(n)]
    heuristic_value=cal_heuristic(s,s.next_possible_move)
    max_hue_val=max(heuristic_value)
    if max_hue_val==100:
        "\n\t\t<<<<Tiger has killed Goat>>>"
    else:
        which_move=max(heuristic_value)
        ind=heuristic_value.index(which_move)
        go_tiger_at=s.next_possible_move[ind]
        s.tiger_pos=go_tiger_at
        s.current_pos=[s.tiger_pos,s.goat1_pos,s.goat2_pos,s.goat3_pos]
        changes_in_goat(s)


#---------------------------------------------------------------------------------------------------------------------
def check_stuck(s):
    possible_moves=[i for i in s.points[s.tiger_pos] if i not in s.current_pos]
    if not possible_moves:
        return True
    elif(len(possible_moves)==1 and possible_moves[0]=='I'):
        return True
    else:
        return False
                

#-----------------------------------------------------------------------------------------------------------------

def Points():
    return {'A':['B','C','D'],'B':['A','C','E'],'C':['A','B','D'],'D':['A','C','G'],'E':['B','F'],'F':['E','G','I'],'G':['D','F'],'H':['I'],'J':['I'],'I':['F','H','J']}

#-------------------------------------------------------------------------------------------------------------------


def Kills():
    return {'A':['E','G'],'B':['D'],'D':['B'],'C':[],'E':['A','G'],'F':[],'G':['E','A'],'H':['J'],'J':['H'],'I':[]}

#--------------------------------------------------------------------------------------------------------------------

def set_of_rules():
    print("\n\t1. All goats can move to their neighbour nodes. They can take only only one step at once\n\t2. Tiger can take only one step to its neighbour nodes if, next neighbour node is empty.\n\t3. Tiger can kill any goat if any goat next to it has an empty neighbour and all (Tiger, Goat and neighbour) are linear.\n\t4. Tiger is stuck only if all neighbours of tiger are occupied by goats. In this case User is winner\n\t5. Tiger can't go to 'I' position.\n\t6. If tiger kills two goats then User Loses.")
    
#--------------------------------------------------------------------------------------------------------------------

def start():    
    print("*********\tWELCOME\t**********\n\tPRESS 1 FOR GAME RULES \n\tPRESS 2 to START GAME")
    inp=int(input("\tYour choice:"))
    if(inp==1):
        set_of_rules()
    elif(inp==2):
        b=board()
        total_moves=0
        while(True):
            move_goat(b)
            changes_in_goat(b)
            if(check_stuck(b)):
                print("\n\n\t\t*********  CONGRATULATIONS  **********\n\t\t********** YOU WON *********")
                print('\n\tNo. of moves taken ',total_moves)
                break
            AI_Tiger(b)
            if(b.current_pos.count('o')>=2):
                print('\t************AI Tiger won**********\n\t********Try next time...........*********\n \tNo. Of Moves Taken ',total_moves)
                break
            total_moves+=1 
    else:
        print("\tWrong Input")
        start()

#****************************************** THANK YOU**************************************************************    
start()