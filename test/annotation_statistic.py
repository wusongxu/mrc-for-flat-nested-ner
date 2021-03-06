#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# author: xiaoy li
# statistic for entity


import os
import sys
import json
import sys

root_path = "/".join(os.path.realpath(__file__).split("/")[:-2])
print(root_path)
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from data_preprocess.file_utils import load_conll
from metric.flat_span_f1 import bmes_decode


def statistic_entity_for_sequence_labeling(input_file_path, ner_type="flat"):
    entity_statistic_dict = {}

    if ner_type == "flat":
        """
        Desc:
            input file should be : 
            王 B-PERSON
            小 M-PERSON
            明 E-PERSON
        """
        annotate_sentences = load_conll(input_file_path)
        for item in annotate_sentences:
            word_items, label_items = item
            sentence, tags = bmes_decode([[c, l] for c, l in zip(word_items, label_items)])
            # tags: [{'term': '上海', 'tag': 'GPE', 'begin': 0, 'end': 2}, {'term': '浦东', 'tag': 'GPE', 'begin': 2, 'end': 4}]
            for entity_item in tags:
                if entity_item.tag not in entity_statistic_dict.keys():
                    entity_statistic_dict[entity_item.tag] = 1
                else:
                    entity_statistic_dict[entity_item.tag] += 1
    elif ner_type == "nest":
        pass
    else:
        raise ValueError("Please notice your entity type do not exists !!")

    print("check the number of entities ")
    print("=*="*20)
    sum_of_entity = sum([entity_v for entity_v in entity_statistic_dict.values()])
    print("Total number of entity is : {}".format(sum_of_entity))
    for entity_k, entity_v in entity_statistic_dict.items():
        print("{} -> {}".format(entity_k, entity_v))

    return entity_statistic_dict



def statistic_entity_for_mrc_ner(input_file_path, ner_type="flat"):
    """
    Example in input_file_path should be:
    [{"context": "上 海 浦 东 开 发 与 法 制 建 设 同 步",
    "end_position": [],
    "entity_label": "PER",
    "impossible": true,
    "qas_id": "0.2",
    "query": "人名,包括虚构的人物",
    "span_position": [],
    "start_position": []} ]
    """
    entity_statistic_dict = {}

    with open(input_file_path, "r") as f:
        data_instances = json.load(f)
        for data_item in data_instances:
            if data_item["entity_label"] not in entity_statistic_dict.keys():
                entity_statistic_dict[data_item["entity_label"]] = 0
            entity_statistic_dict[data_item["entity_label"]] += len(data_item["span_position"])

    sum_of_entity = sum([entity_v for entity_v in entity_statistic_dict.values()])
    print("Total number of entity is : {}".format(sum_of_entity))
    for entity_k, entity_v in entity_statistic_dict.items():
        print("{} -> {}".format(entity_k, entity_v))

    return entity_statistic_dict


def run_stat_for_tagger_input(data_dir):
    print("*** *** *** *** "*15)
    print("TAGGER datasets -> ")
    print("*** *** *** *** "*15)
    # data_dir = "/data/nfsdata/nlp/datasets/sequence_labeling/CN_NER/OntoNote4NER"
    ner_type = "flat"  # choices are ["flat", "nest"]
    entity_statistic_dict_summary = dict()
    for data_type in ["train", "dev", "test"]:
        if ner_type == "flat":
            input_file_path = os.path.join(data_dir, data_type + ".char.bmes")
        elif ner_type == "nest":
            input_file_path = os.path.join(data_dir, )
        print("=*=" * 20)
        print("*** *** {} *** ***".format(data_type))
        tmp_entity_statistic_dict = statistic_entity_for_sequence_labeling(input_file_path, ner_type="flat")
        entity_statistic_dict_summary[data_type] = tmp_entity_statistic_dict

    return entity_statistic_dict_summary


def run_stat_for_mrc_input(data_dir):
    print("*** *** *** *** "*15)
    print("MRC-NER datasets -> ")
    print("*** *** *** *** "*15)
    # data_dir = "/data/xiaoya/nfs2data_xiaoya/dataset/mrc-ner/zh_ontonotes4"
    ner_type = "flat"  # choices are ["flat", "nest"]
    entity_statistic_dict_summary = dict()
    for data_type in ["train", "dev", "test"]:
        input_file_path = os.path.join(data_dir, "mrc-ner.{}".format(data_type))
        print("=*=" * 20)
        print("*** *** {} *** ***".format(data_type))
        tmp_entity_statistic_dict = statistic_entity_for_mrc_ner(input_file_path, ner_type="flat")
        entity_statistic_dict_summary[data_type] = tmp_entity_statistic_dict

    return entity_statistic_dict_summary



def main(tagger_data_dir, mrc_data_dir):
    tagger_statistic_summary = run_stat_for_tagger_input(tagger_data_dir)
    mrc_statistic_summary = run_stat_for_mrc_input(mrc_data_dir)
    # the number of entity should be the same for mrc-ner and sequence-tagger
    entity_type = [tmp_k for tmp_k in mrc_statistic_summary.keys()]
    for entity_item in entity_type:
        assert tagger_statistic_summary[entity_item] == mrc_statistic_summary[entity_item]



if __name__ == "__main__":
    #######################################################################################
    # zh_msra: "/data/xiaoya/nfs2data_xiaoya/data_repo/data-mrc_ner/flat/msra_zh"
    # zh_ontonotes: "/data/nfsdata/nlp/datasets/sequence_labeling/CN_NER/OntoNote4NER"
    #######################################################################################
    # zh_msra: "/data/xiaoya/work/datasets/mrc_ner/zh_msra"
    # zh_ontonotes: "/data/xiaoya/work/datasets/mrc_ner/zh_onto4"
    tagger_data_dir = sys.argv[1]
    mrc_data_dir = sys.argv[2]
    main(tagger_data_dir, mrc_data_dir)
    # python3 annotation_statistic.py <path_to_tagger_data_dir> <path_to_mrc_data_dir>

