import csv
import pandas as pd
import random
import numpy as np
import sys
import getopt
from nltk.tokenize import sent_tokenize, word_tokenize
import os
import statistics
import re




def get_data_1_run_all(ordner,ordner_run,ip_2): # ds data und run data
    tsv_list_results  = get_data_1_run_tsv(ordner,ordner_run)
    tsv_runtime = get_runtime(ordner,ordner_run)
    if ip_2 == "y":
        tsv_list_ds = get_data_1_run_ds(ordner,ordner_run)
    #print(tsv_runtime)
    liste_for_save =  tsv_list_results + [tsv_runtime]
    if ip_2 == "y":
        liste_for_save = tsv_list_results + [tsv_runtime] + tsv_list_ds
    return liste_for_save

def get_data_1_run_ds(ordner,ordner_run):
    df = pd.read_csv(str(ordner) + "/" + ordner_run + "/" + "DS_results.tsv"  ,header=0, sep="\t")
    anz_rel_test  = get_column_name_list(df)[1]
    all_other_val = get_all_colums(df)[1]
    anz_test_abstracts = all_other_val[0]
    anz_rel_train = all_other_val[1]
    anz_train_abstracts = all_other_val[2]
    gesanz_rel = all_other_val[3]
    gesanz_abstarcts = all_other_val[4]
    anteil_rel_test_ges = rund_str(float(get_column_name_list(df)[1]) / float(all_other_val[3]))
    null_eins_verh_test = rund_str(all_other_val[5])
    null_eins_verh_train = rund_str(all_other_val[6])
    null_eins_verh_test_train = rund_str(all_other_val[7])
    output_list_tsv = [anz_rel_test, anz_test_abstracts,anz_rel_train,anz_train_abstracts,gesanz_rel,gesanz_abstarcts,anteil_rel_test_ges,null_eins_verh_test,null_eins_verh_train,null_eins_verh_test_train]
    return output_list_tsv

def df_to_list(df,column):
    #print(df)
    #print(column)
    list_1 = list(df[column])
    #print(list_1)
    return list_1



def get_data_1_run_tsv(ordner,ordner_run):
    df = pd.read_csv(str(ordner) + "/" + ordner_run + "/" + "test_scores.tsv"  ,header=0, sep="\t")
    f1  = rund_str(get_column_name_list(df)[1])
    all_other_val = get_all_colums(df)[1]
    reca = rund_str(all_other_val[0])
    prec = rund_str(all_other_val[1])
    spec = rund_str(all_other_val[2])
    output_list_tsv = [str(ordner_run), str(f1),str(reca),str(prec),str(spec)]
    return output_list_tsv

def rund_str(str):
    return round(float(str),3)

    #for ind in df.index:
        #print(ind)

def get_column_name_list(df):
	column_name_list = []
	for col in df.columns:
		column_name_list.append(col)
	return column_name_list

def get_all_colums(df):
    column_name_list = get_column_name_list(df)
    #print(column_name_list)
    tsv_as_list = []
    for column_name in column_name_list:
        column_as_list  = []
        #print(df,column_name)
        #print("XXXXX")
        column_as_list = df_to_list(df,column_name)
        tsv_as_list.append(column_as_list)
    return tsv_as_list

def get_runtime(ordner,ordner_run):
    df = pd.read_csv(str(ordner) + "/" + ordner_run + "/" + "run_laufzeit.tsv"  ,header = 0, sep="\t")
    runtime_full  = get_column_name_list(df)[0]
    #print(runtime_full)
    return round_runtime(runtime_full)

def round_runtime(rt):
    a = float(rt)
    min = a / 60
    #print("min:",min)
    h = round((min /60),2)
    min_ueber  = round((min % 60),2)
    #print("minüber:",min_ueber)
    sek = round((min_ueber - int(min_ueber)) * 60)
    #print(sek)
    output = str(int(h)) + "h " + str(int(min_ueber)) + "min " + str(sek)+ "sek"
    return output




def write_data_1_run_in_results_tsv_title(ordner,ip_2):
    with open(str(ordner) + "/" + 'results.tsv', 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        if ip_2 == "y":
            tsv_writer.writerow(['run', 'f1', 'recall', 'precision', 'specifity', "runtime"])
            out_file.close()
        else:
            tsv_writer.writerow(['run', 'f1', 'recall', 'precision', 'specifity', "runtime", 'anzahl rel in test.tsv',"davon anzahl der abstracts","anzahl rel in train.tsv"," davon anzahl der abstracts","gesamtanzahl rel","gesamtanzahl Abstracts","anteil test rel an rel ges", "1/0 Verhältnis test.tsv", "1/0 Verhältnis train.tsv", "1/0 Verhältnis test/train.tsv"])
            out_file.close()

def write_data_1_run_in_results_tsv(ordner,print_list):
    with open(str(ordner) + "/" + 'results.tsv', 'a') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(print_list)

def runtime_med_std(runtime_li):
    #print(type(runtime_li))
    a = re.findall(r'\d+',runtime_li)
    #print(type(float(a[0])))
    in_sek = float(a[0])*3600 + float(a[1]) * 60 + float(a[2])
    return in_sek

def add_std_in_results_and_med(ordner):
    df = pd.read_csv(str(ordner) + "/" + 'results.tsv',header=0, sep="\t")
    column_name  = get_column_name_list(df)
    #print(column_name)
    #print(column_name)
    all_other = get_all_colums(df)
    #print(all_other)
    all_other_std = []
    all_other_med = []
    all_run_times = []
    for li in all_other[1:5]:
        #print(li)
        all_other_std.append(statistics.stdev(list_to_float(li)))
        all_other_med.append(statistics.mean(list_to_float(li)))
    for li_run in all_other[5]:
        all_run_times.append(runtime_med_std(li_run))

    #print(all_run_times)
    med_runtime = statistics.mean(all_run_times)
    std_runtime = statistics.stdev(all_run_times)
    add_list = ["Standardabweichung:"] + round_list(all_other_std) + [round_runtime(std_runtime)]
    add_list_2 = ["Mittelwert"] + round_list(all_other_med) + [round_runtime(med_runtime)]
    with open(str(ordner) + "/" + 'results.tsv', 'a') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(add_list_2)
        tsv_writer.writerow(add_list)

def list_to_float(li):
    li_out = []
    for el in li:
        li_out.append(float(el))
    return li_out

def round_list(li):
    li_out = []
    for el in li:
        li_out.append(round(el,3))
    return li_out

def main():
    ip = "y"
    ip_2 = "n"
    argv  =sys.argv[1:]
    opts, argv = getopt.getopt(argv, "f")
    if argv[0] in os.listdir():
        print(">>> auswertung beginnt")
        ordner = argv[0]
        write_data_1_run_in_results_tsv_title(ordner,ip_2)
        #print(sorted(os.listdir(str(ordner) + "/")))
        for ordner_run in sorted(os.listdir(str(ordner) + "/")):
            if ordner_run == 'results.tsv' or ordner_run == '.~lock.results.tsv#':
                continue
            else:
                write_data_1_run_in_results_tsv(ordner,get_data_1_run_all(ordner,ordner_run,ip_2))
                #get_data_1_run_all(ordner,ordner_run)
    else:
        print("!!!angegebener Ordner nicht existent ")
    if ip == "y":
        add_std_in_results_and_med(ordner)
    print('>>> results.tsv erfolgreich erstellt')






###############################################################################
#run


main()
