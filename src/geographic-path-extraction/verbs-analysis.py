from collections import Counter
from pathlib import Path
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import verbnet as vn
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
import os
import numpy as np


def convert_to_base_verb(verb_list):
    verb_list = [item.lower() for item in verb_list]
    verb_list = [WordNetLemmatizer().lemmatize(item, 'v') for item in verb_list]
    return verb_list


def verbs_in_verbnet(verb):

    vn_results = vn.classids(lemma=verb)
    return 1 if vn_results else 0



def verbs_in_framenet(verb):

    fn_results = fn.frames_by_lemma(verb)
    print(fn_results)
    return 1 if fn_results else 0


def find_synonyms(verb):
    syn = wn.synsets(verb, pos=wn.VERB)
    syn_list = []

    for item in syn:

        for lemma in item.lemmas():
            syn_list.append(lemma.name())


    syn_list = list(set(syn_list))
    return syn_list


def travel_verb_instances(data):

    travel = data["Travel verbs"].str.cat(sep=',')
    travel_verbs = travel.split(",")
    travel_verbs = convert_to_base_verb(travel_verbs)
    counter1 = Counter(travel_verbs)
    travel_verb_dict = dict(counter1)


    verbs = []
    counts = []
    is_verbs_in_vn = []
    is_verbs_in_fn = []
    is_verbs_in_both = []
    is_verbs_not_in_both = []
    fn_frames = []
    is_synonyms_available = []
    synonyms = []
    is_any_syns_in_net = []
    syns_in_vn = []
    syns_in_fn = []

    for verb in travel_verb_dict:

        verbs.append(verb)
        counts.append(travel_verb_dict[verb])
        verb = verb.lower()
        fn_frame = []
        fn_results = []
        #print(fn_frame)
        syn_list = []
        syn_in_vn = []
        syn_not_in_vn = []
        syn_in_fn = []
        syn_not_in_fn = []

        is_any_syn_in_net = 0
        is_synonyms = 0

        is_in_vn = verbs_in_verbnet(verb)
        is_in_fn = verbs_in_framenet(verb)

        # print("Verb is in verbnet %s",is_in_vn)
        # print("Verb is in framenet %s", is_in_fn)

        is_not_in_both = 1 if not is_in_vn and not is_in_fn else 0
        is_in_both = 1 if is_in_vn and is_in_fn else 0

        # print("Verb is in both %s", is_in_both)
        # print("Verb is not in both %s", is_not_in_both)

        if is_in_fn:
            fn_results = fn.frames_by_lemma(verb)
            if fn_results:
                for item in fn_results:
                    name = item.name
                    fn_frame.append(name)



        if is_not_in_both:
            syn_list = find_synonyms(verb)

            is_synonyms = 1 if len(syn_list) > 0 else 0

            for syn in syn_list:
                is_syn_in_vn = verbs_in_verbnet(syn)
                is_syn_in_fn = verbs_in_framenet(syn)

                syn_in_vn.append(syn) if is_syn_in_vn else syn_not_in_vn.append(syn)
                syn_in_fn.append(syn) if is_syn_in_fn else syn_not_in_fn.append(syn)

                is_any_syn_in_net = is_any_syn_in_net + 1 if is_syn_in_vn or is_syn_in_fn else is_any_syn_in_net



        is_verbs_in_vn.append(is_in_vn)
        is_verbs_in_fn.append(is_in_fn)
        is_verbs_in_both.append(is_in_both)
        is_verbs_not_in_both.append(is_not_in_both)
        fn_frames.append((",".join(fn_frame)))
        is_synonyms_available.append(is_synonyms)
        synonyms.append((",").join(syn_list))
        is_any_syns_in_net.append(is_any_syn_in_net)
        syns_in_vn.append((",".join(syn_in_vn)))
        syns_in_fn.append((",".join(syn_in_fn)))


        # print("==========Syn list============")
        # print(syn_list)
        #
        # print("========Syn in VN========")
        # print(syn_in_vn)
        #
        # print("========Syn in FN========")
        # print(syn_in_fn)
        #
        # print(is_any_syn_in_net)
        #
        # print(fn_frames)
        # print("================================================================================")


    # print(verbs)
    # print(counts)
    # print(is_verbs_in_vn)
    # print(is_verbs_in_fn)
    # print(is_verbs_in_both)
    # print(is_verbs_not_in_both)
    # print(fn_frames)
    # print(is_synonyms_available)
    # print(synonyms)
    # print(is_any_syns_in_net)
    # print(syns_in_vn)
    # print(syns_in_fn)

    #final_list = list(zip(verbs,counts,is_verbs_in_vn,is_verbs_in_fn,is_verbs_in_both,is_verbs_not_in_both,fn_frames,is_synonyms_available,synonyms,is_any_syns_in_net,syn_in_vn,syn_in_fn))

    #print(data,final_list)

    df = pd.DataFrame(np.column_stack([verbs,counts,is_verbs_in_vn,is_verbs_in_fn,is_verbs_in_both,is_verbs_not_in_both,fn_frames,is_synonyms_available,synonyms,is_any_syns_in_net,syns_in_vn,syns_in_fn]), columns=['Verb','Count','Is in VerbNet','Is in FrameNet', 'Is in both','is not in both','FN Frames','Is Synonyms','Synonyms','Is any syn in Net','Synonyms in VN', 'Synonyms in FN'])


    return df

datapath = Path(__file__).resolve().parents[2]

#book = ['part1','part2','part3']
book = ['book']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-with-verbs.csv'.format(part,part) # Input individual index files
    data = pd.read_csv(readfile,sep='\t', encoding='latin1',error_bad_lines=False)

    outdata = travel_verb_instances(data)



    outdir = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction'.format(part)

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-verbs-analysis.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)


    #print(unique_travel_verbs)
