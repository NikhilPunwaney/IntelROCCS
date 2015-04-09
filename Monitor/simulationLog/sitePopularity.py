#!/usr/bin/python

import os,sys

## Retrieving waitTimes files
execfile("runWaitTimes.py")
site_averageTime = site_averageTime
site_emptySpace = site_emptySpace
site_totalSpace = site_totalSpace
AnalysisOps_dict = AnalysisOps_dict
sitesPerData = sitesPerData

sorted_sample_byminscore = [('T2_AT_Vienna', site_averageTime['T2_AT_Vienna'], site_emptySpace['T2_AT_Vienna'], site_totalSpace['T2_AT_Vienna'])]

def sort_sites(a, x, lo = 0, hi = None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if site_averageTime[x] < a[mid][1]: lo = mid+1
        else: hi = mid
    a.insert(lo, (x, site_averageTime[x], site_emptySpace[x], site_totalSpace[x]))

## Populating our lists    
for i in site_averageTime:
    if i != 'T2_AT_Vienna':
        sort_sites(sorted_sample_byminscore, i, lo = 0, hi = None)
    else:
        pass

duplicates = []

def distribution(listt):
    d = [float(listt[0][1] - i[1]) for i in listt]
    b = sum(d)
    f = [float(x/b) for x in d]
    g = [0.0]
    for i in f:
	g.append(float(g[-1]+i))
    return g

import random

def get_ind(listt):
    list_d = distribution(listt)
    random_fl = random.random()
    for i in range(len(sorted_sample_byminscore)):
        if random_fl >= list_d[i] and random_fl < list_d[i+1]:
	    return i
	else:
	    pass

duplicate_sites = {}
max_dist = []

## Assuming we duplicated a dataset
def copying(listx):
    a = listx[-1]
    e_int = get_ind(sorted_sample_byminscore)
    breakloop = 0
    if breakloop > 29:
	max_dist.append(a)
	listx.pop()
    while float(a[0][4])/1000 > sorted_sample_byminscore[e_int][2]:
	e_int = get_ind(sorted_sample_byminscore)
    b = sorted_sample_byminscore[e_int][0]
    sorted_sample_byminscore.pop(e_int)
    site_emptySpace[b] -= float(a[0][4])/1000
    sort_sites(sorted_sample_byminscore, b, lo = 0, hi = None)
    duplicates.append((a[0], b))
    listx.pop()
    a[0][0] = str(int(a[0][0])+1)
    sitesPerData[a[0][5]] += 1 ## updating number of sites
    AnalysisOps_dict[a[0][5]].append(b)
    ## re-adding them to the sorted lists
    sort_it_1(listx, a[0], lo = 0, hi = None)
#    print "Copied " + a[0][5] + " to " + b
#    print b + " has " + str(100*site_emptySpace[b]/site_totalSpace[b]) + "% free space and " + str(site_averageTime[b]) + " seconds average wait time."
    duplicate_sites[b] = 1

#GRAPHS

row = int(raw_input("How many progressions do you want to see: "))+1
column = 1
initial_threshold = 200
final_threshold = int(raw_input("What should we set the final average popularity threshold to: "))
intervals = (initial_threshold - final_threshold)/float(row * column)
canvas = ROOT.TCanvas()
canvas1 = ROOT.TCanvas()
canvas2 = ROOT.TCanvas()
#canvas.Divide(column, row+1)
#canvas1.Divide(column, row+1)
#canvas2.Divide(column, row+1)

graphhh_0 = ROOT.TH1D("% Empty Space","% Empty Space",100,0,50)
graphh_0 = ROOT.TH1D("# Dataset Copies Distribution","# Dataset Copies Distribution",45,5,50)
graph_0 = ROOT.TH1D("Average Dataset Popularity Distribution","Average Dataset Popularity Distribution",100,0,initial_threshold)

graphhh_0.SetFillColorAlpha(1, 1)
graphh_0.SetFillColorAlpha(1, 1)
graph_0.SetFillColorAlpha(1, 1)

for k in site_emptySpace:
    val = 100*site_emptySpace[k]/site_totalSpace[k]
    graphhh_0.Fill(val, 1)

for k in sorted_sample_bymaxcurrent:
    vall = int(k[0][0])
    val = float(k[1])
    if vall > 5:
	graphh_0.Fill(vall, 1)
    else:
	pass
    if val < initial_threshold and val > 0.0:
        graph_0.Fill(val,vall*k[1]**2)
    else:
	pass

canvas1.cd()
graphh_0.Draw()
canvas.cd()
graph_0.Draw()
canvas2.cd()
graphhh_0.Draw()

graph_list = []
graphh_list = []
graphhh_list = []
for i in range(row*column):#(row * column - 1):
    graph_list.append('graph_'+str(i+1))
    graphh_list.append('graphh_'+str(i+1))
    graphhh_list.append('graphhh_'+str(i+1))

count_Sites = 0

for i in range(row*column):#(row * column - 1):
    while sorted_sample_bymaxcurrent[-1][1] > initial_threshold - (i+1)*intervals:
        copying(sorted_sample_bymaxcurrent)
	count_Sites += 1
    globals()[graphhh_list[i]] = ROOT.TH1D(str(initial_threshold - (i+1)*intervals + 2),str(initial_threshold - (i+1)*intervals),100,0,50)
    globals()[graph_list[i]] = ROOT.TH1D(str(initial_threshold - (i+1)*intervals + 1),str(initial_threshold - (i+1)*intervals),100,0,initial_threshold - (i+1)*intervals)
    globals()[graphh_list[i]] = ROOT.TH1D(str(initial_threshold - (i+1)*intervals),str(initial_threshold - (i+1)*intervals),45,5,50)
    for k in site_emptySpace:
        val = 100*site_emptySpace[k]/site_totalSpace[k]
        globals()[graphhh_list[i]].SetLineColor(i+2)
	globals()[graphhh_list[i]].SetFillColorAlpha(i+2, 1)
	globals()[graphhh_list[i]].Fill(val, 1)
    for k in sorted_sample_bymaxcurrent:
        vall = int(k[0][0])
	val = float(k[1])
	if vall > 5:
	    globals()[graphh_list[i]].SetLineColor(i+2)
	    globals()[graphh_list[i]].SetFillColorAlpha(i+2, 1)
	    globals()[graphh_list[i]].Fill(vall, 1)
	else: 
	    pass
        if val > 0.0 and val + 5 < initial_threshold - (i+1)*intervals:
            globals()[graph_list[i]].SetLineColor(i+2)
	    globals()[graph_list[i]].SetFillColorAlpha(i+2, 1)
	    globals()[graph_list[i]].Fill(val,vall*k[1]**2)
        else:
            pass
    canvas2.cd()
    globals()[graphhh_list[i]].Draw("same")
    canvas2.SaveAs("Graphs2.png")
    canvas1.cd()
    globals()[graphh_list[i]].Draw("same")
    canvas1.SaveAs("Graphs1.png")
    canvas.cd()
    globals()[graph_list[i]].Draw("same")
    canvas.SaveAs("Graphs.png")

canvas2.cd()
canvas2.SaveAs("Graphs2.png")
canvas1.cd()
canvas1.SaveAs("Graphs1.png")
canvas.cd()
canvas.SaveAs("Graphs.png")


print str(count_Sites) + ' data sets were duplicated across ' + str(len(duplicate_sites)) + ' different sites!'

###################

import os
import time

os.system("touch test_7_60.txt")

localtime = time.asctime( time.localtime(time.time()) )

with open("test_7_60.txt", "a") as mfile:
	mfile.write("date_time = ")
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

os.system("mv test_7_60.txt test_7_60.py")
