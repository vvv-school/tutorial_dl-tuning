# Fine-tuning a deep CNN with Caffe

Contents:

* [Get ready for the afternoon](#get-ready-for-the_afternoon)
* [Get ready for this tutorial](#get-ready-for-this-tutorial)
* [Start the tutorial: run the tester](#start-the-tutorial-run-the-tester)
* [Complete the tutorial: run fine-tuning](#complete-the-tutorial-run-fine-tuning)
* [Bonus question](#bonus-question)

## Get ready for the afternoon

#### Check the RAM of the Virtual Machine (VM)

The deep learning labs are tested on the provided VM with the RAM set to 4096 MB (and 2 CPUs). Increase the RAM of your VM to this value in order to run the exercises (also 3GB may be sufficient, but if you have problems with this requirement let us know and we will find a solution!).

#### Check the data

You should have already extracted the iCW (iCubWorld) dataset, otherwise do it now:

```sh
$ cd $ROBOT_CODE/datasets
$ tar -zxvf iCW-vvv18.tar.gz
```
NOTE: if you want to move the dataset in another folder, move the archive and then extract it, since it contains many images!

#### Create a folder for the deep learning repositories that you will clone

Create a folder where you will clone all the tutorials and assignments of this hands on session: in all the code provided, we will suppose this is:

```sh
$ mkdir $ROBOT_CODE/dl-lab
```
We encourage to create the same if you use the VM (but you will be able to change it the code that will be used).

#### Get missing Python packages

You should already have all required dependencies for running the labs but these ones, which you must install now:

```
$ sudo apt install python-pip
$ pip install easydict
```

## Get ready for this tutorial

#### Get the code

Clone this repository inside `$LAB_DIR`:

```sh
$ cd $ROBOT_CODE/dl-lab
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
3. check that `Caffe_DIR` is set to your `caffe/build/install` directory (on the VM setup this is `/home/icub/robot-code/caffe/build/install`)
4. check that `OpenCV_DIR` points to an `OpenCV` installation (on the VM this is `opt/ros/kinetic/share/OpenCV-3.3.1`)

## Start the tutorial: run the tester

Since the fine-tuning that we are going to run will take some minutes to complete (10 to 15 minutes, depending on the machine), we first ensure that the full train/test pipeline works on your system by running this ''tester''. This is exactly like the fine-tuning we are going to launch, but runs only for 2 epochs and test the model on a couple of images.

#### Generate the lists of train/val/test images

Open the `create_imagesets.py` script with a text editor, e.g.:

```sh
$ cd $ROBOT_CODE/dl-lab/tutorial_dl-tuning
$ gedit create_imagesets.py
```

This script uses the configuration file `imageset_config.yml` (located inside `id_2objects`) to select train/val/test images from the `iCW` dataset and create three corresponding files, containing the list of the selected images.

Look at lines 25-29 and check that the paths are correct (they should, if you are using the VM and followed instructions so far).

Run the script in the following way:

```sh
$ cd $ROBOT_CODE/dl-lab/tutorial_dl-tuning
$ ./create_imagesets.py
```

Once done, check that a folder named `images_lists` inside `id_2objects` has been created and contains the `train.txt`, `val.txt`, `test.txt` and `labels.txt`.

[**NOTE**] Look at the content of `imageset_config.yml`: can you understand how we are defining the train/val/test sets? Can you understand whether the generated image lists are correct, based on the configuration file?

#### Configure (and understand) the script

Open the `train_and_test_net_tester.sh` script with a text editor, e.g.:

```sh
$ cd $ROBOT_CODE/dl-lab/tutorial_dl-tuning/id_2objects
$ gedit train_and_test_net_tester.sh
```

Look at the file. Can you understand what the different sections are doing?

While reading the file, check also that the paths to the code and data are correct for your system. Specifically:

1. `LAB_DIR` points to the directory `$ROBOT_CODE/dl-lab`
2. `IMAGES_DIR` points to the directory of the `iCW` dataset. Be sure that this path ends with a `/` included, e.g. `home/icub/robot-code/datasets/iCW/`.
3. The `Caffe_ROOT` env variable is used to locate `caffe` (in the VM it is defined in `~/.bashrc-dev`)
4. At line 114, check that the pre-trained model `bvlc_reference_caffenet.caffemodel` is correctly located

The rest of the paths should be ok if the above are correct.

[**NOTE (IMPORTANT for the ASSIGNMENT)**] Look at the `train_val.prototxt`, `deploy.prototxt` and `solver.prototxt` that are pointed by this file. Can you understand the comments that we added to explain the relevant parts of these files?

#### Run the script

```sh
$ cd $ROBOT_CODE/dl-lab/tutorial_dl-tuning/id_2objects
$ ./train_and_test_net_tester.sh
```

Now look at the logging messages. The (tester) training should take less than 5 minutes to complete and you should be able to see something like this:

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

Then you should also be able to see some images displayed one after the other. If you read at the very end the message `***** Done! *****`, then you are ready for fine-tuning networks on your machine! Let us know if something does not work.

## Complete the tutorial: run fine-tuning

This is the actual training that we are going to run. The procedure is the same that you followed to run the ''tester'' script. This time we do not need to generate the lists of train/val/test images since we are going to use the same. Therefore:

Open the `train_and_test_net.sh` script with a text editor:

```sh
$ cd $ROBOT_CODE/dl-lab/tutorial_dl-tuning/id_2objects
$ gedit train_and_test_net.sh
```

and check that everything is set up correctly. All paths are the same as for `train_and_test_net_tester.sh` except that now the training protocol is not `all-0-tester` but `all-3` (line 96).

Run the script like the previous one:

```sh
$ cd $ROBOT_CODE/dl-lab/tutorial_dl-tuning/id_2objects
$ ./train_and_test_net.sh
```

Once the script finishes, look at the produced files:

```sh
$ cd $ROBOT_CODE/dl-lab/tutorial_dl-tuning/id_2objects/
$ ls
```
The `lmdb_train` and `lmdb_val` folder contain the databases of the train and validation images, while the `mean.binaryproto` is the mean image of the training set.

Look now inside the protocol folder:

```sh
$ cd $ROBOT_CODE/dl-lab/tutorial_dl-tuning/id_2objects/all-3
$ ls
```
Here you can find:

1. `final.caffemodel`: **these are the weights of the fine-tuned model!**
2. `caffeINFOtrain.txt` and `caffeINFOval.txt`, together with `caffeINFO_loss.png`, `caffeINFO_acc.png` and `caffeINFO_lr.png` are the result of parsing the output log file produced by Caffe (`caffe.INFO`) and contain, respectively in the form of tables or pictures, the train/validation performances achieved during training. Note that this information is produced by Caffe more or less frequently depending on the `display` parameter set in the `solver.prototxt`.
2. `test_acc.txt`: **accuracy achieved by testing the trained model on the test set** (computed based on the predictions that were also displayed)

## Bonus question

Consider the training protocols that we adopted in the ''tester'' and then in the actual fine-tuning of the network, by comparing the `solver.prototxt` and the `train_val.prototxt` files used in the two cases (folders `all-0-tester` and `all-3`).

Apart from the different number of epochs (2 in the tester and 4 in the other case), which is the other difference between the two?

[**HELP**] Look at the learning rates of the different layers of the network (`base_lr` parameter in the `solver.prototxt` and `lr_mult` layer parameters in the `train_val.prototxt`): How are these set in the two cases? Why do you think in the tester we kept all layers frozen except the very last one, while in the fine-tuning we instead adapted the weights of all layers?
