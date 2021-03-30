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



# print("INSERT INTO HorFragment Values(1, 10, 'Men');")
# print("INSERT INTO HorFragment Values(1, 11, 'Men');")
# print("INSERT INTO HorFragment Values(1, 12, 'Men');")
# print("INSERT INTO HorFragment Values(2, 10, 'Women');")
# print("INSERT INTO HorFragment Values(2, 11, 'Women');")
# print("INSERT INTO HorFragment Values(2, 12, 'Women');")
# print("INSERT INTO HorFragment Values(3, 10, 'Children');")
# print("INSERT INTO HorFragment Values(3, 11, 'Children');")
# print("INSERT INTO HorFragment Values(3, 12, 'Children');")



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

# other data

print("INSERT INTO Fragments Values(9 , 1, 'Hor', 'Room');")
print("INSERT INTO Fragments Values(10, 2, 'Hor', 'Room');")
print("INSERT INTO Fragments Values(11, 3, 'Hor', 'Room');")
print("INSERT INTO Fragments Values(12, 1, 'Ver', 'Guest');")
print("INSERT INTO Fragments Values(13, 2, 'Ver', 'Guest');")
print("INSERT INTO Fragments Values(14, 3, 'Ver', 'Guest');")
print("INSERT INTO Fragments Values(15, 1, 'DHor', 'Reserve');")
print("INSERT INTO Fragments Values(16, 2, 'DHor', 'Reserve');")
print("INSERT INTO Fragments Values(17, 3, 'DHor', 'Reserve');")




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


print("INSERT INTO DHorFragment Values(15, 20, 9, '1');")
print("INSERT INTO DHorFragment Values(15, 21, 9, '1');")
print("INSERT INTO DHorFragment Values(15, 22, 9, '1');")
print("INSERT INTO DHorFragment Values(16, 20, 10,'2');")
print("INSERT INTO DHorFragment Values(16, 21, 10,'2');")
print("INSERT INTO DHorFragment Values(16, 22, 10,'2');")
print("INSERT INTO DHorFragment Values(17, 20, 11,'3');")
print("INSERT INTO DHorFragment Values(17, 21, 11,'3');")
print("INSERT INTO DHorFragment Values(17, 22, 11,'3');")

print("CREATE TABLE `Room` (id int not null, city varchar(10) not null, reserveId int not null, roomNo int not null);")
print("CREATE TABLE `Reserve` ( reserveId int not null, checkIn varchar(10) not null, checkOut varchar(10) not null);")

#site 1
print("CREATE TABLE `Guest` ( id int not null, reserveId int not null, name varchar(10) not null);")
print("CREATE TABLE `Guest` ( id int not null, address varchar(50) not null, email varchar(20) not null, phone varchar(10) not null, city varchar(10) not null);")
print("CREATE TABLE `Guest` ( id int not null, payment varchar(10) not null);")

print("INSERT INTO `Room` VALUES(1, 'Delhi', 1, 401);")
print("INSERT INTO `Room` VALUES(2, 'Delhi', 2, 402);")
print("INSERT INTO `Room` VALUES(3, 'Delhi', 3, 404);")
print("INSERT INTO `Room` VALUES(4, 'Delhi', 4, 501);")

print("INSERT INTO `Room` VALUES(5, 'Goa', 5, 203);")
print("INSERT INTO `Room` VALUES(6, 'Goa', 6, 201);")
print("INSERT INTO `Room` VALUES(7, 'Goa', 7, 601);")
print("INSERT INTO `Room` VALUES(8, 'Goa', 8, 999);")

print("INSERT INTO `Room` VALUES(9, 'Pune', 9, 205);")
print("INSERT INTO `Room` VALUES(10, 'Pune', 10, 206);")
print("INSERT INTO `Room` VALUES(11, 'Pune', 11, 207);")
print("INSERT INTO `Room` VALUES(12, 'Pune', 12, 210);")


print("INSERT INTO `Reserve` VALUES(1, '12:00:01', '13:00:05');")
print("INSERT INTO `Reserve` VALUES(2, '12:10:01', '12:02:05');")
print("INSERT INTO `Reserve` VALUES(3, '12:10:01', '11:01:05');")
print("INSERT INTO `Reserve` VALUES(4, '12:00:31', '14:01:00');")

print("INSERT INTO `Reserve` VALUES(5, '12:00:11', '14:00:00');")
print("INSERT INTO `Reserve` VALUES(6, '12:00:51', '11:00:25');")
print("INSERT INTO `Reserve` VALUES(7, '14:00:01', '13:20:25');")
print("INSERT INTO `Reserve` VALUES(8, '16:00:01', '11:00:25');")

print("INSERT INTO `Reserve` VALUES(9, '18:00:01', '13:00:11');")
print("INSERT INTO `Reserve` VALUES(10, '12:10:01', '13:00:05');")
print("INSERT INTO `Reserve` VALUES(11, '12:03:01', '12:00:05');")
print("INSERT INTO `Reserve` VALUES(12, '12:20:01', '12:00:05');")

print("INSERT INTO `Guest` Values(1, 1, 'name1');")
print("INSERT INTO `Guest` Values(2, 2, 'name2');")
print("INSERT INTO `Guest` Values(3, 3, 'name3');")
print("INSERT INTO `Guest` Values(4, 4, 'name4');")
print("INSERT INTO `Guest` Values(5, 5, 'name5');")
print("INSERT INTO `Guest` Values(6, 6, 'name6');")
print("INSERT INTO `Guest` Values(7, 7, 'name7');")
print("INSERT INTO `Guest` Values(8, 8, 'name8');")
print("INSERT INTO `Guest` Values(9, 9, 'name9');")
print("INSERT INTO `Guest` Values(10, 10, 'name10');")
print("INSERT INTO `Guest` Values(11, 11, 'name11');")
print("INSERT INTO `Guest` Values(12, 12, 'name12');")


print("INSERT INTO `Guest` Values(1, 'address1', 'email1', 'phone1', 'city1');")
print("INSERT INTO `Guest` Values(2, 'address2', 'email2', 'phone2', 'city2');")
print("INSERT INTO `Guest` Values(3, 'address3', 'email3', 'phone3', 'city3');")
print("INSERT INTO `Guest` Values(4, 'address4', 'email4', 'phone4', 'city4');")
print("INSERT INTO `Guest` Values(5, 'address5', 'email5', 'phone5', 'city5');")
print("INSERT INTO `Guest` Values(6, 'address6', 'email6', 'phone6', 'city6');")
print("INSERT INTO `Guest` Values(7, 'address7', 'email7', 'phone7', 'city7');")
print("INSERT INTO `Guest` Values(8, 'address8', 'email8', 'phone8', 'city8');")
print("INSERT INTO `Guest` Values(9, 'address9', 'email9', 'phone9', 'city9');")
print("INSERT INTO `Guest` Values(10, 'address10', 'email10', 'phone10', 'city10');")
print("INSERT INTO `Guest` Values(11, 'address11', 'email11', 'phone11', 'city11');")
print("INSERT INTO `Guest` Values(12, 'address12', 'email12', 'phone12', 'city12');")



print("INSERT INTO `Guest` Values(1, 'yes');")
print("INSERT INTO `Guest` Values(2, 'yes');")
print("INSERT INTO `Guest` Values(3, 'no');")
print("INSERT INTO `Guest` Values(4, 'yes');")
print("INSERT INTO `Guest` Values(5, 'no');")
print("INSERT INTO `Guest` Values(6, 'no');")
print("INSERT INTO `Guest` Values(7, 'yes');")
print("INSERT INTO `Guest` Values(8, 'yes');")
print("INSERT INTO `Guest` Values(9, 'no');")
print("INSERT INTO `Guest` Values(10,'no');")
print("INSERT INTO `Guest` Values(11,'yes');")
print("INSERT INTO `Guest` Values(12,'yes');")
