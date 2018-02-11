#!/usr/bin/python
import os
import itertools
from itertools import groupby
import numpy as np
import math


def create_train_val_test_sets(IMAGES_DIR, cfg, OUTPUT_DIR):

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if cfg.EXP_KIND[:2] == 'ca':
        exp_id = False
    elif cfg.EXP_KIND[:2] == 'id':
        exp_id = True
    else:
        raise Exception('Unsupported exp_kind in the question config file!')

    if exp_id:
        lbl_idx = 1
    else:
        lbl_idx = 0

    if not exp_id:
        Ymap = dict([(val, idx) for idx, val in enumerate(cfg.CATEGORIES)])
        with open(os.path.join(OUTPUT_DIR, 'labels.txt'), 'w') as f:
            for val in cfg.CATEGORIES:
                f.write("%s %d\n" % (val, Ymap[val]))
    else:
        obj_names = [item for item in cfg.CATEGORIES for i in range(len(cfg.OBJ_PER_CAT.TRAIN))]
        tmp = [item for i in range(len(cfg.CATEGORIES)) for item in cfg.OBJ_PER_CAT.TRAIN ]
        obj_names = ["{}{}".format(a_, b_) for a_, b_ in zip(obj_names, tmp)]
        Ymap = dict([ (val, idx) for idx, val in enumerate(obj_names) ])
        with open(os.path.join(OUTPUT_DIR, 'labels.txt'), 'w') as f:
            for val in obj_names:
                f.write("%s %d\n" % (val, Ymap[val]))

    #registry = [val for sublist in [[os.path.relpath(os.path.join(i[0], j), IMAGES_DIR) for j in i[2]] for i in os.walk(IMAGES_DIR)] for val in sublist]
    #registry_nofilename = [os.path.dirname(item) for item in registry if os.path.splitext(item)[1] == '.jpg']
    #registry = [item for item in registry if os.path.splitext(item)[1] == '.jpg']

    registry = [os.path.join(root, name)
                 for root, dirs, files in os.walk(IMAGES_DIR)
                    for name in sorted([os.path.splitext(item)[0] for item in files if item.endswith(".jpg")], key=int)]
    registry_nofilename = [os.path.relpath(os.path.dirname(item), IMAGES_DIR) for item in registry]
    registry = [os.path.relpath(item, IMAGES_DIR)+".jpg" for item in registry]

    # TRAINING set

    categories = cfg.CATEGORIES
    instances = cfg.OBJ_PER_CAT.TRAIN
    transformations = cfg.TRANSF_PER_OBJ.TRAIN
    days = cfg.DAY_PER_TRANSF.TRAIN
    if len(days) == 2:
        days = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8']
    elif days[0]=='1':
        days = ['day1', 'day3', 'day5', 'day7']
    else:
        days = ['day2', 'day4', 'day6', 'day8']
    cameras = ['left']

    selected_branches = itertools.product(categories, instances, transformations, days, cameras)
    selected_branches = list(selected_branches)
    selected_branches = [os.path.join(item[0], item[0]+item[1], os.path.join(*item[2:])) for item in selected_branches]

    registry_nofilename_train = [item for item in registry_nofilename if item in selected_branches]
    registry_train = [item for item in registry if os.path.dirname(item) in selected_branches]

    Nframes = [len(list(group)) for key, group in groupby(registry_nofilename_train)]
    Ndirs = len(Nframes)
    startend = [0] * (Ndirs + 1)
    startend[1:] = np.cumsum(Nframes)

    if cfg.LIMIT_FRAMES.TRAIN.ACTIVE:
        tokeep_indices = []
        for ii in xrange(0, Ndirs):
            tmp = np.random.permutation(Nframes[ii]) + startend[ii]
            tmp = tmp[:min(Nframes[ii], cfg.LIMIT_FRAMES.TRAIN.MAX)]
            tokeep_indices = np.concatenate((tokeep_indices, tmp), axis=0)
        tokeep_indices = tokeep_indices.astype(int)
        registry_train = [registry_train[i] for i in tokeep_indices]

    if cfg.DIVIDE_TRAINVAL_SET.ACTIVE:

        print 'Going to create validation set by splitting the training set...'

        if cfg.DIVIDE_TRAINVAL_SET.VALIDATION_SPLIT == 'step':
            validation_step = 1 / cfg.DIVIDE_TRAINVAL_SET.VALIDATION_PERC
            registry_val = registry_train[::int(validation_step)]
            del registry_train[::int(validation_step)]
        elif cfg.DIVIDE_TRAINVAL_SET.VALIDATION_SPLIT == 'random':
            fidxs = np.random.permutation(len(registry_train))
            fidxs = fidxs.astype(int)
            split_idx = int(math.floor(cfg.DIVIDE_TRAINVAL_SET.VALIDATION_PERC * len(registry_train)))
            registry_val = [registry_train[i] for i in fidxs[:split_idx]]
            registry_train = [registry_train[i] for i in fidxs[split_idx:]]
        else:
            raise Exception('Wrong validation_split in config file!')

    Ytrain = [Ymap[item.split(os.sep)[lbl_idx]] for item in registry_train]
    if cfg.DIVIDE_TRAINVAL_SET.ACTIVE:
        Yval = [Ymap[item.split(os.sep)[lbl_idx]] for item in registry_val]

    with open(os.path.join(OUTPUT_DIR, 'train.txt'), 'w') as f:
        for line in xrange(len(registry_train)):
            f.write("%s %d\n" % (registry_train[line], Ytrain[line]))

    if cfg.DIVIDE_TRAINVAL_SET.ACTIVE:
        with open(os.path.join(OUTPUT_DIR, 'val.txt'), 'w') as f:
            for line in xrange(len(registry_val)):
                f.write("%s %d\n" % (registry_val[line], Yval[line]))

    # VALIDATION set

    if not cfg.DIVIDE_TRAINVAL_SET.ACTIVE:

        categories = cfg.CATEGORIES
        instances = cfg.OBJ_PER_CAT.VAL
        transformations = cfg.TRANSF_PER_OBJ.VAL
        days = cfg.DAY_PER_TRANSF.VAL
        if len(days) == 2:
            days = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8']
        elif days[0] == '1':
            days = ['day1', 'day3', 'day5', 'day7']
        else:
            days = ['day2', 'day4', 'day6', 'day8']
        cameras = ['left']

        selected_branches = itertools.product(categories, instances, transformations, days, cameras)
        selected_branches = list(selected_branches)
        selected_branches = [os.path.join(item[0], item[0]+item[1], os.path.join(*item[2:])) for item in selected_branches]

        registry_nofilename_val = [item for item in registry_nofilename if item in selected_branches]
        registry_val = [item for item in registry if os.path.dirname(item) in selected_branches]

        Nframes = [len(list(group)) for key, group in groupby(registry_nofilename_val)]
        Ndirs = len(Nframes)
        startend = [0] * (Ndirs + 1)
        startend[1:] = np.cumsum(Nframes)

        if cfg.LIMIT_FRAMES.VAL.ACTIVE:
            tokeep_indices = []
            for ii in xrange(0, Ndirs):
                tmp = np.random.permutation(Nframes[ii]) + startend[ii]
                tmp = tmp[:min(Nframes[ii], cfg.LIMIT_FRAMES.VAL.MAX)]
                tokeep_indices = np.concatenate((tokeep_indices, tmp), axis=0)
            tokeep_indices = tokeep_indices.astype(int)
            registry_val = [registry_val[i] for i in tokeep_indices]

        Yval = [Ymap[item.split(os.sep)[lbl_idx]] for item in registry_val]

        with open(os.path.join(OUTPUT_DIR, 'val.txt'), 'w') as f:
            for line in xrange(len(registry_val)):
                f.write("%s %d\n" % (registry_val[line], Yval[line]))

    # TEST set

    categories = cfg.CATEGORIES
    instances = cfg.OBJ_PER_CAT.TEST
    transformations = cfg.TRANSF_PER_OBJ.TEST
    days = cfg.DAY_PER_TRANSF.TEST
    if len(days) == 2:
        days = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8']
    elif days[0] == '1':
        days = ['day1', 'day3', 'day5', 'day7']
    else:
        days = ['day2', 'day4', 'day6', 'day8']
    cameras = ['left']

    selected_branches = itertools.product(categories, instances, transformations, days, cameras)
    selected_branches = list(selected_branches)
    selected_branches = [os.path.join(item[0], item[0] + item[1], os.path.join(*item[2:])) for item in
                         selected_branches]

    registry_nofilename_test = [item for item in registry_nofilename if item in selected_branches]
    registry_test = [item for item in registry if os.path.dirname(item) in selected_branches]

    Nframes = [len(list(group)) for key, group in groupby(registry_nofilename_test)]
    Ndirs = len(Nframes)
    startend = [0] * (Ndirs + 1)
    startend[1:] = np.cumsum(Nframes)

    if cfg.LIMIT_FRAMES.TEST.ACTIVE:
        tokeep_indices = []
        for ii in xrange(0, Ndirs):
            if cfg.LIMIT_FRAMES.TEST.STARTING_IMG < 0:
                starting_idx = max(0, int(np.random.uniform(0, 1) * (Nframes[ii] - cfg.LIMIT_FRAMES.TEST.MAX)))
            else:
                starting_idx = max(0, min(cfg.LIMIT_FRAMES.TEST.STARTING_IMG, Nframes[ii] - cfg.LIMIT_FRAMES.TEST.MAX))
            tmp = range(starting_idx+ startend[ii], min(Nframes[ii]+ startend[ii], starting_idx + cfg.LIMIT_FRAMES.TEST.MAX+ startend[ii]))
            tokeep_indices = np.concatenate((tokeep_indices, tmp), axis=0)
        tokeep_indices = tokeep_indices.astype(int)
        registry_test = [registry_test[i] for i in tokeep_indices]

    Ytest = [Ymap[item.split(os.sep)[lbl_idx]] for item in registry_test]

    with open(os.path.join(OUTPUT_DIR, 'test.txt'), 'w') as f:
        for line in xrange(len(registry_test)):
            f.write("%s %d\n" % (registry_test[line], Ytest[line]))
