import re
import sys
from unidecode import unidecode

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output


def check_sublist(lstA, lstB): # lst A, B gom cac tu trong trong list cha
    count = 0
    if len(lstA) == len(lstB):
        for i in range(len(lstA)):
            if lstA[i] == lstB[i]:
                count +=1
        ave = count/len(lstA)
    else:
        for i in range(len(lstA)):
            for j in range(len(lstB)):
                if lstA[i] == lstB[j]:
                    count += 1
                    break
                else:
                    continue
            continue
        ave = count/min(len(lstA), len(lstB))
    print(ave)
    if ave > 0.75:
        return True
    else:
        return False



if __name__ == '__main__':
    print(convert('chưa kip tận hưởng hạnh phúc cô dâu chết tức tưởi ngay trong đám cưới của minh tại cung điện sang trọng chi vi món tráng miệng').split())
    split = convert('chưa kip tận hưởng hạnh phúc cô dâu chết tức tưởi ngay trong đám cưới của minh  cung điện sang trọng chi vi món tráng ').split()
    split_2 = convert('trong đám cưới của minh tại cung điện sang trọng chi vi món tráng miệng').split()
    check_sublist(split, split_2)