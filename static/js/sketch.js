var c1, c2;

let xspacing = 1; // Distance between horizontal location
let w; // width
let theta = 0.0; // Start angle at 0
let amplitude = 100.0; // Height of wave
let period = 1000.0; // How many pixels before the wave repeats
let dx; // Value for incrementing x
let yvalues; // Using an array to store height values for the wave
let emotion = "angry";



function setup() {
  createCanvas(windowWidth, windowHeight);
  // Define colors
  c1 = color("white");
  c2 = color("yellow"); //Color to change with emotion

  w = width + 16;
  dx = (TWO_PI / period) * xspacing;
  yvalues = new Array(floor(w));

}

function draw() {
  setGradient(c1, c2);
  //frameRate(30);
  strokeWeight(1);
  ellipse(mouseX, mouseY, 30, 30);
  calcWave();
  renderWave();
}

function setGradient(c1, c2) {
  // noprotect
  noFill();
  for (var y = 0; y < height; y++) {
    var inter = map(y, 0, height, 0, 1);
    var c = lerpColor(c1, c2, inter);
    stroke(c);
    line(0, y, width, y);
  }
}

function calcWave() {
  // Increment theta (try different values for
  // 'angular velocity' here)
  theta += 0.02;

  // For every x value, calculate a y value with sine function
  let x = theta;
  for (let i = 0; i < yvalues.length; i++) {
    switch(emotion) {
      case "happy":
        yvalues[i] = sin(x) * amplitude; // sine
        break;
      case "angry":
        yvalues[i] = (x * amplitude) % 150; // saw
        break;
      default:
        yvalues[i] = (x % 5) < 5/2 ? x*amplitude : 0; // square
        break;
    }
    x += dx;
    if(x < 5) {
      emotion = "happy";
    } else {
      emotion = "angry";
    }
  }
}

function renderWave() {
  strokeWeight(5);
  stroke(0,99);
  noFill();
  beginShape();
  vertex(0, height);
  vertex(0,height/2)
  // A simple way to draw the wave with an ellipse at each location
  for (let x = 0; x <= yvalues.length; x++) {
    vertex(x, (height/2) + yvalues[x]);
  }
  vertex(width, height/2);
  vertex(width, height);
  endShape();
}