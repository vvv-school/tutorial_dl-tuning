
import os
import os.path as osp
import numpy as np
from easydict import EasyDict as edict

__C = edict()
cfg = __C


# Categories involved in the problem:
# it must be always a cell array, also with a single element
# e.g. setlist.categories = {'mug'}
# --> look in the 'iCW' folder to check the available categories
# (in this case: 'mug', 'remote', and 'sodabottle')
__C.CATEGORIES = ["cat1", "cat2"]

# Experiment kind:
# either 'cat' (obj. categorization) or 'id' (obj. identification)
__C.EXP_KIND = "cat OR id"

# At each level of the 'iCW' hierarchy, we must define
# one train, one validation and one test set:
# e.g. in this task we want to learn to discriminate
# between 10 objects (5 mugs and 5 remotes)
# by training on 4 transformation sequences per object
# and testing the system on the mixed sequence

# Objects per category:
# if the experiment is identification, the three sets will be equal
# (like in this example)
# in categorization, instead, usually the system is trained
# on some object instances per category and tested on others
# (and usually one or two instances are kept for validation)
# --> look in the 'iCW' folder to check
# the number of objects per category available (in this case: 10)
__C.OBJ_PER_CAT = edict()
__C.OBJ_PER_CAT.TRAIN = ["from 1 to 10 available"]
__C.OBJ_PER_CAT.VAL = ["from 1 to 10 available"]
__C.OBJ_PER_CAT.TEST = ["from 1 to 10 available"]

# Transformations per object:
# --> look in the 'iCW' folder to check
# the transformations per object available
__C.TRANSF_PER_OBJ = edict()
__C.TRANSF_PER_OBJ.TRAIN = ["available: ROT2D, ROT3D, SCALE, TRANSL, MIX"]
__C.TRANSF_PER_OBJ.VAL = ["available: ROT2D, ROT3D, SCALE, TRANSL, MIX"]
__C.TRANSF_PER_OBJ.TEST = ["available: ROT2D, ROT3D, SCALE, TRANSL, MIX"]

# Days per transformation:
# there are two sequences, acquired in different days, available
# you can choose to train on the first one ["1"], or the second one ["2"]
# or both ["1", "2"] (the same for testing)
# here we chose day 1
__C.DAY_PER_TRANSF = edict()
__C.DAY_PER_TRANSF.TRAIN = ["1 and/or 2 available"]
__C.DAY_PER_TRANSF.VAL = ["1 and/or 2 available"]
__C.DAY_PER_TRANSF.TEST = ["1 and/or 2 available"]

# Whether to put a max limit on the #frames
# to be sampled from each img sequence
__C.LIMIT_FRAMES = edict()
__C.LIMIT_FRAMES.TRAIN = edict()
__C.LIMIT_FRAMES.TRAIN.ACTIVE = True
__C.LIMIT_FRAMES.TRAIN.MAX = -1
__C.LIMIT_FRAMES.VAL = edict()
__C.LIMIT_FRAMES.VAL.ACTIVE = True
__C.LIMIT_FRAMES.VAL.MAX = -1
  # differently from training and validation,
  # the test frames are extracted as contiguous sequences
  # (like a short video on which you test the system):
  # you can start the sequence
  # either from a random or arbitrary frame:
  # in the first case, TEST_STARTING_IMG: -1
  # in the second case, TEST_STARTING_IMG: <number>
  # such that TEST_STARTING_IMG + MAX < ~70 ]
__C.LIMIT_FRAMES.TEST = edict()
__C.LIMIT_FRAMES.TEST.ACTIVE = True
__C.LIMIT_FRAMES.TEST.MAX = -1
__C.LIMIT_FRAMES.TEST.STARTING_IMG = 1000

# Whether to use a fraction of the training set for validation:
# this flag must be set to true in case you defined equal
# training and validation sets (like in this example,
# --> pay attention to disable the flag when you specify
# training and validation sets as different sets
__C.DIVIDE_TRAINVAL_SET = edict()
__C.DIVIDE_TRAINVAL_SET.ACTIVE = True
  # depending on whether we want to sample
  # validation frames at constant step or randomly
  # this field can be either "random" or "step"
__C.DIVIDE_TRAINVAL_SET.VALIDATION_SPLIT = "random or step available"
  # the validation fraction will be in (0,1)
  # NOTE: if validation_split is "step" then
  # the sampling step is computed as 1/VALIDATION_PERC
__C.DIVIDE_TRAINVAL_SET.VALIDATION_PERC = 0.0


def _merge_a_into_b(a, b):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    if type(a) is not edict:
        return

    for k, v in a.iteritems():
        # a must specify keys that are in b
        if not b.has_key(k):
            raise KeyError('{} is not a valid config key'.format(k))

        # the types must match, too
        old_type = type(b[k])
        if old_type is not type(v):
            if isinstance(b[k], np.ndarray):
                v = np.array(v, dtype=b[k].dtype)
            else:
                raise ValueError(('Type mismatch ({} vs. {}) '
                                'for config key: {}').format(type(b[k]),
                                                            type(v), k))

        # recursively merge dicts
        if type(v) is edict:
            try:
                _merge_a_into_b(a[k], b[k])
            except:
                print('Error under config key: {}'.format(k))
                raise
        else:
            b[k] = v
            #setattr(b, k, v)


def cfg_from_file(filename):
    """Load a config file and merge it into the default options."""
    import yaml
    with open(filename, 'r') as f:
        yaml_cfg = edict(yaml.load(f))

    _merge_a_into_b(yaml_cfg, __C)


