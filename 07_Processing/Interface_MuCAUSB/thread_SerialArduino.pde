public class ArduinoSerial implements Runnable {
  Thread thread;
  private long timer0;

  public ArduinoSerial() {
    timer0 = millis();
  }

  public void start() {
    thread = new Thread(this);
    thread.start();
  }

  public void run() {
    while (true) {
      // Update values based on incoming serial messages
      String serialData_ = serialData;

      if (serialData_ != "") {
        serialData_ = serialData_.trim();

        char adr_ = serialData_.charAt(0);
        if (serialData_.length() > 3) {
          serialData_ = serialData_.substring(1, serialData_.length());

          switch(adr_) {
            case 'z' :
              // GET COORDINATES
              int[] rowtouch_ = int(split(serialData_, 'x')); 
              if (rowtouch_.length == COLS + 1) {
                int rowIndex_ = int(rowtouch_[0]);
  
                for (int i = 0; i < COLS; i++) {
                  pointGrid[rowIndex_][i].pushNewRawVal(rowtouch_[i+1]);
                }
              }
  
              dataCounter++;
              break;
            default :
              break;
          }
          serialData_ = "";
        }
      }
      delay(1);
    }
  }

  public void stop() {
    thread = null;
  }
}
