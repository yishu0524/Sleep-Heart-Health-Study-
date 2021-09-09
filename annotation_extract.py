

import numpy as np
import pandas as pd
from xml.dom import minidom
import os
from xml.etree import ElementTree
#local
#profusion_dir=r'C:\Users\ASUS\Documents\school\SleepHeartHealthStudy'
#csv_dir=r'C:\Users\ASUS\Documents\school\SleepHeartHealthStudy'
csv_dir = '../../../../datacommons/plusds/sleep/shhs/shhs/datasets'
profusion_dir = '../../../../datacommons/plusds/sleep/shhs/shhs/polysomnography/annotations-events-profusion'
csv_file = os.path.join(csv_dir, 'shhs1-dataset-0.13.0.csv')
patients = pd.read_csv(csv_file)
patient_ids = patients['nsrrid']
patient_id = patient_ids[4841]
study='shhs1'
def annotations_extract(study, patient_id):
    profusion_file = os.path.join(profusion_dir, study+'-'+str(patient_id)+'-profusion'+'.xml')


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

        sleep_stages = []
        att = root.find('SleepStages')
        for i in range(len(att)):
            sleep_stages.append(int(att[i].text))

        return data, sleep_stages


    data_profusion, sleep_stages = profusion_xml_to_dataframe(profusion_file)
    Epoch_length=30;
    d = {'Event': sleep_stages, 'Start': np.array(range(len(sleep_stages)))*Epoch_length, 'Duration': np.ones(len(sleep_stages))*Epoch_length}
    df = pd.DataFrame(data=d)
    frames = [df, data_profusion[['Event', 'Start','Duration']]]

    result = pd.concat(frames)
    result.sort_values(by=['Start', 'Duration'])

    return result
    result = annotations_extract(study, patient_id)
    result.to_csv('annotations-'+str(patient_id)+'.csv')
