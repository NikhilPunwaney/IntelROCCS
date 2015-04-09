import subprocess
import ast
import os
os.system("rm output.txt")
os.system("touch output.txt")
os.system("touch condensedoutput.txt")
os.system("rm condensedoutput.py")

for i in range(int(raw_input("How many hours back should we look start logging in wait times: "))):
	subprocess.call(['./WaitTimesQuick', "%i"%((i+1)*3600),"%i"%(i*3600)])
f = open("output.txt")

x = []

for line in f.readlines():
	x = line.split('}{')

x[0] = x[0][1:]
x[-1] = x[-1][:len(x[-1])-1]

with open("condensedoutput.txt", "a") as myfile:
	myfile.write('log_files = {')
	for i in x:    
		myfile.write(i)
		myfile.write(', ')
	myfile.write('}')

os.system("mv condensedoutput.txt condensedoutput.py")

site_log = dict()
site_averageTime = dict()

execfile('condensedoutput.py')

log_files = log_files

for dataset in log_files:
  for site in log_files[dataset]:
    if site == 'unknown':
      continue
    else:
      if site_log.has_key(site):
        site_log[site].append([dataset, log_files[dataset][site]])
      else:
        site_log[str(site)] = [[str(dataset), log_files[dataset][site]]]

execfile('dataSetPopularity')

AnalysisOps_dict = AnalysisOps_dict
sitesPerData = sitesPerData

sorted_sample_bymaxcurrent = sorted_sample_bymaxcurrent
data_set_dict = dict()
for i in sorted_sample_bymaxcurrent:
  a = i[0]
  data_set_dict[a[5]] = float(a[2])*float(a[4])/float(a[3])

## Retrieving site summary
openfile = open("log/IntelROCCS/Monitor/MonitorSummary.txt")
all_sites = [i.split() for i in openfile.readlines()]

for i in all_sites:
  site_averageTime[i[0]] = 0.0

for site in site_log:
  for entry in site_log[site]:
    if site_averageTime.has_key(site) and data_set_dict.has_key(entry[0]):
      site_averageTime[site] += entry[1]*data_set_dict[entry[0]]
    else:
      pass

#site_emptySpace = dict()
site_emptySpace = yes_EmpSpa
site_totalSpace = dict()
for i in all_sites:
  #site_emptySpace[i[0]] = 0.9*float(i[1]) - float(i[2])
  site_totalSpace[i[0]] = float(i[1])

############

comment = '''
import os
import time

os.system("touch initial.txt")

localtime = time.asctime( time.localtime(time.time()) )

with open("initial.txt", "a") as mfile:
        mfile.write(str(localtime))
        mfile.write("\n")
        mfile.write("yes_AnalOps = ")
        mfile.write(str(AnalysisOps_dict))
        mfile.write("\n")
        mfile.write("yes_SorSam = ")
        mfile.write(str(sorted_sample_bymaxcurrent))
	mfile.write("\n")
        mfile.write("yes_EmpSpa = ")
        mfile.write(str(site_emptySpace))
'''

	
