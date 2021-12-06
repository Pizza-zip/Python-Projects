#################################################################
#  Code that allows to get arduino data from the serial monitor #
#  and to visualize this data live using the "drawnow" library  #
#################################################################

import serial  # will enable us to start the communication with the Arduino software
from drawnow import drawnow, plt  # import necessary methods from drawnow

# create an object and opens the port, in this case COM3. 
# note that the baudrate, 9600 in our case must be specified.
arduino_serial = serial.Serial("COM4", 9600) # adjust com number as necessary

# create empty lists to capture all temperature values with respect to time
degree = []
LDR = []

# turn on interactive mode for data visualization
plt.ion()

# this variable initializes a counter that will allow us to delete the 31st point (of course in reverse order) on
# both the temperature and the time data so that we are always visualizing the last 30 data points. In Pycharm,
# a snapshot is taken for the graphs of the previous data as the plot shifts to accommodate for newer data. This is
# good if we only want to focus on the most recent data for our project and takes less resources which means
# lower possibility for 'overload' or the likes of it. Furthermore it will allow the graph to not be too squished
# as all data are being plotted on the same graph. This can be deleted simply by deleting the variable below and
# the last 4 lines in the while loop.

count = 0

# In order to know which column is which
print("degree, LDR")

# define a function that will plot the data to be visualized.
def plot_live_data():
    plt.title("Live Streaming Data - Godin rules!")
    plt.grid(True)
    plt.xlabel("Degree (o)")
    plt.ylabel("LDR (OHMS)")
    plt.plot(degree, LDR)

# create an infinite while loop to continuously fetch the data from the arduino serial monitor
while True:

    # we use the readline() method to read the data line by line but it is in byte mode
    # so we need to decode it using utf-8 so that our data can be represented as a string
    arduino_string_data = arduino_serial.readline().decode("utf-8")

    # our data is now in this form using the split() method:
    # [time_value, temp_value] but these values are not numbers yet
    dataArray = arduino_string_data.split(",")

    # convert both time and temperature values as floats
    # for them to be interpreted as numbers so that the plot can be made
    # indexing is used to get each individual data in their respective variables
    d = float(dataArray[0])
    l = float(dataArray[1])

    # print the data to see what the current values are and look at your graph to
    # visualize the effect. Also for potential debugging purposes.
    print(f"{degree}, {LDR}")

    # add each individual data to their respective arrays after each while loop execution
    degree.append(d)
    LDR.append(l)

    # pass in our function to drawnow to plot the data live and pause some fraction of a second
    # to avoid potential overload of the program due to live plotting
    drawnow(plot_live_data)
    plt.pause(0.0001)

    # After every while loop one data point is appended for both the time and the temperature,
    # and the count will correspond to the same number. So here we are basically saying: if there
    # are more than 30 points on the plot, so 31, delete the the first point of each array or list.
    # For example, let's say that there are now 31 points in temperature.
    # temperature = [1st point, 2nd point, ..., 31st point]
    # The condition below will be met and therefore 1st point is deleted by
    # temperature.pop(0) because index starts at 0. pop(indexNumber) removed the item at index indexNumber.
    # So now the data being visualized is from the 2nd point
    # to the 31st point and the process continues ...
    count += 1
    if count > 500:
        LDR.pop(0)
        degree.pop(0)
