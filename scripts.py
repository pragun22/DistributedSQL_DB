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
# 	print("INSERT INTO Attributes Values({0}, '{1}', '{2}');".format(i, attribs[i-1], relat[i-1]))



# print("INSERT INTO Fragments Values(1, 1, 'Hor', 'Category');")
# print("INSERT INTO Fragments Values(2, 2, 'Hor', 'Category');")
# print("INSERT INTO Fragments Values(3, 3, 'Hor', 'Category');")
# print("INSERT INTO Fragments Values(4, 1, 'Ver', 'Supplier');")
# print("INSERT INTO Fragments Values(5, 2, 'Ver', 'Supplier');")
# print("INSERT INTO Fragments Values(6, 1, 'DHor', 'Product');")
# print("INSERT INTO Fragments Values(7, 2, 'DHor', 'Product');")
# print("INSERT INTO Fragments Values(8, 3, 'DHor', 'Product');")











print("INSERT INTO HorFragment Values(1, 10, 'Men');")
print("INSERT INTO HorFragment Values(1, 11, 'Men');")
print("INSERT INTO HorFragment Values(1, 12, 'Men');")
print("INSERT INTO HorFragment Values(2, 10, 'Women');")
print("INSERT INTO HorFragment Values(2, 11, 'Women');")
print("INSERT INTO HorFragment Values(2, 12, 'Women');")
print("INSERT INTO HorFragment Values(3, 10, 'Children');")
print("INSERT INTO HorFragment Values(3, 11, 'Children');")
print("INSERT INTO HorFragment Values(3, 12, 'Children');")


print("INSERT INTO VerFragment Values(4, 1);")
print("INSERT INTO VerFragment Values(4, 2);")
print("INSERT INTO VerFragment Values(4, 3);")
print("INSERT INTO VerFragment Values(4, 4);")
print("INSERT INTO VerFragment Values(5, 1);")
print("INSERT INTO VerFragment Values(5, 5);")
print("INSERT INTO VerFragment Values(5, 6);")
print("INSERT INTO VerFragment Values(5, 7);")
print("INSERT INTO VerFragment Values(5, 8);")
print("INSERT INTO VerFragment Values(5, 9);")


print("INSERT INTO DHorFragment Values(6, 13, 1);")
print("INSERT INTO DHorFragment Values(6, 14, 1);")
print("INSERT INTO DHorFragment Values(6, 15, 1);")
print("INSERT INTO DHorFragment Values(6, 16, 1);")
print("INSERT INTO DHorFragment Values(6, 17, 1);")
print("INSERT INTO DHorFragment Values(6, 18, 1);")
print("INSERT INTO DHorFragment Values(6, 19, 1);")
print("INSERT INTO DHorFragment Values(7, 13, 2);")
print("INSERT INTO DHorFragment Values(7, 14, 2);")
print("INSERT INTO DHorFragment Values(7, 15, 2);")
print("INSERT INTO DHorFragment Values(7, 16, 2);")
print("INSERT INTO DHorFragment Values(7, 17, 2);")
print("INSERT INTO DHorFragment Values(7, 18, 2);")
print("INSERT INTO DHorFragment Values(7, 19, 2);")
print("INSERT INTO DHorFragment Values(8, 13, 3);")
print("INSERT INTO DHorFragment Values(8, 14, 3);")
print("INSERT INTO DHorFragment Values(8, 15, 3);")
print("INSERT INTO DHorFragment Values(8, 16, 3);")
print("INSERT INTO DHorFragment Values(8, 17, 3);")
print("INSERT INTO DHorFragment Values(8, 18, 3);")
print("INSERT INTO DHorFragment Values(8, 19, 3);")