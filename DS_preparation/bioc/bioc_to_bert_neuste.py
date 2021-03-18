import pandas as pd
import random
import numpy as np
from tqdm import tqdm
from time import sleep
import string
from nltk import sent_tokenize
import os





def get_file_mit_headline(file):
	column_name_storage = ["A","B","C","D","E","F","G","H","I","J","K"]
	df = pd.read_csv(file, sep="\t", header=None)
	column_name_needed = column_name_storage[:len(df.columns)]
	df.columns = column_name_needed
	df.to_csv(str(file[:-4])+ "_header.tsv",index=False, header=True, sep='\t')
	print(str(file[:-4])+ "_header.tsv" + " wurde erstellt")

def read_relations(file_relations):
	df_rel = pd.read_csv(file_relations, sep="\t")
	column_name_list = get_column_name_list(df_rel)
	relations_full = []
	for ind in df_rel.index:
		id_1_row = df_rel[column_name_list[0]][ind]
		CPR_type_1_row = df_rel[column_name_list[1]][ind]
		y_n_1_row = df_rel[column_name_list[2]][ind]
		e1_1_row = get_arg_number(df_rel[column_name_list[4]][ind])
		e2_1_row = get_arg_number(df_rel[column_name_list[5]][ind])
		relations_full.append((id_1_row,CPR_type_1_row,y_n_1_row,e1_1_row,e2_1_row))
	return relations_full
		#print(id_1_row,CPR_type_1_row,y_n_1_row,e1_1_row,e2_1_row)

def read_entities(file_entities):
	df_rel = pd.read_csv(file_entities, sep="\t")
	column_name_list = get_column_name_list(df_rel)
	entities_full = []
	for ind in df_rel.index:
		id_1_row = df_rel[column_name_list[0]][ind]
		entity_number_1_row = get_arg_number(df_rel[column_name_list[1]][ind])
		entity_type_1_row = df_rel[column_name_list[2]][ind]
		entity_start_1_row = df_rel[column_name_list[3]][ind]
		entity_end_1_row = df_rel[column_name_list[4]][ind]
		entity_1_row = df_rel[column_name_list[5]][ind]
		entities_full.append((id_1_row,entity_number_1_row,entity_type_1_row,entity_start_1_row,entity_end_1_row,entity_1_row))
	return entities_full


def read_abstracts(file_abstracts):
	df_rel = pd.read_csv(file_abstracts, sep="\t")
	column_name_list = get_column_name_list(df_rel)
	abstracts_full = []
	for ind in df_rel.index:
		id_1_row = df_rel[column_name_list[0]][ind]
		title_1_row = df_rel[column_name_list[1]][ind]
		abstract_1_row = df_rel[column_name_list[2]][ind]
		abstracts_full.append((id_1_row,title_1_row,abstract_1_row))
	return abstracts_full




def get_rest_for_relations(relations_full,entities_full,abstracts_full):
	output_list = []
	for pair in relations_full:
		e1_number = pair[3]
		e2_number = pair[4]
		e1_found = False
		e2_found = False
		#print(e1_number, e2_number)
		relation_type = pair[1]
		id = pair[0]
		for entity in entities_full:
			if entity[0] == id:
				if entity[1] == e1_number:
					e1_start = entity[3]
					e1_ende = entity[4]
					e1_type = entity[2]
					e1_name = entity[5]
					e1_found = True
				elif entity[1] == e2_number:
					e2_start = entity[3]
					e2_ende = entity[4]
					e2_type = entity[2]
					e2_name = entity[5]
					e2_found = True
			if e1_found and e2_found:
				tupel_1_run = (id,relation_type,e1_number,e1_type,e1_start,e1_ende,e1_name,e2_number,e2_type,e2_start,e2_ende,e2_name)
				output_list.append(tupel_1_run)
				e1_start = "ERROR!!!!!!"
				e1_ende = "ERROR!!!!!!"
				e2_start = "ERROR!!!!!!"
				e2_ende = "ERROR!!!!!!"
				e1_type	= "ERROR!!!!!!"
				e2_type	= "ERROR!!!!!!"
				break
	return output_list












def get_arg_number(arg):
	arg_sliced = arg[arg.index("T")+ 1:]
	return arg_sliced








def df_to_list(df,column):
	list_1 = df[column].to_list()
	return list_1

def get_column_name_list(df):
	column_name_list = []
	for col in df.columns:
		column_name_list.append(col)
	return column_name_list

def get_all_colums(df):
    column_name_list = get_column_name_list(df)
    tsv_as_list = []
    for column_name in column_name_list:
        column_as_list  = []
        column_as_list = df_to_list(df,column_name)
        tsv_as_list.append(column_as_list)
    return tsv_as_list

def compare_tsvs(file_big,file_small):
    df_big = pd.read_csv(file_big, sep="\t")
    df_small = pd.read_csv(file_small, sep="\t")
    df_big_all = get_all_colums(df_big)
    df_small_all = get_all_colums(df_small)
    counter = 0
    for el in df_small_all[0]:
        if el in df_big_all[0]:
            counter += 1
            print(df_small_all[0].index(el))
    print(counter/len(df_big_all[0])," of ", file_small, " in ", file_big)
    return counter/len(df_big_all[0])

def nltk_text_to_sen(text):
	return sent_tokenize(text)

def abstracts_full_to_sentences_solo_with_id(abstracts_full):
	abstract_list_all = []
	for abstract in abstracts_full:
		abstract_list_1 = []
		abstract_id = abstract[0]
		abstract_title = abstract[1]
		title_abstract_id = str(abstract_id) + "-0"
		abstract_text = abstract[2]
		#print(abstract_id,abstract_title)
		abstract_text_satz_liste = nltk_text_to_sen(abstract_text)
		abstract_list_1.append(abstract_id)
		abstract_list_1.append((title_abstract_id,abstract_title))
		#print(abstract_list_1)
		for counter, satz in enumerate(abstract_text_satz_liste,1):
			satz_abstract_id = str(abstract_id) + "-" + str(counter)
			abstract_list_1.append((satz_abstract_id,satz))
			#print(satz_abstract_id,satz)
		#print(abstract_list_1)
		abstract_list_all.append(abstract_list_1)
	return abstract_list_all

def abstracts_full_to_sentences_solo_with_id_add(abstracts_full):
	abstract_list_all = []
	for abstract in abstracts_full:
		abstract_list_1 = []
		abstract_id = abstract[0]
		abstract_title = abstract[1]
		title_abstract_id = str(abstract_id) + "-0"
		abstract_text = abstract[2]
		#print(abstract_id,abstract_title)
		abstract_text_satz_liste = nltk_text_to_sen(abstract_text)
		abstract_text_satz_liste_space = add_space_after_sen(abstract_text_satz_liste)
		#print(abstract_text_satz_liste_space)
		abstract_list_1.append(abstract_id)
		abstract_list_1.append((title_abstract_id,abstract_title))
		#print(abstract_list_1)
		for counter, satz in enumerate(abstract_text_satz_liste_space,1):
			satz_abstract_id = str(abstract_id) + "-" + str(counter)
			abstract_list_1.append((satz_abstract_id,satz))
			#print(satz_abstract_id,satz)
		#print(abstract_list_1)
		abstract_list_all.append(abstract_list_1)
	return abstract_list_all


def add_space_after_sen(abstract_text_satz_liste):
	output_list = []
	for num in range(0,len(abstract_text_satz_liste)-1):	#-1 da an letztes kein leerzeichen dran
		output_list.append(abstract_text_satz_liste[num] + "X")
	output_list.append(abstract_text_satz_liste[-1]) #um das letzte ohne X anzuhängen
	return output_list


def list_list_to_dict(li):
	keys = []
	values  = []
	for el in li:
		keys.append(el[0])
		values.append(el[1:])
	dic = dict(zip(keys, values))
	return dic

def get_satz_tuple(abstract,e1_start):
	summe_len = 0 #wegen indice - länge ausgleich
	counter = 0
	if e1_start == 0:
		return abstract[0][0],abstract[0][1],(len(abstract[0][1])-1)
	while summe_len < e1_start:
		#print(counter,summe_len)
		summe_len += len(abstract[counter][1]) # +1 wegen leerzeichen
		counter +=1
	return abstract[counter -1][0],abstract[counter -1][1],summe_len +1 #mit +1 passt es für nicht null (fast alle)

def interact_converter(int_type):
	if int_type in ["CPR:3","CPR:4","CPR:5","CPR:6","CPR:9"]:
		return "1"
	elif int_type == "CPR:10":
		return "0"
	else:
		print("!!!Falscher interactionstype")

def find_sentence_from_relation_prepare_lists_for_save(all_relations,abstract_list_all): # noch gucken dass das mit den types passt
	abstract_list_all_dict = list_list_to_dict(abstract_list_all)
	satz_liste_for_save = []
	interaction_1_0_for_save = []
	satz_id_liste_for_save = []
	for relation in all_relations:
		#print(relation)
		abstract_id = relation[0]
		#print(abstract_id)
		type = relation[1]
		if type not in ["CPR:3","CPR:4","CPR:5","CPR:6","CPR:9","CPR:10"]:
			continue
		#print(type)
		interaction_1_0 = interact_converter(type)
		e1_number = relation[2]
		e1_type = relation[3]
		e1_start = relation[4]
		e1_ende = relation[5]
		e1_name = relation[6]
		e2_number = relation[7]
		e2_type = relation[8]
		e2_start = relation[9]
		e2_ende = relation[10]
		e2_name = relation[11]
		#print(e1_name,e1_start,e2_name,e2_start)
		abstract = abstract_list_all_dict.get(abstract_id)
		satz_tuple = get_satz_tuple(abstract,e1_start)
		#print(satz_tuple)
		satz_id = satz_tuple[0]
		satz = satz_tuple[1]
		satz_len_bis_inklusive_dahin = satz_tuple[2]
		start_satz = satz_len_bis_inklusive_dahin -len(satz)
		e1_stelle_im_satz = e1_start - start_satz
		e2_stelle_im_satz = e2_start - start_satz
		rauscutten = False
		if satz[e1_stelle_im_satz] == e1_name[0]: # wenn alles passt
			satz_ersetzt = type_in_satz_ersetzen_besser(satz, e1_name, e2_name,e1_start, e1_ende, e2_ende, e2_start, right_type(e1_type),right_type(e2_type),e1_stelle_im_satz,e2_stelle_im_satz)
		elif satz[e1_stelle_im_satz] != e1_name[0]:
			#print("nur schlechtes ersetzen möglich")
			#print(satz)
			#print(e1_name)
			satz_ersetzt = type_in_satz_ersetzen(satz, e1_name, e2_name, right_type(e1_type),right_type(e2_type))
			#print(satz_ersetzt)
		if satz_ersetzt.count("@COMPOUND$") != 1 and satz_ersetzt.count("@PROTEIN$") !=1: #Kontrolle
			print("!!!! Fehler: zuviele Entities ersetzt")
			print("Ursprünglicher Satz:")
			print(satz)
			print("Ersetzter Satz:")
			print(satz_ersetzt)
			print("c:",satz_ersetzt.count("@COMPOUND$"),"p:",satz_ersetzt.count("@PROTEIN$"))
			print("==> rauscutten?")
			ip = input("==> y/n?")
			if ip == "y":
				rauscutten = True
			else:
				rauscutten = False

		if rauscutten == False:
			satz_liste_for_save.append(satz_ersetzt)
			interaction_1_0_for_save.append(interaction_1_0)
			satz_id_liste_for_save.append(satz_id)

		else:
			continue
	#print(len(satz_liste_for_save))
	#print(len(interaction_1_0_for_save))
	#print(len(satz_id_liste_for_save))
	return satz_liste_for_save, interaction_1_0_for_save,satz_id_liste_for_save

def type_in_satz_ersetzen_besser(satz, e1, e2,e1_start, e1_ende, e2_ende, e2_start, entity_type_1,entity_type_2,e1_stelle_im_satz,e2_stelle_im_satz):
	len_alt = len(satz)
	#print(satz + "___")
	len_e1 = e1_ende - e1_start
	len_e2 = e2_ende - e2_start
	len_dif_wort = len(entity_type_1) + 2 - len(e1)
	satz_part_1 = satz[0:e1_stelle_im_satz]
	satz_part_2 = satz[e1_stelle_im_satz + len_e1: len_alt]
	satz_a = satz_part_1 + "@"+ entity_type_1.upper() +"$" + satz_part_2
	len_neu = len(satz_a)
	len_dif = len_neu -len_alt
	#if "@COMPOUND$" not in satz_a: #kontrolle
		#print(satz_a)
	if e1_start < e2_start: # noch nicht okay!!!!!!!!!!!!!!!!!!!!! e2_start passt nicht
		satz_a_part_1 = satz_a[0:e2_stelle_im_satz + len_dif] # 1.teil passt
		#print(satz_a)
		#print(satz_a_part_1)
		#print(e2, e2_stelle_im_satz + len_e2 + len_dif_wort)
		#print(satz_a.index(e2))
		satz_a_part_2 = satz_a[e2_stelle_im_satz + len_e2 + len_dif_wort: len_neu]
		#print(satz_a_part_2)
		satz_output = satz_a_part_1 + "@"+ entity_type_2.upper() +"$" + satz_a_part_2
		#print(satz_output)
	elif e1_start > e2_start: #funktioniert
		satz_a_part_1 = satz_a[0:e2_stelle_im_satz]
		#print(satz_a_part_1)
		satz_a_part_2 = satz[e2_stelle_im_satz + len_e2: len_neu]
		satz_output = satz_a_part_1 + "@"+ entity_type_2.upper() +"$" + satz_a_part_2
		#print(satz_output)
	#if " @COMPOUND$ " not in satz_output and " @PROTEIN$ " not in satz_output: #kontrolle
		#print(satz_output)
	return satz_output
	#verhindern dass mehrmals gleioches wort mehrmals ersetzt wird ==> e stellen verwenden

def type_in_satz_ersetzen_besser_try(satz, e1, e2,e1_start, e1_ende, e2_ende, e2_start, entity_type_1,entity_type_2,e1_stelle_im_satz,e2_stelle_im_satz):
	len_alt = len(satz)
	#print(satz + "___")
	len_e1 = e1_ende - e1_start
	len_e2 = e2_ende - e2_start
	len_dif_wort = len(entity_type_1) + 2 - len(e1)
	satz_part_1 = satz[0:e1_stelle_im_satz]
	satz_part_2 = satz[e1_stelle_im_satz + len_e1: len_alt]
	satz_a = satz_part_1 + "@"+ entity_type_1.upper() +"$" + satz_part_2
	len_neu = len(satz_a)
	len_dif = len_neu -len_alt
	if e1_start < e2_start: # noch nicht okay!!!!!!!!!!!!!!!!!!!!! e2_start passt nicht
	#print(satz_a)
		 #print(satz_a_part_2)
		 satz_output = satz_a.replace("e2","@"+ entity_type_2.upper() +"$")
	elif e1_start > e2_start: #funktioniert
		 satz_a_part_1 = satz_a[0:e2_stelle_im_satz]
		 #print(satz_a_part_1)
		 satz_a_part_2 = satz[e2_stelle_im_satz + len_e2: len_neu]
		 satz_output = satz_a_part_1 + "@"+ entity_type_2.upper() +"$" + satz_a_part_2
		 #print(satz_output)
	return satz_output
	#verhindern dass mehrmals gleioches wort mehrmals ersetzt wird ==> e stellen verwenden


def type_in_satz_ersetzen(satz, e1, e2, entity_type_1,entity_type_2):
	satz_output_1 = satz.replace(e1,"@"+ entity_type_1.upper() +"$")
	satz_output = satz_output_1.replace(e2,"@"+ entity_type_2.upper() +"$")
	return satz_output

def right_type(word):
	if word == "GENE-Y":
		return "PROTEIN"
	elif word == "GENE-N":
		return "PROTEIN"
	elif word == "CHEMICAL":
		return "COMPOUND"
	else:
		return "Type unbekannt!!!!!!!!!!!!"

def save_as_tsv(lists_as_tupel,file): # nachher machen
	df = pd.DataFrame(list(zip(lists_as_tupel[0], lists_as_tupel[1],lists_as_tupel[2])),columns =['sentence', 'label','sentence-id'])
	df.to_csv(str(file)+ "bioc_full.tsv",index=False, header=True, sep='\t')
	print(">>> " + str(file) + "bioc_full.tsv" + " created succesfully" )

def create_filesnames_from_filestamm(stamm):
	file_relations = str(stamm) + "_relations.tsv"
	file_abstracts = str(stamm) + "_abstracts.tsv"
	file_entities = str(stamm) + "_entities.tsv"
	file_gold = str(stamm) + "_gold_standard.tsv"
	return file_relations,file_abstracts,file_entities,file_gold


######################################

def main(stamm):
	filenames = create_filesnames_from_filestamm(stamm)
	print(filenames)
	file_relations = filenames[0]
	file_abstracts = filenames[1]
	file_entities = filenames[2]
	file_gold = filenames[3]

	file = file_relations[:-13]
	print(file)
	get_file_mit_headline(file_relations)
	get_file_mit_headline(file_abstracts)
	get_file_mit_headline(file_entities)
	get_file_mit_headline(file_gold)
	print("xxx")
	relations_full = read_relations(file_relations)
	entities_full = read_entities(file_entities)
	abstracts_full = read_abstracts(file_abstracts)
	all_relations = get_rest_for_relations(relations_full,entities_full,abstracts_full)
	abstract_list_all = abstracts_full_to_sentences_solo_with_id_add(abstracts_full)
	find_sentence_from_relation_prepare_lists_for_save(all_relations,abstract_list_all)
	save_as_tsv(find_sentence_from_relation_prepare_lists_for_save(all_relations,abstract_list_all),file)
	os.remove(str(file_relations[:-4])+ "_header.tsv")
	os.remove(str(file_abstracts[:-4])+ "_header.tsv")
	os.remove(str(file_entities[:-4])+ "_header.tsv")
	os.remove(str(file_gold[:-4])+ "_header.tsv")






















#######################################

#df_abstracts = pd.read_csv(file_abstracts, sep="\t")
#df_entities = pd.read_csv(file_entities, sep="\t")
#df_gold = pd.read_csv(file_gold, sep="\t")
#df_relations = pd.read_csv(file_relations, sep="\t")
#file_abstracts = "chemprot_sample_abstracts.tsv"
#file_entities = "chemprot_sample_entities.tsv"
#file_gold = "chemprot_sample_gold_standard.tsv"
#file_relations = "chemprot_sample_relations.tsv"

main("chemprot_sample")
