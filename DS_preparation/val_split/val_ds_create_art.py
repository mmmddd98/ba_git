'''
   This script is for use after the full dataset is splitted in the 10 parts for 10 cross fold validation.
   Just specify the folder with the 10 parts as sys.argv-command-line argument.
   It creates the trainingdataset by putting 9 of the 10 splitted ds together and uses the 10th as testdataset.
   The script repeats that in every of the 10 possible constellations, so in the end every dataset is one time the testdataset.
   The output is a new folder in the sys.argv-command-line argument-folder.
 '''

import os
import glob
import pandas as pd
import sys
import getopt

#os.chdir(ordner)
#extension = 'tsv'
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

def get_1_file(doc_name,ordner):
    df = pd.read_csv(str(ordner) + "/" + str(doc_name),header=0, sep="\t")
    column_name  = get_column_name_list(df)
    #print(column_name)
    all_other_val = get_all_colums(df)
    return all_other_val

def write_data_1_run_in_results_tsv(ordner,print_list):
    with open(str(ordner) + "/" + 'results_all_parts.tsv', 'a') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(print_list)

def save_test_tsv(test_index_list, test_sent_list, test_label_list, ordner,ds):
    df = pd.DataFrame(list(zip(test_index_list, test_sent_list,test_label_list)),columns =['index', 'sentence','label'])
    df.to_csv(str(ordner) + "/" + "val_ds/ds-"+ str(ds) + "/test.tsv",index=False, header=True, sep='\t')

def save_train_tsv(full_list_ohne_test,ordner,ds): #ohne index
    train_label_list = []
    train_sent_list = []
    for el in full_list_ohne_test:
        train_label_list = train_label_list + el[2]
        train_sent_list = train_sent_list + el[1]
    #index noch neu kreiren
    df = pd.DataFrame(list(zip(train_sent_list,train_label_list)),columns =['sentence','label'])
    df.to_csv(str(ordner) + "/" + "val_ds/ds-"+ str(ds) + "/train.tsv",index=False, header=True, sep='\t')

def create_files(ordner,full_list):
    os.mkdir(str(ordner) + "/" + "val_ds")
    for i in range(1,len(full_list) + 1):
        os.mkdir(str(ordner) + "/" + "val_ds/ds-"+ str(i))
        #print(len(full_list[i-1]))
        test_index_list = full_list[i-1][0]
        #print(len(test_index_list))
        test_sent_list = full_list[i-1][1]
        #print(len(test_sent_list))
        test_label_list = full_list[i-1][2]
        #print(len(test_label_list))
        full_list_ohne_test_1 = full_list[:i-1]
        full_list_ohne_test_2 = full_list[i:]
        full_list_ohne_test = full_list_ohne_test_1 + full_list_ohne_test_2
        save_test_tsv(test_index_list, test_sent_list, test_label_list, ordner,i)
        save_train_tsv(full_list_ohne_test,ordner,i)




def main():
    argv  =sys.argv[1:]
    opts, argv = getopt.getopt(argv, "f")
    if argv[0] in os.listdir():
        print(">>> erstellen der cross-fold-datasets beginnt")
        ordner = argv[0]
    doc_list = []
    for doc in os.listdir(ordner):
        if "result" not in doc:
            doc_list.append(doc)
    sorted_doc_list = sort_mit_10(doc_list)
    full_list  = []
    for doc_sorted in sorted_doc_list:
        full_list.append(get_1_file(doc_sorted,ordner))
    create_files(ordner,full_list)
    print(">>> cross-fold-datasets erfolgreich erstellt")





#combine all files in the list
#combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
#combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

##############################################################################

main()
