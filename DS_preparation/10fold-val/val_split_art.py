'''
   This script splits the in a tsv-file converted CPI-DS in 10 parts for 10-cross fold validation.
   Just paste the name of inputfile in the main-function in the last line.
   When you run the scipt you can choose if you would like to have an extra column with indices (necessary for BioBert).
   In addition you have to enter the number of 10 cross fold validations-datasets you want to create.
   and how many different of these DS-pairs (Test and Training-DS) you want to create.
   !!! Important: The splitting is article based ==> So in the end there will be a tenth of the total article number in every of the 10 cv-datasets.
   But because the number of sentences and also the number of pairs in every article is various the script needs to avoid
   that all the article with many pairs are in the same of the 10 ds.
   Therefore the function "auswerten" evaluates standard deviation of the number of pairs included in every of the 10 ds.
   In addition "auswerten" determines the standard deviation of the proportion of the number of positive and negative pairs in every of the 10 ds.
   Also "auswerten" determines the standard deviation of number of sentences included in every of the 10 ds.
   If only one of these 3 standard deviation falls below the limit, set in the "auswerten"-funtion, the script will create a new random split and values it again, until the limits are met.
   The 10 splitted datasets are outputted in a one new folder, together with a "results.tsv" file for every of the 10 parts that saves the values of "auswerten".
   To get the ready datasets for BioBert use, have a look at the "val_ds_create_art.py" script.
 '''

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
	dif_sent = wv_art(sentence_id_list_full)
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

def wv_art_list_return(art_id_list_full):
	#print(len(sentence_id_list_full))
	liste_sortiert = collections.OrderedDict.fromkeys(art_id_list_full).keys()
	return list(liste_sortiert)

def wv_art(art_id_list_full):
	liste_sortiert = collections.OrderedDict.fromkeys(art_id_list_full).keys()
	#print(len(liste_sortiert))
	return len(liste_sortiert)


def get_column_name_list(df):
	column_name_list = []
	for col in df.columns:
		column_name_list.append(col)
	return column_name_list

def get_random_part_neu(liste ,parts_number):
	le = wv_art(liste)
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
    le = len(liste)
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
	id_list_full_sortiert = wv_art_list_return(sentence_id_list_full)
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

def split_tuples(file_tupel_full,list_of_art_id_lists):
	tupel_list_full  = []
	for id_art_list_1 in list_of_art_id_lists:
		tupel_list_1  = []
		for art_id in id_art_list_1:
			for tupel in file_tupel_full:
				#print(tupel)
				#print(tupel[2][:tupel[2].index("-")])
				if tupel[2][:tupel[2].index("-")] == art_id:
					#print(tupel[2][:tupel[2].index("-")],art_id)
					tupel_list_1.append(tupel)
		tupel_list_full.append(tupel_list_1)
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

def get_sent_stdabw(tuple_split):
	anz_sent = []
	for li in tuple_split:
		all_sent_eine_li = []
		for tupel in li:
			 all_sent_eine_li.append(tupel[2])
		all_sent_eine_li_sorted = collections.OrderedDict.fromkeys(all_sent_eine_li).keys()
		anz_sent.append(len(all_sent_eine_li_sorted))
		#print(len(all_sent_eine_li_sorted))
	return statistics.stdev(anz_sent)




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




def auswerten(tuple_split,int_std_grenze,n_y_std_grenze,sent_stdabw_grenze):
	auswerten  = False
	interctions_stdabw = get_interctions_stdabw(tuple_split)
	print("interaction standardabweichung:\t",round(interctions_stdabw,2),"\tgefordert: ",int_std_grenze)
	int_n_y_stdabw  = get_int_n_y_stdabw(tuple_split)
	print("1/0 standardabweichung:     \t",round(int_n_y_stdabw,2),"\tgefordert: ",n_y_std_grenze)
	sent_stdabw  = get_sent_stdabw(tuple_split)
	print("sentence standardabweichung:\t",round(sent_stdabw,2),"\tgefordert: ",sent_stdabw_grenze)
	if interctions_stdabw < int_std_grenze and int_n_y_stdabw < n_y_std_grenze and sent_stdabw < sent_stdabw_grenze :
		auswerten = True
	return auswerten

def ds_results_save(anzahl_int,anzahl_satz,anzahl_art,null_eins_verhaeltnis,counter,parts_number,anzahl_int_ges,anzahl_satz_ges,anzahl_art_ges,run):
	file_res = open(str(parts_number) + "_cross_fold_val" + str(run) + "/part_" + str(counter) +  "_results.tsv", "w")
	file_res.write("anzahl Artikel:" + "\t" + str(anzahl_art) + "\n")
	file_res.write("gesamtanzahl Artikel:" + "\t" + str(anzahl_art_ges) + "\n")
	file_res.write("anteil an ges. Artikel:" + "\t" + '{0:1.3f}'.format(round(anzahl_art/anzahl_art_ges,3)) + "\n")
	file_res.write("anzahl der Sätze:" + "\t" + str(anzahl_satz) + "\n")
	file_res.write("gesamtanzahl Sätze:" + "\t" + str(anzahl_satz_ges) + "\n")
	file_res.write("anteil an ges. Sätze:" + "\t" + '{0:1.3f}'.format(round(anzahl_satz/anzahl_satz_ges,3)) + "\n")
	file_res.write("anzahl Interactions:" + "\t" + str(anzahl_int) + "\n")
	file_res.write("gesamtanzahl Interactions:" + "\t" + str(anzahl_int_ges) + "\n")
	file_res.write("anteil an ges. Interactions:" + "\t" + '{0:1.3f}'.format(round(anzahl_int/anzahl_int_ges,3)) + "\n")
	file_res.write("null eins verhältnis:" + "\t" + '{0:1.3f}'.format(round(null_eins_verhaeltnis,3)) + "\n")
	file_res.close()

def save_all(tupel_split,file,parts_number,ip_index_spalte,list_of_art_lists,anzahl_int_ges,anzahl_satz_ges,anzahl_art_ges,run):
	if len(tupel_split) == parts_number:
		for counter,li in enumerate(tupel_split,1): ######enumeraste als infut füt save as tsv
			#print(li)
			save_lists = get_lists_for_save(li)
			liste_satz_save = save_lists[0]
			liste_label_save = save_lists[1]
			save_as_tsv(liste_satz_save,liste_label_save,file,parts_number,ip_index_spalte,counter)
			anzahl_int = len(liste_satz_save)
			anzahl_art = len(list_of_art_lists[counter-1])
			li_sent_id = []
			for tupel in li:
				li_sent_id.append(tupel[2])
			li_sent_sorted = collections.OrderedDict.fromkeys(li_sent_id).keys()
			anzahl_satz = len(li_sent_sorted)
			null_eins_verhaeltnis = (liste_label_save.count("0") + liste_label_save.count(0))/(liste_label_save.count("1") + liste_label_save.count(1))
			ds_results_save(anzahl_int,anzahl_satz,anzahl_art,null_eins_verhaeltnis,counter,parts_number,anzahl_int_ges,anzahl_satz_ges,anzahl_art_ges,run)

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
	df_save.to_csv(str(parts_number) + "_cross_fold_val" + str(run) +  "/part" + "_" + str(counter) + ".tsv",index=False, header=True, sep='\t')


def convert_sen_to_art(sentence_id_list_full):
	art_li  = []
	for sen in sentence_id_list_full:
		art_li.append(sen[:sen.index("-")])
	#print("len sentence_id_list_full:", len(sentence_id_list_full))
	#print("len art_li:", len(art_li))
	return art_li




################################################################################


def main(file,ip_index_spalte,run):
	parts_number = 10
	os.mkdir(str(parts_number) + "_cross_fold_val" + str(run))
	#parts_number = input("wieviele parts?" + "\n" + "==> ")
	file_lists = read_file(file)
	sentence_list_full = file_lists[0]
	label_list_full = file_lists[1]
	sentence_id_list_full = file_lists[2]
	sentence_id_list_full_sorted = collections.OrderedDict.fromkeys(sentence_id_list_full).keys()
	anzahl_satz_ges = len(sentence_id_list_full_sorted)
	print("anzahl der sätze:",anzahl_satz_ges)

	art_id_list_full = convert_sen_to_art(sentence_id_list_full)
	art_id_list_full_sorted = collections.OrderedDict.fromkeys(art_id_list_full).keys()
	anzahl_art_ges = len(art_id_list_full_sorted)
	print("anzahl der art:",anzahl_art_ges)
	file_tupel_full = lists_to_tuple_list(file_lists)
	anzahl_int_ges = len(file_tupel_full)
	print("anzahl der interactions:",anzahl_int_ges)
	#print(len(file_tupel_full))
	print("1.Versuch")
	random_zahlen_part = get_random_part_neu_neu(art_id_list_full_sorted, parts_number)
	#print(random_zahlen_part)
	list_of_art_lists = create_split_id_lists(random_zahlen_part,art_id_list_full_sorted)
	tuple_split = split_tuples(file_tupel_full,list_of_art_lists)
	#print(tuple_split)
	c = 2
	while auswerten(tuple_split,33,0.2,19) == False: #used 22,0.12,10
		print(str(c) + ".Versuch")
		random_zahlen_part = get_random_part_neu_neu(art_id_list_full_sorted, parts_number)
		list_of_art_lists = create_split_id_lists(random_zahlen_part,art_id_list_full_sorted)
		tuple_split = split_tuples(file_tupel_full,list_of_art_lists)
		c = c + 1
	save_all(tuple_split,file,parts_number,ip_index_spalte,list_of_art_lists,anzahl_int_ges,anzahl_satz_ges,anzahl_art_ges,run)
	print(">>> Splitten in die " + str(parts_number) + " Parts erfolgreich")






	#tuple_split_1 = tuple_split[0]
	#tuple_split_2 = tuple_split[1]
	#list_split_save_1 = get_lists_for_save(tuple_split_1)
	#list_split_save_2 = get_lists_for_save(tuple_split_2)
	#save_as_tsv(list_split_save_1,file,"test",ip_index_spalte)
	#save_train_tsv(list_split_save_2,file,"train")
	#print(">>> " + str(file[:-4]) +"_test" + ".tsv" +" and " + str(file[:-4]) +"_train" + ".tsv" + " created succesfully")


#!!!!!!!!!!!!!1noch gucken dass bei save all die anz der sätze und der ints und gesammt ankommt!!!!!!!!!!!!!!!!!!!!#
#besser: aus tuple_split in auswerten noch holen !!!!!!!!!!!!!!!!!!!!!!!!!!!!#







############################################################################
ip_index_spalte = input("with index-column?" + "\n" +  "==> enter y/n" + "\n" + "==> ")
wv_runs  = int(input("How many 10-cross_fold datasets you want to have?" + "\n" +  "==> enter a number" + "\n" + "==> "))
for run in list(range(1,wv_runs + 1)):
	main("CPI-DS._full_cut_rdy.tsv",ip_index_spalte,run)
