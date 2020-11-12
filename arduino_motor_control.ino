#include <SoftwareSerial.h> //시리얼 통신 라이브러리 호출

#define RT_A1 8 //오른쪽 바퀴
#define RT_B1 9 //오른쪽 바퀴
#define LEFT_A2 6 //오른쪽 바퀴
#define LEFT_B2 7 //오른쪽 바퀴


char value;
int moving = 0;


void DriveLeftMotorA();
void DriveLeftMotorS();
void DriveLeftMotorR();
void DriveLeftMotorL();

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);   //시리얼모니터 
    pinMode(LEFT_A2, OUTPUT);
    pinMode(LEFT_B2, OUTPUT);
    pinMode(RT_A1, OUTPUT);
    pinMode(RT_B1, OUTPUT);
    
//  pinMode(RIGHT_A2, OUTPUT);
//  pinMode(LEFT_B1, OUTPUT);
//  pinMode(RIGHT_B2, OUTPUT);  
  
  Serial.println("Neuro Car is ready to start");
}

void loop() {
  // put your main code here, to run repeatedly:

     while(Serial.available()){
      value = Serial.read();

      if(value=='a') {
        moving = 1;
      }

     if(moving=='1');
     {
        Serial.println(" ::Test Left Motor Front");
        DriveLeftMotorF();
     }
     if(value=='B' && moving=='1')
     {
        Serial.println(" ::Test Left Motor Back");
        DriveLeftMotorB();
     }
     if(value=='s' && moving=='1')
     {
        Serial.println(" ::Test Left Motor Stop");
        DriveLeftMotorS();
        moving = 0;
        
     }
     if(value=='l' && moving=='1')
     {
        Serial.println(" ::Test Left Motor Stop");
        DriveLeftMotorL();
        value = 'a';
     }
     if(value=='r' && moving=='1')
     {
        Serial.println(" ::Test Left Motor Stop");
        DriveLeftMotorR();
        value = 'a';
     }

     
   }

}

void DriveLeftMotorF()
{
    digitalWrite(LEFT_A2, HIGH);
    digitalWrite(LEFT_B2, LOW);
    digitalWrite(RT_A1, HIGH);
    digitalWrite(RT_B1, LOW); 
}

void DriveLeftMotorB()
{
    digitalWrite(LEFT_A2, LOW);
    digitalWrite(LEFT_B2, HIGH);
    digitalWrite(RT_A1, LOW);
    digitalWrite(RT_B1, HIGH);
}

void DriveLeftMotorS()
{
    digitalWrite(LEFT_A2, LOW);
    digitalWrite(LEFT_B2, LOW);
    digitalWrite(RT_A1, LOW);
    digitalWrite(RT_B1, LOW);
}

void DriveLeftMotorL()
{
    digitalWrite(LEFT_A2, LOW);
    digitalWrite(LEFT_B2, HIGH);
    digitalWrite(RT_A1, HIGH);
    digitalWrite(RT_B1, LOW);
    delay(1500);
    digitalWrite(LEFT_A2, HIGH);
    digitalWrite(LEFT_B2, LOW);
    digitalWrite(RT_A1, HIGH);
    digitalWrite(RT_B1, LOW); 
    delay(3000);
    digitalWrite(LEFT_A2, HIGH);
    digitalWrite(LEFT_B2, LOW);
    digitalWrite(RT_A1, LOW);
    digitalWrite(RT_B1, HIGH);
    delay(1500);
}

void DriveLeftMotorR()
{
    digitalWrite(LEFT_A2, HIGH);
    digitalWrite(LEFT_B2, LOW);
    digitalWrite(RT_A1, LOW);
    digitalWrite(RT_B1, HIGH);
    delay(1500);
    digitalWrite(LEFT_A2, HIGH);
    digitalWrite(LEFT_B2, LOW);
    digitalWrite(RT_A1, HIGH);
    digitalWrite(RT_B1, LOW); 
    delay(3000);
    digitalWrite(LEFT_A2, LOW);
    digitalWrite(LEFT_B2, HIGH);
    digitalWrite(RT_A1, HIGH);
    digitalWrite(RT_B1, LOW);
    delay(1500);
}
