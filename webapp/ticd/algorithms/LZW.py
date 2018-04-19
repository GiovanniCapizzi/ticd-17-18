# coding=utf-8

#    _                               _      _______              _    _      _      _
#   | |                             | |    |___  (_)            | |  | |    | |    | |
#   | |     ___ _ __ ___  _ __   ___| |______ / / ___   ________| |  | | ___| | ___| |__
#   | |    / _ \ '_ ` _ \| '_ \ / _ \ |______/ / | \ \ / /______| |/\| |/ _ \ |/ __| '_ \
#   | |___|  __/ | | | | | |_) |  __/ |    ./ /__| |\ V /       \  /\  /  __/ | (__| | | |
#   \_____/\___|_| |_| |_| .__/ \___|_|    \_____/_| \_/         \/  \/ \___|_|\___|_| |_|
#                        | |
#                        |_|

#in_text = "La signora Aurora ha programmato in Java un software per la gestione dei ristoranti."

in_text = "bcababbcbcbaaaabbc"


def encode(i_text, logging=False):

    """
    >>> encode("bcababbcbcbaaaabbc")
    ([2, 3, 1, 2, 6, 4, 9, 1, 11, 8, 3], {1: 'a', 2: 'b', 3: 'c'})

    :param i_text:
    :param logging:
    :return output:
    """



    # Initialization -----------------------
    in_alph = sorted(set(i_text))
    codebook = {}
    inverted_codebook = {}
    for index, item in enumerate(in_alph):
        codebook[item] = index + 1
        inverted_codebook[index + 1] = item

    # Position
    cursor = 0
    limit = len(i_text)
    output = []

    if logging:
        print("CODING...\n", i_text)

    # End of Initialization -----------------

    while cursor < limit:
        current = i_text[cursor]
        if logging:
            print("The current word is", current, 'at index', cursor)

        # searching the longest word in the dictionary
        relative_index = cursor + 1

        while i_text[cursor: relative_index] in codebook:
            relative_index += 1
            if relative_index > limit:
                # end of string, outputting remaining text,
                # relative_index bound doesn't matter in python substring
                coding_word = i_text[cursor:relative_index]
                output.append(codebook[coding_word])
                if logging:
                    print("and outputting the remaining", codebook[coding_word], "value")
                return output, inverted_codebook

        # add this new word to the codebook
        word = i_text[cursor:relative_index]
        codebook[word] = len(codebook)+1
        # outputting value
        coding_word = i_text[cursor:relative_index - 1]
        output.append(codebook[coding_word])

        if logging:
            print("I'm putting", word, "in the dictionary")
            print("outputting", codebook[coding_word], "value")
            print("moving cursor from ", cursor, "to ", cursor + len(coding_word))

        cursor += len(coding_word)


def decode(i_coded_text, codebook, logging=False):

    """
    >>> decode([2, 3, 1, 2, 6, 4, 9, 1, 11, 8, 3], {1: 'a', 2: 'b', 3: 'c'})
    'bcababbcbcbaaaabbc'

    :param i_coded_text:
    :param codebook:
    :param logging:
    :return output:
    """

    # Initialization -----------------------

    output = ''
    # last word added
    last = ''

    # End of Initialization -----------------

    for item in i_coded_text:
        if item in codebook.keys():
            current_item = codebook[item]
            output += current_item

            # adding new key to codebook
            candidate = last+current_item
            c_len = len(candidate)
            if c_len > 1:
                # searching the longest word in the dictionary
                relative_index = 1

                while relative_index <= c_len and candidate[0: relative_index] in codebook.values():
                    relative_index += 1

                # O(1) len sui dict
                codebook[len(codebook)+1] = candidate[0:relative_index]

            last = current_item
        else:
            adding = last + last[0]
            output += adding
            codebook[len(codebook)+1] = adding
            last = adding

        if logging:
            print("{Item %s,Codebook[item] %s,codebook %s}" % (item, codebook[item], codebook))

    return output


# TEST CODE --------------

if __name__ == '__main__':

    print("Testing code ")
    code, inverted_codebook = encode(in_text)
    print(decode(code, inverted_codebook ))

