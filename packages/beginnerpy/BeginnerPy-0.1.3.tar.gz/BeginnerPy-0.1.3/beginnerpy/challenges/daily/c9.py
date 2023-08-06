def censor(str):
    str = str.split(' ')
    newstr = ""
    for string in str:
        if len(string) > 4:
            newstr += ("*" * len(string))
        else:
            newstr += string
        newstr += " "
    return newstr


assert censor("The code is fourty") == "The code is ******"
assert censor("Two plus three is five") == "Two plus ***** is five"
assert censor("aaaa aaaaa 1234 12345") == "aaaa ***** 1234 *****"
assert censor("abcdefghijklmnop") == "****************"
assert censor("a") == "a"
print("Success")
