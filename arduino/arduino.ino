//用户信息,用户信息，需要填改写成自己的
#define UID "1" //用户uid
#define DIVICEID "1" 
#define LED1ID "1"
#define LED2ID "2"
#define DHT11_TID "3"
#define DHT11_HID "4"
#define LED1PIN 2
#define LED2PIN 9
#define DHT11_PIN  4 //温湿度传感器接UNO的gpio2
#define RELAYS_ON "1"
#define RELAYS_OFF "0"


#define KEY "a53b177974c6705d5235e755fe8bb397" //用户KEY

#include <dht11.h>
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
bool subscribeFlag =true;

/*
  检查并读取串口收到的数据
*/
void doUartTick()
{
  
  if (Serial.available())
  {
    buffUart[buffUartIndex++] = Serial.read();
    preUartTick = millis();
    if(buffUartIndex>=MAX_PACKETSIZE - 1){
      buffUartIndex = MAX_PACKETSIZE-2;
      preUartTick = preUartTick - 200;
    }
  }
  if(buffUartIndex>0 && (millis() - preUartTick>=100))
  {
    buffUart[buffUartIndex]=0x00;
    //Serial.flush();
    parseUartPackage(buffUart,buffUartIndex);
    buffUartIndex = 0;
  }
}    
/*
  处理串口收到的数据
 */
void parseUartPackage(char *p,size_t len)
{
 // DebugSerial.println("[UART Read:]");
 // DebugSerial.println(p);
  
 if (strstr(p,"cmd=upload&res=1") != NULL)
  {   
      DebugSerial.println("upload successful...");
  }
  else if (strstr(p,"cmd=subscribe&res=1") != NULL)
  {
      subscribeFlag=true;
      DebugSerial.println("Subscribe uid successful...");
  }
  else
  {
        setDigitalPin(p,LED1ID,LED1PIN);
        setDigitalPin(p,LED2ID,LED2PIN);
  }

}

void setDigitalPin(char *p,String sensorID,int pin)
{
     char relaysStr[64]; memset(relaysStr,0,64);
     
      
      sprintf(relaysStr,"cmd=publish&sensorid=%s&state=",sensorID.c_str());
      //DebugSerial.println(relaysStr);
    if (strstr(p,relaysStr) != NULL)
    {
        DebugSerial.print(sensorID);
        DebugSerial.println(strstr(p,relaysStr));
        
        if (strstr(strstr(p,"sensorid=")+strlen(relaysStr),RELAYS_ON) != NULL)
      {
        digitalWrite(pin, HIGH); //打开继电器
        DebugSerial.println("open relays!");
      }
      else if (strstr(strstr(p,relaysStr)+strlen(relaysStr),RELAYS_OFF) != NULL)
      {
        digitalWrite(pin, LOW); //关闭继电器
        DebugSerial.println("Close relays!");
      }
    }
}
     
/*
  * 发送数据到串口
 */
void sendUART(char *p,size_t len)
{
  //DebugSerial.println("[UART send:]");
  //DebugSerial.println(p);
  Serial.write(p,len);
}

/*
  * 发送数据到串口
 */
void sendUART(char *p)
{
  //DebugSerial.println("[UART send:]");
  //DebugSerial.println(p);
  Serial.print(p);
}

/*
  订阅用户，用于接受数据
 */
void doSubscribe()
{
  if(  millis() - subscribeTick > 2000 ) {
    subscribeTick=millis();
      char suid[64]; memset(suid,0,64);
    //sprintf(suid , "cmd=subscribe&userid=%s\n\r" , UID);
    sprintf(suid , "cmd=publish&userid=%s&sensorid=1" , UID);
    sendUART(suid);
    delay(500);
    sprintf(suid , "cmd=publish&userid=%s&sensorid=2" , UID);
    sendUART(suid);
  }
}
/*
  读取传感器数据并上传
 */
void doUpdata()
{
  if(millis()-updataTick >2*1000){//5s上传一次数据
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
      sprintf(str, "cmd=upload&sensorid=%s&value=%d\r\n", 
        DHT11_TID , (int)DHT11.temperature);
      sendUART(str);
      memset(str,0,128);
      sprintf(str, "cmd=upload&sensorid=%s&value=%d\r\n", 
        DHT11_HID , (int)DHT11.humidity);
      sendUART(str);
  }
}


void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
DebugSerial.begin(9600);
  pinMode(LED1PIN ,OUTPUT);
  pinMode(LED2PIN ,OUTPUT);
  digitalWrite(LED1PIN,HIGH);
}

void loop() {
  doSubscribe();
  //doUpdata();
  doUartTick();
}
