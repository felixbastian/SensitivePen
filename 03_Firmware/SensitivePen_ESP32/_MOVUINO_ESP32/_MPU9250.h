#if !defined(_MOVUINOESP32_MPU9250_)
#define _MOVUINOESP32_MPU9250_

#include "Wire.h"
#include "I2Cdev.h"
#include "MPU9250.h"

#define MPU_I2C_ADDRESS 0x69

class MovuinoMPU9250
{
private:
  MPU9250 _imu;

public:
  float ax, ay, az; // store accelerometre values
  float gx, gy, gz; // store gyroscope values
  float mx, my, mz; // store magneto values

  MovuinoMPU9250();
  ~MovuinoMPU9250();

  void begin();
  void update();
  void printData();

  void magnometerCalibration();
  void accelerometerCalibration();
  void gyroscopeCalibration();
};

MovuinoMPU9250::MovuinoMPU9250() : _imu(Wire, MPU_I2C_ADDRESS)
{
}

MovuinoMPU9250::~MovuinoMPU9250()
{
}

void MovuinoMPU9250::begin()
{
  Wire.begin();

  int status = this->_imu.begin();

  if (status < 0)
  {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while (1)
    {
    }
  }

  int statusGyro = this->_imu.setGyroRange(MPU9250::GYRO_RANGE_1000DPS);
  int statusAccel = this->_imu.setAccelRange(MPU9250::ACCEL_RANGE_8G);

  if (statusGyro < 0 || statusAccel < 0)
  {
    Serial.println("ERROR while setting range :");
    Serial.println("Accel range : " + statusAccel);
    Serial.println("Gyro range : " + statusGyro);
  }
  else
  {
    Serial.println("RAS for the range");
  }
}

void MovuinoMPU9250::update(){
  // Update
  this->_imu.readSensor();
  // Accel
  this->ax = -this->_imu.getAccelX_mss();
  this->ay = this->_imu.getAccelY_mss();
  this->az = this->_imu.getAccelZ_mss();
  // Gyro
  this->gx = this->_imu.getGyroX_rads();
  this->gy = -this->_imu.getGyroY_rads();
  this->gz = -this->_imu.getGyroZ_rads();
  // Mag
  this->mx = this->_imu.getMagX_uT();
  this->my = -this->_imu.getMagY_uT();
  this->mz = -this->_imu.getMagZ_uT();
}

void MovuinoMPU9250::magnometerCalibration()
{
  /*
   * Calibrate magnetometer of the IMU using the IMU function
   */
  Serial.println("Calibrating Magnetometer : ");
  Serial.println("Please continuously and slowly move the sensor in a figure 8 while the function is running");

  int statusMagCal = this->_imu.calibrateMag();
  if (statusMagCal < 0)
  {
    Serial.println("ERROR while calibrating");
  }
  else
  {
    Serial.println("Magnetometer's calibration OK");
  }
}

void MovuinoMPU9250::accelerometerCalibration()
{
  /*
   * Calibrate accelerometer of the IMU using the IMU function
   */
  Serial.println("Calibrating accelerometer : ");

  int statusAccelCal = this->_imu.calibrateAccel();
  if (statusAccelCal < 0)
  {
    Serial.println("ERROR while calibrating");
  }
  else
  {
    Serial.println("Accelerometer's calibration OK");
  }
}

void MovuinoMPU9250::gyroscopeCalibration()
{
  /*
   * Calibrate Gyro of the IMU using the IMU function
   */
  Serial.println("Calibrating Gyro : ");

  int statusGyrCal = this->_imu.calibrateGyro();
  if (statusGyrCal < 0)
  {
    Serial.println("ERROR while calibrating");
  }
  else
  {
    Serial.println("Gyroscope's calibration OK");
  }
}

void MovuinoMPU9250::printData()
{
  /* 
   * display the data of IMU 
   */
  Serial.print(this->_imu.getAccelX_mss(), 6);
  Serial.print("\t");
  Serial.print(this->_imu.getAccelY_mss(), 6);
  Serial.print("\t");
  Serial.print(this->_imu.getAccelZ_mss(), 6);
  Serial.print("\t");
  Serial.print(this->_imu.getGyroX_rads(), 6);
  Serial.print("\t");
  Serial.print(this->_imu.getGyroY_rads(), 6);
  Serial.print("\t");
  Serial.print(this->_imu.getGyroZ_rads(), 6);
  Serial.print("\t");
  Serial.print(this->_imu.getMagX_uT(), 6);
  Serial.print("\t");
  Serial.print(this->_imu.getMagY_uT(), 6);
  Serial.print("\t");
  Serial.print(this->_imu.getMagZ_uT(), 6);
  Serial.println();
}

#endif // _MOVUINOESP32_MPU9250_
