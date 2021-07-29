//https://www.newhavendisplay.com/appnotes/datasheets/touchpanel/FT5x16_registers.pdf
//https://www.buydisplay.com/download/ic/FT5206.pdf
#include "Wire.h"

#define I2C_ADDRESS       0x38

#define MODE_TEST         0x40

// RAW
#define NUM_ROWS          21 // 21
#define ROW_GAP           9
#define NUM_COLUMNS       6

#define ROWS_USE          4

#define CALIBRATION_MAX   3
#define CALIB_THRESHOLD   0

//// ============================== CLASS ==============================

class MuCa {
  public:
    MuCa();
    void init(bool raw = false);

    //int ROWS_USE = NUM_ROWS - ROW_GAP

    bool poll();

    bool updated();

    //RAW
    bool useRaw = false;
    short grid[ROWS_USE * NUM_COLUMNS];

    // manual callibration
    void calibrate(float variance);
    void setGain(int val);


  private:
    bool isInit = false;
    bool calibrationDone = false;

    //RAW
    void getRawData();
    short calibrateGrid[ROWS_USE * NUM_COLUMNS];
    int calibrationSteps = 0;
};

////  ============================== INITIALIZATION ==============================

MuCa::MuCa() {}

void MuCa::init(bool raw ) {
  useRaw = raw;
  digitalWrite(25, LOW);
  digitalWrite(26, LOW);

  Wire.begin();
  Wire.setClock(400000); // 400000 https://www.arduino.cc/en/Reference/WireSetClock

  // Initialization
 
   Wire.beginTransmission(I2C_ADDRESS);
   Wire.write(byte(0x00));
   Wire.write(byte(MODE_TEST));
   Wire.endTransmission(I2C_ADDRESS);
    
  delay(100);
  Serial.println("MuCa initialized");
  delay(100);
  isInit = true;
}


//// ============================== UPDATE ==============================


bool MuCa::updated() {
 if (!isInit) return false;
 poll();
 if (useRaw) return true;
}

bool MuCa::poll() {
 if (useRaw) {
   getRawData();
 }
}

//// ============================== RAW ==============================
//void MuCa::unsureTestMode() { }


void MuCa::getRawData() {

  // Start scan
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(byte(0x00));
  Wire.write(byte(0xc0));
  Wire.endTransmission();


  // Read Data
  for (unsigned int rowAddr = 0; rowAddr < ROWS_USE; rowAddr++) {

    byte result[2  * NUM_COLUMNS];

    //Start transmission
    Wire.beginTransmission(I2C_ADDRESS);
    Wire.write(byte(0x01));
    Wire.write(rowAddr+ROW_GAP);
    unsigned int st = Wire.endTransmission();
    if (st < 0) Serial.print("i2c write failed");

    delayMicroseconds(100); // Wait at least 100us


    Wire.beginTransmission(I2C_ADDRESS);
    Wire.write(byte(16)); // The address of the first column is 0x10 (16 in decimal).
    Wire.endTransmission(false);
    Wire.requestFrom(I2C_ADDRESS, 2 * NUM_COLUMNS, false); // TODO : false was added IDK why
    unsigned int g = 0;
    while (Wire.available()) {
      result[g++] = Wire.read();
    }


    for (unsigned int col = 0; col < NUM_COLUMNS; col++) {
      unsigned  int output = (result[2 * col] << 8) | (result[2 * col + 1]); // Get High and Low bytes for an intersection of row and column

      if (calibrationSteps == CALIBRATION_MAX) {
        grid[(rowAddr * NUM_COLUMNS) +  NUM_COLUMNS - col - 1] = CALIB_THRESHOLD + output - calibrateGrid[(rowAddr * NUM_COLUMNS) +  NUM_COLUMNS - col - 1];
      } else {
        calibrateGrid[(rowAddr * NUM_COLUMNS) +  NUM_COLUMNS - col - 1] = output;
        grid[(rowAddr * NUM_COLUMNS) +  NUM_COLUMNS - col - 1] = output;
      }
    }
    // Serial.println();


  } // End foreachrow

}


//// ============================== CALIBRATION ==============================

void MuCa::calibrate(float variance){
  calibrationSteps = 0;
  while (calibrationSteps != CALIBRATION_MAX) {
    getRawData();
    if (grid[0] < 5000) return;
    if (calibrationSteps == 0 && !calibrationDone) {
      memcpy(calibrateGrid, grid, sizeof(grid));
    }
    else {
      for (int i = 0; i < (ROWS_USE * NUM_COLUMNS); i++) {
        calibrateGrid[i] = (calibrateGrid[i] + grid[i]) /2;//(variance * grid[i]);
      }
    }
    //Serial.println("Calibrate");
    calibrationSteps++;
  }
  calibrationDone = true;
}

void MuCa::setGain(int gain) {
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(byte(0x07));
  Wire.write(byte(gain));
  Wire.endTransmission();
}


//https://www.buydisplay.com/download/ic/FT5206.pdf + https://github.com/optisimon/ft5406-capacitive-touch/blob/master/CapacitanceVisualizer/FT5406.hpp
// https://github.com/hyvapetteri/touchscreen-cardiography + http://optisimon.com/raspberrypi/touch/ft5406/2016/07/13/raspberry-pi-7-inch-touchscreen-hacking/
//https://www.newhavendisplay.com/app_notes/FT5x16.pdf + https://www.newhavendisplay.com/appnotes/datasheets/touchpanel/FT5x16_registers.pdf
//https://github.com/azzazza/patch_kernel_q415/blob/master/drivers/input/touchscreen/ft5x06_ts.c
