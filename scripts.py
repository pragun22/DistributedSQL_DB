attribs = [
"Id", #supp
"ContanctNumber",
"ContactName",
"CompanyName",
"Email",
"Phone",
"City",
"Address",
"PostalCode",
"Id", # categ
"Name", #Categ
"Decription", #Categ
"Id", #products
"Name", #Product
"Decription", #Product
"Quantity",
"Price",
"SupplierId",
"CategoryId",
]
relat = [
"Supplier", #supp
"Supplier",
"Supplier",
"Supplier",
"Supplier",
"Supplier",
"Supplier",
"Supplier",
"Supplier",
"Category", # categ
"Category", #Categ
"Category", #Categ
"Products", #products
"Products", #Product
"Products", #Product
"Products",
"Products",
"Products",
"Products",
]

# for i in range(1, len(attribs) + 1):
	# print("INSERT INTO Attributes Values({0}, '{1}', '{2}');".format(i, attribs[i-1], relat[i-1]))
attribs = [
"reserveId", #resreve
"checkIn",
"checkOut",
"id", #room
"city",
"reserveId",
"roomNo",
"guestId", #Guest
"reserveId",
"name", 
"address",
"email", 
"phone", 
"cit",
"payment", #Product
]
relat = [
"Reserve",
"Reserve",
"Reserve",
"Room", # categ
"Room", #Categ
"Room", #Categ
"Room", #Categ
"Guest", #Product
"Guest", #Product
"Guest",
"Guest",
"Guest",
"Guest",
"Guest",
"Guest"
]

for i in range(1, len(attribs) + 1):
	print("INSERT INTO Attributes Values({0}, '{1}', '{2}');".format(i+19, attribs[i-1], relat[i-1]))



# print("INSERT INTO Fragments Values(1, 1, 'Hor', 'Category');")
# print("INSERT INTO Fragments Values(2, 2, 'Hor', 'Category');")
# print("INSERT INTO Fragments Values(3, 3, 'Hor', 'Category');")
# print("INSERT INTO Fragments Values(4, 1, 'Ver', 'Supplier');")
# print("INSERT INTO Fragments Values(5, 2, 'Ver', 'Supplier');")
# print("INSERT INTO Fragments Values(6, 1, 'DHor', 'Product');")
# print("INSERT INTO Fragments Values(7, 2, 'DHor', 'Product');")
# print("INSERT INTO Fragments Values(8, 3, 'DHor', 'Product');")

print("INSERT INTO Fragments Values(9 , 1, 'Hor', 'Room');")
print("INSERT INTO Fragments Values(10, 2, 'Hor', 'Room');")
print("INSERT INTO Fragments Values(11, 3, 'Hor', 'Room');")
print("INSERT INTO Fragments Values(12, 1, 'Ver', 'Guest');")
print("INSERT INTO Fragments Values(13, 2, 'Ver', 'Guest');")
print("INSERT INTO Fragments Values(14, 3, 'Ver', 'Guest');")
print("INSERT INTO Fragments Values(15, 1, 'DHor', 'Reserve');")
print("INSERT INTO Fragments Values(16, 2, 'DHor', 'Reserve');")
print("INSERT INTO Fragments Values(17, 3, 'DHor', 'Reserve');")










# print("INSERT INTO HorFragment Values(1, 10, 'Men');")
# print("INSERT INTO HorFragment Values(1, 11, 'Men');")
# print("INSERT INTO HorFragment Values(1, 12, 'Men');")
# print("INSERT INTO HorFragment Values(2, 10, 'Women');")
# print("INSERT INTO HorFragment Values(2, 11, 'Women');")
# print("INSERT INTO HorFragment Values(2, 12, 'Women');")
# print("INSERT INTO HorFragment Values(3, 10, 'Children');")
# print("INSERT INTO HorFragment Values(3, 11, 'Children');")
# print("INSERT INTO HorFragment Values(3, 12, 'Children');")


print("INSERT INTO HorFragment Values(9, 23, 'Delhi');")
print("INSERT INTO HorFragment Values(9, 24, 'Delhi');")
print("INSERT INTO HorFragment Values(9, 25, 'Delhi');")
print("INSERT INTO HorFragment Values(9, 26, 'Delhi');")

print("INSERT INTO HorFragment Values(10, 23, 'Mumbai');")
print("INSERT INTO HorFragment Values(10, 24, 'Mumbai');")
print("INSERT INTO HorFragment Values(10, 25, 'Mumbai');")
print("INSERT INTO HorFragment Values(10, 26, 'Mumbai');")

print("INSERT INTO HorFragment Values(11, 23, 'Goa');")
print("INSERT INTO HorFragment Values(11, 24, 'Goa');")
print("INSERT INTO HorFragment Values(11, 25, 'Goa');")
print("INSERT INTO HorFragment Values(11, 26, 'Goa');")


print("INSERT INTO VerFragment Values(12, 27);")
print("INSERT INTO VerFragment Values(12, 28);")
print("INSERT INTO VerFragment Values(12, 29);")
print("INSERT INTO VerFragment Values(13, 27);")
print("INSERT INTO VerFragment Values(13, 30);")
print("INSERT INTO VerFragment Values(13, 31);")
print("INSERT INTO VerFragment Values(13, 32);")
print("INSERT INTO VerFragment Values(13, 33);")
print("INSERT INTO VerFragment Values(14, 27);")
print("INSERT INTO VerFragment Values(14, 34);")


# print("INSERT INTO DHorFragment Values(6, 13, 1);")
# print("INSERT INTO DHorFragment Values(6, 14, 1);")
# print("INSERT INTO DHorFragment Values(6, 15, 1);")
# print("INSERT INTO DHorFragment Values(6, 16, 1);")
# print("INSERT INTO DHorFragment Values(6, 17, 1);")
# print("INSERT INTO DHorFragment Values(6, 18, 1);")
# print("INSERT INTO DHorFragment Values(6, 19, 1);")
# print("INSERT INTO DHorFragment Values(7, 13, 2);")
# print("INSERT INTO DHorFragment Values(7, 14, 2);")
# print("INSERT INTO DHorFragment Values(7, 15, 2);")



print("INSERT INTO DHorFragment Values(15, 20, 9, '1');")
print("INSERT INTO DHorFragment Values(15, 21, 9, '1');")
print("INSERT INTO DHorFragment Values(15, 22, 9, '1');")
print("INSERT INTO DHorFragment Values(16, 20, 10,'2');")
print("INSERT INTO DHorFragment Values(16, 21, 10,'2');")
print("INSERT INTO DHorFragment Values(16, 22, 10,'2');")
print("INSERT INTO DHorFragment Values(17, 20, 11,'3');")
print("INSERT INTO DHorFragment Values(17, 21, 11,'3');")
print("INSERT INTO DHorFragment Values(17, 22, 11,'3');")
