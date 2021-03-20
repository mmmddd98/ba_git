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




def get_data_1_run_all(ordner,ordner_run): # ds data und run data
    tsv_list_results  = get_data_1_run_tsv(ordner,ordner_run)
    tsv_list_ds = get_data_1_run_ds(ordner,ordner_run)
    #print(tsv_list_ds)
    tsv_runtime = get_runtime(ordner,ordner_run)
    #print(tsv_runtime)
    liste_for_save =  tsv_list_results + [tsv_runtime] +  tsv_list_ds
    #print(liste_for_save)
    return liste_for_save

def get_data_1_run_ds(ordner,ordner_run):
    df = pd.read_csv(str(ordner) + "/" + ordner_run + "/" + "DS_results.tsv"  ,header=0, sep="\t")
    anz_art_ges  = int(get_column_name_list(df)[1])
    all_other_val = get_all_colums(df)[1]
    art_verh_test_ges = all_other_val[2]
    anz_sent_ges = int(all_other_val[3])
    sent_verh_test_ges = all_other_val[6]
    anz_int_ges = int(all_other_val[7])
    int_verh_test_ges = all_other_val[10]
    verh_n_y_ges = all_other_val[11]
    null_eins_verh_test = all_other_val[12]
    null_eins_verh_train = all_other_val[13]
    null_eins_verh_test_train = all_other_val[14]
    output_list_tsv = [anz_art_ges, art_verh_test_ges,anz_sent_ges,sent_verh_test_ges,anz_int_ges,int_verh_test_ges,verh_n_y_ges,null_eins_verh_test,null_eins_verh_train,null_eins_verh_test_train]
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
    df = pd.read_csv(str(ordner) + "/" + ordner_run + "/" + "run_laufzeit.tsv"  ,header=0, sep="\t")
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




def write_data_1_run_in_results_tsv_title(ordner):
    with open(str(ordner) + "/" + 'results.tsv', 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['run', 'f1', 'recall', 'precision', 'specifity', "runtime", 'Gesamtanzahl Artikel',"Anteil Artikel in Test.tsv zu ges.","Gesamtanzahl Sätze"," Anteil Sätze in Test.tsv zu ges.","Gesamtanzahl Interactions","Anteil Interactions in Test.tsv zu ges.","Gesamtes 0/1 Verhältnis", "1/0 Verhältnis test.tsv", "1/0 Verhältnis train.tsv", "1/0 Verhältnis test/train.tsv"])
        out_file.close()

def write_data_1_run_in_results_tsv(ordner,print_list):
    with open(str(ordner) + "/" + 'results.tsv', 'a') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(print_list)

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

def round_list_neu(li):
    li_out = []
    for el in li:
        li_out.append(round(el,4))
    print(li_out)
    return li_out

def runtime_med_std(runtime_li):
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
    rest_std = []
    rest_mean = []
    for li in all_other[1:5]:
        #print(li)
        all_other_std.append(statistics.stdev(list_to_float(li)))
        all_other_med.append(statistics.mean(list_to_float(li)))
    for li_run in all_other[5]:
        all_run_times.append(runtime_med_std(li_run))

    for li in all_other[6:]:
        #print(li)
        #print(li)
        rest_std.append(statistics.stdev(li))
        rest_mean.append(statistics.mean(li))


    #print(all_run_times)
    med_runtime = statistics.mean(all_run_times)
    std_runtime = statistics.stdev(all_run_times)
    add_list = ["Standardabweichung:"] + round_list(all_other_std) + [round_runtime(std_runtime)] + round_list_neu(rest_std)
    add_list_2 = ["Mittelwert"] + round_list(all_other_med) + [round_runtime(med_runtime)] + round_list_neu(rest_mean)
    with open(str(ordner) + "/" + 'results.tsv', 'a') as out_file:
        print(add_list)
        print(add_list_2)
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(add_list_2)
        tsv_writer.writerow(add_list)


def main():
    ip = input("mit Mittelwert + Standardabweichungs-zeile?" + "\n" +  "==> enter y/n" + "\n" + "==> ")
    argv  =sys.argv[1:]
    opts, argv = getopt.getopt(argv, "f")
    if argv[0] in os.listdir():
        print(">>> auswertung beginnt")
        ordner = argv[0]
        write_data_1_run_in_results_tsv_title(ordner)
        #print(sorted(os.listdir(str(ordner) + "/")))
        for ordner_run in sorted(os.listdir(str(ordner) + "/")):
            if ordner_run == 'results.tsv' or ordner_run == '.~lock.results.tsv#':
                continue
            else:
                write_data_1_run_in_results_tsv(ordner,get_data_1_run_all(ordner,ordner_run))
                #get_data_1_run_all(ordner,ordner_run)
        print('>>> results.tsv erfolgreich erstellt')
    if ip == "y":
        add_std_in_results_and_med(ordner)

    else:
        print("!!!angegebener Ordner nicht existent ")



###############################################################################
#run


main()
