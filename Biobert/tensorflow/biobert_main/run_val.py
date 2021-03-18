import os
import timeit
import time
from pathlib import Path
import shutil


def export_enter(biobert_dir,re_dir,task_name,output_dir):
    #print(output_dir)
    if biobert_dir  =="def":
        biobert_dir = "../pretrained_weights/biobert_v1.1_pubmed"
    #model
    os.environ['BIOBERT_DIR'] = str(biobert_dir)
    print(">>> Biobert dir:" )
    os.system("echo $BIOBERT_DIR")

    #input
    os.environ['RE_DIR'] = "../ds/" + str(re_dir)
    print(">>> input dir:" )
    os.system("echo $RE_DIR")

    #os.system("export TASK_NAME="+task_name)
    os.environ['TASK_NAME'] = str(task_name)
    print(">>> Taskname:" )
    os.system("echo $TASK_NAME")

    #output
    a_2 = ("../results/" + str(output_dir))
    #print(a_2)
    #os.system("export OUTPUT_DIR=" + str(a_2))
    os.environ['OUTPUT_DIR'] = str(a_2)
    print(">>> Output dir:" )
    os.system("echo $OUTPUT_DIR")
    return a_2

def create_out_folder_in_results(headfolder,von,bis):
    os.mkdir("../results/" + str(headfolder))
    for x in range(von,bis +1):
        os.mkdir("../results/" + str(headfolder) + "/" + str(x))
        print(">>> " + str(headfolder) + "/" + str(x) + " created <<<")



def run():
    #os.system("python3 run_re.py --task_name=$TASK_NAME --do_train=true --do_eval=true --do_predict=true --vocab_file=$BIOBERT_DIR/vocab.txt --bert_config_file=$BIOBERT_DIR/bert_config.json --init_checkpoint=$BIOBERT_DIR/model.ckpt-1000000 --max_seq_length=128 --train_batch_size=32 --learning_rate=2e-5 --num_train_epochs=3.0 --do_lower_case=false --data_dir=$RE_DIR --output_dir=$OUTPUT_DIR")
    print("wäre gerunnt")

def eval():
    os.system("python3 ./biocodes/re_eval.py --output_path=$OUTPUT_DIR/test_results.tsv --answer_path=$RE_DIR/test.tsv")

def ein_run(input_folder,output_folder):
    start = timeit.default_timer()
    output_dir = export_enter("def",str(input_folder),"gad",output_folder)
    Path(str(output_dir)).mkdir(parents=True, exist_ok=True)
    input_preprocess(input_folder,output_dir)
    #print(output_dir)
    time.sleep(4)
    os.system("echo $OUTPUT_DIR")
    run()
    stop = timeit.default_timer()
    file = open(str(output_dir) + "/run_laufzeit.tsv", "w")
    file.write(str(stop - start))
    eval()

#############################################################################################################################################################################################################


def input_preprocess(input_folder,output_dir):
    inhalt = sorted(os.listdir("../ds/" + str(input_folder)))
    if len(inhalt) != 3:
        print(">>> falsche Anzahl an input-files")
    stor  = get_name_train_and_test_file(inhalt)
    #print(stor)
    test_file_name  = stor[0]
    train_file_name  = stor[1]
    os.rename("../ds/" + str(input_folder) + "/" + test_file_name,"../ds/" + str(input_folder) + "/" + "test.tsv" )
    os.rename("../ds/" + str(input_folder) + "/" + train_file_name,"../ds/" + str(input_folder) + "/" + "train.tsv" )
    insert_dev(input_folder)
    print(">>> preprocess finished")

def get_name_train_and_test_file(input_files_list):
    for file_name in input_files_list:
        #print(file_name[-9:])
        if file_name[-8:]  == "test.tsv":
            test_file_name = file_name
        elif file_name[-9:]  == "train.tsv":
            train_file_name = file_name
    return test_file_name,train_file_name

def insert_dev(input_folder):
    shutil.copy("../ds/dev.tsv","../ds/" + str(input_folder) + "/dev.tsv")





def main(name_val_folder):
    files = os.listdir("../ds/cross_val/" + str(name_val_folder))
    files.sort()  
    #print(files)
    for i in files:
        print(i)
        ein_run("cross_val/"+ str(name_val_folder)+ "/" + str(i),"cross_val/"+ str(name_val_folder)+ "/" + str(i))
    
    
    


################################################################################


main("val_ds_test")





