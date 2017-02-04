# Fine-tuning deep CNNs with Caffe

## Get ready for the afternoon

#### Increase the RAM of the Virtual Machine

The Deep Learning labs are tested on the provided VM, with the RAM increased to 2048 MB. Increase the RAM of your VM at least to this value in order to run the exercises. Let us know if you have problems with this requirement.

#### Get the data

Download the iCubWorld (iCW) dataset from this [link](https://data.mendeley.com/datasets/g7vvyk6gds/1/files/ffe5bac4-1ded-4bfd-a595-ef5393e69304/iCW.tar.gz?dl=1) in a folder of your choice (in the course labs we will suppose `/home/icub/robot-code/datasets`). Extract the archive in the same folder:

```sh
$ cd $ROBOT_CODE/datasets
$ wget https://data.mendeley.com/datasets/g7vvyk6gds/1/files/ffe5bac4-1ded-4bfd-a595-ef5393e69304/iCW.tar.gz
$ tar -zxvf iCW.tar.gz
```
NOTE: if you want to move the dataset in another folder, move the archive and then extract it, since it contains many images.

#### Create a folder for the Deep Learning course

Create a folder of your choice where you will clone all the tutorials and assignments of the Deep Learning course: we will suppose this is

```sh
$ LAB_DIR=/home/icub/vvv17_deep-learning
$ mkdir $LAB_DIR
```
You can create the same if you use the VM, otherwise you will be able to change it the code that will be used.

#### Get gnuplot and/or MATLAB

Since you are supposed to have MATLAB for other courses (e.g. Machine Learning), in these labs we will provide some MATLAB scripts for plotting results and generating some data.
While being useful, MATLAB is not mandatory for completing the labs.

We provide also an equivalent `gnuplot` script to plot results, which can be used in place of MATLAB. You can install `gnuplot` by doing:
```
$ sudo apt-get install gnuplot
```

Still, if you have neither MATLAB nor `gnuplot`, you will be able to complete the labs.

## Get ready for first tutorial

#### Get the code

Clone this repository inside `$LAB_DIR`:

```sh
$ cd $LAB_DIR
$ git clone https://www.github.com/vvv-school/tutorial_dl-tuning.git
```

#### Compile the code

Compile the scripts that are provided with the repository:

```sh
$ cd tutorial_dl-tuning/scripts/src
$ mkdir build
$ cd build
$ ccmake ../
$ make
```

NOTES: 

1. you do not have to install this code, `make` is sufficient
2. check that `CPU_ONLY=ON` and `USE_CUDNN=OFF` if you have not built `caffe` for the GPU (which is the case if you are using the provided VM)
3. check that `Caffe_DIR` is set to your `caffe` `build` directory (on the VM setup this is `/home/icub/robot-code/caffe/build`)
4. check that `OpenCV_DIR` points to an `OpenCV` installation (on the VM this is `opt/ros/kinetic/share/OpenCV-3.1.0-dev`) 

#### Configure the fine-tuning script to run on your laptop:

Open the `train_and_test_net_tester.sh` script with a text editor, e.g.:

```sh
$ cd $LAB_DIR/tutorial_dl-tuning/id_2objects_caffenet
$ gedit train_and_test_net_tester.sh
```

Check that the paths to the code and data are correct for your system. Specifically:

1. `LAB_DIR` must point to the directory that you created above
2. `IMAGES_DIR` must point to the directory containing the `iCW` dataset that you downloaded. Be sure that this path ends with a `/` included, e.g. `home/icub/robot-code/datasets/iCW/`
3. the environment variable `Caffe_ROOT` is used: check that you have defined this variable in your system to point to the directory where you have cloned `caffe` (in the VM setup the variable has already been defined in `~/.bashrc-dev`)
4. at line 24 the file `bvlc_reference_caffenet.caffemodel` is used: check that after installing `caffe	` you downloaded it, as explained in the provided instructions [here](https://github.com/vvv-school/vvv-school.github.io/blob/master/instructions/how-to-prepare-your-system.md#install-caffe)
5. the rest of the paths should be ok, if the above variables are correct

#### Run the fine-tuning script

```sh
$ cd $LAB_DIR/tutorial_dl-tuning/id_2objects_caffenet
$ ./train_and_test_net_tester.sh
```

Now look at the logging messages. The (dummy) training should take less than 5 minutes to complete and you should be able to see something like this:

```sh
I0203 22:10:30.673301  3769 caffe.cpp:251] Starting Optimization
I0203 22:10:30.675755  3769 solver.cpp:279] Solving CaffeNet_iCubWorld
I0203 22:10:30.675798  3769 solver.cpp:280] Learning Rate Policy: poly
I0203 22:10:30.772714  3769 solver.cpp:337] Iteration 0, Testing net (#0)
I0203 22:10:37.816495  3769 solver.cpp:404]     Test net output #0: accuracy = 0.526042
I0203 22:10:37.818120  3769 solver.cpp:404]     Test net output #1: loss = 0.722712 (* 1 = 0.722712 loss)
I0203 22:10:39.182849  3769 solver.cpp:228] Iteration 0, loss = 1.06601
I0203 22:10:39.182965  3769 solver.cpp:244]     Train net output #0: accuracy = 0.34375
I0203 22:10:39.183007  3769 solver.cpp:244]     Train net output #1: loss = 1.06601 (* 1 = 1.06601 loss)
I0203 22:10:39.183043  3769 sgd_solver.cpp:106] Iteration 0, lr = 0.01
I0203 22:11:11.826850  3769 solver.cpp:337] Iteration 24, Testing net (#0)
I0203 22:11:19.271281  3769 solver.cpp:404]     Test net output #0: accuracy = 1
I0203 22:11:19.271347  3769 solver.cpp:404]     Test net output #1: loss = 6.33019e-06 (* 1 = 6.33019e-06 loss)
I0203 22:11:20.578449  3769 solver.cpp:228] Iteration 24, loss = 0.482432
I0203 22:11:20.578583  3769 solver.cpp:244]     Train net output #0: accuracy = 0.96875
I0203 22:11:20.578625  3769 solver.cpp:244]     Train net output #1: loss = 0.482432 (* 1 = 0.482432 loss)
I0203 22:11:20.578662  3769 sgd_solver.cpp:106] Iteration 24, lr = 0.00707107
I0203 22:11:52.532905  3769 solver.cpp:454] Snapshotting to binary proto file icw_iter_48.caffemodel
I0203 22:11:54.411671  3769 sgd_solver.cpp:273] Snapshotting solver state to binary proto file icw_iter_48.solverstate
I0203 22:11:56.336150  3769 solver.cpp:317] Iteration 48, loss = 0.687042
I0203 22:11:56.338747  3769 solver.cpp:337] Iteration 48, Testing net (#0)
I0203 22:12:03.345867  3769 solver.cpp:404]     Test net output #0: accuracy = 0.994792
I0203 22:12:03.345939  3769 solver.cpp:404]     Test net output #1: loss = 0.0168321 (* 1 = 0.0168321 loss)
I0203 22:12:03.345948  3769 solver.cpp:322] Optimization Done.
I0203 22:12:03.345954  3769 caffe.cpp:254] Optimization Done.
```

Then you should also be able to see 6 images displayed one after the other. If you read at the very end the message `***** Done! *****` then you are ready for the labs! Let us know if something does not work.
