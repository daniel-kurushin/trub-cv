#include <Stepper.h>

#define STEPS 200
#define LIMIT_A A1
#define LIMIT_B A2
#define FAST 2
#define SLOW 3

#define ON_LIMIT_A ! digitalRead(LIMIT_A)
#define ON_LIMIT_B ! digitalRead(LIMIT_B)

#define GO_FAST digitalRead(FAST) == 0 && digitalRead(SLOW) == 1
#define GO_SLOW digitalRead(FAST) == 1 && digitalRead(SLOW) == 0
#define GO_NONE digitalRead(FAST) == 1 && digitalRead(SLOW) == 1

#define SP_NONE   0
#define SP_SLOW   8
#define SP_FAST 100

enum tstate {ST_IDLE, ST_LIMIT_A, ST_GO_A, ST_LIMIT_B, ST_GO_B, ST_STOP};

Stepper a_stepper(STEPS, 6, 7, 8, 9);

int read_speed()
{
  if (GO_FAST) return SP_FAST;
  if (GO_SLOW) return SP_SLOW;
  if (GO_NONE) return SP_NONE;  
}

void setup()
{
  a_stepper.setSpeed(SP_SLOW);
  Serial.begin(9600);
  pinMode( 5, 1);
  pinMode(10, 1);
  pinMode(FAST, 0);
  pinMode(SLOW, 0);
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

tstate state = ST_IDLE;
tstate old_state = state;
int current_speed = 0;
int old_speed = 0;

void loop()
{
  current_speed = read_speed();
  if (current_speed != old_speed) 
  {
    old_speed = current_speed;
    disable();
    if (current_speed != SP_NONE) a_stepper.setSpeed(current_speed);
    else {
      old_state = state;
      state = ST_STOP;
    }
    delay(100);
  }
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
    case ST_STOP:
      disable();
      if (current_speed != SP_NONE) 
      { 
        a_stepper.setSpeed(current_speed);
        state = old_state;
      }
      break;
  }
}
