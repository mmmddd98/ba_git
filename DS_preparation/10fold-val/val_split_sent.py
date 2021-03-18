import pandas as pd
import random
import numpy as np
from tqdm import tqdm
from time import sleep
import collections
import itertools
import sys
from datetime import datetime
import shutil
import os
import statistics


def read_file(file):
	df = pd.read_csv(str(file), sep="\t")
	column_name_list = get_column_name_list(df)
	#print(column_name_list)
	sentence_list_full = []
	label_list_full = []
	sentence_id_list_full = []
	for ind in df.index:
		sentence = df[column_name_list[0]][ind]
		sentence_list_full.append(sentence)
		label = df[column_name_list[1]][ind]
		label_list_full.append(label)
		sentence_id = df[column_name_list[2]][ind]
		sentence_id_list_full.append(sentence_id)
	dif_sent = wv_saetze(sentence_id_list_full)
	return sentence_list_full,label_list_full,sentence_id_list_full


def lists_to_tuple_list(li):
	file_tupel_full = []
	if len(li[0]) == len(li[1]) and len(li[0]) == len(li[2]):
		for (satz, label, satz_id) in zip(li[0], li[1], li[2]):
			file_tupel_full.append((satz, label, satz_id))
		return file_tupel_full
	else:
		print("!!!fehler bei der länge der listen!!!")



def wv_saetze(sentence_id_list_full):
	liste_sortiert = collections.OrderedDict.fromkeys(sentence_id_list_full).keys()
	#print(len(liste_sortiert))
	return len(liste_sortiert)

def wv_saetze_list_return(sentence_id_list_full):
	#print(len(sentence_id_list_full))
	liste_sortiert = collections.OrderedDict.fromkeys(sentence_id_list_full).keys()
	return list(liste_sortiert)

def get_column_name_list(df):
	column_name_list = []
	for col in df.columns:
		column_name_list.append(col)
	return column_name_list

def get_random_part_neu(liste ,parts_number):
	le = wv_saetze(liste)
	#print(le)
	num_1_part = int(le / parts_number)
	#print(num_1_part)
	rest = le % parts_number
	#print(rest)
	parts_liste_same = parts_number  * [num_1_part]
	#print(parts_liste_same)
	for el in range(0,rest):
		parts_liste_same[el] = parts_liste_same[el]  + 1
	#print(parts_liste_same)
	parts_liste_same_cop = parts_liste_same
	list_le = list(range(1,le+1))
	#print(list_le)
    #if sum(parts_liste_same)  == le:
        #for list in parts_liste_same_cop:



	#else:
		#print(">>> fehler bei dem erstellen der random zahlen liste")

def get_random_part_neu_neu(liste ,parts_number):
    le = wv_saetze(liste)
    #print(le)
    num_1_part = int(le / parts_number)
    list_le = list(range(1,le+1))
    #print(list_le)
    random.shuffle(list_le)
    #print(list_le)
    list_splitted = [list_le[i * num_1_part:(i + 1) * num_1_part] for i in range((len(list_le) + num_1_part - 1) // num_1_part )]
    #print(list_splitted)
    #print(len(list_splitted))
    #print(len(list_splitted[0]))
    #print(len(list_splitted[1]))
    if len(list_splitted) == parts_number:
        return list_splitted
    elif len(list_splitted) == parts_number + 1:
        for el in  range(0,len(list_splitted[-1])):
            list_splitted[el].append(list_splitted[-1][el])
        return list_splitted[:-1]

    #print(len(list_splitted[0]))
    #print(len(list_splitted[1]))
    #print(list_splitted[0][-1])
    #print(list_splitted[1][-1])


def create_split_id_lists(random_zahlen_part,sentence_id_list_full):
	id_list_full_sortiert = wv_saetze_list_return(sentence_id_list_full)
	#print(id_list_full_sortiert)
	#print(random_zahlen_part)
	list_of_id_lists = []
	for random_li in random_zahlen_part:
		eine_id_list = []
		for random_zahl in random_li:
			eine_id_list.append(id_list_full_sortiert[random_zahl-1])
			#print(random_zahl)
		list_of_id_lists.append(eine_id_list)
	return list_of_id_lists

def split_tuples(file_tupel_full,list_of_id_lists):
	tupel_list_full  = []
	for id_list_1 in list_of_id_lists:
		tupel_list_1  = []
		for id in id_list_1:
			for tupel in file_tupel_full:
				if tupel[2] == id:
					tupel_list_1.append(tupel)
		tupel_list_full.append(tupel_list_1)
	#print(len(tupel_list_full))
	return tupel_list_full

def check(tuple_split):
	eins  = tuple_split[0]
	rest = tuple_split[1] + tuple_split[2] +tuple_split[3] + tuple_split[4] +tuple_split[5] + tuple_split[6] +tuple_split[7] + tuple_split[8] +tuple_split[9]
	for el in eins:
		if el in rest:
			print("nene")


def get_interctions_stdabw(tuple_split):
	len_list = []
	for li in tuple_split:
		len_list.append(len(li))
	return statistics.stdev(len_list)


def get_int_n_y_stdabw(tuple_split):
	n_y_verh = []
	for li in tuple_split:
		y_count = 0
		n_count = 0
		for tup in li:
			if tup[1] == 1:
				y_count = y_count + 1
			elif tup[1] == 0:
				n_count = n_count + 1
		n_y_verh.append(n_count/y_count)
	return statistics.stdev(n_y_verh)




def auswerten(tuple_split,int_std_grenze,n_y_std_grenze):
	auswerten  = False
	interctions_stdabw = get_interctions_stdabw(tuple_split)
	print("interaction standardabweichung:",round(interctions_stdabw,2),".....gefordert: ",int_std_grenze)
	int_n_y_stdabw  = get_int_n_y_stdabw(tuple_split)
	print("1/0 standardabweichung:" + "         ",round(int_n_y_stdabw,2),".....gefordert: ",n_y_std_grenze)
	if interctions_stdabw < int_std_grenze and int_n_y_stdabw < n_y_std_grenze:
		auswerten = True
	return auswerten

def ds_results_save(anzahl_rel,satz_anz,satz_anz_ges,null_eins_verhaeltnis,counter,parts_number):
	file_res = open(str(parts_number) + "_cross_fold_val/""part_" + str(counter) +  "_results.tsv", "w")
	file_res.write("anzahl rel:" + "\t" + str(anzahl_rel) + "\n")
	file_res.write("anzahl der Sätze:" + "\t" + str(satz_anz) + "\n")
	file_res.write("gesamtzahl der Sätze:" + "\t" + str(satz_anz_ges) + "\n")
	file_res.write("null eins verhältnis:" + "\t" + str(null_eins_verhaeltnis) + "\n")
	file_res.close()

def save_all(tupel_split,file,parts_number,ip_index_spalte,list_of_id_lists):
	if len(tupel_split) == parts_number:
		for counter,li in enumerate(tupel_split,1): ######enumeraste als infut füt save as tsv
			save_lists = get_lists_for_save(li)
			liste_satz_save = save_lists[0]
			liste_label_save = save_lists[1]
			save_as_tsv(liste_satz_save,liste_label_save,file,parts_number,ip_index_spalte,counter)
			anzahl_rel = len(liste_satz_save)
			satz_anz = len(list_of_id_lists[counter-1])
			satz_anz_ges = 0
			for li in list_of_id_lists:
				satz_anz_ges = satz_anz_ges + len(li)
			null_eins_verhaeltnis = (liste_label_save.count("0") + liste_label_save.count(0))/(liste_label_save.count("1") + liste_label_save.count(1))
			ds_results_save(anzahl_rel,satz_anz,satz_anz_ges,null_eins_verhaeltnis,counter,parts_number)
	else:
		print("Anzahl der parts passen nicht ")



def get_lists_for_save(tupel_split):
	liste_satz_save = []
	liste_label_save = []
	for tupel in tupel_split:
		liste_satz_save.append(tupel[0])
		liste_label_save.append(tupel[1])
	return liste_satz_save, liste_label_save



def save_as_tsv(satz_list,label_list,file,parts_number,ip_index_spalte,counter):
	index_list = list(range(0,len(satz_list)-1))
	if ip_index_spalte == "y":
		df_save = pd.DataFrame(list(zip(index_list, satz_list, label_list)),columns =['index','sentence', 'label'])
	elif ip_index_spalte == "n":
		df_save = pd.DataFrame(list(zip(satz_list, label_list)),columns =['sentence', 'label'])
	else:
		print("!!!fehler beim saven!!!")
	df_save.to_csv(str(parts_number) + "_cross_fold_val/"+ "part"+ "_" + str(counter) + ".tsv",index=False, header=True, sep='\t')
	print(">>> Splitten in die" + str(parts_number) + "Parts erfolgreich")




################################################################################


def main(file):
	ip_index_spalte = input("mit index-spalte?" + "\n" +  "==> enter y/n" + "\n" + "==> ")
	parts_number = 10
	os.mkdir(str(parts_number) + "_cross_fold_val")
	#parts_number = input("wieviele parts?" + "\n" + "==> ")
	file_lists = read_file(file)
	sentence_list_full = file_lists[0]
	label_list_full = file_lists[1]
	sentence_id_list_full = file_lists[2]
	file_tupel_full = lists_to_tuple_list(file_lists)
	#print(len(file_tupel_full))
	print("1.Versuch")
	random_zahlen_part = get_random_part_neu_neu(sentence_id_list_full, parts_number)
	list_of_id_lists = create_split_id_lists(random_zahlen_part,sentence_id_list_full)
	tuple_split = split_tuples(file_tupel_full,list_of_id_lists)
	c = 2
	while auswerten(tuple_split,12,0.09) == False:
		print(str(c) + ".Versuch")
		random_zahlen_part = get_random_part_neu_neu(sentence_id_list_full, parts_number)
		list_of_id_lists = create_split_id_lists(random_zahlen_part,sentence_id_list_full)
		tuple_split = split_tuples(file_tupel_full,list_of_id_lists)
		c = c + 1
	save_all(tuple_split,file,parts_number,ip_index_spalte,list_of_id_lists)






	#tuple_split_1 = tuple_split[0]
	#tuple_split_2 = tuple_split[1]
	#list_split_save_1 = get_lists_for_save(tuple_split_1)
	#list_split_save_2 = get_lists_for_save(tuple_split_2)
	#save_as_tsv(list_split_save_1,file,"test",ip_index_spalte)
	#save_train_tsv(list_split_save_2,file,"train")
	#print(">>> " + str(file[:-4]) +"_test" + ".tsv" +" and " + str(file[:-4]) +"_train" + ".tsv" + " created succesfully")










############################################################################

main("CPI-DS._full_cut_rdy.tsv")
