class DataPoint {
  // COORDINATES
  public float X;      // X coordinate of the data point
  public float Y;      // Y coordinate of the data point
  
  // DATA VALUES
  private IntList rawVals;               // array list to store each new incoming raw data
  private int N = 10;                    // size of the list
  private float curSmoothVal = 0.0;      // current smooth data = mean of the current raw data list
  private float oldSmoothVal = 0.0;      // last smooth data
  private float curDerivVal = 0.0f;      // difference between current and previous smooth data
  private float smoothValOffset = 0.0;   // reference data value
  public float curSRelativeVal = 0.0;    // curSmoothVal offset from smoothValOffset (curSRelativeVal = curSmoothVal - smoothValOffset)
  public float curRemapVal = 0.0;        // remap data based on the entire row, range between 0.0 and 1.0
  
  DataPoint(int indRow_, int indCol_) {
    // Compute center of data point coordinated based on row and column index
    float w_ = COLS * maxDiameter;
    float h_ = ROWS * maxDiameter;
    float x0 = (width - w_)/2. + maxDiameter/2.;
    float y0 = (height - h_)/2. + maxDiameter/2.;
    this.X = x0 + indCol_ * maxDiameter;
    this.Y = y0 + indRow_ * maxDiameter;
    
    this.rawVals = new IntList(); // initialize raw data list
  }
  
  //----------------------------------------------------------------------------
  
  public void pushNewRawVal(int rawVal_){
    // Add a new raw data value in the list
    if(rawVal_ > 0){
      this.rawVals.append(rawVal_); // add new raw value
    }
    else{
      this.rawVals.append(0);       // value can not be negative, so default = 0
    }
    
    while(this.rawVals.size() > N){
      this.rawVals.remove(0);       // remove older data from the list
    }
    
    if(this.rawVals.size() > 0){
      this.updateDataVals();        // update all data vals based on new incoming raw data 
    }
  }
  
  //----------------------------------------------------------------------------
  
  private void updateDataVals(){
    this.getSmoothVal();          // call function to smooth raw data
    this.getSmoothRelativeVal();  // call function to get the smooth relative data
    this.getDerivVal();           // call function to get derivative of current data
  }
  
  private void getSmoothVal(){
    // Compute mean of last N incoming data
    int meanVal_ = 0;
    for(int i=0; i < this.rawVals.size(); i++){
      meanVal_ += this.rawVals.get(i);
    }
    this.curSmoothVal = meanVal_ / float(this.rawVals.size());
  }
  
  private void getSmoothRelativeVal(){
    this.curSRelativeVal = this.curSmoothVal - this.smoothValOffset; // offset data value
  }
  
  private void getDerivVal(){
    this.curDerivVal = this.curSmoothVal - this.oldSmoothVal;
    this.oldSmoothVal = this.curSmoothVal;
  }
  
  //----------------------------------------------------------------------------
  
  void setOffsetValue(){
    this.smoothValOffset = this.curSmoothVal; // set current value as reference value
  }
  
  //----------------------------------------------------------------------------
  
  void shiftRawVal(){
    // Update data list to keep a stable data flow
    if(this.rawVals.size() >= N){
      this.rawVals.append(this.rawVals.get(this.rawVals.size()-1)); // duplicate last value
      this.rawVals.remove(0); // remove first value
    }
    
    // Call functions to update values
    this.updateDataVals();        // update all data vals based on new incoming raw data
  }
  
  //----------------------------------------------------------------------------
  
  void display(int maxDiameter_) {
    fill(getLerpColor(this.curRemapVal)); // get color point
    noStroke();
    float d_ = this.curRemapVal * maxDiameter_;
    ellipse(this.X,this.Y,d_,d_);
  }
  
  //----------------------------------------------------------------------------
  
  color getLerpColor(float amt_){
    // Set the color of the data point based on its value
    color newColor_ = purple;
    if(amt_ > 0.5){
      // shade from yellow to red if value between .5 and 1.0
      newColor_ = lerpColor(yellow, red, 2*(amt_ - 0.5));
    }
    else{
      // shade from blue to yellow if value between .0 and .5
      newColor_ = lerpColor(blue, yellow, 2*amt_);
    }
    return newColor_;
  }
}
