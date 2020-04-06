let c1, c2;
let pad;
let frame = 30; // framerate
let t = 0, dt = 1 / frame;
let fmin = .2, fmax = .5, df = .001, f = .5; // Hertz
let amplitude = 100.0; // Height of wave
let yvalues, ysize = frame; // Using an array to store height values for the wave
let strokeWidth = 5;
let background;

function setup() {
  createCanvas(windowWidth, windowHeight);
  frameRate(frame);
  pad = Math.ceil(width / ysize) + 5; // pad between each point on screen
  // Define colors
  c1 = color("white");
  c2 = color(bkg_color); //Color to change with emotion
  background = select("#emo-context");
  background.style("background", c2);
  yvalues = new Array(ysize);
}

function draw() {
  c2 = color(bkg_color);
  background.style("background", c2);
  clear();
  calcWave();
  renderWave();
}

function calcWave() {
  // For every x value, calculate a y value with sine function
  let x = TWO_PI * f * t;
  let y = 0;
  switch(emotion) {
    case "happiness":
      y = sin(x) * amplitude; // sine
      break;
    case "surprise":
      y = sin(x) * amplitude; // sine
      break;
    case "anger":
      y = sin(x) * amplitude; // sine
      break;
    case "contempt":
      y = sin(x) * amplitude; // sine
      break;
    case "disgust":
      y = sin(x) * amplitude; // sine
      break;
    case "fear":
      y = sin(x) * amplitude; // sine
      break;
    case "sadness":
      y = (x * amplitude) % 150; // saw
      break;
    case "neutral":
      y = 1  ; // line
      break;
    default:
      y = (x % 5) < 5/2 ? x*amplitude : 0; // square
      break;
  }
  t += dt;
  yvalues.splice(0, 1); // remove first element
  yvalues.splice(yvalues.length - 1, 0, y); // add the last
}

function renderWave() {
  blendMode(ADD);
  strokeWeight(strokeWidth);
  stroke(0,99);
  fill(220);
  beginShape();
  vertex(0 - strokeWidth, height);
  vertex(0 - strokeWidth,height/2);
  // A simple way to draw the wave with an ellipse at each location
  for (let x = 0; x <= yvalues.length; x++) {
    vertex(x * pad, (height/2) + yvalues[x]);
  }
  vertex(width + strokeWidth, height/2);
  vertex(width + strokeWidth, height);
  endShape();
}