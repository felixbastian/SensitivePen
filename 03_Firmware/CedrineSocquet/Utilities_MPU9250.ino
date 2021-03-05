void printMPURawData(){
  // display the data
  Serial.print(mpu9250.getAccelX_mss(),3);
  Serial.print("\t");
  Serial.print(mpu9250.getAccelY_mss(),3);
  Serial.print("\t");
  Serial.print(mpu9250.getAccelZ_mss(),3);
  Serial.print("\t");
  Serial.print(mpu9250.getGyroX_rads(),3);
  Serial.print("\t");
  Serial.print(mpu9250.getGyroY_rads(),3);
  Serial.print("\t");
  Serial.print(mpu9250.getGyroZ_rads(),3);
  Serial.print("\t");
  Serial.print(mpu9250.getMagX_uT(),3);
  Serial.print("\t");
  Serial.print(mpu9250.getMagY_uT(),3);
  Serial.print("\t");
  Serial.print(mpu9250.getMagZ_uT(),3);
  Serial.print("\t");
  Serial.println(mpu9250.getTemperature_C(),3);
  delay(100);
}
void printMPUData(){
  // display the data
  Serial.print(ax,3);
  Serial.print("\t");
  Serial.print(ay,3);
  Serial.print("\t");
  Serial.print(az,3);
  Serial.print("\t");
  Serial.print(gx,3);
  Serial.print("\t");
  Serial.print(gy,3);
  Serial.print("\t");
  Serial.print(gz,3);
  Serial.print("\t");
  Serial.print(mx,3);
  Serial.print("\t");
  Serial.print(my,3);
  Serial.print("\t");
  Serial.print(mz,3);
  delay(100);
}

void GetMpuData(float *ax, float *ay, float *az, float *gx, float *gy, float *gz, float *mx, float *my, float *mz)
{
  
  *ax = mpu9250.getAccelX_mss();
  *ay = mpu9250.getAccelY_mss();
  *az = mpu9250.getAccelZ_mss();
  *gx = mpu9250.getGyroX_rads();
  *gy = mpu9250.getGyroY_rads();
  *gz = mpu9250.getGyroZ_rads();
  *mx = mpu9250.getMagX_uT();
  *my = mpu9250.getMagY_uT();
  *mz = mpu9250.getMagZ_uT();
}
