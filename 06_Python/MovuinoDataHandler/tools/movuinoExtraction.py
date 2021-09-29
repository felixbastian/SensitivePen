import serial


def MovuinoExtraction(serialPort, path):
    isReading = False
    ExtractionCompleted = False
    print("-> Opening serial port {}".format(serialPort))
    arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
    line_byte = ''
    line_str = ''
    datafile = ''
    nbRecord = 1

    while ExtractionCompleted != True:
        line_byte = arduino.readline()
        line_str = line_byte.decode("utf-8")

        if "XXX_end" in line_str and isReading == True :
            isReading = False
            ExtractionCompleted = True
            print("End of data sheet")

            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                print("Add new file : {}".format(path + "_" + str(nbRecord) + ".csv"))
                file.write(datafile)

        if "XXX_newRecord" in line_str and isReading == True :

            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                print("Add new file : {}".format(path + "_" + str(nbRecord) + ".csv"))
                file.write(datafile)

            datafile = ''
            line_str = ''
            nbRecord += 1

        if (isReading):
            if line_str != '':
                datafile += line_str.strip() + '\n'

        if ("XXX_beginning" in line_str):
            isReading = True
            print("Record begins")