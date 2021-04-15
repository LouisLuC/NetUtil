import re
s = '''Dear user,
This email confirms that your have submitted sp|P49810|PSN2_HUMAN-sp|B2K312|SYR_YERPB to Threpp.
You can track job status at 

Yang Zhang lab
Department of Computational Medicine and Bioinformatics
University of Michigan
'''
a = re.search("https://zhanglab.ccmb.med.umich.edu/Threpp/output/(\w+)\s", s)

