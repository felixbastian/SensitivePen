#if !defined(_MOVUINO_NEOPIXEL_)
#define _MOVUINO_NEOPIXEL_

#include <Adafruit_NeoPixel.h>

#define PIN_NEOPIX 15

class MovuinoNeopixel
{
private:
    Adafruit_NeoPixel _pix;
    unsigned long _timeShow0;
    int _brightness = 255;
    int _color;

    uint8_t getRed(uint32_t color_);
    uint8_t getGreen(uint32_t color_);
    uint8_t getBlue(uint32_t color_);

    // Blink animation
    bool _isBlinking = false;
    unsigned long _timeBlink0;
    int _timeBlinkOn;
    int _timeBlinkOff;
    int _nBlink;

    // Breath animation
    bool _isBreathing = false;
    float _breathIntens = 1.0f;
    int _timeBreath;

    // Rainbow animation
    bool _isRainbow = false;
    long _rainbowHue = 0;

public:
    MovuinoNeopixel();
    ~MovuinoNeopixel();

    void begin();
    void update();
    void forceUpdate();

    // Setters
    void turnOff();
    void turnOn();
    void setColor(uint32_t color_);
    void setColor(uint8_t red_, uint8_t green_, uint8_t blue_);
    void setBrightness(int bright_);
    void lerpTo(uint32_t toColor_, float intensity_);

    // Animations
    void breathOn(int periodMs_);
    void breathOn(int periodMs_, float intensity_);
    void breathOff();
    void blinkOn(int timeOn_);
    void blinkOn(int timeOn_, int nBlink_);
    void asyncBlinkOn(int timeOn_, int timeOff_);
    void asyncBlinkOn(int timeOn_, int timeOff_, int nBlink_);
    void blinkOff();
    void rainbowOn();
    void rainbowOff();

    // Getters
    uint32_t getColor();
};

MovuinoNeopixel::MovuinoNeopixel() : _pix(1, PIN_NEOPIX, NEO_GRB + NEO_KHZ800)
{
}

MovuinoNeopixel::~MovuinoNeopixel()
{
}

void MovuinoNeopixel::begin()
{
    this->_pix.begin();
    this->_pix.show();
    this->_color = this->getColor();
    this->_timeShow0 = millis();
}

void MovuinoNeopixel::update()
{
    if (millis() - this->_timeShow0 > 20)
    {
        if (this->_isRainbow)
        {
            this->_rainbowHue += 256;
            if (this->_rainbowHue >= 5 * 65536)
                this->_rainbowHue = 0;
            this->setColor(this->_pix.gamma32(this->_pix.ColorHSV(this->_rainbowHue)));
        }

        if (this->_isBreathing)
        {
            float r_ = 0.5 * (1 + sin(PI * (millis() / (float)(this->_timeBreath))));
            r_ = 1 - r_ * this->_breathIntens;
            int bright_ = (int)(this->_brightness * r_);
            this->_pix.setBrightness(bright_);
            this->_pix.setPixelColor(0, this->_color); // loose color when brightness = 0
        }

        if (this->_isBlinking)
        {
            int period_ = this->_timeBlinkOn + this->_timeBlinkOff;
            unsigned long blkTime_ = millis() - this->_timeBlink0;
            int tCycle_ = blkTime_ % period_;
            if (tCycle_ < this->_timeBlinkOn)
                this->turnOn();
            else
                this->turnOff();

            if (this->_nBlink != -1 && (blkTime_ > this->_nBlink * period_))
                this->blinkOff(); // stop blinking after _nBlink cycles
        }

        this->_timeShow0 = millis();
        this->_pix.show();
    }
}

void MovuinoNeopixel::forceUpdate()
{
    this->_pix.show();
}

// -----------------------------------------
//                SETTERS
// -----------------------------------------
void MovuinoNeopixel::turnOff()
{
    this->_pix.setBrightness(0);
}
void MovuinoNeopixel::turnOn()
{
    this->_pix.setBrightness(this->_brightness);
    this->_pix.setPixelColor(0, this->_color);
}
void MovuinoNeopixel::setColor(uint32_t color_)
{
    this->_color = color_;
    this->_pix.setPixelColor(0, color_);
}
void MovuinoNeopixel::setColor(uint8_t red_, uint8_t green_, uint8_t blue_)
{
    uint32_t col_ = _pix.Color(red_, green_, blue_);
    this->setColor(col_);
}
void MovuinoNeopixel::setBrightness(int bright_)
{
    this->_brightness = bright_;
    this->_pix.setBrightness(bright_);
}
void MovuinoNeopixel::lerpTo(uint32_t toColor_, float intensity_)
{
    if (intensity_ > 1)
        intensity_ = 1;
    intensity_ = abs(intensity_);

    uint8_t red_ = this->getRed(this->_color) * (1 - intensity_) + this->getRed(toColor_) * intensity_;
    uint8_t green_ = this->getGreen(this->_color) * (1 - intensity_) + this->getGreen(toColor_) * intensity_;
    uint8_t blue_ = this->getBlue(this->_color) * (1 - intensity_) + this->getBlue(toColor_) * intensity_;
    this->_pix.setPixelColor(0, this->_pix.Color(red_, green_, blue_));
}

// -----------------------------------------
//                ANIMATIONS
// -----------------------------------------
void MovuinoNeopixel::blinkOn(int timeOn_)
{
    this->asyncBlinkOn(timeOn_, timeOn_, -1);
}
void MovuinoNeopixel::blinkOn(int timeOn_, int nBlink_)
{
    this->asyncBlinkOn(timeOn_, timeOn_, nBlink_);
}
void MovuinoNeopixel::asyncBlinkOn(int timeOn_, int timeOff_)
{
    this->asyncBlinkOn(timeOn_, timeOff_, -1);
}
void MovuinoNeopixel::asyncBlinkOn(int timeOn_, int timeOff_, int nBlink_)
{
    if (!timeOn_)
        this->turnOff();
    else
    {
        this->_timeBlinkOn = timeOn_;
        this->_timeBlinkOff = timeOff_;
        this->_nBlink = nBlink_;
        this->_timeBlink0 = millis();
        this->_isBlinking = true;
    }
}
void MovuinoNeopixel::blinkOff()
{
    this->_isBlinking = false;
    this->_pix.setBrightness(this->_brightness);
}

void MovuinoNeopixel::breathOn(int periodMs_)
{
    this->breathOn(periodMs_, 1.0f);
}
void MovuinoNeopixel::breathOn(int periodMs_, float intensity_)
{
    if (intensity_ > 1)
        intensity_ = 1;
    this->_breathIntens = abs(intensity_);
    this->_timeBreath = periodMs_;
    this->_isBreathing = true;
}
void MovuinoNeopixel::breathOff()
{
    this->_isBreathing = false;
    this->_pix.setBrightness(this->_brightness);
}
void MovuinoNeopixel::rainbowOn()
{
    // Based on Adafruit Neopixel strandtest example
    this->_isRainbow = true;
}
void MovuinoNeopixel::rainbowOff()
{
    this->_isRainbow = false;
}

// -----------------------------------------
//                GETTERS
// -----------------------------------------
uint32_t MovuinoNeopixel::getColor()
{
    return this->_pix.getPixelColor(0);
}
uint8_t MovuinoNeopixel::getRed(uint32_t color_)
{
    return (color_ >> 16) & 0xFF;
}
uint8_t MovuinoNeopixel::getGreen(uint32_t color_)
{
    return (color_ >> 8) & 0xFF;
}
uint8_t MovuinoNeopixel::getBlue(uint32_t color_)
{
    return color_ & 0xFF;
}

#endif // _MOVUINO_NEOPIXEL_
