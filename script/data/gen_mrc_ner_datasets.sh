#!/usr/bin/env bash
# -*- coding: utf-8 -*-


# author: xiaoy li
# description:
# generate mrc-ner datasets for experiments


REPO_PATH=/data/xiaoya/work/mrc-for-flat-nested-ner
export PYTHONPATH="$PYTHONPATH:$REPO_PATH"

# data files
# en_ace2004, en_ace2005, en_conll03, en_ontonotes5, en_genia, zh_ontonotes4, zh_msra
DATASET_SIGN=$1
ENTITY_SIGN=$2
QUERY_SIGN=$3
SOURCE_DATA_DIR=$4
TARGET_DATA_DIR=$5

mkdir -p $TARGET_DATA_DIR

for DATA_TYPE in train dev test
do
  if [[ $ENTITY_SIGN == "flat" ]]; then
    SOURCE_INPUT_FILE=$SOURCE_DATA_DIR/${DATA_TYPE}.char.bmes
  elif [[ $ENTITY_SIGN == "nested" ]]; then
    SOURCE_INPUT_FILE=$SOURCE_DATA_DIR/${DATA_TYPE}.ner.json
  else
    echo "unkown type of entity."
  fi

  TARGET_OUTPUT_FILE=$TARGET_DATA_DIR/mrc-ner.${DATA_TYPE}

  python3 $REPO_PATH/run/generate_mrc_datasets_from_seq_labeling.py \
  --path_to_source_data_file $SOURCE_INPUT_FILE \
  --path_to_save_mrc_data_file $TARGET_OUTPUT_FILE \
  --dataset_name $DATASET_SIGN \
  --entity_sign $ENTITY_SIGN \
  --query_sign $QUERY_SIGN
done