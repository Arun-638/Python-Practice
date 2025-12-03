units = int(input("Enter the units: "))
bill = 0
if units>=0 and units<=100:
    bill = units*5
elif units>100 and units<=200:
    bill = units*7
else:
    bill = units*10
print("Bill for a Customer = ",bill)