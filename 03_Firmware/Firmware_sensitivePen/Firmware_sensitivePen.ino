/*
 * Firmwrae that sends dats data of the sensitive pen:
 * Format:
 * -> Nappe : z(Indcol)X(ValueHexa)X...X... ..q
 * -> MPU : 
 *    - Acceleration : a(ValueX)c(ValueY)c(ValueZ)q
 *    - Gyroscope : g(ValueX)c(ValueY)c(ValueZ)q
 *    - Magnetmetre : m(ValueX)c(ValueY)c(ValueZ)q
 */


#if (RAMEND < 1000)
  #define SERIAL_BUFFER_SIZE 16
#else
  #define SERIAL_BUFFER_SIZE 64
#endif

#include "MuCa_firmware_raw.h"
#include "MPU9250.h"
#include <bluefruit.h>
#include <Adafruit_LittleFS.h>
#include <InternalFileSystem.h>

//MuCa
MuCa muca;

//MPU9250
MPU9250 mpu9250(Wire, 0x68);

int status;

float ax, ay, az; // store accelerometre values
float gx, gy, gz; // store gyroscope values
float mx, my, mz; // store magneto values
float x;

// BLE Service
BLEDfu  bledfu;  // OTA DFU service
BLEDis  bledis;  // device information
BLEUart bleuart; // uart over ble
BLEBas  blebas;  // battery

void setup()
{
  Serial.begin(115200);
  x=50.0;
  //MPU Launch
  status = mpu9250.begin();
  if (status < 0)
  {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
  }
  
  Serial.println("Bluefruit52 BLEUART Example");
  Serial.println("---------------------------\n");

  // Setup the BLE LED to be enabled on CONNECT
  // Note: This is actually the default behaviour, but provided
  // here in case you want to control this LED manually via PIN 19
  Bluefruit.autoConnLed(true);

  // Config the peripheral connection with maximum bandwidth 
  // more SRAM required by SoftDevice
  // Note: All config***() function must be called before begin()
  //Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);

  Bluefruit.begin();
  Bluefruit.setTxPower(4);    // Check bluefruit.h for supported values
  Bluefruit.setName("SENSITIVEPEN");
  //Bluefruit.setName(getMcuUniqueID()); // useful testing with multiple central connections
  Bluefruit.Periph.setConnectCallback(connect_callback);
  Bluefruit.Periph.setDisconnectCallback(disconnect_callback);

  // To be consistent OTA DFU should be added first if it exists
  bledfu.begin();

  // Configure and Start Device Information Service
  bledis.setManufacturer("Adafruit Industries");
  bledis.setModel("Bluefruit Feather52");
  bledis.begin();

  // Configure and Start BLE Uart Service
  bleuart.begin();

  // Start BLE Battery Service
  blebas.begin();
  blebas.write(100);

  // Set up and start advertising
  startAdv();

  Serial.println("Please use Adafruit's Bluefruit LE app to connect in UART mode");
  Serial.println("Once connected, enter character(s) that you wish to send");
  muca.init(false); // useInterrupt ne fonctionne pas bien
  muca.useRaw = true;
  muca.calibrate(1.0);
}


void loop()
{

  //Read the sensor
  mpu9250.readSensor();
  Serial.print("---------------    MPU Data    ---------------");
  //printMPUData();
  
  Serial.print("------------    MPU Var Data    --------------");
  GetMpuData(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);

  /*----------- Print on the serial ------------------
  printAcceleration();
  printGyroscope();
  printMagnetometre();
  
  printNappeData();
  */
  //printBluetoothNappeData();
  //printBluetoothAcceleration();
  //printBluetoothGyroscope();

  delay(100);
}
