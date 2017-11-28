import os
import conf.inputConfiguration as sci
import conf.outputConfiguration as sco
from datetime import datetime, timedelta
import shutil

#import pdb; pdb.set_trace()
file_prefix = 'received_data_'
input_path = sci.INPUTFILES_PATH[0]
used_path = sci.USEDFILES_PATH
processed_path = sco.PROCESSEDFILES_PATH

used = []
processed = []
retry = []

dt = datetime.now() - timedelta(hours=1)
start_dt = dt.replace(minute=0,second=0,microsecond=0)
end_dt = dt.replace(minute=59,second=59,microsecond=999999)

for root, dirs, files in os.walk(used_path, topdown=False):
   for name in files:
      used.append(name)

for root, dirs, files in os.walk(processed_path, topdown=False):
   for name in files:
      processed.append(name)

for file in used:
    file_dt = datetime.strptime(file[len(file_prefix):len(file_prefix)+26], '%Y-%m-%d_%H:%M:%S.%f')
    if len(file[len(file_prefix):]) > 94:
        continue
    if file_dt >= start_dt and file_dt <= end_dt:
        print 'Moving ' + used_path + '/' + file + ' to ' + input_path + '/' + file
        shutil.move(used_path + '/' + file, input_path + '/' + file)