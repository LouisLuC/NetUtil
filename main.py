from sys import argv
import config_self_use as cfg
# import config as cfg 
from EmailListener import EmailListener
from WebListener import WebListener
import requests as rq
import time
from re import search

assert len(argv) == 4, "Useage: "+argv[0]+" <seq_path> <out_put_path> <PPI_list>"

# set-up
seq_path  = "seqs"# argv[1]
out_path  = "out"# argv[2]
list_path = "ppi_test_1.txt"# argv[3]
# command $ python main.py seqs out ppi_test_1.txt

def main():
    list_file      = open(list_path)
    email_listener = EmailListener(cfg.email_host, cfg.user, cfg.password)
    web_listener   = WebListener()


    for line in list_file.readlines():
        line = line.strip()
        
        # processing PPI pairs file
        ids = line.split(",")
        ids = [id.strip() for id in ids]
        task_id = ids[0] + "-" + ids[1]

        files = {
            "seq_fileA":open(seq_path + "/" + ids[0] + ".fasta", "rb"),
            "seq_fileB":open(seq_path + "/" + ids[1] + ".fasta", "rb"),
        }

        fields = {
            "TARGET":task_id,
            "REPLY-E-MAIL":cfg.user
        }

        # push query
        print("ready to sent " + task_id)
        while True:
            push = rq.post(cfg.host_url+cfg.put_loc, data = fields, files = files)
            if push.ok:
                # check email for received email to retrieve the task id
                if cfg.confirm_info in push.text:
                    print("query " + task_id +" has been sented to Threpp")
                    break
                else:
                    print(push.text)
                    exit()

        # listen to email
        search_term = '(SUBJECT "' + task_id +'" SUBJECT "received" FROM "yangzhanglab")'
        match = email_listener.listen(search_term, cfg.out_id_pattern, return_match=True)
        out_id = match.group(1)
        print("Task_id getted: " + out_id)

        # listen to the Threpp output page until result is ready
        there_is_result = web_listener.listen(cfg.host_url+cfg.out_loc+out_id, "result.zip", return_match=False)
        if there_is_result:
            print("result complete")
            web_listener.pull(cfg.host_url+cfg.out_loc+out_id + "/result.zip", rename=task_id+".zip")
        print(task_id + " download complete\n\n")
            
        # close
        files["seq_file_A"].close()
        files["seq_file_B"].close()

    # garbage collection
    list_file.close()       
    email_listener.close()
    email_listener.logout()

# test
main()

if __name__ == "__main__":
    main()
    """
    list_file      = open(list_path)
    email_listener = EmailListener(cfg.email_host, cfg.user, cfg.password)
    web_listener   = WebListener()


    for line in list_file.readlines():
        line = line.strip()
        
        # processing PPI pairs file
        ids = line.split(",")
        ids = [id.strip() for id in ids]
        seq_file_A = open(seq_path + "/" + ids[0] + ".fasta", "rb")
        seq_file_B = open(seq_path + "/" + ids[1] + ".fasta", "rb")
        task_id = ids[0] + "-" + ids[1]

        files = {
            "seq_fileA":seq_file_A,
            "seq_fileB":seq_file_B,
        }

        fields = {
            "TARGET":task_id,
            "REPLY-E-MAIL":cfg.user
        }

        # push query
        print("ready to sent " + task_id)
        while True:
            push = rq.post(cfg.host_url+cfg.put_loc, fields, files)
            if push.ok:
                # check email for received email to retrieve the task id
                if cfg.confirm_info in push.text:
                    print("query " + task_id +" has been sented to Threpp")
                    break

        # listen to email
        search_term = '(SUBJECT "' + task_id +'" SUBJECT "received" FROM "yangzhanglab")'
        match = email_listener.listen(search_term, cfg.out_id_pattern, return_match=True)
        out_id = match.group(1)
        print("Task_id getted: " + out_id)

        # listen to the Threpp output page until result is ready
        there_is_result = web_listener.listen(cfg.host_url+cfg.out_loc+out_id, "result.zip", return_match=False)
        if there_is_result:
            print("result complete")
            web_listener.pull(cfg.host_url+cfg.out_loc+out_id + "/result.zip", rename=task_id+".zip")
        print(task_id + " download complete\n\n")
            
        # close
        seq_file_A.close()
        seq_file_B.close()

    # garbage collection
    list_file.close()       
    email_listener.close()
    email_listener.logout()
    """