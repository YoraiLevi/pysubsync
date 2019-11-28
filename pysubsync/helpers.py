def unpackTupleList(lst):
    newlst = []
    for t in lst:
        newlst.append(t[0])
        newlst.append(t[1])
    return newlst


def packList2Tuple(lst):
    return list(zip(lst[0::2], lst[1::2]))