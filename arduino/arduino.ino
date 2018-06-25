//用户信息,用户信息，需要填改写成自己的
#define UID "1" //用户uid
#define DIVICEID "1" 
#define LED1ID "1"
#define LED2ID "2"
#define DHT11_TID "3"
#define DHT11_HID "4"
#define LED1PIN 2
#define LED2PIN 3

#define KEY "a53b177974c6705d5235e755fe8bb397" //用户KEY

#include<dht11.h>
dht11 DHT11;
#include <SoftwareSerial.h>
SoftwareSerial DebugSerial(10, 11);//rx tx

#define MAX_PACKETSIZE 512
//uartdata
char buffUart[MAX_PACKETSIZE];
unsigned int buffUartIndex=0;
unsigned long preUartTick=millis();

unsigned long updataTick=millis();

unsigned long subscribeTick=millis();
bool subscribeFlag =false;


/*
  * 发送数据到串口
 */
void sendUART(char *p,size_t len)
{
  DebugSerial.println("[UART send:]");
  DebugSerial.println(p);
  Serial.write(p,len);
}

/*
  * 发送数据到串口
 */
void sendUART(char *p)
{
  DebugSerial.println("[UART send:]");
  DebugSerial.println(p);
  Serial.print(p);
}


/*
  读取传感器数据并上传
 */
void doUpdata()
{
  if(millis()-updataTick >5*1000){//5s上传一次数据
    updataTick=millis();

    int chk = DHT11.read(DHT11_PIN);
    switch (chk)
      {
        case DHTLIB_OK: 
              DebugSerial.println("OK"); 
              break;
        case DHTLIB_ERROR_CHECKSUM: 
              DebugSerial.println("Checksum error"); 
              break;
        case DHTLIB_ERROR_TIMEOUT: 
              DebugSerial.println("Time out error"); 
              break;
        default: 
              DebugSerial.println("Unknown error"); 
              break;
      }

      char str[128]; memset(str,0,128);
      sprintf(str, "cmd=upload&deviceID=%s&value=%d\r\n", 
        DHT11_TID , (int)DHT11.temperature);
      sendUART(str);
      memset(str,0,128);
      sprintf(str, "cmd=upload&deviceID=%s&value=%d\r\n", 
        DHT11_HID , (int)DHT11.humidity);
      sendUART(str);
  }
}


void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
  pinMode(LED1PIN ,OUTPUT);
  pinMode(LED2PIN ,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Hello world");
  delay(500);
}
