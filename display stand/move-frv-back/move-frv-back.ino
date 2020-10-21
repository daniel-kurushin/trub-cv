#include <Stepper.h>

#define STEPS 200
#define LIMIT_A A1
#define LIMIT_B A2
#define ON_LIMIT_A ! digitalRead(LIMIT_A)
#define ON_LIMIT_B ! digitalRead(LIMIT_B)


Stepper a_stepper(STEPS, 6, 7, 8, 9);

void setup()
{
  a_stepper.setSpeed(8);
  Serial.begin(9600);
  pinMode( 5, 1);
  pinMode(10, 1);
}

void enable()
{
  digitalWrite( 5, 1);
  digitalWrite(10, 1);
}

void disable()
{
  digitalWrite( 5, 0);
  digitalWrite(10, 0);
}

void go(int steps)
{
  enable();
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
      delay(3000);
      if (ON_LIMIT_A) state = ST_LIMIT_A;
      else if (ON_LIMIT_B) state = ST_LIMIT_B;
      else state = ST_GO_A;
      break;
    case ST_LIMIT_A:
      disable();
      delay(3000);
      state = ST_GO_B;
      break;
    case ST_LIMIT_B:
      disable();
      delay(3000);
      state = ST_GO_A;
      break;
    case ST_GO_A:
      if (ON_LIMIT_A) state = ST_LIMIT_A;
      else go(-10);
      break;
    case ST_GO_B:
      if (ON_LIMIT_B) state = ST_LIMIT_B;
      else go( 10);
      break;
    case ST_ERROR:
      disable();
  }
}
