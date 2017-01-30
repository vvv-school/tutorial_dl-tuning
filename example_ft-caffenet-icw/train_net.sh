# set the directory where you have downloaded iCW and cloned the repos
LAB_DIR=/home/icub/giulia/Dropbox/SANDBOX/VVV17/vvv17-tutorials/
echo $LAB_DIR

########## TUTORIAL and EXERCISE
# set the directory of this tutorial
TUTORIAL_DIR=$LAB_DIR/tutorial_dl-tuning
echo $TUTORIAL_DIR
# set the name of the example/exercise
EX=example-ft-caffenet-icw
echo $EX

########## CAFFE stuff
# set the path to caffe executable
CAFFE_BIN=$Caffe_ROOT/build/tools/caffe
echo $CAFFE_BIN
# set the path to CaffeNet model (you should already have downloaded it)
WEIGHTS_FILE=$Caffe_ROOT/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel
echo $WEIGHTS_FILE

########## SCRIPTS
# set the path to the scripts (that you have just built)
COMPUTE_MEAN_BIN=$TUTORIAL_DIR/scripts/src/build/compute_mean_vvv17/compute_mean_vvv17
echo $COMPUTE_MEAN_BIN
CREATE_LMDB_BIN=$TUTORIAL_DIR/scripts/src/build/create_lmdb_vvv17/create_lmdb_vvv17
echo $CREATE_LMDB_BIN
PARSE_LOG_SH=$TUTORIAL_DIR/scripts/parse_caffe_log.sh
echo $PARSE_LOG_SH

########## SOLVER --> ARCHITECTURE and TEST
# set the path to the solver, which points to the train_val.prototxt
SOLVER_FILE=$TUTORIAL_DIR/$EX/solver.prototxt
echo $SOLVER_FILE
#
TEST_FILE=$TUTORIAL_DIR/$EX/test.prototxt
echo $TEST_FILE

########## IMAGES
IMAGES_DIR=$TOP_DIR/iCWU/
echo $IMAGES_DIR

########## TRAIN, VALIDATION and TEST sets: list of images
FILELIST_TRAIN=$TUTORIAL_DIR/$EX/images_lists/train.txt
echo $FILELIST_TRAIN
FILELIST_VAL=$TUTORIAL_DIR/$EX/images_lists/val.txt
echo $FILELIST_VAL
FILELIST_TESTS=$TUTORIAL_DIR/$EX/images_lists/test.txt
echo $FILELIST_TEST

########## TRAIN (plus mean image), VALIDATION and TEST databases for caffe
LMDB_TRAIN=$TUTORIAL_DIR/$EX/lmdb_train/
echo $LMDB_TRAIN
LMDB_VAL=$TUTORIAL_DIR/$EX/lmdb_val/
echo $LMDB_VAL
LMDB_TEST=$TUTORIAL_DIR/$EX/lmdb_test/
echo $LMDB_TEST
#
BINARYPROTO_MEAN=$TUTORIAL_DIR/$EX/mean.binaryproto
echo $BINARYPROTO_MEAN

########## create DATABASES
rm -rf $LMDB_TRAIN
$CREATE_LMDB_BIN --resize_width=256 --resize_height=256 --shuffle $IMAGES_DIR $FILELIST_TRAIN $LMDB_TRAIN
rm -rf $LMDB_VAL
$CREATE_LMDB_BIN --resize_width=256 --resize_height=256 --shuffle $IMAGES_DIR $FILELIST_VAL $LMDB_VAL
rm -rf $LMDB_TEST
$CREATE_LMDB_BIN --resize_width=256 --resize_height=256 --shuffle $IMAGES_DIR $FILELIST_VAL $LMDB_TEST
# 
$COMPUTE_MEAN_BIN $LMDB_TRAIN $BINARYPROTO_MEAN

########## TRAIN!
cd $TUTORIAL_DIR/$EX
$CAFFE_BIN train -solver $SOLVER_FILE -weights $WEIGHTS_FILE --log_dir=$LAB_DIR/$EX
$PARSE_LOG_SH $LAB_DIR/$EX/caffe.INFO caffe_INFO_train.txt caffe_INFO_val.txt

########## TEST!
$CAFFE_BIN test -model $TEST_FILE -weights $FINAL_MODEL -iterations $N_ITER

