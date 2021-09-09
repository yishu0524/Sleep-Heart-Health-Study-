import numpy as np
import pandas as pd
from xml.dom import minidom
import os
from xml.etree import ElementTree
import csv
#local
#profusion_dir=r'C:\Users\ASUS\Documents\school\SleepHeartHealthStudy'
#csv_dir=r'C:\Users\ASUS\Documents\school\SleepHeartHealthStudy'
csv_dir = '../../../../datacommons/plusds/sleep/shhs/shhs/datasets/'
profusion_dir = '../../../../datacommons/plusds/sleep/shhs/shhs/polysomnography/annotations-events-profusion/shhs1'
csv_file = os.path.join(csv_dir, 'shhs1-dataset-0.13.0.csv')
patients = pd.read_csv(csv_file)
print('file found!')
patient_ids = patients['nsrrid']
#patient_id = patient_ids[4840]
study='shhs1'
#result =  annotations_extract(study,patient_id);
#print('processing '+str(patient_id))


def profusion_xml_to_dataframe(profusion_file):
    tree = ElementTree.parse(profusion_file)
    root = tree.getroot()

    data = pd.DataFrame([])
    for att in root.find('ScoredEvents'):
        try:
                #         print(att.find('ScoredEvent').find('Start').text)
                # att.find('ScoredEvent').text
                #         print("==")
                #         print(att.find('Start').text)
                #         print(att.find('Duration').text)
                # print (att.find('EventType'))

            data = data.append([[
                    att.find('Name').text,
                    att.find('Start').text,
                    att.find('Duration').text,
                    att.find('Input').text
                ]])

        except Exception as ex:
            pass


    data.columns = ['Event', 'Start', 'Duration', 'Input']

    data.reset_index(inplace=True)
    data.drop(['index'], axis=1, inplace=True)

    data['Duration'] = pd.to_numeric(data['Duration'])
    data['Start'] = pd.to_numeric(data['Start'])
    summary = data.groupby("Event")["Event"].count()
    #sleep_stages = []
    #att = root.find('SleepStages')
    #for i in range(len(att)):
    #    sleep_stages.append(int(att[i].text))

    return data, summary


print('call')
conditions=['Arousal ()','Hypopnea','Mixed Apnea','Obstructive Apnea','SpO2 artifact','SpO2 desaturation']

summarys = [ [] for _ in range(len(conditions))]

for patient_id in patient_ids:
    print('processing '+str(patient_id)+'\n')
    profusion_file = os.path.join(profusion_dir, study+'-'+str(patient_id)+'-profusion.xml')
    data, summary = profusion_xml_to_dataframe(profusion_file)
    
    #print(summary)
    index = []
    for i, x in enumerate(summary.index):
        if x in conditions:
            loc = conditions.index(x)
            index.append(loc)
            summarys[loc].append(summary[i])

    for j in list(set( range(0,len(conditions))) - set(index) ):
        summarys[j].append(0)

#print(summarys)
base_path='.'
with open(os.path.join(base_path,'count.csv'),'w') as f:
    wr = csv.writer(f)
    wr.writerows(np.transpose(summarys))
    #base_path='.'

    #result.to_csv( os.path.join(base_path, 'annotations-summary'+str(patient_id)+'.csv'))
