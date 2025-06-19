import random

def triangelfordelning(medelvärde, std, dricks):
    vänster = medelvärde - 3 * std
    höger = medelvärde + 3 * std
    topp = medelvärde + dricks
    slumptal = random.triangular(vänster, höger, topp)
    return round(slumptal), round(vänster), round(höger)