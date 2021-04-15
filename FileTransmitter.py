import requests as rq
url = "https://zhanglab.ccmb.med.umich.edu/Threpp/bin/receive.cgi"

"""
seq_file_1 = open("./seq1.fasta", "r")
seq_file_2 = open("./seq2.fasta", "r")
ID = seq_file_1.split(".")[0] + "-" + seq_file_2.split(".")[0]
"""

ID = "testweb"
Email = "1730416031@suda.edu.cn"
seqa = "MNKSQLIDKIAAGADISKAAAGRALDAIIASVTESLKEGDDVALVGFGTFAVKERAARTGRNPQTGKEITIAAAKVPSFRAGKALKDAVN"
seqb = "MALTKAEMSEYLFDKLGLSKRDAKELVELFFEEIRRALENGEQVKLSGFGNFDLRDKNQRPGRNPKTGEDIPITARRVVTFRPGQKLKSRVENASPKDE"

files = {
    "seq_fileA":open("seq1.fasta", "rb"),
    "seq_fileB":open("seq2.fasta", "rb")
}
fields = {
    "TARGET":ID,
    "REPLY-E-MAIL":Email,
#    "SEQUENCEA":seqa,
#    "SEQUENCEB":seqb
}

result = rq.post(url, data = fields, files = files, stream=True)

rp = rq.get("https://zhanglab.ccmb.med.umich.edu/Threpp/output/TPP332")