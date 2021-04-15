from sys import argv
from config import CONFIG as cfg
from EmailListener import EmailListener
from PushPull import pull
import requests as rq
import time
from re import search

assert len(argv) == 4, "Useage: "+argv[0]+" <seq_path> <out_put_path> <PPI_list>"
# set-up
seq_path = argv[1]
out_path = argv[2]
list_path = argv[3]
email = cfg["user"]
time_interval = 300
out_id_pattern = "https://zhanglab.ccmb.med.umich.edu/Threpp/output/(\w+)\s"

# time out setted for every step
# not used
time_out = 1800

host_url = "https://zhanglab.ccmb.med.umich.edu/Threpp/"
put_loc = "bin/receive.cgi"
out_loc = "output/"
confirm_info = "A confirmation email for how to retrieve your job will be send to"

if __name__ == "__main__":
    list_file = open(list_path)
    listener = EmailListener(cfg["email_host"], cfg["user"], cfg["password"])

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
            "REPLY-E-MAIL":email
        }

        # push query
        while True:
            push = rq.post(host_url+put_loc, fields, files)
            if push.ok:
                # check email for received email to retrieve the task id
                if confirm_info in push.text:
                    print("query" + task_id +" sented to Threpp")
                    break

        # listen to email
        search_term = '(SUBJECT "' + task_id +'" SUBJECT "received" FROM "yangzhanglab")'
        match = listener.listen(search_term, out_id_pattern, return_match=True)
        out_id = match.group(1)
        print("Task_id get back: " + out_id)

        # listen to the Threpp output page until result is ready
        while True:
            rp = rq.get(host_url+out_loc+out_id)
            if "result.zip" in rp.text:
                break
            time.sleep(time_interval)
        pull(host_url+out_loc+out_id, rename = task_id + ".zip")

        # close
        seq_file_A.close()
        seq_file_B.close()

    # garbage collection
    list_file.close()       
    listener.close()
    listener.logout()
    
# TODO timeout system and log system