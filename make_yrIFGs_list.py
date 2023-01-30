import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Plots all the results of ISCE filterred wrapped interfrograms from Sentinel stack processing.')
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Date list of IFGs')
parser.add_argument('-sd', '--sd', type=str, metavar='', required=True, help='Path')
parser.add_argument('-eg', '--eg', type=str, metavar='', required=True, help='Date')

args = parser.parse_args()


date12List = np.loadtxt(args.input, dtype=bytes).astype(str) # number of interferograms
mDates = [i.split('_')[0] for i in date12List] # master date
sDates = [i.split('_')[1] for i in date12List] # slave date

# master month
mMonth = [i for i in mDates if i.startswith(tuple(['201711','201712','201801','201811','201812','201901','201911', '201912', '202001', '202011' '2020212', '202101', '202111', '202112', '202201']))]
mMonth = [*set(mMonth)] # remove duplicate date

# slave month
sMonth = [i for i in mDates if i.startswith(tuple(['201711','201712','201801','201811','201812','201901','201911', '201912', '202001', '202011' '2020212', '202101', '202111', '202112', '202201']))]
sMonth = [*set(sMonth)] # remove duplicate date

# create new lsit
new = []

for i in range(len(mMonth)):
    for j in range(len(sMonth)): 
        if mMonth[i] == sMonth[j]: #same date
            continue
        elif int(mMonth[i]) > int(sMonth[j]): #difference
            continue
        elif (str(mMonth[i])+'_'+str(sMonth[j])) in date12List: #duplicate 
            continue
        else:
            new.append('python make_ifg.py -m ' + str(mMonth[i]) + ' -s ' + str(sMonth[j])+ ' -sd ' + args.sd + ' -eg ' + args.eg)

# open file in write mode
with open(r'yrsIFGs.txt', 'w') as fp:
    for lines in new:
        fp.write("%s\n" % lines)
    print('Done')
