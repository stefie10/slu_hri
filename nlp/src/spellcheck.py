#from enchant.checker import SpellChecker
import enchant



checker = enchant.Dict("en_us")



def spellcheck(str):
    from chunker import tokenize
    indexes, tokens = tokenize(str)
    result = ""
    first = True
    for idx, token in zip(indexes, tokens):
        if not first:
            result += " "

        if (not token in [",", ".", "?", "!"] and
            not checker.check(token)):
            suggestions =  checker.suggest(token)
            if len(suggestions) != 0:
                result += checker.suggest(token)[0]
            else:
                result += token
        else:
            result += token
        first = False
    return result

    
