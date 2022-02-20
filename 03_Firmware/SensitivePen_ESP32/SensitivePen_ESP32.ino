#include <elapsedMillis.h>

#include "_MOVUINO_ESP32/_MPU9250.h"
#include "_MOVUINO_ESP32/_Button.h"
#include "_MOVUINO_ESP32/_Recorder.h"
#include "_MOVUINO_ESP32/_Neopixel.h"

// Color swap
#define WHITE255 ((255 << 16) | (255 << 8) | 255)
#define RED ((255 << 16) | (0 << 8) | 0)
#define GREEN ((0 << 16) | (250 << 8) | 0)
#define YELLOW ((200 << 16) | (175 << 8) | 0)
#define BLUE ((0 << 16) | (0 << 8) | 255)
#define MAGENTA ((255 << 16) | (0 << 8) | 255)

// Command for serial messages
#define CMD_FORMAT_SPIFF 'f' // Format the SPIFF
#define CMD_CREATE_FILE 'c'  // Create a new file in the SPIFF
#define CMD_READ_FILE 'r'    // Read the file
#define CMD_ADD_LINE 'a'     // Add a ne line in the SPIFFS (usefull for debugging)
#define CMD_STOP_RECORD 's'  // Stop the record
#define CMD_LISTING_DIR 'l'  // List files in the directory
#define CMD_SPIFF_INFO 'i'   // Get informations about the spiff

#define BATTERY_PIN 36       // Used to read the battery level
#define BATTERY_MIN_VAL 1900 // ~3.3v
#define BATTERY_MAX_VAL 2500 // ~4.2v

MovuinoMPU9250 mpu = MovuinoMPU9250();
MovuinoButton button = MovuinoButton();
MovuinoRecorder recorder = MovuinoRecorder();
MovuinoNeopixel neopix = MovuinoNeopixel();

bool isBtnHold = false;
bool isCallibrating = false;
elapsedMillis dlyRec;

String recordId = "SensitivePen";
String colsId = "ax,ay,az,gx,gy,gz,mx,my,mz";

int timeHoldCallib = 1800;

uint32_t colOn = BLUE;
uint32_t colRec = RED;
uint32_t colCallib = MAGENTA;
uint32_t colReadFiles = YELLOW;
uint32_t colFormat = RED;

void setup()
{
  Serial.begin(115200);
  pinMode(BATTERY_PIN, INPUT);
  
  // Neopixel
  neopix.begin();
  neopix.setBrightness(5);
  showBatteryLevel();
  normalMode();
  freezBlink(2);
  neopix.update();
  
  // Other
  mpu.begin();
  button.begin();
  recorder.begin();
  freezBlink(4);
}

void loop()
{
  neopix.update();
  button.update();

  if (Serial.available() > 0)
  {
    char serialMessage = Serial.read();
    Serial.print("\n");
    Serial.print("Message received : ");
    Serial.println(serialMessage);

    //--------- Serial command -------------
    switch (serialMessage)
    {
    case CMD_CREATE_FILE:
      Serial.println("Creation of ");
      recorder.newRecord(recordId);
      break;
    case CMD_READ_FILE:
      Serial.println("reading all recorded files ");
      readAllfiles();
      break;
    case CMD_FORMAT_SPIFF:
      Serial.println("Formating the SPIFFS (data files)...");
      freezColorStrob(5, colFormat);
      neopix.setColor(colFormat);
      neopix.forceUpdate();
      recorder.formatSPIFFS();
      normalMode();
      break;
    case CMD_LISTING_DIR:
      Serial.println("Listing directory");
      neopix.blinkOn(50, 2);
      recorder.listDirectory();
      break;
    case CMD_SPIFF_INFO:
      Serial.println("Print info SPIFFS");
      neopix.blinkOn(50, 2);
      recorder.printStateSPIFFS();
      break;
    case CMD_ADD_LINE:
      neopix.blinkOn(50, 2);
      recorder.addRow();
      break;
    case CMD_STOP_RECORD:
      stopRecord();
      break;
    default:
      break;
    }
  }

  // -----------------------------------------
  //                RECORDER
  // -----------------------------------------
  if (button.isReleased())
  {
    if (!isBtnHold)
    {
      if (!recorder.isRecording())
      {
        startRecord();
      }
      else
      {
        stopRecord();
      }
    }
    isBtnHold = false;
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

  // -----------------------------------------
  //               CALLIBRATION
  // -----------------------------------------
  if (button.timeHold())
  {
    // Color shade
    float r_ = (button.timeHold() - 400) / (float)timeHoldCallib;
    neopix.lerpTo(colCallib, r_);

    if (button.timeHold() > timeHoldCallib)
    {
      neopix.setColor(colCallib); // lock color
      if (button.timeHold() > timeHoldCallib + 20)
      {
        isBtnHold = true;
        freezBlink(2);
        if (!recorder.isRecording() && !isCallibrating)
        {
          isCallibrating = true;
          mpu.magnometerCalibration();
          isCallibrating = false;
          neopix.blinkOn(100, 2);
          normalMode();
        }
      }
    }
  }
}

void normalMode() {
  neopix.setColor(colOn);
}

void startRecord()
{
  recorder.newRecord(recordId);
  recorder.defineColumns(colsId);
  
  freezColorStrob(2, RED);
  neopix.rainbowOn();
  neopix.breathOn(1000, 0.8);
}

void stopRecord()
{
  freezColorStrob(2, GREEN);
  neopix.rainbowOff();
  neopix.breathOff();
  recorder.stop();
  normalMode();
}

void readAllfiles()
{
  freezColorStrob(2, colReadFiles);
  neopix.setColor(colReadFiles);
  neopix.forceUpdate();

  recorder.readAllRecords();
  
  freezBlink(3);
  normalMode();
}

void freezBlink(int nblink_)
{
  for (int i = 0; i < nblink_; i++)
  {
    neopix.turnOff();
    neopix.forceUpdate();
    delay(50);
    neopix.turnOn();
    neopix.forceUpdate();
    delay(50);
  }
}

void freezColorStrob(int nblink_, uint32_t color_)
{
  uint32_t curCol_ = neopix.getColor();
  for (int i = 0; i < nblink_; i++)
  {
    neopix.setColor(color_);
    neopix.forceUpdate();
    delay(100);
    neopix.setColor(curCol_);
    neopix.forceUpdate();
    delay(100);
  }
}

void showBatteryLevel(void)
{
  int sum;
  int level;

  sum = 0;
  for (uint8_t i = 0; i < 10; i++) // Do the average over 10 values
    sum += analogRead(BATTERY_PIN);
  
  if (sum < BATTERY_MIN_VAL * 10)
    sum = BATTERY_MIN_VAL * 10;

  if (sum > BATTERY_MAX_VAL * 10)
    sum = BATTERY_MAX_VAL * 10;
   
  level = ((float)((sum / 10) - BATTERY_MIN_VAL ) / (float)(BATTERY_MAX_VAL - BATTERY_MIN_VAL)) * 100.0;
  
  if (level >= 50)
    neopix.setColor((uint32_t)GREEN);
  else if (level >= 25)
    neopix.setColor((uint32_t)YELLOW);
  else
    neopix.setColor((uint32_t)RED);
    
  neopix.forceUpdate();
  delay(2500);
  Serial.printf("Battery Reading: %d\n", sum / 10);
  Serial.printf("Battery Level: %d%%\n", level);
  delay(2500);
}