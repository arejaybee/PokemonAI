from Pokemon import Pokemon
import random
from time import sleep
import sys
def getItem(item, xpath):
    return item.find_element_by_xpath(xpath)

def makePokemonArray(arrayOfNames):
    retArray = []
    for name in arrayOfNames:
        name.replace("-Alola","") #for now ignore forms
        retArray.append(Pokemon(name.strip()))
    return retArray

class PokemonBattler:
    def __init__(self, theirTeam, driver, room, theirName):
        self.theirTeam = makePokemonArray(theirTeam)
        self.myTeam = [Pokemon("Pikachu"),Pokemon("Charizard"), Pokemon("Blastoise"), Pokemon("Venusaur"), Pokemon("Snorlax"), Pokemon("Espeon")]
        self.driver = driver
        self.theirName = theirName
        self.room = room
        self.BattleOptions = {"attk1" : None,
                "attk2" : None,
                "attk3" : None,
                "attk4" : None,
                "mega"  : None,
                "switch1" : None,
                "switch2" : None,
                "switch3" : None,
                "switch4" : None,
                "switch5" : None,
                "switch6" : None}
        self.chooseLead()
        while(not self.isBattleOver()):
            try:
                self.chooseAction()
            except:
                #print("No options to load!")
                sleep(10)
        print("And the winner is: "+self.winner)
        getItem(self.driver, "//*[@id=\"header\"]/div[2]/div/ul[2]/li/button").click()
    def isBattleOver(self):
        try:
            winText = getItem(self.driver, "//*[contains(text(), 'won the battle!')]")
            self.winner = winText.text.replace("won the battle!","") 
            return True
        except:
            return False
        
    def chooseAction(self):
        #print("Entered Choose Action")
        canAttack = True
        try:
            moveMenu = getItem (self.driver, "//div[@class='movemenu']")
            self.BattleOptions["attk1"] = getItem(moveMenu, ".//button[1]")
            self.BattleOptions["attk2"] = getItem(moveMenu, ".//button[2]")
            self.BattleOptions["attk3"] = getItem(moveMenu, ".//button[3]")
            self.BattleOptions["attk4"] = getItem(moveMenu, ".//button[4]")
        except:
            canAttack = False
            #print("Am I fainted? No moves to select!")
        switchMenu = getItem(self.driver, "//div[@class='switchmenu']")
        self.BattleOptions["switch1"] = getItem(switchMenu, ".//button[1]")
        self.BattleOptions["switch2"] = getItem(switchMenu, ".//button[2]")
        self.BattleOptions["switch3"] = getItem(switchMenu, ".//button[3]")
        self.BattleOptions["switch4"] = getItem(switchMenu, ".//button[4]")
        self.BattleOptions["switch5"] = getItem(switchMenu, ".//button[5]")
        self.BattleOptions["switch6"] = getItem(switchMenu, ".//button[6]")
        #print("Loaded options")
        action = random.randint(1,18)
        #print("Got the action as: "+str(action))        
        if(canAttack and action <= 12):
            action = action%4+1
            #print("I have chosen attack "+str(action))
            self.BattleOptions["attk"+str(action)].click()
        else:
            action = (action%6)+1
            #print("I have chosen to swap to "+str(action))
            self.BattleOptions["switch"+str(action)].click()
            
    def chooseLead(self):
        leadMenu = getItem(self.driver, "//div[@class='switchmenu']")
        self.BattleOptions["switch1"] = getItem(leadMenu, ".//button[1]")
        self.BattleOptions["switch2"] = getItem(leadMenu, ".//button[2]")
        self.BattleOptions["switch3"] = getItem(leadMenu, ".//button[3]")
        self.BattleOptions["switch4"] = getItem(leadMenu, ".//button[4]")
        self.BattleOptions["switch5"] = getItem(leadMenu, ".//button[5]")
        self.BattleOptions["switch6"] = getItem(leadMenu, ".//button[6]")
        action = random.randint(1,6)
        self.BattleOptions["switch"+str(action)].click()
        
    def Battle():
        print("BATTLING!")
