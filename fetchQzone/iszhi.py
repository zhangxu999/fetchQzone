def iszhi(x):
    cnt=0
    if x<=1:
        return False
    for m in range(1,x+1):
        if x%m==0:
            ++cnt
        if cnt>2:
            return True
    return False
