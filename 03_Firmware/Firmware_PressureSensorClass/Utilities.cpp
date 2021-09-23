int getArrayMin(int *array_, int size_)
{
  int min_ = array_[0];
  for (int i = 0; i < size_; i++)
  {
    if (array_[i] < min_)
    {
      min_ = array_[i];
    }
  }
  return min_;
}

float getFloatsMin(float *array_, int size_)
{
  float min_ = array_[0];
  for (int i = 0; i < size_; i++)
  {
    if (array_[i] < min_)
    {
      min_ = array_[i];
    }
  }
  return min_;
}

int getArrayMax(int *array_, int size_)
{
  int max_ = array_[0];
  for (int i = 0; i < size_; i++)
  {
    if (array_[i] > max_)
    {
      max_ = array_[i];
    }
  }
  return max_;
}

int getArrayRange(int *array_, int size_)
{
  int range_ = getArrayMax(array_, size_) - getArrayMin(array_, size_);
  return range_;
}

float getFloatsMax(float *array_, int size_)
{
  float max_ = array_[0];
  for (int i = 0; i < size_; i++)
  {
    if (array_[i] > max_)
    {
      max_ = array_[i];
    }
  }
  return max_;
}

float getArrayMean(int *array_, int size_)
{
  float mean_ = 0.0f;
  for (int i = 0; i < size_; i++)
  {
    mean_ += float(array_[i]) / size_;
  }
  return mean_;
}

float sumArray(float *array_, int size_)
{
  float sum_ = 0.0f;
  for (int i = 0; i < size_; i++)
  {
    sum_ += array_[i] ;
  }
  return sum_;
}

float getMaxIndex(float *array_, int size_)
{
  int ind_ = 0;
  float max_ = array_[ind_];
  for (int i = 0; i < size_; i++)
  {
    if (array_[i] > max_)
    {
      ind_ = i;
    }
  }
  return ind_;
}
