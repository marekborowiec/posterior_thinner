#! /usr/bin/env python
# posterior_thinner.py by Marek Borowiec


from __future__ import division
import sys, re

Usage = """
Given burnin and samples_number this program extracts 
the desired number of samples from the posterior 
and writes a new file.
Usage:
	posterior_thinner.py your_sample_file.runX.p burnin trees_number > new_file.txt
Example:
	posterior_thinner.py my_ants_20m.run1.p 5000 1000 > thinned_my_ants.run1.txt
"""
# check if there are enough arguments passed
if len(sys.argv) < 4:
	print(Usage)

else:
	# define file name, burnin, and number of trees to be retained from sys.argv
	FileName = sys.argv[1]
	Burnin = sys.argv[2]
	Samples_no = sys.argv[3]
	
	# get all lines from the file
	All_lines_list = [line.split("\r\n") for line in open(FileName)]
	
	# assumes that the first two lines contain the header, as in MrBayes output
	Header = All_lines_list[:2]
	
	# all samples lines
	All_samples_list = All_lines_list[2:]
	
	# calculate at what interval the trees shuld be sampled from post-burnin 
	Iteration = ( len(All_samples_list) - int(Burnin) - 1 ) / int(Samples_no)
	
	# get only post-burnin trees (add one to account for the starting tree)
	No_burnin_samples = All_samples_list[(int(Burnin)):]

	# get the thinned sample of post-burnin trees
	try:
		Thinned_samples = No_burnin_samples[0::int(Iteration)]
	except ValueError:
		Thinned_samples = No_burnin_samples
		
	# print the header and thinned sample
	print str('\n'.join(map(str, Header))).replace("['", "").replace("\\n']", "").replace("', '", ";").replace('\\t','\t')
	print str('\n'.join(map(str, Thinned_samples))).replace("['", "").replace("\\n']", "").replace("', '", ";").replace('\\t','\t')
