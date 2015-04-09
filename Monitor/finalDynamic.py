import math
import os, sys
import ROOT

class DataSet:
        def __init__(self, name, popularity, num_sites, size, files):
                self.name = name
		self.pop = popularity
                self.num = num_sites
                self.size = float(size)
		self.files = float(files)
        def __str__(self):
                return "DataSet(%s)" % (self.name)
        def __repr__(self):
                return self.__str__()

class Site:
        def __init__(self, name, size, used, wait):
                self.name = name
		self.size = float(size)
                self.used = float(used)
                self.wait = float(wait)
                self.empty = float(size) - used
        def __str__(self):
                return "Site(%s)" % (self.name)
        def __repr__(self):
                return self.__str__()

openFile = open(os.environ.get('DETOX_DB')+"status/DatasetsInPhedexAtSites.dat")
runningDataSets = [i.split() for i in openFile.readlines()]
dataSetsDict = {}
for i in runningDataSets:
    	if i[1] == 'AnalysisOps' and i[5][:2] == "T2":
       		if i[0] in dataSetsDict:
               		dataSetsDict[i[0]].append(i[5])
       		else:
               		dataSetsDict[i[0]] = [i[5]]

openFile = open(os.environ.get('MONITOR_DB')+"/DatasetSummaryAll.txt")
allDataSets = [i.split() for i in openFile.readlines()]
improvedDataSets = [DataSet(x[5], float(x[2]), len(dataSetsDict[x[5]]), float(x[4]), float(x[3])) for x in allDataSets]

def average_pop(x):
    try:
        return x.pop/(x.files*x.num)
    except ZeroDivisionError:
        print x
        sys.exit(-1)

def sort_data_insert(a, x, lo = 0, hi = None):
        if lo < 0:
                raise ValueError('lo must be non-negative')
        if hi is None:
                hi = len(a)
        while lo < hi:
                mid = (lo+hi)//2
                if average_pop(x) < average_pop(a[mid]): hi = mid
                else: lo = mid+1
        a.insert(lo, x)

dataSets = []
for i in improvedDataSets:
	if i.name in dataSetsDict:
		sort_data_insert(dataSets, i, 0, None)

waitTimeDicts = []

for i in range(int(raw_input("How many hours back should we look start logging in wait times: "))):
        waitTimeDicts.append(subprocess.call(['./WaitTimesQuick', "%i"%((i+1)*3600),"%i"%(i*3600)]))

combinedDict = {}
for i in waitTimeDicts:
	for j in i:
		combinedDict[j] = i[j]

siteLog = {}

for dataset in combinedDict:
	for site in combinedDict[dataset]:
		if site == 'unknown':
			continue
		else:
			if siteLog.has_key(site):
				siteLog[site].append([dataset, combinedDict[dataset][site]])
			else:
				siteLog[site] = [[dataset, combinedDict[dataset][site]]]

openFile = open(os.environ.get('MONITOR_DB')+"/MonitorSummary.txt")
allSites = [i.split() for i in openFile.readlines()]

siteAverageTime = {}

for i in allSites:
	siteAverageTime[i[0]] = 0.0

for site in siteLog:
	for entry in siteLog[site]:
		if siteAverageTime.has_key(site) and dataSetsDict.has_key(entry[0]):
			siteAverageTime[site] += entry[1]*data_set_dict[entry[0]]
		else:
			pass







openFile = open(os.environ.get('MONITOR_DB')+"/MonitorSummary.txt")
allSites = [i.split() for i in openFile.readlines()]
improvedSites = [Site(x[0], float(x[1]), float(x[2]), wait) for x in allSites]

def sort_site_insert(a, x, lo = 0, hi = None):
        if lo < 0:
                raise ValueError('lo must be non-negative')
        if hi is None:
                hi = len(a)
        while lo < hi:
                mid = (lo+hi)//2
                if x.wait < a[mid].wait: lo = mid+1
                else: hi = mid
        a.insert(lo, x)

sites = []
for i in improvedSites:
	sort_site_insert(sites, i, 0, None)

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
