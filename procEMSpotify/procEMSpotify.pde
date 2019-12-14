import http.requests.*;
import processing.video.*;

PostRequest req;
Capture cam;

PImage im;
String b64, resp;

int begunAt;

void setup() {
  size(640,480);
  req = new PostRequest("localhost");
  String[] cameras = Capture.list();
  
  if (cameras.length == 0) {
    println("There are no cameras available for capture.");
    exit();
  } else {
    println("Available cameras:");
    for (int i = 0; i < cameras.length; i++) {
      println(cameras[i]);
    }
    
    cam = new Capture(this, cameras[0]);
    cam.start();
    begunAt = millis();
  }
}

void draw() {
  // image retrieval and send...
  if (millis()-begunAt > 3000 && cam.available()) { // for now each 30 seconds send an acquired image
    cam.read();
    im = (PImage)cam;
    
    println(im.toString()); // actually should retrieve b64 or some kind of bitstream...
    req.addData("file", im.toString());
    req.send();
    resp = req.getContent();
  }
}
