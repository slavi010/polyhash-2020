data = [1,2,3,4,5,6]
for i,k in zip(data[0::1], data[1::1]):
    print(str(i), '+', str(k), '=', str(i+k))