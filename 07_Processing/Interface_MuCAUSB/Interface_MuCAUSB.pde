import processing.serial.*;

// Serial communication
Serial myPort; // Serial communication with touch sensor
ArduinoSerial arduinoSerial;
Thread serialThread;
String serialData = "";
Serial myPortLed; // Serial communication with leds pannel

// Colors
color red = color(245, 91, 85);
color blue = color(125, 222, 227);
color yellow = color(243, 240, 114);
color purple = color(73, 81, 208);

// Size
int maxDiameter = 75;       // Max range to display data point

// Sensors
DataPoint[][] pointGrid;    // Array of data points from the touch surface
int ROWS = 25;              // number of data point on X axis for touch surface
int COLS = 25;              // number of data point on Y axis for touch surface
int dataCounter = 0;        // count number of incoming data
long timerDataCounter0 = 0; // timer to compute incoming data rate

void setup()
{
  // Set size
  size(700, 700);
  maxDiameter = int(width / float(ROWS) - 10);

  // Set data point grid
  pointGrid = new DataPoint[ROWS][COLS];
  for (int i = 0; i < ROWS; i++) {
    for (int j = 0; j < COLS; j++) {
      pointGrid[i][j] = new DataPoint(i, j);
    }
  }

  // Set serial communication with touch sensors
  println(Serial.list());
  String portName = Serial.list()[1];
  myPort = new Serial(this, portName, 115200); // initialize serial communication
  arduinoSerial = new ArduinoSerial();
  serialThread = new Thread(arduinoSerial);
  serialThread.start();                       // start serial thread

  timerDataCounter0 = millis();

  // Set serial communication with leds pannel
  delay(1);

  myPort.clear();
}

void draw()
{
  background(purple);

  // Update values at each draw even if no new values are coming to generate smooth animation
  for (int i = 0; i < ROWS; i++) {
    for (int j = 0; j < COLS; j++) {
      pointGrid[i][j].shiftRawVal();
    }
  }

  // Remap and display data points
  for (int i = 0; i < ROWS; i++) {
    // Get row data range
    float minRow_ = 1000.0;
    float maxRow_ = 0.0;
    int sumRow_ = 0;
    for (int j = 0; j < COLS; j++) {
      sumRow_ += pointGrid[i][j].curSRelativeVal;

      if (minRow_ > pointGrid[i][j].curSRelativeVal) {
        minRow_ = pointGrid[i][j].curSRelativeVal;
      }
      if (maxRow_ < pointGrid[i][j].curSRelativeVal) {
        maxRow_ = pointGrid[i][j].curSRelativeVal;
      }
    }

    // Get remap values for the current row and display data point
    for (int j = 0; j < COLS; j++) {
      pointGrid[i][j].curRemapVal = (pointGrid[i][j].curSRelativeVal - minRow_) / (maxRow_ - minRow_);
      pointGrid[i][j].curRemapVal *= sumRow_;
      pointGrid[i][j].curRemapVal /= 1024.0; // 1024 = max analog range
      pointGrid[i][j].curRemapVal = constrain(pointGrid[i][j].curRemapVal, 0.0, 1.0);

      pointGrid[i][j].display(maxDiameter); // display data point
    }
  }
 
  if (millis() - timerDataCounter0 > 1000) {
    println("serial speed = ", int(1000 * dataCounter / (millis() - timerDataCounter0)), "data/seconde");
    timerDataCounter0 = millis();
    dataCounter = 0;
  }

}

void mousePressed() {
  for (int i = 0; i < ROWS; i++) {
    for (int j = 0; j < COLS; j++) {
      pointGrid[i][j].setOffsetValue();
    }
  }
}

void serialEvent(Serial myPort) {
  String message = myPort.readStringUntil(113);

  if (message != null)
  {
    serialData = message;
    //serialData = message.substring( 0, message.length()-1 ); // remove 'q' character
    myPort.clear();
  }
}
