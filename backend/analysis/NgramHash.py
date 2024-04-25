# KOR_MAX_LEN_n_2 = 72
# FOR_MAX_LEN_n_2 = 82

def n_gram_hash(text, n, where):
    result = []
    if len(text) > n:
        for i in range(len(text)):
            if i+n > len(text):
                break
            result.append(hash(text[i:i+n]))
    else:
        result.append(hash(text))
    # if where == "korean":
    #     result = result + [0.0 for _ in range(KOR_MAX_LEN_n_2 - len(result))]
    # else:
    #     result = result + [0.0 for _ in range(FOR_MAX_LEN_n_2 - len(result))]
    return result
