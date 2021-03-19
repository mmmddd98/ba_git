'''This script is made to split the in a tsv-file converted CPI-DS in 2 parts.
   Just paste the name of inputfile in the main-function in the last line.
   When you run the scipt ypu can choose if you would like to have an extra column with indices (necessary for BioBert).
   In addition you have to enter the proportion of the number of articles in testfile on the total  number of articles
   and how many different of these DS-pairs (Test and Training-DS) you want to create.
   !!! Important: The splitting is article based ==> With your input (propotion of the testfile)
   you define the number of the articles that will be in the to output files.
   So all pairs contained in one article will be after the splitting together either in the testfile or the training file.
   But every article contains a various number of sentences and therefore a various number of pairs.
   To avoid getting randomly all the article with many pairs in the same outputfile there is the function "auswerten" that values the result of the splitting.
   The input of "auswerten" describes how much (the proportion (number of senteces in test / total number of sentences)is
   allowed to differ from the entered proportion of the testfile on the total DS-size (abstracts-based!).
   Besides "auswerten" checks that the proportion (number of interactions in test / total number of interactions)
   do not differ that much from the entered proportion of the testfile on the total DS-size (abstracts-based!).
   In addition "auswerten" checks that the proportion of positive pairs with an existing interaction("1") and negative pairs without interaction ("0")
   is approximately the same in the test and train file.
   If only one of these 3 requirements does not met, the script will create a new random split and values it again, until the requirements are met.
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

def get_random_part_neu(le ,anteil: float):
	zahlen_anteil = round(le * anteil)
	random_zahlen_part = random.sample(range(0,le-1), zahlen_anteil)
	#print(len(random_zahlen_part))
	return random_zahlen_part



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


def create_split_id_lists(random_zahlen_part,art_id_list_full_sorted):
	art_id_list_1 = []
	art_id_list_2 = []
	for id in enumerate(art_id_list_full_sorted):
		if id[0] in random_zahlen_part:
			art_id_list_1.append(id[1])
		else:
			art_id_list_2.append(id[1])
	#print(len(art_id_list_1),len(art_id_list_2))
	return art_id_list_1,art_id_list_2

def split_tuples(file_tupel_full,id_list_1,id_list_2):
	tuple_split_1 = []
	tuple_split_2 = []
	#print("len_ges:",len(file_tupel_full))
	for tupel in file_tupel_full:
		if tupel[2][:tupel[2].index("-")] in id_list_1 and tupel[2][:tupel[2].index("-")] not in id_list_2:
			tuple_split_1.append(tupel)
		elif tupel[2][:tupel[2].index("-")] in id_list_2 and tupel[2][:tupel[2].index("-")] not in id_list_1:
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

def get_ver_int(tuple_split):
	anz_int_1 = len(tuple_split[0])
	anz_int_2 = len(tuple_split[1])
	return anz_int_1, anz_int_2

def get_ver_art(tuple_split):
	id_1 = []
	for i in tuple_split[0]:
		id_1.append(i[2])
	id_2 = []
	for e in tuple_split[1]:
		id_2.append(e[2])
	id_1_sorted = collections.OrderedDict.fromkeys(convert_sen_to_art(id_1)).keys()
	id_2_sorted = collections.OrderedDict.fromkeys(convert_sen_to_art(id_2)).keys()
	anz_ver_1 = len(id_1_sorted)
	anz_ver_2 = len(id_2_sorted)
	#print(anz_ver_1)
	#print(anz_ver_2)
	#print(anz_ver_1 + anz_ver_2)
	return anz_ver_1,anz_ver_2

def get_ver_sen(tuple_split):
	id_1 = []
	for i in tuple_split[0]:
		id_1.append(i[2])
	id_2 = []
	for e in tuple_split[1]:
		id_2.append(e[2])
	id_1_sorted = collections.OrderedDict.fromkeys(id_1).keys()
	id_2_sorted = collections.OrderedDict.fromkeys(id_2).keys()
	anz_ver_1 = len(convert_sen_to_art(id_1_sorted))
	anz_ver_2 = len(convert_sen_to_art(id_2_sorted))
	return anz_ver_1,anz_ver_2

def get_ver_n_y(tuple_split):
	n_y_1 = []
	for i in tuple_split[0]:
		n_y_1.append(i[1])
	#print(n_y_1)
	n_y_2 = []
	for e in tuple_split[1]:
		n_y_2.append(e[1])
	return n_y_1.count(0),n_y_1.count(1),n_y_2.count(0),n_y_2.count(1)

def auswerten(anteil,tuple_split,sen_grenze,int_grenze,n_y_grenze):
	auswerten  = False
	sen = get_ver_sen(tuple_split)
	ver_sen = sen[0]/(sen[1] + sen[0])
	sen_g_1 = anteil*(1 - sen_grenze)
	sen_g_2 = anteil*(1 + sen_grenze)
	n_y = get_ver_n_y(tuple_split)
	#print(n_y)
	n_y_1 = n_y[0]/n_y[1]
	n_y_2 = n_y[2]/n_y[3]
	n_y_g_1 = (1 - n_y_grenze)
	n_y_g_2 =(1 + n_y_grenze)
	ver_n_y = n_y_1 / n_y_2
	art = get_ver_art(tuple_split)
	ver_art = art[0]/(art[1] + art[0])
	int = get_ver_int(tuple_split)
	ver_int = int[0]/(int[1]+int[0])
	int_g_1 = anteil*(1 - int_grenze)
	int_g_2 = anteil*(1 + int_grenze)
	print("Verhältnis Artikel:      " + "\t",round(ver_art,4))
	print("Verhältnis Sätze:        " + "\t", round(ver_sen,4),"\tgefordert:",round(sen_g_1,4), "-", round(sen_g_2,4))
	print("Verhältnis Interactions:"+ "\t", round(ver_int,4),"\tgefordert:",round(int_g_1,4), "-", round(int_g_2,4))
	print("Verhältnis 0/1:         " + "\t", round(ver_n_y,4),"\tgefordert:",round(n_y_g_1,4), "-", round(n_y_g_2,4))
	if sen_g_2 > ver_sen > sen_g_1  and int_g_2 > ver_int > int_g_1 and n_y_g_2 > ver_n_y > n_y_g_1:
		auswerten = True
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

def get_lists_for_save(tupel_split):
	li_1_save_sent = []
	li_1_save_lab = []
	for i in tupel_split[0]:
		li_1_save_sent.append(i[0])
		li_1_save_lab.append(i[1])
	li_2_save_sent = []
	li_2_save_lab = []
	for e in tupel_split[1]:
		li_2_save_sent.append(e[0])
		li_2_save_lab.append(e[1])
	return [li_1_save_sent,li_1_save_lab],[li_2_save_sent,li_2_save_lab]

def convert_sen_to_art(sentence_id_list_full):
	art_li  = []
	for sen in sentence_id_list_full:
		art_li.append(sen[:sen.index("-")])
	#print("len sentence_id_list_full:", len(sentence_id_list_full))
	#print("len art_li:", len(art_li))
	return art_li

def save_all(tuple_split,file,ip_index_spalte,anzahl_int_ges,anzahl_satz_ges,anzahl_art_ges,n_y_verh_ges):
	save_lists = get_lists_for_save(tuple_split)
	save_as_tsv(save_lists[0],file,"test",ip_index_spalte)
	save_train_tsv(save_lists[1],file,"train")
	ds_results_save(tuple_split,anzahl_int_ges,anzahl_satz_ges,anzahl_art_ges,n_y_verh_ges)

def ds_results_save(tuple_split,anzahl_int_ges,anzahl_satz_ges,anzahl_art_ges,n_y_verh_ges):
	int = get_ver_int(tuple_split)
	art = get_ver_art(tuple_split)
	sen = get_ver_sen(tuple_split)
	n_y = get_ver_n_y(tuple_split)
	file_res = open("DS_results.tsv", "w")
	file_res.write("Gesamtanzahl Artikel:" + "\t" + str(anzahl_art_ges) + "\n")
	file_res.write("Anzahl Artikel in Test:" + "\t" + str(art[0]) + "\n")
	file_res.write("Anzahl Artikel in Train:" + "\t" + str(art[1]) + "\n")
	file_res.write("Anteil von Test an gesamten Artikeln:" + "\t" + str(round((art[0]/anzahl_art_ges),4)) + "\n")

	file_res.write("Gesamtanzahl Sätze:" + "\t" + str(anzahl_satz_ges) + "\n")
	file_res.write("Anzahl Sätze in Test:" + "\t" + str(sen[0]) + "\n")
	file_res.write("Anzahl Sätze in Train:" + "\t" + str(sen[1]) + "\n")
	file_res.write("Anteil von Test an gesamten Sätzen:" + "\t" + str(round((sen[0]/anzahl_satz_ges),4)) + "\n")

	file_res.write("Gesamtanzahl interactions:" + "\t" + str(anzahl_int_ges) + "\n")
	file_res.write("Anzahl Interaktionen in Test:" + "\t" + str(int[0]) + "\n")
	file_res.write("Anzahl Interaktionen in Train:" + "\t" + str(int[1]) + "\n")
	file_res.write("Anteil von Test an gesamten Interaktionen:" + "\t" + str(round((int[0]/anzahl_int_ges),4)) + "\n")

	file_res.write("Gesamtes 0/1 Verhältnis:" + "\t" + str(round((n_y_verh_ges),4)) + "\n")
	file_res.write("0/1 Verhältnis in Test:" + "\t" + str(round((n_y[0]/n_y[1]),4)) + "\n")
	file_res.write("0/1 Verhältnis in Train:" + "\t" + str(round((n_y[2]/n_y[3]),4)) + "\n")
	file_res.write("Verhältnis des 0/1 Verhältnis von Test und Train:" + "\t" + str(round(((n_y[0]/n_y[1])/(n_y[2]/n_y[3])),4)) + "\n")
	file_res.close()


	#print(n_y_1)
	n_y_2 = []
	for e in tuple_split[1]:
		n_y_2.append(e[1])







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
	file_lists = read_file(file)
	sentence_list_full = file_lists[0]
	label_list_full = file_lists[1]
	n_y_verh_ges = label_list_full.count(0)/label_list_full.count(1)
	sentence_id_list_full = file_lists[2]
	#print(len(sentence_id_list_full))
	sentence_id_list_full_sorted = collections.OrderedDict.fromkeys(sentence_id_list_full).keys()
	anzahl_satz_ges = len(sentence_id_list_full_sorted)
	art_id_list_full = convert_sen_to_art(sentence_id_list_full)
	art_id_list_full_sorted = collections.OrderedDict.fromkeys(art_id_list_full).keys()
	anzahl_art_ges = len(art_id_list_full_sorted)
	print("anzahl der art:",anzahl_art_ges)
	print("anzahl der sätze:",anzahl_satz_ges)
	file_tupel_full = lists_to_tuple_list(file_lists)
	anzahl_int_ges = len(file_tupel_full)
	print("anzahl der interactions:",anzahl_int_ges)
	random_zahlen_part = get_random_part_neu(anzahl_art_ges, anteil)
	list_of_art_lists = create_split_id_lists(random_zahlen_part,art_id_list_full_sorted)
	id_list_1 = list_of_art_lists[0]
	id_list_2 = list_of_art_lists[1]
	tuple_split = split_tuples(file_tupel_full,id_list_1,id_list_2)

	print("\n" + "1.Versuch")
	c = 2
	while auswerten(anteil,tuple_split,0.01,0.01,0.01) == False:
		print("\n" + str(c) + ".Versuch")
		random_zahlen_part = get_random_part_neu(anzahl_art_ges, anteil)
		list_of_art_lists = create_split_id_lists(random_zahlen_part,art_id_list_full_sorted)
		id_list_1 = list_of_art_lists[0]
		id_list_2 = list_of_art_lists[1]
		tuple_split = split_tuples(file_tupel_full,id_list_1,id_list_2)
		c = c + 1
	save_all(tuple_split,file,ip_index_spalte,anzahl_int_ges,anzahl_satz_ges,anzahl_art_ges,n_y_verh_ges)
		#list_split_save_1 = get_lists_for_save(tuple_split_1)
		#list_split_save_2 = get_lists_for_save(tuple_split_2)
		#save_as_tsv(list_split_save_1,file,"test",ip_index_spalte)
		#save_train_tsv(list_split_save_2,file,"train")
	#file_res = open("DS_results.tsv", "w")
	#file_res.write("XXXXXX" + "\t" + "XXXXXXXXXXXX" + "\n")
	#print(">>> " + str(file[:-4]) +"_test" + ".tsv" +" and " + str(file[:-4]) +"_train" + ".tsv" + " created succesfully")


def main_ohne_while(file,anteil):
	#ip_index_spalte = input("mit index-spalte?" + "\n" +  "==> enter y/n" + "\n" + "==> ")
	ip_index_spalte = "y"
	file_lists = read_file(file)
	sentence_list_full = file_lists[0]
	label_list_full = file_lists[1]
	sentence_id_list_full = file_lists[2]
	#print(len(sentence_id_list_full))
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
	random_zahlen_part = get_random_part_neu(anzahl_art_ges, anteil)
	#print(random_zahlen_part)
	list_of_art_lists = create_split_id_lists(random_zahlen_part,art_id_list_full_sorted)
	id_list_1 = list_of_art_lists[0]
	id_list_2 = list_of_art_lists[1]
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


ueber_main("CPI-DS_full_cut.tsv")
