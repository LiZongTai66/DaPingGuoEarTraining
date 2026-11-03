/* DaPingGuo BLE / UART gateway, for App 1.1 and 1.2.
 * Test mode ONLY acknowledges PING and emergency stop, never pretends the FPGA works.
 * Normal mode: ESP32 stores/schedules songs; FPGA owns sound, mappings and live telemetry.
 */
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>
#include "protocol.h"
#include <esp_timer.h>

// FIRST USE: keep 1, connect USB only, verify the phone connects to DaPingGuo-Test.
// AFTER FPGA code + verified UART wiring: change to 0 and upload again.
#ifndef DPG_TEST_ONLY
#define DPG_TEST_ONLY 0
#endif
static constexpr int FPGA_RX=18; // ESP input, connects to FPGA esp_tx
static constexpr int FPGA_TX=17; // ESP output, connects to FPGA esp_rx
static constexpr uint32_t BAUD=115200;
static const char *SERVICE="6e400001-b5a3-f393-e0a9-e50e24dcca9e";
static const char *RX_UUID="6e400002-b5a3-f393-e0a9-e50e24dcca9e";
static const char *TX_UUID="6e400003-b5a3-f393-e0a9-e50e24dcca9e";

HardwareSerial fpga(1);
BLECharacteristic *txChar=nullptr;
BLE2902 *cccd=nullptr;
QueueHandle_t incoming=nullptr;
volatile bool connected=false, disconnected=false, incomingOverflow=false;
Decoder uartDecoder;
SongEvent song[MAX_EVENTS];
uint32_t expected=0, received=0, playingIndex=0;
bool receiving=false, songReady=false, playing=false;
uint64_t dueUs=0;
uint32_t lastPongMs=0, lastNotifyMs=0;
bool fpgaAlive=false;
uint8_t currentVoice=0,currentVolume=100;
static constexpr unsigned TX_DEPTH=256;
Frame notifyQueue[TX_DEPTH];unsigned notifyRead=0,notifyWrite=0,notifyCount=0;
bool notifyOverflow=false;

void queueNotify(const Frame &f){
 if(!connected)return;
 if(notifyCount==TX_DEPTH){notifyOverflow=true;return;}
 notifyQueue[notifyWrite]=f;notifyWrite=(notifyWrite+1)%TX_DEPTH;++notifyCount;
}
void errorReply(uint8_t code){queueNotify(Frame::make(0x82,code));}
void ack(const Frame &f){queueNotify(Frame::make(0x81,f.cmd(),f.a0(),f.a1()));}
void toFpga(const Frame &f){fpga.write(f.b,6);}
void stateReply(){queueNotify(Frame::make(0x85,playing?1:0,currentVoice,currentVolume));}
void stopSong(bool silence){
 playing=false;playingIndex=0;
 if(silence&&!DPG_TEST_ONLY)toFpga(Frame::make(0x03));
}
bool alive(){return fpgaAlive&&uint32_t(millis()-lastPongMs)<10000;}

class ServerCallbacks:public BLEServerCallbacks {
 void onConnect(BLEServer*) override {connected=true;Serial.println("BLE connected; waiting for subscription / protocol handshake");}
 void onDisconnect(BLEServer*) override {connected=false;disconnected=true;}
};
class RxCallbacks:public BLECharacteristicCallbacks {
 Decoder decoder;
 void onWrite(BLECharacteristic *c) override {
  auto value=c->getValue();Frame f;
  for(size_t i=0;i<value.length();++i)if(decoder.feed(uint8_t(value[i]),f)){
   if(xQueueSend(incoming,&f,0)!=pdTRUE)incomingOverflow=true;
  }
 }
};

uint32_t diagRxBytes=0,diagFrames=0,diagPongs=0,diagPhone=0,diagPhonePing=0;
uint32_t diagLastProbe=0,diagLastPrint=0,diagSeq=0;
int diagMapMode=-1,diagMapRevision=-1,diagLastCmd=-1;
uint8_t diagTail[12]={};unsigned diagTailCount=0,diagTailWrite=0;
void handlePhone(const Frame &f){
 ++diagPhone;if(f.cmd()==0x20)++diagPhonePing;
 if(DPG_TEST_ONLY){
  if(f.cmd()==0x20)queueNotify(Frame::count(0x83,f.arg()));
  else if(f.cmd()==0x03)ack(f);
  else errorReply(2); // Test mode does not claim downloads, mappings or sound succeeded.
  return;
 }
 switch(f.cmd()){
  case 0x20: toFpga(f);break; // PONG comes from the real FPGA, never fabricated here.
  case 0x10:{
   const uint32_t n=f.arg();
   if(n<1||n>MAX_EVENTS){errorReply(3);break;}
   stopSong(true);expected=n;received=0;receiving=true;songReady=false;ack(f);break;
  }
  case 0x11:
   if(!receiving){errorReply(4);break;}
   if(received>=expected||received>=MAX_EVENTS){receiving=false;songReady=false;errorReply(3);break;}
   if((f.a1()!=0&&(f.a1()<21||f.a1()>108))||(f.a1()==0&&f.a2()!=0)){
    receiving=false;songReady=false;errorReply(4);break;
   }
   song[received++]={f.a0(),f.a1(),f.a2()};break;
  case 0x12:
   if(f.arg()!=expected||received!=expected||expected==0||(!receiving&&!songReady)){
    receiving=false;songReady=false;errorReply(4);break;
   }
   receiving=false;songReady=true;queueNotify(Frame::count(0x84,received));break;
  case 0x13:
   if(!songReady||receiving){errorReply(4);break;}
   if(!alive()){errorReply(7);break;}
   if(!playing){
    toFpga(Frame::make(0x03));playingIndex=0;playing=true;
    dueUs=uint64_t(esp_timer_get_time())+uint64_t(song[0].dt)*5000;
   }
   ack(f);stateReply();break;
  case 0x14:stopSong(true);ack(f);stateReply();break;
  case 0x03:stopSong(false);toFpga(f);break;
  case 0x01:case 0x02:
   if(playing||receiving){errorReply(6);break;}
   toFpga(f);break;
  case 0x40:case 0x41:case 0x42:case 0x43:case 0x44:case 0x45:case 0x46:
   if(playing||receiving){errorReply(6);break;}
   toFpga(f);break;
  case 0x04:case 0x05:case 0x30:toFpga(f);break;
  default:errorReply(2);break;
 }
}
void pumpUart(){
 Frame f;
 while(fpga.available()){
  const uint8_t byte=uint8_t(fpga.read());++diagRxBytes;
  diagTail[diagTailWrite]=byte;diagTailWrite=(diagTailWrite+1)%12;if(diagTailCount<12)++diagTailCount;
  if(!uartDecoder.feed(byte,f))continue;
  ++diagFrames;diagLastCmd=f.cmd();
  if(f.cmd()==0x83)++diagPongs;
  if(f.cmd()==0x89){diagMapRevision=f.a0();diagMapMode=f.a1();}
  if(f.cmd()==0x83){lastPongMs=millis();fpgaAlive=true;}
  if(f.cmd()==0x86&&f.a0()<=1)currentVoice=f.a0();
  if(f.cmd()==0x81&&f.a0()==0x04)currentVoice=f.a1();
  if(f.cmd()==0x81&&f.a0()==0x05)currentVolume=f.a1();
  queueNotify(f);
 }
}
void pumpSong(){
 if(!playing)return;
 if(!alive()){stopSong(true);errorReply(7);stateReply();return;}
 // Absolute deadlines prevent loop/BLE processing time from accumulating into tempo drift.
 // Limit catch-up work so commands, heartbeat and stop remain responsive.
 for(int budget=0;budget<8&&playing;++budget){
  const uint64_t now=esp_timer_get_time();
  if(now<dueUs||fpga.availableForWrite()<6)return;
  const auto &e=song[playingIndex];
  if(e.note!=0)toFpga(Frame::make((e.flags&0x80)?0x01:0x02,e.note,e.flags&0x7f));
  ++playingIndex;
  if(playingIndex==received){
   playing=false;toFpga(Frame::make(0x03));stateReply();break;
  }
  dueUs+=uint64_t(song[playingIndex].dt)*5000;
 }
}
void pumpNotify(){
 if(!connected||!cccd->getNotifications()||notifyCount==0)return;
 if(uint32_t(millis()-lastNotifyMs)<2)return;
 uint8_t bytes[18];unsigned n=0;
 while(notifyCount&&n<3){memcpy(bytes+n*6,notifyQueue[notifyRead].b,6);notifyRead=(notifyRead+1)%TX_DEPTH;--notifyCount;++n;}
 txChar->setValue(bytes,n*6);txChar->notify();lastNotifyMs=millis();
 if(notifyOverflow&&notifyCount<TX_DEPTH){notifyOverflow=false;errorReply(8);}
}
bool protocolSelfTest(){
 static_assert(sizeof(SongEvent)==3,"Song event must be exactly three bytes");
 const Frame note=Frame::make(1,60,100);
 if(note.b[5]!=0x5e)return false;
 Decoder d;Frame out;int found=0;
 for(uint8_t b:note.b)if(d.feed(b,out))++found;
 if(found!=1||out.cmd()!=1||out.a0()!=60||out.a1()!=100)return false;
 d.reset();found=0;
 for(unsigned i=0;i<5;++i)if(d.feed(note.b[i],out))++found;
 const Frame ping=Frame::count(0x20,0x123456);
 for(uint8_t b:ping.b)if(d.feed(b,out))++found;
 return found==1&&out.cmd()==0x20&&out.arg()==0x123456;
}
// Probes traverse the real FPGA UART; no PONG is fabricated.
// The 0xFE prefix keeps diagnostic sequences separate from ordinary App sequences.
void pumpDiagnostic(){
 const uint32_t now=millis();
 if(!DPG_TEST_ONLY && !playing && !receiving && now-diagLastProbe>=2000 && fpga.availableForWrite()>=6){
  diagLastProbe=now;toFpga(Frame::count(0x20,0xFE0000 | ((++diagSeq)&0xFFFF)));
 }
 if(now-diagLastPrint<2000)return;diagLastPrint=now;
 if(!Serial)return;
 Serial.printf("DIAG ms=%lu BLE=%d SUB=%d phone=%lu phonePing=%lu probe=%lu RXbytes=%lu frames=%lu PONG=%lu lastCmd=%02X mapMode=%d rev=%d queue=%u tail=",
  (unsigned long)now,connected,cccd?cccd->getNotifications():0,
  (unsigned long)diagPhone,(unsigned long)diagPhonePing,(unsigned long)diagSeq,
  (unsigned long)diagRxBytes,(unsigned long)diagFrames,(unsigned long)diagPongs,
  diagLastCmd,diagMapMode,diagMapRevision,notifyCount);
 for(unsigned i=0;i<diagTailCount;++i)Serial.printf("%02X",diagTail[(diagTailWrite+12-diagTailCount+i)%12]);
 Serial.println();
}
void setup(){
 Serial.begin(115200);delay(400);Serial.println("DaPingGuo UART DIAGNOSTIC - temporary, existing features retained");
 if(!protocolSelfTest()){Serial.println("Protocol self-test FAILED");while(true)delay(1000);}
 Serial.println("Protocol self-test PASS");
 Serial.println(DPG_TEST_ONLY?"DaPingGuo TEST ONLY: no FPGA required; only PING/stop accepted":"DaPingGuo NORMAL: GPIO17 TX -> FPGA RX; GPIO18 RX <- FPGA TX");
 incoming=xQueueCreate(128,sizeof(Frame));
 if(!incoming){Serial.println("Queue allocation failed");while(true)delay(1000);}
 if(!DPG_TEST_ONLY){fpga.setRxBufferSize(4096);fpga.begin(BAUD,SERIAL_8N1,FPGA_RX,FPGA_TX);}
 BLEDevice::init(DPG_TEST_ONLY?"DaPingGuo-Test":"DaPingGuo");
 auto *server=BLEDevice::createServer();server->setCallbacks(new ServerCallbacks());
 auto *service=server->createService(SERVICE);
 txChar=service->createCharacteristic(TX_UUID,BLECharacteristic::PROPERTY_NOTIFY);
 cccd=new BLE2902();txChar->addDescriptor(cccd);
 auto *rx=service->createCharacteristic(RX_UUID,BLECharacteristic::PROPERTY_WRITE);
 rx->setCallbacks(new RxCallbacks());service->start();
 auto *adv=BLEDevice::getAdvertising();adv->addServiceUUID(SERVICE);adv->setScanResponse(true);
 adv->setMinPreferred(0x06);adv->setMaxPreferred(0x12);BLEDevice::startAdvertising();
 Serial.println("Advertising started. Use App -> BLE scan; do not pair as classic Bluetooth.");
}
void loop(){
 if(disconnected){
  disconnected=false;stopSong(true);receiving=false;songReady=false;
  notifyCount=notifyRead=notifyWrite=0;notifyOverflow=false;
  xQueueReset(incoming);uartDecoder.reset();fpgaAlive=false;
  cccd->setNotifications(false);BLEDevice::startAdvertising();
 }
 if(incomingOverflow){incomingOverflow=false;stopSong(true);receiving=false;songReady=false;errorReply(8);}
 if(!DPG_TEST_ONLY)pumpUart();
 Frame f;
 for(int i=0;i<8&&xQueueReceive(incoming,&f,0)==pdTRUE;++i)handlePhone(f);
 if(!DPG_TEST_ONLY)pumpSong();
 pumpNotify();pumpDiagnostic();delay(1);
}

