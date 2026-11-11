import wave,math,struct
rate=22050
with wave.open('/tmp/cyberslap_audio.wav','wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate)
 for n in range(rate*10):
  t=n/rate;v=.065*math.sin(2*math.pi*220*t)+.04*math.sin(2*math.pi*330*t)
  for hit in (3.7,5.35,6.1):
   d=t-hit
   if 0<=d<.23:v+=.23*math.exp(-22*d)*math.sin(2*math.pi*380*d)
  v*=max(0,min(1,t*3,(10-t)*3))
  w.writeframesraw(struct.pack('<h',int(max(-1,min(1,v))*32767)))
