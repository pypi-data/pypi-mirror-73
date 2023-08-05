## Imports
# None Needed ;) #PythonicPower

## Object
class Menu():
    def __init__(self, name: str = "My Menu", color: str = "None", optionCount: int = 2):
        self.counter = int(0)
        self.menuName = name
        self.colorTemp = color
        self.optionCount = int(optionCount)
        self.optionList = []

    def addOption(self, option: str = "Default Option"):
        if self.counter >= self.optionCount:
            return False
        else:
            self.counter += 1
            self.optionList.append(option)
            return True

    def resolveColor(self):
        from colorama import Fore
        from colorama import init as colInit
        colInit()
        if self.colorTemp == "green":
            return Fore.GREEN
        elif self.colorTemp == "red":
            return Fore.RED
        elif self.colorTemp == "cyan":
            return Fore.CYAN
        elif self.colorTemp == "yellow":
            return Fore.YELLOW
        else:
            return None

    def displayMenu(self, mode: str = "default"):
        from colorama import Fore
        from colorama import init as colInit
        colInit()
        color = self.resolveColor()
        if color == None:
            if mode == "default":
                from os import system
                system("cls")
                print(f"\t{self.menuName}\n\nOptions:")
                counterT = 1
                for option in self.optionList:
                    print(f"\t[{counterT}] - {option}")
                    counterT += 1
                optionSel = int(input("\nSelection: "))
                return optionSel
            else:
                from time import sleep
                import sys
                print("Unknown Menu Mode Thrown. Exiting.")
                sleep(2)
                sys.exit()
        else:
            if mode == "default":
                from os import system
                system("cls")
                print(color + f"\t{self.menuName}\n\nOptions:")
                counterT = 1
                for option in self.optionList:
                    print(f"\t[{counterT}] - {option}")
                    counterT += 1
                optionSel = int(input("\nSelection: " + Fore.RESET))
                return optionSel
            else:
                from time import sleep
                import sys
                print("Unknown Menu Mode Thrown. Exiting.")
                sleep(2)
                sys.exit()