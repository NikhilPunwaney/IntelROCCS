import math
import random
import ROOT

class DataSet:
	def __init__(self, name, popularity, num_sites, size):
		self.pop = popularity
		self.name = name
		self.num = num_sites
		self.size = float(size)
	def __str__(self):
    		return "DataSet(%s)" % (self.name)
	def __repr__(self):
    		return self.__str__()

class Site:
	def __init__(self, name, size, used, total, wait, jobs):
		self.size = float(size)
                self.name = name
                self.used = float(used)
		self.total = total
		self.wait = float(wait)
		self.jobs = jobs
		self.empty = float(size) - used
	def __str__(self):
                return "Site(%s)" % (self.name)
        def __repr__(self):
                return self.__str__()

class Job:
	def __init__(self, number, time, dataset):
		self.number = number
                self.time = float(time)
                self.dset = dataset
	def __str__(self):
                return "Job(%s)" % (self.number)
        def __repr__(self):
                return self.__str__()

DataSets = []
for i in range(1000):
	DataSets.append(DataSet(i, (random.random()*2.0)**2.0,  1, random.random()))

Sites = []
for i in range(50):
	Sites.append(Site(i, 100000, 1, [], 1, 1))

Jobs = []
count = 0
for i in DataSets:
	for j in range(int(i.pop*1000)):
		Jobs.append(Job(count, random.random(), i))
		count += 1

DataSets_Dict = {}
for i in DataSets:
	DataSets_Dict[i.name] = []

Sites_Dict = {}
for i in Sites:
	Sites_Dict[i.name] = []

for i in DataSets:
	x = int(random.random()*len(Sites))
	Sites_Dict[Sites[x].name].append(i.name)
	Sites[x].used += i.size
	DataSets_Dict[i.name].append(Sites[x].name)

for i in Jobs:
	dataset = i.dset.name
	choices = len(DataSets_Dict[dataset])
	x = int(random.random()*choices)
	site = DataSets_Dict[dataset][x]
	Sites[site].wait += float(i.time)
	Sites[site].jobs += 1

for i in Sites:
	i.total.append(i.wait)
	i.wait = 0

initialWaitTimes = []
sumWaitTimes = 0
for i in Sites:
	initialWaitTimes.append((i.name, i.total[0]))
	sumWaitTimes += i.total[0]
#print "Initial Site Average Wait Times: "
#print initialWaitTimes
print "Initial Average Site Wait Time: " + str(sumWaitTimes/len(Sites))

max_init = 0
min_init = float("inf")
for i in Sites:
        if i.total[0] < min_init:
                min_init = i.total[0]
        if i.total[0] > max_init:
                max_init = i.total[0]

print "Initial Max Wait Time: " + str(max_init)
print "Initial Min Wait Time: " + str(min_init)

threshold = float(raw_input("Threshold: "))
num_iterations = float(raw_input("Number of Iterations: "))

canvas = ROOT.TCanvas();
canvas.Divide(1,int(num_iterations)+1);

graph_init = ROOT.TH1D("Wait Times", "Wait Time", 30, 0, 30000);
graph_init.SetFillColorAlpha(1, 1);

for i in Sites:
    val = i.total[0]
    graph_init.Fill(val, 1)

canvas.cd(1);

graph_init.Draw()

def sort_data_insert(a, x, lo = 0, hi = None):
    	if lo < 0:
        	raise ValueError('lo must be non-negative')
    	if hi is None:
        	hi = len(a)
    	while lo < hi:
        	mid = (lo+hi)//2
        	if x.pop/x.num < a[mid].pop/a[mid].num: hi = mid
        	else: lo = mid+1
    	a.insert(lo, x)

def sort_site_insert(a, x, lo = 0, hi = None):
    	if lo < 0:
        	raise ValueError('lo must be non-negative')
    	if hi is None:
        	hi = len(a)
    	while lo < hi:
        	mid = (lo+hi)//2
        	if x.total[-1] < a[mid].total[-1]: lo = mid+1
        	else: hi = mid
    	a.insert(lo, x)

def distribution(listt):
    	d = [float(listt[0].total[-1] - i.total[-1]) for i in listt]
    	b = max(1,sum(d))
    	f = [float(x/b) for x in d]
    	g = [0.0]
    	for i in f:
        	g.append(float(g[-1]+i))
	return g

def get_ind(listt):
    	list_d = distribution(listt)
    	random_fl = random.random()
	for i in range(len(sorted_sites)):
       		if random_fl >= list_d[i] and random_fl < list_d[i+1]:
            		return i
        	else:
            		pass
	return int(random.random()*len(sorted_sites))  

def copying(listx):
    	a = listx.pop()
    	e_int = get_ind(sorted_sites)
    	while a.size > sorted_sites[e_int].empty or a.name in Sites_Dict[sorted_sites[e_int].name]:
        	e_int = get_ind(sorted_sites)
    	b = sorted_sites[e_int].name
    	sorted_sites.pop(e_int)
    	Sites[b].used += a.size
	Sites_Dict[b].append(a.name)
	DataSets[a.name].num += 1
	DataSets_Dict[a.name].append(b)
    	sort_site_insert(sorted_sites, Sites[b], 0, None)
	sort_data_insert(sorted_dataSets, DataSets[a.name], 0, None)

max_averagePopularity = 4.0
each_iteration = (max_averagePopularity - threshold)/num_iterations
iterations = [max_averagePopularity - float(i+1)*each_iteration for i in range(int(num_iterations))]

graph_list = []
for i in range(int(num_iterations)):
    graph_list.append('graph_'+str(i+1))

count = 0
for k in iterations:

	sorted_dataSets = []
	for i in DataSets:
        	sort_data_insert(sorted_dataSets, i, 0, None)

	sorted_sites = []
	for i in Sites:
	        sort_site_insert(sorted_sites, i, 0, None)
	
	while sorted_dataSets[-1].pop/sorted_dataSets[-1].num > k:
		copying(sorted_dataSets)

	for i in Jobs:
        	dataset = i.dset.name
        	min_sort = []
        	for j in range(len(DataSets_Dict[dataset])):
                	min_sort.append((j, Sites[DataSets_Dict[dataset][j]].wait))
		x = (None, float("inf"))
		for j in min_sort:
			if j[1] < x[1]:
				x = j
		site = DataSets_Dict[dataset][x[0]]
        	Sites[site].wait += float(i.time)
        	Sites[site].jobs += 1

	for i in Sites:
        	i.total.append(i.wait)
        	i.wait = 0

	newWaitTimes = []
	sumWaitTimes = 0
	for i in Sites:
        	newWaitTimes.append((i.name, i.total[-1]))
        	sumWaitTimes += i.total[-1]
#	print "New Site Average Wait Times: "
#	print newWaitTimes
	print "New Average Site Wait Time: " + str(sumWaitTimes/len(Sites))

	max_new = 0
	min_new = float("inf")
	for i in Sites:
		if i.total[-1] < min_new:
	                min_new = i.total[-1]
	        if i.total[-1] > max_new:
	                max_new = i.total[-1]

	print "New Max Wait Time: " + str(max_new)
	print "New Min Wait Time: " + str(min_new)
	
	globals()[graph_list[count]] = ROOT.TH1D(str(count+1), str(count+1), 30, 0, 30000)
	globals()[graph_list[count]].SetFillColorAlpha(count+2, 1)

	for i in Sites:
	    	val = i.total[-1]
	    	globals()[graph_list[count]].Fill(val, 1)
	
	canvas.cd(count+2)
	globals()[graph_list[count]].Draw()
	count += 1
	canvas.SaveAs("Graphs.png")
