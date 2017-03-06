import randomcolor

RANDOMIZER = randomcolor.RandomColor()

def randcolor():
    cols = RANDOMIZER.generate(luminosity="bright", format_="rgb")
    col = cols[0][4:-1]
    return tuple(int(x) for x in col.split(", "))
