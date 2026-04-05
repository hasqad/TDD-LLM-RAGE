def num_decodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    
    dp = [1, 1]
    
    for i in range(2, len(s) + 1):
        one_digit = int(s[i-1])
        two_digits = int(s[i-2:i])
        
        if one_digit != 0:
            dp.append(dp[-1] + (dp[-2] if 9 < two_digits <= 26 else 0))
        else:
            dp.append(dp[-2] if 10 <= two_digits <= 26 else 0)
    
    return dp[-1]