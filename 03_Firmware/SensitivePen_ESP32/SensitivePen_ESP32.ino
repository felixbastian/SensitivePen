#include "_MOVUINO_ESP32/_MPU9250.h"
#include "_MOVUINO_ESP32/_Button.h"
#include "_MOVUINO_ESP32/_Record.h"

MovuinoMPU9250 mpu = MovuinoMPU9250();
MovuinoButton button = MovuinoButton();
MovuinoRecord record = MovuinoRecord();

//Command for serial messages
#define CMD_FORMAT_SPIFF 'f' //Format the SPIFF
#define CMD_CREATE_FILE 'c'  //Create a new file in the SPIFF
#define CMD_READ_FILE 'r'    //Read the file
#define CMD_ADD_LINE 'a'     //Add a ne line in the SPIFFS (usefull for debugging)
#define CMD_STOP_RECORD 's'  //Stop the record
#define CMD_LISTING_DIR 'l'  //List files in the directory
#define CMD_PRINT_DAT 'p'    //print one line of data
#define CMD_SPIFF_INFO 'i'   //get informations about the spiff

bool isLock = true;
long timeRecord0 = -999999;

void setup()
{
  Serial.begin(115200);
  mpu.begin();
  button.begin();
  record.begin();
  // record.newRecord();
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
      record.newRecord("SensitivePen");
      break;
    case CMD_READ_FILE: //Reading File
      Serial.println("reading ");
      record.readFile();
      break;
    case CMD_FORMAT_SPIFF:
      Serial.println("Formating the SPIFFS (data files)...");
      record.formatSPIFFS();
      break;
    case CMD_LISTING_DIR:
      Serial.println("Listing directory");
      record.listDirectory();
      break;
    case CMD_SPIFF_INFO:
      Serial.println("Print info SPIFFS");
      record.printStateSPIFFS();
      break;
    case 'u':
      Serial.println("Pressed u");
      break;
    case 'g':
      record.pushData<float>(666.666);
      break;
    case 'h':
      record.pushData<int>(666);
      break;
    case 'e':
      record.newRow();
      break;
    case 'z':
      record.newRecord();
      record.defineColumns("ax,ay,az,gx,gy,gz,mx,my,mz");
      timeRecord0 = millis();
      isLock = false;
    default:
      break;
    }
  }

  mpu.update();
  // mpu.printData();

  if (millis() - timeRecord0 < 3000)
  {
    record.newRow();
    record.pushData<float>(mpu.ax);
    record.pushData<float>(mpu.ay);
    record.pushData<float>(mpu.az);
    record.pushData<float>(mpu.gx);
    record.pushData<float>(mpu.gy);
    record.pushData<float>(mpu.gz);
    record.pushData<float>(mpu.mx);
    record.pushData<float>(mpu.my);
    record.pushData<float>(mpu.mz);
  }
  else
  {
    if (!isLock)
    {
      isLock = true;
      record.stop();
      Serial.print("stop record with nRow = ");
      Serial.println(record.nRow);
    }
  }

  button.update();
  if (button.isPressed())
  {
    Serial.println("isPressed");
  }
  if (button.isDoubleTap())
  {
    Serial.println("\t isDoubleTap");
  }
  if (button.timeHold())
  {
    Serial.print("\t\t");
    Serial.println(button.timeHold());

    // record.writeInFile();
  }
}