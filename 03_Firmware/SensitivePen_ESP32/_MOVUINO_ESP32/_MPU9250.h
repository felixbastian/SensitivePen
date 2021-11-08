#if !defined(_MOVUINOESP32_MPU9250_)
#define _MOVUINOESP32_MPU9250_

#include "Wire.h"
#include "I2Cdev.h"
#include "MPU9250.h"

#define MPU_I2C_ADDRESS 0x69

class MovuinoMPU9250
{
private:
    MovuinoMPU9250 * imu;

    void magnometerCalibration();
    void accelerometerCalibration();
    void gyroscopeCalibration();
    
    void print9axesDataMPU();

public:
    float ax, ay, az; // store accelerometre values
    float gx, gy, gz; // store gyroscope values
    float mx, my, mz; // store magneto values
    
    MovuinoMPU9250(/* args */);
    ~MovuinoMPU9250();

    void get9axesDataMPU();
};

MovuinoMPU9250::MovuinoMPU9250(/* args */) : imu(Wire, MPU_I2C_ADDRESS)
{
    Wire.begin();

    int status = this->imu.begin();

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

    // this->magnometerCalibration();

    int statusGyro = this->imu.setGyroRange(MPU9250::GYRO_RANGE_1000DPS);
    int statusAccel = this->imu.setAccelRange(MPU9250::ACCEL_RANGE_8G);

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

MovuinoMPU9250::~MovuinoMPU9250()
{
}

void MovuinoMPU9250::magnometerCalibration()
{
  /*
   * Calibrate magnetometer of the IMU using the IMU function
   */
  Serial.println("Calibrating Magnetometer : ");
  Serial.println("Please continuously and slowly move the sensor in a figure 8 while the function is running");
  
  int statusMagCal = this->imu.calibrateMag();
  if (statusMagCal<0)
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
  
  int statusAccelCal = this->imu.calibrateAccel();
  if (statusAccelCal<0)
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
  
  int statusGyrCal = this->imu.calibrateGyro();
  if (statusGyrCal<0)
  {
    Serial.println("ERROR while calibrating");
  }
  else
  {
    Serial.println("Gyroscope's calibration OK");
  }
}

void MovuinoMPU9250::print9axesDataMPU(){
  /* 
   * display the data of IMU 
   */
  Serial.print(this->imu.getAccelX_mss(),6);
  Serial.print("\t");
  Serial.print(this->imu.getAccelY_mss(),6);
  Serial.print("\t");
  Serial.print(this->imu.getAccelZ_mss(),6);
  Serial.print("\t");
  Serial.print(this->imu.getGyroX_rads(),6);
  Serial.print("\t");
  Serial.print(this->imu.getGyroY_rads(),6);
  Serial.print("\t");
  Serial.print(this->imu.getGyroZ_rads(),6);
  Serial.print("\t");
  Serial.print(this->imu.getMagX_uT(),6);
  Serial.print("\t");
  Serial.println(this->imu.getMagY_uT(),6);
}

void MovuinoMPU9250::get9axesDataMPU(){
    //Accel
    this->ax = this->imu.getAccelX_mss();
    this->ay = this->imu.getAccelY_mss();
    this->az = this->imu.getAccelZ_mss();
    //Gyro
    this->gx = this->imu.getGyroX_rads();
    this->gy = this->imu.getGyroY_rads();
    this->gz = this->imu.getGyroZ_rads();
    //Mag
    this->mx = this->imu.getMagX_uT();
    this->my = this->imu.getMagY_uT();
    this->mz = this->imu.getMagZ_uT();
}

#endif // _MOVUINOESP32_MPU9250_
