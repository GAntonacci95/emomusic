Shape myShape;
boolean increase=true;
color emo = color(255,0,0);
float curve = 6;
float speed = 1;
//Shape myShape2;
//Shape myShape3;

void setup(){
  size(500,500);
  myShape = new Shape(emo,curve,speed); //first argument is color, second the curvature of the corners
 // myShape2 = new Shape(color(255,0,0),6,2);
 // myShape3 = new Shape(color(255,0,0),6,2);
}

void draw(){
  background(255,0,0);
  myShape.display();
  myShape.drive();
  //myShape2.display();
 // myShape2.drive();
 // myShape3.display();
 // myShape3.drive();
}

class Shape{
  color c; 
  float edge;
  float speed;
  float inc;
  float xpos;
  float ypos;
  
  Shape(color tempc, float tempedge, float tempspeed){ //  float tempinc  float tempval
    c = tempc; 
    edge = tempedge;
    speed = tempspeed;
    //val = tempval;
    inc = 1;
    xpos = width/2;
    ypos = height/2;
  }
  
  void display(){
    rectMode(CENTER);
    fill(c);
    rect(xpos,ypos,10+inc,10+inc,edge);
    
  }
  
  void drive(){
    if (inc <width/2 && increase){
      inc++;
    }
    else {
      inc--;
      increase=false;
      if (inc <= 0) {
        increase=true;
      }
    }
}
}
    
    
  
 
