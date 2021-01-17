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
			voter_id = int(data[i][0])
			data[i][0] = voter_id
		except:
			print(f'Could not convert line {data[i][0]} into an integer.')
	# https://stackoverflow.com/questions/16310015/what-does-this-mean-key-lambda-x-x1
	data.sort(key=lambda x: x[2])
	return data

def count_votes(ballots):
	counted_ballots = { }
	for ballot in ballots:
		if ballot[2] in counted_ballots.keys():
			counted_ballots[ballot[2]] = counted_ballots[ballot[2]] + 1
		else:
			counted_ballots[ballot[2]] = 1
	ballot_list = list(zip(list(counted_ballots.keys()), list(counted_ballots.values())))
	# https://stackoverflow.com/questions/16310015/what-does-this-mean-key-lambda-x-x1
	ballot_list.sort(key=lambda x: x[1])
	ballot_list.reverse()
	return ballot_list

# Voter ID,County,Candidate
# 12864552,Marsh,Khan

data = clean_data(get_raw_csv_list(True, 'Resources', 'election_data.csv'))

#   * The total number of votes cast
data_length = len(data)

#   * A complete list of candidates who received votes
candidates = count_votes(data)
candidates_count = len(candidates)

#   * The percentage of votes each candidate won

#   * The total number of votes each candidate won

#   * The winner of the election based on popular vote.


analysis_data=[
  f'  Financial Analysis',
  f'  Election Results',
  f'  -------------------------',
  f'  Total Votes: {data_length}',
  f'  -------------------------',
  f'  -------------------------',
  f'  Winner: {candidates[0][0]}',
  f'  -------------------------' ]

for i in range(candidates_count):
	percent = 100 * (candidates[i][1]/data_length)
	analysis_data.insert(5 + i , f"  {candidates[i][0]}: {percent:.3f}% ({candidates[i][1]})")
	
write_text_file(analysis_data, 'Analysis', 'analysis.txt')

for line in analysis_data:
	print(line)
