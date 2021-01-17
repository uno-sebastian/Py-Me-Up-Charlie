import os
import csv
import time  

# return the list of values form 
# the csv file as a list
def get_raw_csv_list(skip_first_line, path, *paths):
	csv_path = ''
	# https://www.w3schools.com/python/gloss_python_function_arbitrary_arguments.asp
	if not paths:
		csv_path = os.path.join(path)
	else:
		csv_path = os.path.join(path, *paths)
	with open(csv_path) as csv_file:
		# CSV reader specifies delimiter and variable that holds contents
		csv_reader = csv.reader(csv_file, delimiter=',')
		# convert csv data into list
		csv_raw_data = list(csv_reader)
		#skip the first line
		if (skip_first_line):
			csv_raw_data.pop(0)
		# return value
		return csv_raw_data

# saves the list of strings into path
def write_text_file(lines, path, *paths):
	text_path = ''
	# https://www.w3schools.com/python/gloss_python_function_arbitrary_arguments.asp
	if not paths:
		text_path = os.path.join(path)
	else:
		text_path = os.path.join(path, *paths)
	with open(text_path, 'w') as text_file:
		# I prefer to get the length and 
		# iterate as a carryover from my C# habbits
		length = len(lines)
		for i in range(length):
			text_file.write(f'{lines[i]}\n')

def clean_data(data):
	if data is None:
		return data
	length = len(data)
	if length < 1:
		return data
	for i in range(length):
		try:
			# https://www.tutorialspoint.com/python3/time_strptime.htm
			# convert the string value of the time from Feb-2020
			# into a time struct object
			dt = time.strptime(data[i][0], '%b-%Y')
			data[i][0] = dt
		except:
			print(f'Could not convert line {data[i][0]} into time struct.')
		try:
			money = int(data[i][1])
			data[i][1] = money
		except:
			print(f'Could not convert line {data[i][1]} into integer.')
	# https://stackoverflow.com/questions/16310015/what-does-this-mean-key-lambda-x-x1
	data.sort(key=lambda x: x[0])
	return data

# Date,Profit/Losses
# Jan-2010,867884

data = clean_data(get_raw_csv_list(True, 'Resources', 'budget_data.csv'))
data_length = len(data)

#   * The total number of months included in the dataset
time_column = [val[0] for val in data]
# https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
# remove duplicates
time_column = list(set(time_column))
total_months = len(time_column)

#   * The net total amount of "Profit/Losses" over the entire period
total_money = 0
for line in data:
	total_money = total_money + line[1]

#   * Calculate the changes in "Profit/Losses" over the entire period, then find the average of those changes
month_prof_changes=[]
for i in range(1, data_length):
	month_prof_changes.append(data[i][1] - data[i-1][1])

average_change=0
for line in month_prof_changes:
	average_change = average_change + line
average_change = average_change/(data_length-1)

# https://www.tutorialspoint.com/python/list_max.htm
#   * The greatest increase in profits (date and amount) over the entire period
inc_in_prof = max(month_prof_changes)
inc_in_prof_month = data[1 + month_prof_changes.index(inc_in_prof)][0]
inc_in_prof_month = time.strftime('%b-%Y', inc_in_prof_month)

#   * The greatest decrease in losses (date and amount) over the entire periodtime_column = [val[0] for val in raw_data]
dec_in_prof = min(month_prof_changes)
dec_in_prof_month = data[1 + month_prof_changes.index(dec_in_prof)][0]
dec_in_prof_month = time.strftime('%b-%Y', dec_in_prof_month)

analysis_data=[
  f'  Financial Analysis',
  f'  ----------------------------',
  f'  Total Months: {total_months}',
  f'  Total: ${total_money}',
  f'  Average  Change: ${average_change:.2f}',
  f'  Greatest Increase in Profits: {inc_in_prof_month}',
  f'  Greatest Decrease in Profits: {dec_in_prof_month}' ]

write_text_file(analysis_data, 'Analysis', 'analysis.txt')

for line in analysis_data:
	print(line)