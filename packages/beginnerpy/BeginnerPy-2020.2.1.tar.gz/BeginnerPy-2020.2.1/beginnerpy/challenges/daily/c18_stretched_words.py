from typing import AnyStr


def unstretch(word: AnyStr) -> AnyStr:
    return ''.join(char for i, char in enumerate(word) if not i or word[i - 1] != char)


def unstretch_runner(word):
    result = unstretch(word)
    print(result)
    return result


assert unstretch_runner('llossttttt') == 'lost'
assert unstretch_runner('cccccaaaaannnnne') == 'cane'
assert unstretch_runner('hhoooneestttt') == 'honest'
assert unstretch_runner('ppppooowwddddeeerrrr') == 'powder'
assert unstretch_runner('eexxpppppeeccctt') == 'expect'
assert unstretch_runner('rrrrepooooorrttt') == 'report'
assert unstretch_runner('pppaaaaattteeeennnntt') == 'patent'
assert unstretch_runner('mmmeeemoooryy') == 'memory'
assert unstretch_runner('vvvvviiiiisssuuaaalll') == 'visual'
assert unstretch_runner('eeeennnnsuuurrre') == 'ensure'
assert unstretch_runner('iiinncclludddddeee') == 'include'
assert unstretch_runner('ttteestiffffyyy') == 'testify'
assert unstretch_runner('ggrrrrraaaaavvvvviiitttyyyy') == 'gravity'
assert unstretch_runner('cccuuuultttttuuuuurreee') == 'culture'
assert unstretch_runner('qquaalliiifffyy') == 'qualify'
assert unstretch_runner('iiinnccoooonnnnnggggrrrrruuuuooouuuuusss') == 'incongruous'
assert unstretch_runner('eeeennnnttiiiitlllleeeeemmeennnttttt') == 'entitlement'
assert unstretch_runner('aaaaassstttttooniiiiissshhiiinnnnnggg') == 'astonishing'
assert unstretch_runner('cccccoiinnnncccciidddenncee') == 'coincidence'
assert unstretch_runner('prrrrreeeppppaaaarrrrraaattiionn') == 'preparation'
print("You've successfully unstretched all the words! Challenge 18 Successfully Completed!")
