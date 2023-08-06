def boom_intensity(number):
    list1 = []
    if number >= 2:
        list1.append('B')
        for i in range(number):
            list1.append('o')
        list1.append('m')
        if number % 2 == 0:
            list1.append('!')
            return ''.join(list1)
        else:
            return (''.join(list1)).upper()
    else:
        return 'boom'


def boom_intensity(x):
    if x < 2:
        return "boom"
    y = 'Boo'
    if x > 2:
        for i in range(x - 2):
            y += "o"
    y += 'm'
    if not x % 5:
        y = y.upper()
    if x % 2 == 0:
        y += '!'
    print(y)
    return y


assert boom_intensity(0) == "boom"
assert boom_intensity(1) == "boom"
assert boom_intensity(2) == "Boom!"
assert boom_intensity(3) == "Booom"
assert boom_intensity(4) == "Boooom!"
assert boom_intensity(5) == "BOOOOOM"
assert boom_intensity(6) == "Boooooom!"
assert boom_intensity(7) == "Booooooom"
assert boom_intensity(8) == "Boooooooom!"
assert boom_intensity(9) == "Booooooooom"
assert boom_intensity(10) == "BOOOOOOOOOOM!"
assert boom_intensity(11) == "Booooooooooom"
assert boom_intensity(12) == "Boooooooooooom!"
assert boom_intensity(13) == "Booooooooooooom"
assert boom_intensity(14) == "Boooooooooooooom!"
assert boom_intensity(15) == "BOOOOOOOOOOOOOOOM"
assert boom_intensity(16) == "Boooooooooooooooom!"
assert boom_intensity(17) == "Booooooooooooooooom"
assert boom_intensity(18) == "Boooooooooooooooooom!"
assert boom_intensity(19) == "Booooooooooooooooooom"
assert boom_intensity(20) == "BOOOOOOOOOOOOOOOOOOOOM!"
assert boom_intensity(21) == "Booooooooooooooooooooom"
assert boom_intensity(22) == "Boooooooooooooooooooooom!"
assert boom_intensity(23) == "Booooooooooooooooooooooom"
assert boom_intensity(24) == "Boooooooooooooooooooooooom!"
assert boom_intensity(25) == "BOOOOOOOOOOOOOOOOOOOOOOOOOM"
assert boom_intensity(26) == "Boooooooooooooooooooooooooom!"
assert boom_intensity(27) == "Booooooooooooooooooooooooooom"
assert boom_intensity(28) == "Boooooooooooooooooooooooooooom!"
assert boom_intensity(29) == "Booooooooooooooooooooooooooooom"
assert boom_intensity(30) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!"
assert boom_intensity(31) == "Booooooooooooooooooooooooooooooom"
assert boom_intensity(32) == "Boooooooooooooooooooooooooooooooom!"
assert boom_intensity(33) == "Booooooooooooooooooooooooooooooooom"
assert boom_intensity(34) == "Boooooooooooooooooooooooooooooooooom!"
assert boom_intensity(35) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM"
assert boom_intensity(36) == "Boooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(37) == "Booooooooooooooooooooooooooooooooooooom"
assert boom_intensity(38) == "Boooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(39) == "Booooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(40) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!"
assert boom_intensity(41) == "Booooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(42) == "Boooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(43) == "Booooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(44) == "Boooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(45) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM"
assert boom_intensity(46) == "Boooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(47) == "Booooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(48) == "Boooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(49) == "Booooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(50) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!"
assert boom_intensity(51) == "Booooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(52) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(53) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(54) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(55) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM"
assert boom_intensity(56) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(57) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(58) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(59) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(60) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!"
assert boom_intensity(61) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(62) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(63) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(64) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(65) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM"
assert boom_intensity(66) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(67) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(68) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(69) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(70) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!"
assert boom_intensity(71) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(72) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(73) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(74) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(75) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM"
assert boom_intensity(76) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(77) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(78) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(79) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(80) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!"
assert boom_intensity(81) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(82) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(83) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(84) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(85) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM"
assert boom_intensity(86) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(87) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(88) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(89) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(90) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!"
assert boom_intensity(91) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(92) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(93) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(94) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(95) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM"
assert boom_intensity(96) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(97) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(98) == "Boooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom!"
assert boom_intensity(99) == "Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooom"
assert boom_intensity(100) == "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!"
print("BOOOOOOOOM! You did it!!!")
