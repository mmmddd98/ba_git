import xml.etree.cElementTree as ET
import pandas as pd
from tqdm import tqdm
from time import sleep
import collections
import itertools
import sys
from datetime import datetime
import shutil
import os
import statistics

############################################################
def get_sentence(file):
	tree = ET.parse(file)
	root = tree.getroot()
	satz_list = []
	ohne_satz_list = []
	pair_list = []
	for document in root:
		abstract_id = document.attrib["origId"]
		for sentence in document:
			entity_list_von_ein_Satz = []
			pair_list_von_einem_satz = []
			satz = sentence.attrib["text"]
			satz_id =sentence.attrib["origId"]
			satz_list.append(satz)
			for entity in sentence:
				if str(entity)[10:16] == "entity": 	# da manchmal auch pair erreicht
					charoffset = entity.attrib["charOffset"]
					e_start = charoffset_split(charoffset)[0]
					e_end = charoffset_split(charoffset)[1]
					entity_type_id_tupel=(entity.attrib["type"],entity.attrib["text"],get_last_int_character(entity.attrib["id"]),e_start,e_end)
					entity_list_von_ein_Satz.append(entity_type_id_tupel)
				if str(entity)[10:14] == "pair": 	# da manchmal auch entity erreicht
					pair_tuple = (get_last_int_character(entity.attrib["e1"]),get_last_int_character(entity.attrib["e2"]),entity.attrib["interaction"],satz_id)
					pair_list_von_einem_satz.append(pair_tuple)
					#print(pair_tuple)
			ohne_satz_list.append(entity_list_von_ein_Satz)
			pair_list.append(pair_list_von_einem_satz)
	#print(ohne_satz_list)
	return satz_list,ohne_satz_list, pair_list


def charoffset_split(charoffset):
	strich_stelle = charoffset.index("-")
	e_start = charoffset[:strich_stelle]
	e_ende =  charoffset[strich_stelle + 1:len(charoffset)]
	return(e_start,e_ende)

def get_last_int_character(string):
	reverse_string = string[::-1]
	output  = ""
	for i in reverse_string:
		try:
			a = int(i)
			output += i
		except ValueError:
			return output[::-1]


def create_lists_for_save(tup,cut,pri):
	satz_list  = tup[0]
	#print(len(satz_list))
	ohne_satz_list = tup[1]
	#print(len(ohne_satz_list))
	pair_list  = tup[2]
	#print(len(pair_list))
	satz_liste_for_save = []
	interaction_1_0_for_save = []
	satz_id_liste_for_save = []
	if len(satz_list) == len(ohne_satz_list) and len(satz_list) == len(pair_list):
		#print(len(satz_list))
		counter  = 1
		for satz in range(0,len(satz_list)):
			#print(counter)
			satz_konkret  = satz_list[counter-1]
			#print(satz_list_konkret)
			ohne_satz_list_konkret = ohne_satz_list[counter-1]
			entity_id_list_konkret = liste_tupel_zerlegen(ohne_satz_list_konkret)
			#print(ohne_satz_list_konkret)
			pair_list_konkret = pair_list[counter-1]
			#print(pair_list_konkret)
			counter+= 1
			#print(counter)
			for pair in pair_list_konkret:
				index_pair_e1 = pair[0]
				index_pair_e2 = pair[1]
				satz_id = pair[3]
				#print("index_pair_e1:",index_pair_e1)
				#print("index_pair_e2:",index_pair_e2)
				i_e1 = entity_id_list_konkret.index(index_pair_e1)
				i_e2 = entity_id_list_konkret.index(index_pair_e2)
				e1 = ohne_satz_list_konkret[i_e1][1]
				entity_type_1 = ohne_satz_list_konkret[i_e1][0]
				e1_start = ohne_satz_list_konkret[i_e1][3]
				e1_end = ohne_satz_list_konkret[i_e1][4]
				entity_type_2 = ohne_satz_list_konkret[i_e2][0]
				e2 = ohne_satz_list_konkret[i_e2][1]
				e2_start = ohne_satz_list_konkret[i_e2][3]
				e2_end = ohne_satz_list_konkret[i_e2][4]
				interaction_true_false = pair[2]
				interaction_1_0 = true_false_ersetzen(interaction_true_false)
				#print(e1,entity_type_1)
				#print(e2,entity_type_2)
				#print("interaction_true_false:",interaction_true_false)
				satz_for_save = type_in_satz_ersetzen_besser(satz_konkret,e1,int(e1_start), int(e1_end),entity_type_1,e2,int(e2_start), int(e2_end),entity_type_2,pri)
				if satz_for_save == "rauscutten" and cut == True :
					continue
				else:
					satz_liste_for_save.append(satz_for_save)
					interaction_1_0_for_save.append(interaction_1_0)
					satz_id_liste_for_save.append(satz_id)
					#print(satz_for_save)
	return satz_liste_for_save, interaction_1_0_for_save,satz_id_liste_for_save






def liste_tupel_zerlegen(liste):
	drit_liste = []
	for el in liste:
		drit_liste.append(el[2])
	return drit_liste

def type_in_satz_ersetzen(satz, e1, e2, entity_type_1,entity_type_2): #ersetzen über charoffsets + länge des ersten ersetzen
	satz_output_1 = satz.replace(e1,"@"+ entity_type_1.upper() +"$")
	satz_output = satz_output_1.replace(e2,"@"+ entity_type_2.upper() +"$")
	return satz_output

def type_in_satz_ersetzen_besser(satz,e1,e1_start, e1_ende,entity_type_1,e2,e2_start, e2_ende,entity_type_2,pri ):
	len_alt = len(satz)
	len_e1 = len(e1)
	len_e2 = len(e2)
	len_e1_dif = len(entity_type_1) + 2 -len_e1
	#print(len_e1_dif, e1,entity_type_1 )
	e2_start_nach_e1 = e2_start + len_e1_dif
	#print(satz + "___")
	if len(e1) == e1_ende - e1_start: 	#sollte immer passen
		satz_part_1 = satz[:e1_start]
		satz_part_2 = satz[e1_start + len_e1:]
		satz_a = satz_part_1 + "@"+ entity_type_1.upper() +"$" + satz_part_2
		len_neu = len(satz_a)
		#print(satz_a)
		if e1_start < e2_start:
			satz_part_1b = satz_a[:e2_start_nach_e1]
			#print(satz_part_1b)
			satz_part_2b = satz_a[e2_start_nach_e1 + len_e2:]
			satz_output = satz_part_1b + "@"+ entity_type_2.upper() +"$" + satz_part_2b
			#print(satz_output)

		elif e2_start < e1_start:
			satz_part_1b = satz_a[:e2_start]
			#print(satz_part_1b)
			satz_part_2b = satz_a[e2_start + len_e2: len_neu]
			satz_output = satz_part_1b + "@"+ entity_type_2.upper() +"$" + satz_part_2b

		else:
			if pri == True:
				print("!!!!!fehler mit e_länge!!!!!")
				print(satz)
			return "rauscutten"
		#print("da")

		proofed_sentece = proof_sentence(satz,satz_output)
		return proofed_sentece

	else:
		if pri == True:
			print("!!!!!fehler mit e_länge!!!!!")
			print(satz)
			return "rauscutten"

def proof_sentence(satz,satz_output): ###noch machen !!!!!!!!!!!!!!!!
	if satz_output.count("@COMPOUND$") != 1 or satz_output.count("@PROTEIN$") !=1: #Kontrolle
		print("!!!! Fehler: zuviele Entities ersetzt")
		#print("Ursprünglicher Satz:")
		#print(satz)
		#print("Ersetzter Satz:")
		print(satz_output)
		print("c:",satz_output.count("@COMPOUND$"),"p:",satz_output.count("@PROTEIN$"))
		print("************************************************************************")
		return "rauscutten"
	else:
		return satz_output


	#print(satz_a + "___")
	#len_neu = len(satz_a)
	#len_dif = len_neu -len_alt
	#if e1_start < e2_start: # noch nicht okay!!!!!!!!!!!!!!!!!!!!! e2_start passt nicht

		 #satz_output = satz_a.replace("e2","@"+ entity_type_2.upper() +"$")
	#elif e1_start > e2_start: #funktioniert
		 #satz_a_part_1 = satz_a[0:e2_stelle_im_satz]
		 #print(satz_a_part_1)
		# satz_a_part_2 = satz[e2_stelle_im_satz + len_e2: len_neu]
		# satz_output = satz_a_part_1 + "@"+ entity_type_2.upper() +"$" + satz_a_part_2
		 #print(satz_output)
	#verhindern dass mehrmals gleioches wort mehrmals ersetzt wird ==> e stellen verwenden

def true_false_ersetzen(string):
	if string == "True":
		return 1
	elif string == "False" :
		return 0







def save_as_tsv(list1,list2,list3,file, cut = True): # nachher machen
	df = pd.DataFrame(list(zip(list1, list2,list3)),columns =['sentence', 'label','sentence-id'])
	if cut == True:
		df.to_csv(str(file[:-4])+ "._full_cut.tsv",index=False, header=True, sep='\t')
		print(">>> " + str(file[:-4]) + "._full_cut.tsv" + " created succesfully" )
	else:
		df.to_csv(str(file[:-4])+ "._full.tsv",index=False, header=True, sep='\t')
		print(">>> " + str(file[:-4]) + "._full.tsv" + " created succesfully" )






############################################################

############################################################
#main

#def main(file):
#	for i in tqdm(range(100)):

def main(file):
	ip = input("gecuttete Version?" + "\n" +  "==> enter y/n" + "\n" + "==> " )
	if ip == "y":
		cut = True
		ip_2 = input("aussortierte Sätze printen?" + "\n" +  "==> enter y/n" + "\n" + "==> " )
		if ip_2 == "y":
			pri = True
		elif ip_2 == "n":
			pri = False
		else:
			print("ungültige Eingabe")
			return
	elif ip == "n":
		cut = False
		ip_2 = input("aussortierte Sätze printen?" + "\n" +  "==> enter y/n" + "\n" + "==> " )
		if ip_2 == "y":
			pri = True
		elif ip_2 == "n":
			pri = False
		else:
			print("ungültige Eingabe")
			return
	else:
		print("ungültige Eingabe")
		return
	print(cut)
	a = create_lists_for_save(get_sentence(file),cut,pri)
	satz_liste_for_save = a[0]
	interaction_1_0_for_save = a[1]
	satz_id_liste_for_save = a[2]
	save_as_tsv(satz_liste_for_save, interaction_1_0_for_save,satz_id_liste_for_save, file,cut)






############################################################
#run


#main("DS-40.xml")
main("CPI-DS.xml")
