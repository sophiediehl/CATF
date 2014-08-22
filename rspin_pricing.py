import os.path
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

# Get data from August 9-12
curmonth = 8
minday = 9
maxday = 12

hours = 4*24 # 4 days * 24 hours

# Get data from csv file
def get_rows(f):
    rows = []
    for row in csv.reader(f):
        rows.append(row)
    return rows

# Get day (false if not between august 9-12)
def get_day_index(date):
    month = int(date[0:2])
    day = int(date[3:5])
    if month==curmonth and day>=minday and day<=maxday:
	return day - minday
    return "NO"

# What load for each hour?
def get_load_data(folder_load):
    loads = [0]*hours
    ls = os.listdir(folder_load)
    for filename in ls:
	f = open(folder_load+'/'+filename, 'r')
	rows = get_rows(f) # Get file data
	day = get_day_index(rows[2][0]) # Get day index
	hour = int(rows[2][1][0:2]) # Get hour index
	f.close
	if day=="NO": continue # only use august 9-12
	# Collect load data
	load = float(rows[2][2]) # 2nd quarter of the hour
	loads[day*24 + hour] = load
    return loads

# What capacity for each hour?
def get_capacity_data(folder_gen):
    capacities = [0]*hours
    ls = os.listdir(folder_gen)
    for filename in ls:
        f = open(folder_gen+'/'+filename, 'r')
        rows = get_rows(f) # Get file data
        day = get_day_index(rows[1][0])
        f.close()
	if day=="NO": continue # only use august 9-12
        # Collect capacity data
	for hour in range(24):
	    row = rows[hour+1]
	    capacity = float(row[2])
	    capacities[day*24 + hour] = capacity
    return capacities

# What spinning reserve price for each hour?
def get_price_data(folder_price):
    prices = [0]*hours
    ls = os.listdir(folder_price)
    for filename in ls:
        f = open(folder_price+'/'+filename, 'r')
        rows = get_rows(f) # Get file data
        day = get_day_index(rows[1][0])
        f.close()
        if day=="NO": continue # only use august 9-12
        # Only take 2nd quarter of each hour
	if int(rows[1][2]) != 2: continue
	hour = int(rows[1][1]) - 1
	price = float(rows[1][3])
	prices[day*24 + hour] = price
    return prices

if __name__ == "__main__":
    loads = get_load_data(sys.argv[1]+\
	"/zipfiles_load_0812")
    capacities = get_capacity_data(sys.argv[1]+\
	"/zipfiles_gencap_0812")
    prices = get_price_data(sys.argv[1]+\
	"/zipfiles_rspinprice_0812")
    reserve = [capacities[i]-loads[i] for i in range(hours)]
    # Plot results
    print str(np.avg(prices))
    print str(np.avg(reserve))
    plt.plot(reserve, prices, 'ko')
    plt.xlabel("MW of spinning reserve")
    plt.ylabel("Dollars per MW*hour")
    plt.show()


