#include <Wire.h>
#include <VL53L0X.h>
#include <Servo.h>

Servo s;
VL53L0X sensor;

void setup()
{
  Serial.begin(9600);
  s.attach(8);
  Wire.begin();
  sensor.setTimeout(500);
  if (!sensor.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
    delay(1000);
    while (1) {}
  }
  sensor.startContinuous();
}

long t = 0;
int angle = 0;
int da = 1;

void loop()
{
  if (millis() - t > 15)
  {
    if (da == 1) Serial.print(angle);
    else Serial.print(180 + (180 - angle));
    Serial.print("\t");
    Serial.print(sensor.readRangeContinuousMillimeters());
    Serial.print("\n");
    s.write(angle);
    angle += da;
    t = millis();
  }
  if (angle > 179) da = -1;
  if (angle <   1) da =  1;
}
