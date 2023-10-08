def dec2bin(number: int):
    ans = ""
    if ( number == 0 ):
        return 0
    while ( number ):
        ans += str(number&1)
        number = number >> 1
     
    ans = ans[::-1]
 
    return ans