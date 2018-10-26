from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PokemonBattler import PokemonBattler
from time import sleep

USERNAME = "arejaybee-bot"
TEAM_NAME = "OffensiveTeam"
POKEMON_SHOWDOWN_URL = "https://play.pokemonshowdown.com/"

def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

def getItem(item, xpath):
    return item.find_element_by_xpath(xpath)
    
class Util:
    def __init__(self):
        self.inBattle = False
        self.setUpDriver()
        
    def setUpDriver(self):
        print("Setting up Driver...")
        url = "https://play.pokemonshowdown.com"
        self.room = ""
        myOptions = webdriver.ChromeOptions()
        myOptions.add_argument('--ignore-certificate-errors')
        myOptions.add_argument("--test-type")
        self.driver = webdriver.Chrome(options=myOptions)
        self.driver.get(url)
        self.driver.maximize_window()
        print("Driver is loaded!")
        sleep(2)

    def killDriver(self):
        self.driver.close()
        self.driver.quit()
        
    def botLogIn(self):
        print("logging in...")
        getItem(self.driver, "//*[@id=\"header\"]/div[3]/button[1]").click()
        sleep(1)
        login = getItem(self.driver,"/html/body/div[4]/div/form/p[1]/label/input")
        login.send_keys(USERNAME)
        login.submit()
        print("successfully logged in!")
        sleep(2)

    def buildTeam(self):
        print("Importing team from text file...")
        file = open(TEAM_NAME+".txt", "r") 
        team = file.read()
        file.close()
        getItem(self.driver, "//*[@id=\"room-teambuilder\"]/div[2]/p[3]/button").click() #open team builder
        getItem(self.driver, "//*[@id=\"room-teambuilder\"]/div/div[2]/ol/li[4]/button").click() #import team from text
        getItem(self.driver, "//*[@id=\"room-teambuilder\"]/div/div[2]/textarea").send_keys(team) #enter team
        teamNameField = getItem(self.driver, "//*[@id=\"room-teambuilder\"]/div/div[1]/input")
        teamNameField.send_keys(Keys.CONTROL + "a");
        teamNameField.send_keys(Keys.DELETE);
        teamNameField.send_keys(TEAM_NAME) #enter team name
        getItem(self.driver, "//*[@id=\"room-teambuilder\"]/div/div[1]/button[3]").click()  #save team
        getItem(self.driver, "//*[@id=\"header\"]/div[2]/div/ul[1]/li[2]/button").click() #close team builder
        
    def findTeam(self):
        print("Finding team...")
        availTeams = False
        try:
            getItem(self.driver, "//*[@id=\"room-teambuilder\"]/div[2]/ul")
            availTeams = True
        except:
            print("There are no teams yet.")
            return False

        teamFound = False
        i = 0
        while(availTeams and not teamFound):
            try:
                i+=1
                team = getItem(self.driver, "//*[@id=\"room-teambuilder\"]/div[2]/ul/li["+str(i)+"]/div")
                teamName = getItem(team, ".//strong").text
                if(teamName == TEAM_NAME):
                    teamFound = True
            except:
                try:
                    getItem(self.driver, "//*[@id=\"room-teambuilder\"]/div[2]/ul/li/div")
                except:
                    availTeams = False
        return teamFound

    def importOUTeam(self):
        print("Getting OU team ready...")
        getItem(self.driver, "//*[@id=\"room-\"]/div/div[1]/div[2]/div[2]/p[1]/button").click()
        teamTabLoaded = False
        while(not teamTabLoaded):
            try:
                getItem(self.driver, "//*[@id=\"room-teambuilder\"]")
                teamTabLoaded = True
            except:
                print("Waiting for the team tab to load...")
                sleep(3)
        teamExists = self.findTeam()
        if(teamExists):
            getItem(self.driver, "//*[@id=\"header\"]/div[2]/div/ul[1]/li[2]/button")
        else:
            self.buildTeam()
        print("Team is loaded!")
        sleep(1)

    def setModeOU(self):
        battleType = getItem(self.driver, "//*[@id=\"room-\"]/div/div[1]/div[2]/div[1]/form/p[1]/button").click()
        battleModeSet = False
        i = 1
        battleOptions = getItem(self.driver, "/html/body/div[4]/ul[1]")
        while(not battleModeSet):
            try:
                listItem = getItem(battleOptions, ".//li["+str(i)+"]")
                mode = getItem(listItem, ".//button")
                if(mode.text == "OU"):
                    mode.click()
                    battleModeSet = True
                i+=1
            except:
                if(i < 30):
                    i+=1
                else:
                    print("I cannot find OU!!")
                    return
        print("Game mode set to OU")
        
    def setTeam(self):
        getItem(self.driver, "//*[@id=\"room-\"]/div/div[1]/div[2]/div[1]/form/p[2]/button").click() #select the team dropdown
        teamSelectPopUp = getItem(self.driver, "/html/body/div[4]/ul")
        getItem(teamSelectPopUp, ".//li[5]/button").click() #click show all teams
        teamSelectPopUp = getItem(self.driver, "/html/body/div[4]/ul")
        teamFound = False
        i = 5
        while(not teamFound):
            try:
                team = getItem(teamSelectPopUp, ".//li["+str(i)+"]/button")
                print(team.text)
                if(team.text == TEAM_NAME):
                    team.click()
                    teamFound = True
                i+=1
            except:
                print(TEAM_NAME," was not found! on .//li["+str(i)+"]/button")
                return
        print("Team is set")
        sleep(1)
        
    def getOpponentTeam(self):
        pokemonNames = getItem(self.driver, "//*[@id=\""+self.room+"\"]/div[3]/div[2]/div[13]")
        pokemonNames = getItem(pokemonNames, ".//em").text
        pokemonNames = pokemonNames.split("/")
        return pokemonNames
    
    def setUpForBattle(self):
        #set mode as OU
        self.setModeOU()
        #set your team
        self.setTeam()

    def Battle(self):
        continueLoop = True
        #try to click Battle!
        while(continueLoop):
            try:
                randomButton = getItem(self.driver, "//*[contains(text(), 'Find a random opponent')]")
                randomButton = getItem(randomButton, "..").click()
                continueLoop = False
            except:
                print("Waiting for random button.")
                sleep(10)
        print("Waiting for battle to start...")
        self.inBattle = False
        #wait for a battle to start
        while(not self.inBattle):
            try:
                tab = getItem(self.driver, "//*[@id=\"header\"]/div[2]/div/ul[2]/li/a")
                sleep(5)
                tab = getItem(self.driver, "//*[@id=\"header\"]/div[2]/div/ul[2]/li/a") #we have to wait a few seconds then grab this again, because the tab actually starts with junk text and we are too fast
                tabLink = tab.get_attribute("href").replace(POKEMON_SHOWDOWN_URL, "")
                if(not tabLink == "rooms"):
                    self.inBattle = True
                    self.room = "room-"+tabLink
                    print(self.room)
            except:
                print("Waiting for battle to start...")
                sleep(5)
        sleep(5)
        self.getOpponentName()
        self.chatBox = getItem(self.driver,"//*[@id=\""+self.room+"\"]/div[4]/form/textarea[2]")
        self.chatBox.send_keys("Hello,"+self.opponentName+", I am an AI designed to play pokemon. Good luck and have fun!")
        self.chatBox.submit()
        #myTeam = getBotTeam()
        opponentsTeam = self.getOpponentTeam()
        #print(opponentsTeam)
        PokemonBattler(opponentsTeam, self.driver, self.room, self.opponentName)
        sleep(5)
        
    def getOpponentName(self):
        self.opponentName = getItem(self.driver, "//*[@id=\""+self.room+"\"]/div[1]/div/div[9]/div/strong").text

    def getCurrentPokemon(self):
        o = ""
        m = ""
        print(opponentSide)
        complementary = getItem(self.driver, "//*[@id=\""+self.room+"\"]/div[1]/div/div[6]")
        statbar1 = ""
        statbar2 = ""
        sb1Text = ""
        sb2Text = ""
        try:
            statbar1 = getItem(self.driver, "//*[@id=\""+self.room+"\"]/div[1]/div/div[6]/div[1]")
            sb1Text = statbar1.find_element_by_xpath(".//strong").text
        except:
            print("No statbar1")
        try:
            statbar2 = getItem(self.driver, "//*[@id=\""+self.room+"\"]/div[1]/div/div[6]/div[2]")
            sb2Text = statbar2.find_element_by_xpath(".//strong").text
        except:
            print("No statbar1")
        if(opponentSide == "right"):
            if(not(statbar1 == "") and statbar1.get_attribute("class") == "statbar rstatbar"):
                o = sb2Text
                m = sb1Text
            else:
                o = sb1Text
                m = sb2Text
        return m,o
