import http.client
import xml.etree.ElementTree as ET
import time
import socket

#poll OpenSong to find which slide type is shown
class OSPoller:
    NOTRUNNING=-2
    TIMEOUT=-1
    BLANK=0
    SONG=1
    SCRIPTURE=2
    CUSTOM=3
    EXTERNAL=4
    IMAGE=5
    NOCHANGE=99
    
    def __init__(self, url):
        self.url = url

        self.running = False   #presentation started
        self.oldMode = False   #Slide mode (hidden/freeze/normal)
        self.oldType="-"       #slide type song/bible,etc
        self.conn = http.client.HTTPConnection(self.url, timeout=10)
        
    def get_xml(self,uri):
        self.conn.request("GET", uri)
        r1 = self.conn.getresponse()
        res = r1.read()
        return ET.fromstring(res)


    def poll(self):       
        try:  
            q = self.get_xml("/presentation/status")
            self.running = q.find("presentation").get("running")=="1"
            if not self.running:
                return self.NOTRUNNING
            
            slidelist = self.get_xml("/presentation/slide/list")
            q = self.get_xml("/presentation/status")

            slide = q.find("presentation/slide").get("itemnumber")
            mode = q.find("presentation/screen").get("mode")=="N"   #normal mode means slide is visible
            info = slidelist.find("slide[@identifier='{0}']".format(slide))
            n = info.get("type")

            #TODO: when slide is hidden:
            #if mode and not self.oldMode:
            #    print("Show");
            #elif not mode and self.oldMode:
            #    print("Hide");
            
            retval = self.NOCHANGE
            if n != self.oldType:
                if n == "scripture":
                    retval = self.SCRIPTURE
                elif n == "blank":
                     retval = self.BLANK
                elif n == "custom":
                     retval = self.CUSTOM
                elif n == "song":
                    retval = self.SONG
                elif n == "image":
                    retval = self.IMAGE
                else:
                    print("unkown type:{0}".format(n))

            self.oldMode=mode
            self.oldType=n
            return retval
            
        except (ConnectionRefusedError,ConnectionResetError,http.client.CannotSendRequest):
            return self.TIMEOUT
        except socket.timeout:
            return self.TIMEOUT
            
    def Close(self):
        self.conn.close()
        
if __name__ == "__main__":
    g = OSPoller('192.168.0.191:8082')
    for i in range(10):
        
        start = time.time()
        print(g.poll())
        end = time.time()
        print(end - start)
        time.sleep(0.5)
    g.Close()
