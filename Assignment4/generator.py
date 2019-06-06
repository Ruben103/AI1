import os
import random

def randomPremises(variables):
    kb = []
    stopCrit = 0
    for i in range(15):
        string = '['
        rand = random.random()
        if rand > 0.5:
            string += "~"
        string += random.choice(variables)
        for j in range(random.randint(0,5)):
            string += ',~' + random.choice(variables)

        string += ']'
        kb.append(string)
    return kb

def randomConclusion(variables):
    kb = []
    stopCrit = 0
    for i in range(1):
        string = '['
        rand = random.random()
        if rand > 0.5:
            string += "~"
        string += random.choice(variables)
        for j in range(random.randint(0,2)):
            string += ',~' + random.choice(variables)

        string += ']'
        kb.append(string)
    return kb




def main(): 
    variables = ['p','q','r','s','t','u','v','w','x','y',]
    kb = randomPremises(variables)
    print(kb)
    conc = randomConclusion(variables)
    print("\n\n ******* \n\n")
    print(conc)
    pass

if __name__ == "__main__":
    os.system("clear")
    main()