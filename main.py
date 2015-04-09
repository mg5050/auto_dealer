#============Private functions============
#=========================================
#=========================================
def query(text):
	#print "\nQUERY: "+text
	return curs.execute(text)
	
def fetchService(service, col):
	return fetchCol("service", col, "name = \""+service+"\"")

def fetchCar(vin, col):
	return fetchCol("car", col, "vin = "+str(vin))
	
def fetchAppt(cust, vin, date, col):
	return fetchCol("appt", col, "cust = \""+cust+"\" and vin = "+str(vin)+" and date = \""+date+"\"")
	
def fetchCol(table, col, cond):
	query("select "+col+" from "+table+" where "+cond)
	return fetchResult(queryResult(), 0)
	
def printResult(result, col):
	txt = ""
	for row in result:
		txt += fetchResult(row, col)
	return txt
		
def fetchResult(result, index):
	return result[index]

def queryResult():
	return curs.fetchone()
	
def fetchCols(table, col, cond):
	query("select "+col+" from "+table+" where "+cond)
	return queryResults()
	
def queryResults():
	return curs.fetchall()
	
def fetchSalesCost(start, end):
	return fetchCols("car, sale", "car.cost", "car.vin = sale.vin AND sale.ds >= \""+start+"\" and sale.ds <= \""+end+"\"")
	
def fetchSales(start, end, col):
	return fetchCols("sale", col, "ds >= \""+start+"\" and ds <= \""+end+"\"")
	
def fetchSale(vin, col):
	return fetchCol("sale", col, "vin = "+str(vin))
	
def fetchCarsSoldDate(make, model, year, start, end):
	return fetchCols("car, sale", "car.vin", 
	"make = \""+make+"\" AND model = \""+model+"\" AND year = \""+year+"\" AND owner <> \"none\" AND car.vin = sale.vin AND sale.ds >= \""+start+"\" and sale.ds <= \""+end+"\"")
	
def custExist(name):
	query("select * from customer where name = \""+name+"\"")
	if(curs.fetchone() != None): return True
	return False
	
def updateCarOwner(vin, cust):
	query("update car set owner = \""+cust+"\" where vin = "+str(vin))
	return
	
def calcProfit(vin):
	income = int(fetchSale(vin, "price"))
	cost = int(fetchCar(vin, "cost"))
	profit = income - cost
	return profit
	
def calcProfits(make, model, year, start, end):
	profit = 0
	result = fetchCarsSoldDate(make, model, year, start, end)
	for car in result:
		profit += calcProfit(fetchResult(car,0))
	return profit
	
def addSale(cust, vin, price, date):
	query("insert into sale (cust, vin, price, ds) values(\""+cust+"\", "+str(vin)+", "+str(price)+", \""+date+"\")")
	updateCarOwner(vin, cust)
	return
	
def calcAllProfits(start, end):
	query("select distinct make, model, year from car")
	distinct_cars = queryResults()
	txt = ""
	for car in distinct_cars:
		make = fetchResult(car,0)
		model = fetchResult(car,1)
		year = str(fetchResult(car,2))
		txt += "\n" + year + " " + make + " " + model
		txt += "Gross Profits: " + str(calcProfits(make, model, year, start, end))
	return txt
		
def printServiceBill(cust, vin, yr, mk, mdl, date, time, service, duration, cost):
	txt = ""
	txt += "\nName: "+cust
	txt += "\nVIN: "+str(vin)
	txt += "\nYear: "+str(yr)
	txt += "\nMake: "+mk
	txt += "\nModel: "+mdl
	txt += "\nDate of Service: "+date
	txt += "\nTime of Service: "+time
	txt += "\nService Type: "+service
	txt += "\nService Duration: "+str(duration)
	txt += "\nService Cost: "+str(cost)
	return txt
#============Public functions=============
#=========================================
#=========================================
def addCust(name, email):
	print name + email
	if(custExist(name)): print "Customer already exists"
	else: query("insert into customer (name, email) values(\"" + name + "\", \"" + email + "\");")
	return
	
def startAppt(cust, vin, date, time, service):
	query("insert into appt (cust , vin , date , time , service) values (\""+cust+"\","+str(vin)+", \""+date+"\", \""+time+"\", \""+service+"\")")
	return

def finishAppt(cust, vin, date, time):
	yr = fetchCar(vin, "year")
	mk = fetchCar(vin, "make")
	mdl = fetchCar(vin, "model")
	service = fetchAppt(cust, vin, date, "service")
	duration = fetchService(str(service), "dur")
	cost = fetchService(str(service), "price")
	return printServiceBill(cust, vin, yr, mk, mdl, date, time, service, duration, cost)
	
def SellCar(cust, vin, price, date):
	if not(custExist(cust)): 
		print "Add customer first"
		return
		
	addSale(cust, vin, price, date)
	return printSaleBill(cust, vin, price, date)
	
def printSaleBill(cust, vin, price, date):
	yr = fetchCar(vin, "year")
	mk = fetchCar(vin, "make")
	mdl = fetchCar(vin, "model")
	txt =  "\n===Bill of Sale==="
	txt += "\nVIN: "+str(vin)
	txt += "\nYear: "+str(yr)
	txt += "\nMake: "+mk
	txt += "\nModel: "+mdl
	txt += "\nSold to: "+cust
	txt += "\nDate: "+date
	txt += "\nPrice: "+str(price)
	return txt

def saleStats(start, end):
	gross_income = 0
	gross_cost = 0
	gross_profit = 0
	cars_sold = 0
	txt = ""
	result = fetchSales(str(start), str(end), "price")
	for car in result:
		cars_sold += 1
		gross_income += int(fetchResult(car, 0))
		
	result = fetchSalesCost(start, end)
		
	for cost in result:
		gross_cost += int(fetchResult(cost, 0))
		
	gross_profit = gross_income - gross_cost	
	
	txt += "\n-----Sale Statistics for "+start+" to "+end+"-----\n"
	txt += "Cars Sold: "+str(cars_sold)
	txt += "\nGross Income: "+str(gross_income)
	txt += "\nGross Expense: "+str(gross_cost)
	txt += "\nGross Profit: "+str(gross_profit)
	txt += calcAllProfits(start, end)
	print txt
	return txt
###===GUI===
def GUIAddCustomer():
	err = ""
	msg = "Sales - Add Customer"
	title = "GP AutoWorks"
	fields  = ["Name","Email"]
	vals = []
	vals = eg.multenterbox(msg,title, fields)
	while 1: 
		if vals == None: 
			break
		err = ""
		
		# look for errors in the returned values
		for i in range(len(fields)):
			if vals[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % vals[i])
			
		if err == "": 
			break # no problems found
		else:
			vals = eg.multenterbox(err, title, fields, vals)
	addCust(vals[0], vals[1])
	GUImain()
def GUISellCar():
	err = ""
	msg = "Sales - Sell Car"
	title = "GP AutoWorks"
	fields  = ["Customer Name","VIN #", "Price", "Date"]
	vals = []
	vals = eg.multenterbox(msg,title, fields)
	while 1: 
		if vals == None: 
			break
		err = ""
		
		# look for errors in the returned values
		for i in range(len(fields)):
			if vals[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % vals[i])
			
		if err == "": 
			break # no problems found
		else:
			vals = eg.multenterbox(err, title, fields, vals)
	txt = SellCar(vals[0], vals[1], vals[2], vals[3])
	eg.msgbox(txt)
	GUImain()
def GUIaddAppt():
	err = ""
	msg = "Service - Schedule Appointment"
	title = "GP AutoWorks"
	fields  = ["Customer Name","VIN #", "Date", "Time", "Service"]
	vals = []
	vals = eg.multenterbox(msg,title, fields)
	while 1: 
		if vals == None: 
			break
		err = ""
		
		# look for errors in the returned values
		for i in range(len(fields)):
			if vals[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % vals[i])
			
		if err == "": 
			break # no problems found
		else:
			vals = eg.multenterbox(err, title, fields, vals)
	startAppt(vals[0], vals[1], vals[2], vals[3], vals[4])
	GUImain()
def GUIfinishAppt():
	err = ""
	msg = "Service - Car Pickup "
	title = "GP AutoWorks"
	fields  = ["Customer Name","VIN #", "Date", "Time"]
	vals = []
	vals = eg.multenterbox(msg,title, fields)
	while 1: 
		if vals == None: 
			break
		err = ""
		
		# look for errors in the returned values
		for i in range(len(fields)):
			if vals[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % vals[i])
			
		if err == "": 
			break # no problems found
		else:
			vals = eg.multenterbox(err, title, fields, vals)
	txt = finishAppt(vals[0], vals[1], vals[2], vals[3])
	eg.msgbox(txt)
	GUImain()
def GUIsalesStats():
	err = ""
	msg = "Sales - Sales Statistics "
	title = "GP AutoWorks"
	fields  = ["Start Date","End Date"]
	vals = []
	vals = eg.multenterbox(msg,title, fields)
	while 1: 
		if vals == None: 
			break
		err = ""
		
		# look for errors in the returned values
		for i in range(len(fields)):
			if vals[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % vals[i])
			
		if err == "": 
			break # no problems found
		else:
			vals = eg.multenterbox(err, title, fields, vals)
	txt = saleStats(vals[0], vals[1])
	eg.msgbox(txt)
	GUImain()
def GUIshowCust():
	query("select * from customer")
	result = curs.fetchall()
	txt = ""
	for row in result:
		txt += "\nName: "+str(row[0])+" | Email: " + str(row[1])
	eg.msgbox(txt)
	GUImain()

def GUIshowCar():
	query("select * from car")
	result = curs.fetchall()
	txt = ""
	for row in result:
		txt += "\n\nVIN: "+ str(row[0]) + " MSRP: " + str(row[1]) + " Cost: " +str(row[2])+ " Make: "+str(row[3])+" Model: "+str(row[4])+" Year: "+str(row[5])+" Owner:" + str(row[6])
	eg.msgbox(txt)
	GUImain()
def GUIshowSale():
	query("select * from sale")
	result = curs.fetchall()
	txt = ""
	for row in result:
		txt += "\n\nCustomer: "+row[0]+" VIN: "+str(row[1])+" Paid: "+str(row[2])+ " Date: "+str(row[3])
	eg.msgbox(txt)
	GUImain()
def GUIshowAppt():
	query("select * from appt")
	result = curs.fetchall()
	txt = ""
	for row in result:
		txt += "\n\nCustomer: "+row[0]+" VIN: "+str(row[1])+" Date: "+str(row[2])+ " Time: "+str(row[3]) + " Service: "+str(row[4])
	eg.msgbox(txt)
	GUImain()
def GUImain():
	con.commit()
	title = "GP AutoWorks"
	msg     = "Choose Action"
	choices = ["Add Customer", "Sell Car", "Create Appointment", "Pickup Car", "Sales Statistics", "Show Customers", "Show Cars","Show Sales", "Show Appointments"]
	main = eg.choicebox(msg=msg, choices=choices, title=title)
	if(main == choices[0]):
		GUIAddCustomer()
	if(main == choices[1]):
		GUISellCar()
	if(main == choices[2]):
		GUIaddAppt()
	if(main == choices[3]):
		GUIfinishAppt()
	if(main == choices[4]):
		GUIsalesStats()
	if(main == choices[5]):
		GUIshowCust()
	if(main == choices[6]):
		GUIshowCar()
	if(main == choices[7]):
		GUIshowSale()
	if(main == choices[8]):
		GUIshowAppt()
	return 
###===Start Program===	
import mysql.connector
from mysql.connector import errorcode
import easygui as eg

try:
	con = mysql.connector.connect(user='root', password='efsdvvc2', host='127.0.0.1', database='main')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exists")
  else:
    print(err)

curs = con.cursor(buffered=True)


###===GUI actions here===

GUImain()
	
###===End===

con.commit()
con.close()







