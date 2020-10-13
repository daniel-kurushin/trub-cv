#include <Stepper.h>

#define STEPS 200
#define LIMIT_A A1
#define LIMIT_B A2

Stepper a_stepper(STEPS, 6, 7, 8, 9);

void setup()
{
  a_stepper.setSpeed(10);
  Serial.begin(9600);
}

void go(int steps)
{
  analogWrite( 5, 63);
  analogWrite(10, 63);
  a_stepper.step(steps);
}

int x = 10;
String tstates[] = {"ST_IDLE", "ST_LIMIT_A", "ST_GO_A", "ST_LIMIT_B", "ST_GO_B", "ST_ERROR"};
enum tstate {ST_IDLE, ST_LIMIT_A, ST_GO_A, ST_LIMIT_B, ST_GO_B, ST_ERROR};
tstate state = ST_IDLE;

void loop()
{
  switch (state)
  {
    case ST_IDLE:
      delay(1000);
      if (! digitalRead(LIMIT_A)) state = ST_LIMIT_A;
      else if (! digitalRead(LIMIT_B)) state = ST_LIMIT_B;
      else state = ST_GO_A;
      break;
    case ST_LIMIT_A:
      analogWrite( 5, 0);
      analogWrite(10, 0);
      delay(1000);
      state = ST_GO_B;
      break;
    case ST_LIMIT_B:
      analogWrite( 5, 0);
      analogWrite(10, 0);
      delay(1000);
      state = ST_GO_A;
      break;
    case ST_GO_A:
      if (digitalRead(LIMIT_A)) go( 10);
      else state = ST_LIMIT_A;
      break;
    case ST_GO_B:
      if (digitalRead(LIMIT_B)) go(-10);
      else state = ST_LIMIT_B;
      break;
    case ST_ERROR:
      analogWrite( 5, 0);
      analogWrite(10, 0);
  }
}
