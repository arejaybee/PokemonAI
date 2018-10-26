class Pokemon:
    def __init__(self, name):
        self.name = name.replace(" ","")
        print("Making a pokemon for: "+self.name)
        self.types = []
        self.abilities = []
        self.stats = []
        try:
            pokeFile = open("Pokemon/"+self.name+".pkmn", "r")
            pokeFileText = pokeFile.read()
            pokeFileElements = pokeFileText.split()
            elementType = ""
            for element in pokeFileElements:
                element = str(element).strip()
                if(element in ["TYPE", "ABILITIES", "STATS"]):
                    elementType = element
                else:
                    if(elementType == "TYPE"):
                        self.types.append(element)
                    elif(elementType == "ABILITIES"):
                        self.abilities.append(element)
                    elif(elementType == "STATS"):
                        self.stats.append(element)
        except:
            self.name = "UNKOWN"
            self.types = ["???"]
            self.abilities = ["???"]
            self.stats = [0,0,0,0,0,0]

