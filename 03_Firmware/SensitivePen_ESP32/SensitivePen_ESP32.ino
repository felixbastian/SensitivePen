#include <elapsedMillis.h>

#include "_MOVUINO_ESP32/_MPU9250.h"
#include "_MOVUINO_ESP32/_Button.h"
#include "_MOVUINO_ESP32/_Recorder.h"

MovuinoMPU9250 mpu = MovuinoMPU9250();
MovuinoButton button = MovuinoButton();
MovuinoRecorder recorder = MovuinoRecorder();

//Command for serial messages
#define CMD_FORMAT_SPIFF 'f' //Format the SPIFF
#define CMD_CREATE_FILE 'c'  //Create a new file in the SPIFF
#define CMD_READ_FILE 'r'    //Read the file
#define CMD_ADD_LINE 'a'     //Add a ne line in the SPIFFS (usefull for debugging)
#define CMD_STOP_RECORD 's'  //Stop the record
#define CMD_LISTING_DIR 'l'  //List files in the directory
#define CMD_PRINT_DAT 'p'    //print one line of data
#define CMD_SPIFF_INFO 'i'   //get informations about the spiff

bool isBtnHold = false;
elapsedMillis dlyRec;

void setup()
{
  Serial.begin(115200);
  mpu.begin();
  button.begin();
  recorder.begin();
}

void loop()
{
  if (Serial.available() > 0)
  {
    char serialMessage = Serial.read();
    Serial.print("\n");
    Serial.print("Message received : ");
    Serial.println(serialMessage);

    //--------- Serial command -------------
    switch (serialMessage)
    {
    case CMD_CREATE_FILE: //Create a new file and replace the previous one
      Serial.println("Creation of ");
      recorder.newRecord("SensitivePen");
      break;
    case CMD_READ_FILE: //Reading File
      Serial.println("reading ");
      recorder.readAllRecords();
      break;
    case CMD_FORMAT_SPIFF:
      Serial.println("Formating the SPIFFS (data files)...");
      recorder.formatSPIFFS();
      break;
    case CMD_LISTING_DIR:
      Serial.println("Listing directory");
      recorder.listDirectory();
      break;
    case CMD_SPIFF_INFO:
      Serial.println("Print info SPIFFS");
      recorder.printStateSPIFFS();
      break;
    case 'u':
      Serial.println("Pressed u");
      break;
    case 'g':
      Serial.println("Pressed g");
      break;
    case 'h':
      Serial.println("Pressed h");
      break;
    case 'e':
      Serial.println("Pressed e");
      break;
    case 'z':
      recorder.newRecord();
      recorder.defineColumns("ax,ay,az,gx,gy,gz,mx,my,mz");
    default:
      break;
    }
  }

  button.update();
  if (button.isReleased())
  {
    if (!isBtnHold)
    {
      Serial.println("isReleased");
      if (!recorder.isRecording())
      {
        recorder.newRecord("SensitivePen");
        recorder.defineColumns("ax,ay,az,gx,gy,gz,mx,my,mz");
      }
      else
        recorder.stop();
    }
    isBtnHold = false;
  }
  if (button.isDoubleTap())
  {
    Serial.println("\t isDoubleTap");
  }
  if (button.timeHold())
  {
    Serial.print("\t\t");
    Serial.println(button.timeHold());

    if (button.timeHold() > 1000)
    {
      isBtnHold = true;
      if (!recorder.isRecording())
      {
        mpu.magnometerCalibration();
      }
    }
  }

  if (recorder.isRecording())
  {
    if (dlyRec > 10)
    {
      dlyRec = 0;
      mpu.update();

      recorder.addRow();
      recorder.pushData<float>(mpu.ax);
      recorder.pushData<float>(mpu.ay);
      recorder.pushData<float>(mpu.az);
      recorder.pushData<float>(mpu.gx);
      recorder.pushData<float>(mpu.gy);
      recorder.pushData<float>(mpu.gz);
      recorder.pushData<float>(mpu.mx);
      recorder.pushData<float>(mpu.my);
      recorder.pushData<float>(mpu.mz);
    }
  }
}