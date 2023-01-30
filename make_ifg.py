#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:00:12 2020

@author: duttar
"""

import os 
#import numpy as np
import argparse

parser = argparse.ArgumentParser(description='generate config files for new IFG pairs')
parser.add_argument('-m', '--master', type=int, metavar='', required=True, help='Master date')
parser.add_argument('-s', '--slave', type=int, metavar='', required=True, help='Slave date')
parser.add_argument('-sd', '--stackdir', type=str, metavar='', required=True, help='Path to the stack directory')
parser.add_argument('-eg', '--ex_ifgpair', type=str, metavar='', required=True, help='Example IFG pair already processed, eg.: 20200407_20200513')

args = parser.parse_args()

stack_dir = args.stackdir
ex_ifgpair = args.ex_ifgpair
conf_dir = stack_dir + '/configs'
copyfile = stack_dir + '/configs/config_generate_igram_' + ex_ifgpair
pres_dir = stack_dir+ '/run_files_yrifgs'

sys_comm1 = 'cp '+copyfile + ' '+ pres_dir + '/.'
os.system(sys_comm1)

mas_input = args.master
sla_input = args.slave

mas_input = str(mas_input)
sla_input = str(sla_input)

sys_comm2 = 'mv '+ pres_dir + '/config_generate_igram_' + ex_ifgpair + ' ' + \
    pres_dir+'/config_generate_igram_'+mas_input+'_'+sla_input
os.system(sys_comm2)

filename= pres_dir+'/config_generate_igram_'+mas_input+'_'+sla_input
a_file = open(filename, "r")
list_of_lines = a_file.readlines()
list_of_lines[5] = 'reference : '+ stack_dir + '/coreg_secondarys/' + mas_input + '\n'
list_of_lines[6] = 'secondary : '+ stack_dir + '/coreg_secondarys/' + sla_input + '\n'
list_of_lines[7] = 'interferogram : '+ stack_dir + '/interferograms/' + mas_input+'_'+sla_input + '\n'

a_file = open(filename, "w")
a_file.writelines(list_of_lines)
a_file.close()    

print('created the file: '+filename)
sys_comm3 = 'echo SentinelWrapper.py -c ' + stack_dir + '/configs/config_generate_igram_'+mas_input+'_'+sla_input+' >> run_13_new'
os.system(sys_comm3)


copyfile = stack_dir+ '/configs/config_merge_igram_'+ ex_ifgpair

sys_comm1 = 'cp '+copyfile + ' '+ pres_dir + '/.'
os.system(sys_comm1)

sys_comm2 = 'mv '+ pres_dir + '/config_merge_igram_'+ ex_ifgpair + ' '+ \
    pres_dir+'/config_merge_igram_'+mas_input+'_'+sla_input
os.system(sys_comm2)

filename= pres_dir+'/config_merge_igram_'+mas_input+'_'+sla_input
a_file = open(filename, "r")
list_of_lines = a_file.readlines()
list_of_lines[6] = 'inp_reference : '+stack_dir +'/interferograms/' + \
    mas_input+'_'+sla_input + '\n'
list_of_lines[7] = 'dirname : '+stack_dir +'/interferograms/' + \
    mas_input+'_'+sla_input + '\n'
list_of_lines[9] = 'outfile : '+stack_dir +'/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/fine.int\n'

a_file = open(filename, "w")
a_file.writelines(list_of_lines)
a_file.close()

print('created the file: '+filename)
sys_comm3 = 'echo SentinelWrapper.py -c ' + stack_dir + '/configs/config_merge_igram_'+mas_input+'_'+sla_input+' >> run_14_new'
os.system(sys_comm3)


copyfile = stack_dir+ '/configs/config_igram_filt_coh_' + ex_ifgpair

sys_comm1 = 'cp '+copyfile + ' '+ pres_dir + '/.'
os.system(sys_comm1)

sys_comm2 = 'mv '+ pres_dir + '/config_igram_filt_coh_' + ex_ifgpair + ' '+ \
    pres_dir+'/config_igram_filt_coh_'+mas_input+'_'+sla_input
os.system(sys_comm2)

filename= pres_dir+'/config_igram_filt_coh_'+mas_input+'_'+sla_input
a_file = open(filename, "r")
list_of_lines = a_file.readlines()
list_of_lines[5] = 'input : '+stack_dir +'/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/fine.int\n'
list_of_lines[6] = 'filt : '+stack_dir +'/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/filt_fine.int\n'
list_of_lines[7] = 'coh : '+stack_dir +'/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/filt_fine.cor\n'
list_of_lines[9] = 'slc1 : '+stack_dir +'/merged/SLC/' + \
    mas_input+'/'+mas_input + '.slc.full\n'
list_of_lines[10] = 'slc2 : '+stack_dir +'/merged/SLC/' + \
    sla_input+'/'+sla_input + '.slc.full\n'
list_of_lines[11] = 'complex_coh : '+stack_dir +'/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/fine.cor\n'

a_file = open(filename, "w")
a_file.writelines(list_of_lines)
a_file.close() 

print('created the file: '+filename)
sys_comm3 = 'echo SentinelWrapper.py -c ' + stack_dir + '/configs/config_igram_filt_coh_'+mas_input+'_'+sla_input+' >> run_15_new'
os.system(sys_comm3)

copyfile = stack_dir+ '/configs/config_igram_unw_' + ex_ifgpair

sys_comm1 = 'cp '+copyfile + ' '+ pres_dir + '/.'
os.system(sys_comm1)

sys_comm2 = 'mv '+ pres_dir + '/config_igram_unw_' + ex_ifgpair + ' '+ \
    pres_dir+'/config_igram_unw_'+mas_input+'_'+sla_input
os.system(sys_comm2)

filename= pres_dir+'/config_igram_unw_'+mas_input+'_'+sla_input
a_file = open(filename, "r")
list_of_lines = a_file.readlines()
list_of_lines[5] = 'ifg : '+stack_dir +'/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/filt_fine.int\n'
list_of_lines[6] = 'unw : '+stack_dir +'/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/filt_fine.unw\n'
list_of_lines[7] = 'coh : '+stack_dir +'/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/filt_fine.cor\n'

a_file = open(filename, "w")
a_file.writelines(list_of_lines)
a_file.close() 

print('created the file: '+filename)
sys_comm3 = 'echo SentinelWrapper.py -c ' + stack_dir + '/configs/config_igram_unw_'+mas_input+'_'+sla_input+' >> run_16_new'
os.system(sys_comm3)


# move all config files now to configs directory
sys_comm4 = 'mv config_* ' + stack_dir + '/configs/.'
os.system(sys_comm4)
