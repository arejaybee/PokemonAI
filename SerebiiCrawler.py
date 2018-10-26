from selenium import webdriver
from time import sleep
SEREBII = "https://www.serebii.net/"
POKEDEX = "pokedex-sm/"
ABILITYDEX = "abilitydex/"
ATTACKDEX = "attackdex/"
LIBRARY_PATH = "Pokemon/"

def formatID(num):
    if(num < 10):
        return "00"+str(num)
    elif(num<100):
        return "0"+str(num)
    else:
        return str(num)
    
def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

def trimLink(link):
    returnString = ""
    i = len(link)-1
    while i > 0:
        if(link[i] == "/"):
            return returnString
        returnString = link[i]+returnString
        i-=1
        
def trimHref(item, href):
    return trimLink(getItem(item, ".//"+href).get_attribute("href").replace(".shtml",""))

def trimImage(item, image, ending):
    return trimLink(getItem(item, ".//"+image).get_attribute("src").replace(ending,""))

def getItem(item, xpath):
    return item.find_element_by_xpath(xpath)
    
class SerebiiCrawler:
    def __init__(self):
        self.inBattle = False
        self.setUpDriver()

    def formatAttackRow(self, row):
        name = trimHref(row, "td[2]/a")
        attkType = trimImage(row, "td[3]/img",".gif")
        attkCat = trimImage(row, "td[4]/img",".png")
        dmg = getItem(row, ".//td[5]").text
        acc = getItem(row, ".//td[6]").text
        pp = getItem(row, ".//td[7]").text
        return name+" - "+attkType+" - "+attkCat+" - "+dmg+" - "+acc+" - "+pp
        
    def setUpDriver(self):
        print("Serebii - Setting up Driver...")
        self.room = ""
        myOptions = webdriver.ChromeOptions()
        myOptions.add_argument('--ignore-certificate-errors')
        myOptions.add_argument("--test-type")
        self.driver = webdriver.Chrome(options=myOptions)
        self.driver.get(SEREBII+POKEDEX)
        self.driver.maximize_window()
        print("Serebii - Driver is loaded!")
        
    def findPokemonByName(self,pokemonName):
        firstNamesBox = getItem(self.driver, "/html/body/table[2]/tbody/tr[2]/td[2]/font/div[3]/table/tbody/tr[2]/td[1]/form/select")
        secondNamesBox = getItem(self.driver, "/html/body/table[2]/tbody/tr[2]/td[2]/font/div[3]/table/tbody/tr[2]/td[2]/form/select")
        thirdNamesBox = getItem(self.driver, "/html/body/table[2]/tbody/tr[2]/td[2]/font/div[3]/table/tbody/tr[2]/td[3]/form/select")
        nameBox = ""
        if(pokemonName[0].upper() in char_range("A","G")):
            nameBox = firstNamesBox
        elif(pokemonName[0].upper() in char_range ("H","R")):
            nameBox = secondNamesBox
        elif (pokemonName[0].upper() in char_range ("S","Z")):
            nameBox = thirdNamesBox
        else:
            print("Pokemon was not found")
            return

        continueLoop = True
        i = 1
        pokemonURL = ""
        while(continueLoop):
                name = nameBox.find_element_by_xpath(".//option["+str(i)+"]")
                if(name.text.lower() == pokemonName.lower()):
                    continueLoop = False
                    pokemonURL = name.get_attribute("value")
                i+=1
                
        if(pokemonURL == ""):
            print("No URL found!")
            return
        self.driver.get(SEREBII+pokemonURL)

    def getPokemonType(self, firstTable):
        types = ""
        try:
            types = getItem(firstTable, ".//tbody/tr[2]/td[6]/table/tbody/tr[1]") #try to get alolans
        except:        
            types = getItem(firstTable, ".//tbody/tr[2]/td[6]")
        type1 = ""
        type2 = ""
        try:
            type1 = trimHref(types, "a[1]")
            type2 = trimHref(types, "a[2]")
        except:
            try:
                type1 = trimHref(types, "a")
            except:
                print(" has no type? Setting type as UNKOWN")
                type1 = "UNKOWN"
        return type1,type2

    def getAlolaPokemonTypes(self, firstTable):
        types = getItem(firstTable, ".//tbody/tr[2]/td[6]/table/tbody/tr[2]") #try to get alolans
        type1 = ""
        type2 = ""
        try:
            type1 = trimHref(types, "a[1]")
            type2 = trimHref(types, "a[2]")
        except:
            try:
                type1 = trimHref(types, "a")
            except:
                print(" has no type? Setting type as UNKOWN")
                type1 = "UNKOWN"
        return type1,type2
    
    def getPokemonAbilities(self, firstTable, tableNum):
        firstTable = getItem(firstTable, "..")
        abilities = getItem(firstTable, ".//table["+str(tableNum+1)+"]/tbody/tr[2]/td")
        allAbilities = []
        hasAbilities = True
        j = 1
        while(hasAbilities):
            try:
                a = trimHref(abilities, "a["+str(j)+"]")
                allAbilities.append(a)
                j+=1
            except:
                if(j == 1):
                    try:
                        a = trimHref(abilities, "a")
                        allAbilities.append(a)
                    except:
                        print("has no abilities? Setting ability as UNKOWN")
                        allAbilities.append("UNKOWN")
                hasAbilities = False
        return allAbilities
    
    def getPokemonStats(self):
        page = getItem(self.driver, "/html/body/table[2]/tbody/tr[2]/td[2]/font/div[2]/div")
        statTable = getItem(page, "//*[contains(text(), 'Base Stats')]")
        statTable = getItem(statTable, "..")
        stats = []
        for j in range(2,8):
            stats.append(getItem(statTable, ".//td["+str(j)+"]").text)
        return stats

    def hasAlolan(self):
        try:
            getItem(self.driver, "//*[contains(text(), 'Alola Form')]")
            return True
        except:
            return False
        
    def writePokemonFile(self, name, type1, type2, stats):
        file = open(LIBRARY_PATH+name+".pkmn", 'w')
        file.write("TYPE\n")
        file.write(type1+"\n")
        if(not type2 == ""):
            file.write(type2+"\n")
        #file.write("ABILITIES\n")
        #for ability in abiities:
        #    file.write(ability+"\n")
        file.write("STATS\n")
        for stat in stats:
            file.write(stat+"\n")
        file.close()
            
    def buildPokemonLibrary(self):
        for i in range(1, 808):
            hasAlolan = False
            print("Writing pokemon",formatID(i))
            link = SEREBII+POKEDEX+formatID(i)+".shtml"
            self.driver.get(link)
            firstTable = getItem(self.driver,"/html/body/table[2]/tbody/tr[2]/td[2]/font/div[2]/div/p[1]/table[1]")
            name = ""
            tableNum = 1
            try:
                name = getItem(firstTable, ".//tbody/tr[2]/td[2]").text
            except:
                firstTable = getItem(self.driver,"/html/body/table[2]/tbody/tr[2]/td[2]/font/div[2]/div/table[2]")
                tableNum = 2
                name = getItem(firstTable, ".//tbody/tr[2]/td[2]").text
            name = name.replace("♀","-f")
            name = name.replace("♂","-m")
            name = name.strip()
            hasAlolan = self.hasAlolan()
            #print("Name: ",name)
            #print("Is Alolan: ", hasAlolan)
            type1 = ""
            type2 = ""
            abilities = []
            stats = []
            type1,type2 = self.getPokemonType(firstTable)
            #print("Grabbing abilities...")
            #abiities = self.getPokemonAbilities(firstTable, tableNum)
            #print("Grabbing stats...")
            stats = self.getPokemonStats()
            self.writePokemonFile(name, type1, type2, stats)

            if(hasAlolan):
                type1, type2 = self.getAlolaPokemonTypes(firstTable)
                self.writePokemonFile(name.strip()+"-Alola", type1, type2, stats)
        self.driver.close()
        self.driver.quit()
		











        
