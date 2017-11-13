def parse(string):
    res = ""
    for o in string:
        try:
            c = chr(o)
        except:
            pass
        if o == 0x24:
            res += "deriv("
        elif o == 0x25:
            res += "int("
        elif o == 0x2B:
            res += ","
        elif 0x30 <= o <= 0x39:
            res += c # digit
        elif o == 0x3A:
            res += "."
        elif 0x41 <= o <= 0x5A:
            res += c # letter
        elif o == 0x70:
            res += "+"
        elif o == 0x71:
            res += "-"
        elif o == 0x82:
            res += "*"
        elif o == 0x83:
            res += "/"
        elif o == 0xBC:
            res += "sqrt("
        elif o == 0xBD:
            res += "curt("
        elif o == 0xBE:
            res += "ln("
        elif o == 0xBF:
            res += "e^("
        elif o == 0xC0:
            res += "log("
        elif o == 0xC1:
            res += "10^("
        elif o == 0xC2:
            res += "sin("
        elif o == 0xC3:
            res += "arcsin("
        elif o == 0xC4:
            res += "cos("
        elif o == 0xC5:
            res += "arccos("
        elif o == 0xC6:
            res += "tan("
        elif o == 0xC7:
            res += "arctan("
        elif o == 0xF0:
            res += "^"
        else:
            print("unknown ord", o)

    return res
