# These snippets serve only as basic examples.
# Customization is a must.
# You can copy, paste, edit them in whatever way you want.
# Check the data files before designing your plots.

# Generate the necessary data files with 
# parse_caffe_log.sh before plotting.
# Example usage: 
#     ./parse_caffe_log.sh caffe.INFO
# Now you have caffeINFOtrain.txt and caffeINFOval.txt
#     gnuplot -e "iodir='directory/containing/caffe.INFO'" plot_log.gnuplot

# The fields present in the data files that are usually proper to plot along
# the y axis are test accuracy, test loss, training loss, and learning rate.
# Those should plot along the x axis are training iterations and seconds.
# Possible combinations:
# 1. Test accuracy vs. training iterations;
# 2. Test loss vs. training iterations;
# 3. Training accuracy vs. training iterations;
# 4. Training loss vs. training iterations;
# 5. Learning rate vs. training iterations;

###### fields in the data file caffeINFOtrain.txt are
###### iter acc loss
###### fields in the data file caffeINFOval.txt are
###### iter acc loss lr

reset
set terminal png
set output "caffeINFO_acc.png"
set style data points
set key right
set autoscale xy

set title "Accuracy vs. Training Iterations"
set xlabel "Training Iterations"
set ylabel "Accuracy"
plot iodir."/caffeINFOtrain.txt" using 1:2 title "train_acc" pt 7 ps 1, \
     iodir."/caffeINFOval.txt" using 1:2 title "val_acc" pt 7 ps 1,
set grid

reset
set terminal png
set output "caffeINFO_loss.png"
set style data points
set key right
set autoscale xy

set title "Loss vs. Training Iterations"
set xlabel "Training Iterations"
set ylabel "Loss"
plot iodir."/caffeINFOtrain.txt" using 1:3 title "train_loss" pt 7 ps 1, \
     iodir."/caffeINFOval.txt" using 1:3 title "val_loss" pt 7 ps 1,
set grid

reset
set terminal png
set output "caffeINFO_lr.png"
set style data points
set key right
set autoscale xy

set title "Learning Rate vs. Training Iterations"
set xlabel "Training Iterations"
set ylabel "Learning Rate"
plot iodir."/caffeINFOval.txt" using 1:4 title "lr" pt 7 ps 1
set grid
