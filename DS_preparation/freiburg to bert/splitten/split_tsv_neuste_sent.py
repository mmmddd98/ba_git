'''This script is made to split the in a tsv-file converted CPI-DS in 2 parts.
   Just paste the name of inputfile in the main-function in the last line.
   When you run the scipt ypu can choose if you would like to have an extra column with indices (necessary for BioBert).
   In addition you have to enter the proportion of the number of sentences in testfile on the total  number of sentences
   and how many different of these DS-pairs (Test and Training-DS) you want to create.
   !!! Important: The splitting is sentence based ==> With your input (propotion of the testfile)
   you define the number of the sentences that will be in the two output files.
   Through evaluating of the created datasets through the "auswerten"-function the scipt makes sure that the proportion of positive pairs with an existing interaction("1") and negative pairs without       
   interaction ("0") is approximately the same in the test and train file.
   In addition "auswerten" checks that the proportion (number of interactions in test / total number of interactions)
   do not differ that much from the entered proportion of the testfile on the total DS-size (sentence-based!).
   If one of these requirements does not met, the script will create a new random split and values it again, until the requirements are met.
   The splitted datasets are outputted in a new folder with a "DS_results.tsv" file that saves the values of "auswerten" for the specific created datasets.'''

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
	print(len(liste_sortiert))
	return len(liste_sortiert)

def wv_saetze_list_return(sentence_id_list_full):
	liste_sortiert = collections.OrderedDict.fromkeys(sentence_id_list_full).keys()
	return liste_sortiert




def get_random_part(liste ,anteil: float):
	le = wv_saetze(liste)
	zahlen_anteil = round(le * anteil)
	random_zahlen_part = []
	while (len(random_zahlen_part) < zahlen_anteil):
		random_zahl = random.randint(0,le-1)
		if random_zahl not in random_zahlen_part:
			random_zahlen_part.append(random_zahl)
	return random_zahlen_part

def get_random_part_neu(liste ,anteil: float):
	le = wv_saetze(liste)
	zahlen_anteil = round(le * anteil)
	random_zahlen_part = random.sample(range(0,le-1), zahlen_anteil)
	#print(len(random_zahlen_part))
	return random_zahlen_part,le,len(random_zahlen_part)




def df_to_list(df,column):
	list_1 = df[column].to_list()
	return list_1

def split_all(random_zahlen_liste,df):
	column_name_list = get_column_name_list(df)
	gespaltet_liste =[]
	for column in column_name_list:
		column_gespaltet  = split_1_list(df_to_list(df,column),random_zahlen_liste,df)
		gespaltet_liste.append(column_gespaltet)
	return gespaltet_liste


def create_split_id_lists(random_zahlen_part,sentence_id_list_full):
	id_list_full_sortiert = wv_saetze_list_return(sentence_id_list_full)
	id_list_1 = []
	id_list_2 = []
	for id in enumerate(id_list_full_sortiert):
		if id[0] in random_zahlen_part:
			id_list_1.append(id[1])
		else:
			id_list_2.append(id[1])
	return id_list_1,id_list_2

def split_tuples(file_tupel_full,id_list_1,id_list_2):
	tuple_split_1 = []
	tuple_split_2 = []
	#print("len_ges:",len(file_tupel_full))
	for tupel in file_tupel_full:
		if tupel[2] in id_list_1 and tupel[2] not in id_list_2:
			tuple_split_1.append(tupel)
		elif tupel[2] in id_list_2 and tupel[2] not in id_list_1:
			tuple_split_2.append(tupel)
		else:
			print("!!!fehler bei split_tuples!!!")
	#print("len_1:",len(tuple_split_1),"len_2:",len(tuple_split_2))
	return tuple_split_1,tuple_split_2








def get_column_name_list(df):
	column_name_list = []
	for col in df.columns:
		column_name_list.append(col)
	return column_name_list

def get_lists_for_save(tupel_split):
	liste_satz_save = []
	liste_label_save = []
	for tupel in tupel_split:
		liste_satz_save.append(tupel[0])
		liste_label_save.append(tupel[1])
	return liste_satz_save, liste_label_save



def save_as_tsv(liste,file,part,ip_index_spalte):
	list_1_save  = liste[0]
	index_list = list(range(0,len(list_1_save)-1))
	#print(list_1_save)
	#print(len(list_1_save))
	#print("....")
	list_2_save = liste[1]
	#print(len(list_2_save))
	#print(list_2_save)
	if ip_index_spalte == "y":
		df_save = pd.DataFrame(list(zip(index_list, list_1_save, list_2_save)),columns =['index','sentence', 'label'])
	elif ip_index_spalte == "n":
		df_save = pd.DataFrame(list(zip(list_1_save, list_2_save)),columns =['sentence', 'label'])
	else:
		print("!!!fehler beim saven!!!")
	df_save.to_csv(str(file[:-4])+ "_" + str(part) + ".tsv",index=False, header=True, sep='\t')

def save_train_tsv(liste,file,part):
	list_1_save  = liste[0]
	#print(list_1_save)
	#print(len(list_1_save))
	#print("....")
	list_2_save = liste[1]
	#print(len(list_2_save))
	#print(list_2_save)
	df_save = pd.DataFrame(list(zip(list_1_save, list_2_save)),columns =['sentence', 'label'])
	df_save.to_csv(str(file[:-4])+ "_" + str(part) + ".tsv",index=False, header=False, sep='\t')

def auswerten(file,anteil,satz_tup):
	auswerten  = False
	test_satz_anz  = satz_tup[0]
	train_satz_anz  = satz_tup[1]
	satz_anz_ges = satz_tup[2]
	try:
		df_auswerten_1 = pd.read_csv(str(file[:-4]) +"_test" + ".tsv", sep="\t")
		anzahl_rel_1 = len(df_auswerten_1)
		df_auswerten_2 = pd.read_csv(str(file[:-4]) +"_train" + ".tsv" , sep="\t")
		anzahl_rel_2 = len(df_auswerten_2)
		anzahl_ges = anzahl_rel_1 + anzahl_rel_2
		print("anzahl_rel_1:",anzahl_rel_1)
		print("anzahl_rel_2:",anzahl_rel_2)
		print("anzahl_ges:",anzahl_ges)
		rel_verhaeltnis = anzahl_rel_1/anzahl_ges
		print("rel_verhaeltnis:",rel_verhaeltnis)
		null_eins_verhaeltnis_1 = read_file_auswerten_test(file,df_auswerten_1)
		null_eins_verhaeltnis_2 = read_file_auswerten_train(file,df_auswerten_2)
		null_eins_verhaeltnis_1_2  = null_eins_verhaeltnis_1/null_eins_verhaeltnis_2
		print(null_eins_verhaeltnis_1_2)
		if anteil * 0.99 < rel_verhaeltnis < anteil * 1.01 and 0.99 < null_eins_verhaeltnis_1_2 < 1.01:
			auswerten = True
			file_res = open("DS_results.tsv", "w")
			file_res.write("anzahl rel in test.tsv:" + "\t" + str(anzahl_rel_1) + "\n")
			file_res.write(" davon anzahl der Sätze:" + "\t" + str(test_satz_anz) + "\n")
			file_res.write("anzahl rel in train.tsv:" + "\t" + str(anzahl_rel_2) + "\n")
			file_res.write(" davon anzahl der Sätze:" + "\t" + str(train_satz_anz) + "\n")
			file_res.write("gesamtanzahl in train und test.tsv:" + "\t" + str(anzahl_ges) + "\n")
			file_res.write(" gesamtzahl der Sätze:" + "\t" + str(satz_anz_ges) + "\n")
			file_res.write("null eins verhältnis test.tsv :" + "\t" + str(null_eins_verhaeltnis_1) + "\n")
			file_res.write("null eins verhältnis train.tsv :" + "\t" + str(null_eins_verhaeltnis_2) + "\n")
			file_res.write("null eins verhältnis test/train :" + "\t" + str(null_eins_verhaeltnis_1_2) + "\n")
			#abstarct zahlenm noch einfügen
			file_res.close()
		return auswerten
	except FileNotFoundError:
		return auswerten








def read_file_auswerten_train(file,df):
	name_list = get_column_name_list(df)
	#print(name_list)
	#print(len(name_list))
	sentence_id_list_full = df[name_list[1]].tolist()
	#print(sentence_id_list_full)
	occurrences_1 = sentence_id_list_full.count(1)
	occurrences_0 = sentence_id_list_full.count(0)
	return occurrences_0/occurrences_1

def read_file_auswerten_test(file,df):
	name_list = get_column_name_list(df)
	#print(name_list)
	sentence_id_list_full = df["label"].tolist()
	#print(sentence_id_list_full)
	occurrences_1 = sentence_id_list_full.count(1)
	occurrences_0 = sentence_id_list_full.count(0)
	return occurrences_0/occurrences_1




def del_old_file(file):
	if os.path.isfile(str(file[:-4]) +"_test" + ".tsv"):
		os.remove(str(file[:-4]) +"_test" + ".tsv")
		print(">>>" + str(file[:-4]) +"_test" + ".tsv" + " deleted"  )
	if os.path.isfile(str(file[:-4]) +"_train" + ".tsv"):
		os.remove(str(file[:-4]) +"_train" + ".tsv")
		print(">>>" + str(file[:-4]) +"_train" + ".tsv" + " deleted"  )

def create_folder_and_move_file(file1,file2,info_ds,counter,folder):
	os.mkdir(folder + "DS-" + str(counter))
	shutil.move(file1,folder + "DS-" + str(counter))
	shutil.move(file2,folder + "DS-" + str(counter))
	shutil.move(info_ds,folder + "DS-" + str(counter))
	#os.rename(file, "/" + "DS-" + str(counter) + "/" + file)










#schreibe in file groß
#############################################
#main

def main_alt(file, anteil: float):
	for i in tqdm(range(100)):
		df = pd.read_csv(file, sep="\t")
		random_zahlen_part = get_random_part_neu(len(df), anteil)
		liste_gespaltet = split_all(random_zahlen_part,df)
		storage = get_lists_for_s
		save(liste_gespaltet)
		liste_doc_1 = storage[0] #includes n lists for n columns ==> n. part
		#print(liste_doc_1)
		liste_doc_2 = storage[1] #includes n lists for n columns ==> n+1. part
		save_as_tsv(liste_doc_1,file,"test")
		save_train_tsv(liste_doc_2,file,"train")
	print(">>> " + str(file[:-4]) +"_test" + ".tsv" +" and " + str(file[:-4]) +"_train" + ".tsv" + " created succesfully" )


def main(file,anteil,ip_index_spalte):
	#ip_index_spalte = input("mit index-spalte?" + "\n" +  "==> enter y/n" + "\n" + "==> ")
	file_lists = read_file(file)
	sentence_list_full = file_lists[0]
	label_list_full = file_lists[1]
	sentence_id_list_full = file_lists[2]
	file_tupel_full = lists_to_tuple_list(file_lists)
	del_old_file(file)
	test_satz_anz  = 1 #def to start while
	satz_anz_ges = 1 #def to start while
	train_satz_anz = 1 #def to start while
	satz_tup = (test_satz_anz,train_satz_anz,satz_anz_ges)
	while auswerten(file,anteil,satz_tup) == False:
		random_zahlen_part_tup = get_random_part_neu(sentence_id_list_full, anteil)
		random_zahlen_part  = random_zahlen_part_tup[0]
		satz_anz_ges  = random_zahlen_part_tup[1]
		test_satz_anz  = random_zahlen_part_tup[2]
		train_satz_anz = satz_anz_ges - test_satz_anz
		satz_tup = (test_satz_anz,train_satz_anz,satz_anz_ges)
		id_list_split = create_split_id_lists(random_zahlen_part,sentence_id_list_full)
		id_list_1 = id_list_split[0]
		id_list_2 = id_list_split[1]
		tuple_split = split_tuples(file_tupel_full,id_list_1,id_list_2)
		tuple_split_1 = tuple_split[0]
		tuple_split_2 = tuple_split[1]
		list_split_save_1 = get_lists_for_save(tuple_split_1)
		list_split_save_2 = get_lists_for_save(tuple_split_2)
		save_as_tsv(list_split_save_1,file,"test",ip_index_spalte)
		save_train_tsv(list_split_save_2,file,"train")
	#file_res = open("DS_results.tsv", "w")
	#file_res.write("XXXXXX" + "\t" + "XXXXXXXXXXXX" + "\n")
	print(">>> " + str(file[:-4]) +"_test" + ".tsv" +" and " + str(file[:-4]) +"_train" + ".tsv" + " created succesfully")


def main_ohne_while(file,anteil):
	ip_index_spalte = input("mit index-spalte?" + "\n" +  "==> enter y/n" + "\n" + "==> ")
	file_lists = read_file(file)
	sentence_list_full = file_lists[0]
	label_list_full = file_lists[1]
	sentence_id_list_full = file_lists[2]
	file_tupel_full = lists_to_tuple_list(file_lists)
	random_zahlen_part = get_random_part_neu(sentence_id_list_full, anteil)
	id_list_split = create_split_id_lists(random_zahlen_part,sentence_id_list_full)
	id_list_1 = id_list_split[0]
	id_list_2 = id_list_split[1]
	tuple_split = split_tuples(file_tupel_full,id_list_1,id_list_2)
	tuple_split_1 = tuple_split[0]
	tuple_split_2 = tuple_split[1]
	list_split_save_1 = get_lists_for_save(tuple_split_1)
	list_split_save_2 = get_lists_for_save(tuple_split_2)
	save_as_tsv(list_split_save_1,file,"test",ip_index_spalte)
	save_train_tsv(list_split_save_2,file,"train")
	print(">>> " + str(file[:-4]) +"_test" + ".tsv" +" and " + str(file[:-4]) +"_train" + ".tsv" + " created succesfully")

def ueber_main(file):
	ip_index_spalte = input("with index-column?" + "\n" +  "==> enter y/n" + "\n" + "==> ")
	anteil = float(input("How big is the proportion of the test file ?" + "\n" +  "==> "))
	wieviele = input("How many DS?" + "\n" +  "==> ")
	os.mkdir("Split_" + str(wieviele)+"_" +  str(anteil))
	for run in range(1,int(wieviele)+1):
		main(file,anteil,ip_index_spalte)
		create_folder_and_move_file(str(file[:-4]) +"_test" + ".tsv",str(file[:-4]) +"_train" + ".tsv","DS_results.tsv",run,"Split_" + str(wieviele) +"_" +  str(anteil) + "/")













#############################################
#run

##main_alt("CPI-DS_original.tsv", 0.3)
#main("CPI-DS._full_cut.tsv", 0.5)
#main_ohne_while("CPI-DS._full_cut.tsv", 0.5)
#verschiebe_file('test.txt',2)
ueber_main("CPI-DS._full_cut_rdy.tsv")
