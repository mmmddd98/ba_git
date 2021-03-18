import csv
import pandas as pd
import random
import numpy as np
import sys
import getopt
from nltk.tokenize import sent_tokenize, word_tokenize
import os
import re
import statistics




def get_data_1_part(file_name,part,ordner):
    df = pd.read_csv(str(ordner) + "/" + str(file_name),header=0, sep="\t")
    anz_rel  = get_column_name_list(df)[1]
    all_other_val = get_all_colums(df)[1]
    anz_sent = all_other_val[0]
    all_sent = all_other_val[1]
    n_y_rel = all_other_val[2]
    output_list_tsv = [part] +  [anz_rel] +  all_other_val
    output_rdy = []
    for i in output_list_tsv:
        output_rdy.append(round(float(i),3))
    return output_rdy

def df_to_list(df,column):
    #print(df)
    #print(column)
    list_1 = list(df[column])
    #print(list_1)
    return list_1

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
    with open(str(ordner) + "/" + 'results_all_parts.tsv', 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['part', 'anzahl Artikel', 'gesamtanzahl Artikel', 'anteil an ges. Artikel', 'anzahl der Sätze','gesamtanzahl Sätze', 'anteil an ges. Sätze', 'anzahl Interactions', 'gesamtanzahl Interactions', 'anteil an ges. Interactions','null eins verhältnis'])
        out_file.close()

def write_data_1_run_in_results_tsv(ordner,print_list):
    with open(str(ordner) + "/" + 'results_all_parts.tsv', 'a') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(print_list)

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

def df_to_list(df,column):
    #print(df)
    #print(column)
    list_1 = list(df[column])
    #print(list_1)
    return list_1

def sort_mit_10(li):
    li_sor = sorted(li)
    if "part_10.tsv" in li_sor:
        li_sor.append("part_10.tsv")
        li_sor.remove("part_10.tsv")
        #print(li_sor)
    return li_sor

def round_list(li):
    li_out = []
    for el in li:
        li_out.append(round(el,3))
    return li_out

def add_std_in_results(ordner):
    df = pd.read_csv(str(ordner) + "/" + 'results_all_parts.tsv',header=0, sep="\t")
    column_name  = get_column_name_list(df)
    #print(column_name)
    all_other = get_all_colums(df)
    all_other_std = []
    for li in all_other:
        all_other_std.append(statistics.stdev(li))
    add_list = ["Standardabweichung:"] + round_list(all_other_std[1:])
    with open(str(ordner) + "/" + 'results_all_parts.tsv', 'a') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(add_list)



def main():
    argv  =sys.argv[1:]
    opts, argv = getopt.getopt(argv, "f")
    if argv[0] in os.listdir():
        print(">>> auswertung beginnt")
        ordner = argv[0]
        write_data_1_run_in_results_tsv_title(ordner)
        #print(sorted(os.listdir(str(ordner) + "/")))
        #print(os.listdir(ordner))
        #print(sorted(os.listdir(ordner)))

        results_files = []
        for el in os.listdir(ordner):
            if "results" in el and el != '.~lock.part_1_results.tsv#' and el != "results_all_parts.tsv":
                results_files.append(el)

        for res in sort_mit_10(results_files):
            part = extract_digits(res)
            #print(get_data_1_part(res,part,ordner))
            write_data_1_run_in_results_tsv(ordner,get_data_1_part(res,part,ordner))
        print(""">>> Erstellen von "results_all_parts.tsv" erfolgreich """)
        add_std_in_results(ordner)




        #print(get_data_1_part(file_name))

                #write_data_1_run_in_results_tsv(ordner,get_data_1_run_all(ordner,ordner_run))
                #get_data_1_run_all(ordner,ordner_run)
        #print('>>> results.tsv erfolgreich erstellt')
    else:
        print("!!!angegebener Ordner nicht existent ")


def sort_mit_10(li):
    li_sor = sorted(li)
    if "part_10_results.tsv" in li_sor:
        li_sor.append("part_10_results.tsv")
        li_sor.remove("part_10_results.tsv")
        #print(li_sor)
    return li_sor

def extract_digits(str):
    return int(re.findall(r'\d+',str)[0])


###############################################################################
#run


main()
