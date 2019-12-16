import http.requests.*;
import processing.video.*;

PostRequest req;
Capture cam;

PImage im;
String b64enc, resp;

int lastCaptureTime;
int currentCaptureTime;

void setup() {
  size(640,480);
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
    lastCaptureTime = millis();
  }
}

void draw() {
  // image retrieval and send...
  currentCaptureTime = millis();
  if (currentCaptureTime - lastCaptureTime > 3000 && cam.available()) { // for now each 3s send an acquired image
    cam.read();
    im = (PImage)cam;
    
    println(im.toString()); // actually should retrieve b64 or some kind of bitstream...
    req = new PostRequest("localhost"); // port?, unfortunately there's need for reinstantiation
    req.addData("file", im.toString());
    req.send();
    resp = req.getContent();
    lastCaptureTime = currentCaptureTime;
  }
}
