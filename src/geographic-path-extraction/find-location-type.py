import xml.etree.ElementTree as ET
from stanfordcorenlp import StanfordCoreNLP
from nltk.stem.wordnet import WordNetLemmatizer
from pathlib import Path
import pandas as pd
import os

nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')

datapath = Path(__file__).resolve().parents[2]
xml_file = str(datapath) + '/tools/vn-fn.xml'

root = ET.parse(xml_file).getroot()


def get_fn_frame(verb):
    found_frame = []
    found_vn_cls = []
    for type_tag in root.findall('vncls'):
        cls = type_tag.get('class')
        vnmember = type_tag.get('vnmember')
        fnframe = type_tag.get('fnframe')

        if vnmember == verb:
            found_frame.append(fnframe)
            found_vn_cls.append(cls)
    return [found_frame, found_vn_cls]


xml_roles_file = str(datapath) + '/tools/vn-fn-roles.xml'

root_roles = ET.parse(xml_roles_file).getroot()


def get_roles(fn_frame):
    fn_role = []
    vn_role = []
    for item in root_roles.findall('vncls'):
        cls = item.get('class')
        fnframe = item.get('fnframe')

        if cls.startswith('51.1') and fnframe == fn_frame:
            # print("yes")
            for roles in item.findall('roles/role'):
                fn_role.append(roles.get('fnrole'))
                vn_role.append(roles.get('vnrole'))

    return [fn_role, vn_role]


def get_travel_roles(fn_frame, vn_cls):
    is_travel_frame = False
    for item in root_roles.findall('vncls'):

        cls = item.get('class')
        fnframe = item.get('fnframe')
        if cls.startswith('51') and fnframe == fn_frame:
            for roles in item.findall('roles/role'):
                if roles.get('vnrole') == 'Location' or roles.get('vnrole') == 'Source' or roles.get(
                        'vnrole') == 'Destination':
                    is_travel_frame = True
    return is_travel_frame


def get_travel_roles_list(fn_frame, vn_cls):
    roles_list = []
    for item in root_roles.findall('vncls'):

        cls = item.get('class')
        fnframe = item.get('fnframe')
        if cls.startswith('51') and fnframe == fn_frame:
            for roles in item.findall('roles/role'):
                if roles.get('vnrole') == 'Location' or roles.get('vnrole') == 'Source' or roles.get(
                        'vnrole') == 'Destination':
                    roles_list.append(roles.get('fnrole'))
    roles_list = list(set(roles_list))
    return roles_list


def find_verbs(sentence):
    pos = nlp.pos_tag(sentence)
    verbs_list = [item[0] for item in pos if item[1] in {'VB', 'VBD', 'VBG', 'VBN'}]
    return verbs_list


def find_fn_vn_data(data):
    count = 0
    fn_roles = []
    vn_roles = []


def find_travel_frames(verb):
    base_verb = WordNetLemmatizer().lemmatize(verb, 'v')
    fn_frame_list = []
    [found_frame, found_vn_cls] = get_fn_frame(base_verb)
    total_frames = len(found_frame)

    for i in range(0, total_frames):
        is_travel_frame = get_travel_roles(found_frame[i], found_vn_cls[i])
        if is_travel_frame:
            fn_frame_list.append(found_frame[i])

    return fn_frame_list

def find_travel_frames_roles(verb):
    base_verb = WordNetLemmatizer().lemmatize(verb, 'v')
    fn_roles = []
    [found_frame, found_vn_cls] = get_fn_frame(base_verb)
    total_frames = len(found_frame)

    for i in range(0, total_frames):
        roles = get_travel_roles_list(found_frame[i], found_vn_cls[i])

        fn_roles = fn_roles + roles

    return fn_roles


def find(data):
    count = 0
    travel_verbs = []
    travel_verb_frames = []

    for index, row in data.iterrows():
        temp_travel_verbs = []
        temp_travel_verb_frames = []

        sentence = row['sentence']
        verbs = find_verbs(sentence)
        for verb in verbs:
            travel_frames = find_travel_frames(verb)
            # print(travel_frames)

            if len(travel_frames) != 0:
                travel_frames_str = ",".join(travel_frames)

                temp_travel_verbs.append(verb)
                temp_travel_verb_frames.append(travel_frames_str)

        temp_travel_verbs_str = ",".join(temp_travel_verbs)
        temp_travel_verbs_frames_str = ",".join(temp_travel_verb_frames)

        travel_verbs.append(temp_travel_verbs_str)
        travel_verb_frames.append(temp_travel_verbs_frames_str)

        count = count + 1
        print(count)

    data['Travel verbs'] = travel_verbs
    data['Travel verb Frames'] = travel_verb_frames

    return data


    # travel_verb = row['Travel verbs']
    # fn_frame = get_fn_frame(travel_verb)
    # fn_role = []
    # vn_role = []
    #
    # if fn_frame!="":
    #     [fn_role,vn_role] = get_roles(fn_frame)
    #
    # fnrole = ",".join(fn_role)
    # vnrole =  ",".join(vn_role)
    # fn_roles.append(fnrole)
    # vn_roles.append(vnrole)
    # frames.append(fn_frame)

    #     count = count + 1
    #     print(count)
    #
    # data['Frame'] = frames
    # data['FN Role'] =fn_roles
    # data['VN Role'] = vn_roles
def find_location_type(data):
    count = 0
    travel_verbs_role = []

    for index, row in data.iterrows():
        travel_verbs = row['Travel verbs']
        temp_travel_roles = []

        if not isinstance(travel_verbs, float):
            travel_verbs_list = travel_verbs.split(",")

            for verb in travel_verbs_list:
                travel_roles = []
                travel_roles = find_travel_frames_roles(verb)
                travel_roles.append("|")

                if len(travel_roles) != 0:
                    travel_roles_str = ",".join(travel_roles)
                    temp_travel_roles.append(travel_roles_str)
                    temp_travel_roles = list(set(temp_travel_roles))

        print(temp_travel_roles)
        if len(temp_travel_roles) > 1:
            if temp_travel_roles[-1] == '|':
                temp_travel_roles.pop()

        if len(temp_travel_roles) > 1:

            if temp_travel_roles[-1] == ',':
                temp_travel_roles.pop()
        print(temp_travel_roles)

        temp_travel_roles_str = ",".join(temp_travel_roles)

        travel_verbs_role.append(temp_travel_roles_str)


        count = count + 1
        print(count)
        print("=====================================")

    data['Travel verb role'] = travel_verbs_role


    return data

book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-travel-verbs-new.csv'.format(part, part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_location_type(data)

    writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-travel-verbs-new.csv'.format(
        part, part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1', index=False)
