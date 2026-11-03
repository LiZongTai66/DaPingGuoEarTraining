#pragma once
#include <stdint.h>
#include <stddef.h>
struct Frame {
 uint8_t b[6];
 uint8_t cmd()const{return b[1];}
 uint8_t a0()const{return b[2];} uint8_t a1()const{return b[3];}uint8_t a2()const{return b[4];}
 uint32_t arg()const{return (uint32_t(b[2])<<16)|(uint32_t(b[3])<<8)|b[4];}
 static Frame make(uint8_t c,uint8_t a=0,uint8_t b=0,uint8_t d=0){return Frame{{0xAA,c,a,b,d,uint8_t(~uint8_t(c+a+b+d))}};}
 static Frame count(uint8_t c,uint32_t n){return make(c,n>>16,n>>8,n);}
};
class Decoder {
 uint8_t w[6]={};uint8_t used=0;
 public:
 void reset(){used=0;}
 bool feed(uint8_t byte,Frame &out){
  if(used<6)w[used++]=byte;else{for(int i=0;i<5;++i)w[i]=w[i+1];w[5]=byte;}
  if(used==6&&w[0]==0xAA&&w[5]==uint8_t(~uint8_t(w[1]+w[2]+w[3]+w[4]))){
   for(int i=0;i<6;++i)out.b[i]=w[i];used=0;return true;
  }
  return false;
 }
};
struct SongEvent {uint8_t dt,note,flags;};
constexpr uint32_t MAX_EVENTS=16000;
