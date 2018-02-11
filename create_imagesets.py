#!/usr/bin/python

# Example script to generate a recognition task

# This script uses a configuration file
# (id_2objects/imageset_config.yml)
# to create training, validation and test sets
# by selecting image sequences from the iCW dataset
# it generates corresponding train.txt, val.txt and test.txt
# (id_2objects/images_lists)

import os
import os.path as osp
import sys
import pprint


def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)


if __name__ == '__main__':

    EXERCISE = "id_2objects"

    IMAGES_DIR = "/home/icub/robot-code/datasets/iCW"

    TUTORIAL_DIR = "/home/icub/robot-code/dl-lab/tutorial_dl-tuning"

    ##################################################################

    IMAGESET_FILE = osp.join(TUTORIAL_DIR, EXERCISE, "imageset_config.yml")

    add_path(osp.join(TUTORIAL_DIR, 'scripts/python_utils'))

    from create_train_val_test_sets import create_train_val_test_sets
    from imageset_config import cfg, cfg_from_file

    cfg_from_file(IMAGESET_FILE)

    print('Using image sets:')
    pprint.pprint(cfg)

    # Set the directory where you want to generate the
    # train.txt, val.txt, test.txt, labels.txt files
    OUTPUT_DIR = os.path.join(TUTORIAL_DIR, EXERCISE, "images_lists")

    create_train_val_test_sets(IMAGES_DIR, cfg, OUTPUT_DIR)
