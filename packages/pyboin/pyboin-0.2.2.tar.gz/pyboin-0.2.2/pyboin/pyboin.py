import jaconv


vowel_map =\
    [
        ['ア', 'アカサタナハマヤラワガザダバパァ　ャヮ'],
        ['イ', 'イキシチニヒミ　リ　ギジヂビピィ　　　'],
        ['ウ', 'ウクスツヌフムユル　グズヅブプゥッュ　'],
        ['エ', 'エケセテネヘメ　レ　ゲゼデベペェ　　　'],
        ['オ', 'オコソトノホモヨロヲゴゾドボポォ　ョ　'],
    ]


def text2boin(text, cv='katakana'):
    ## -----*----- 母音に変換 -----*----- ##
    if not cv in ('katakana', 'hiragana'):
        raise ValueError("argument cv allows 'katakana' or 'hiragana'")

    ret = ''
    text = jaconv.hira2kata(text)

    # replace
    for i, c in enumerate(text):
        if c == '　':
            ret += '　'

        for pair in vowel_map:
            # match
            if c in pair[1]:
                ret += pair[0]
        # not match
        if len(ret) == i:
            ret += c

    if cv == 'hiragana':
        ret = jaconv.kata2hira(ret)

    return ret


def romanize(char, vowel):
    ## -----*----- 母音を変換 -----*----- ##
    char_romanize = ''
    vowel_list = ['ア', 'イ', 'ウ', 'エ', 'オ']

    # convert vowel
    for i in range(len(vowel_map)):
        for j in range(len(vowel_map[i][1])):
            if char == vowel_map[i][1][j]:
                char_romanize = vowel_map[vowel_list.index(vowel)][1][j]
                return char_romanize

    return char

