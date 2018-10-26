from Pokemon import Pokemon
from DriverUtil import Util
from SerebiiCrawler import SerebiiCrawler
import sys
from time import sleep
def startBattling(util):
        print("Beginning program!")
        util.botLogIn()
        util.importOUTeam()
        util.setUpForBattle()
        for i in range(0,3):
            print("Beginning battle "+str(i+1)+"!")
            util.Battle()
def main():
    try:
        util = Util()
        startBattling(util)
    except:
        print("Unexpected Error: \n",sys.exc_info())
        util.killDriver()
        sleep(60)
        util = Util()
        startBattling(util)
#SerebiiCrawler().buildPokemonLibrary() #Only uncomment this if the files are not there.
main()
