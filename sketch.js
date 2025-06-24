//hello and welcome to my visualiser art piece!
//for the best viewing and interaction please view this on full screen ! 

let table;
let colors = [];
let animatingColors = [];
let phase = 0;
let showBlocks = false;
let waveParticles = [];
let ribbons = [];
let startTime;
let babydollFont;
let moodSelect;
let moodChosen = false;
let transitionProgress = 0;
let transitioning = false;
let currentMood = '';
let nextMood = '';
let currentSong;
let selectedAlbumImg = null;
let selectedAlbumUrl = null;
let words = ['Music', 'In', 'Motion'];
let spread = 0;
let targetSpread = 0;
let noiseOffset = 0;


//custom font
function preload() {
  babydollFont = loadFont('fonts/BabyDoll.ttf');
}

//homepage set up

class FloatingWord {
  constructor(word) {
    this.word = word;
    this.x = random(width);
    this.y = random(height);
    this.vx = random(-1, 1);
    this.vy = random(-1, 1);
    this.hue = random(360);
    this.size = 48;
  }

  update() {
    this.x += this.vx;
    this.y += this.vy;
    if (this.x < 0 || this.x > width) this.vx *= -1;
    if (this.y < 0 || this.y > height) this.vy *= -1;
    this.hue = (this.hue + 1) % 360;
  }

  display() {
    textFont(babydollFont);
    textSize(this.size);
    textAlign(CENTER, CENTER);
    text(this.word, this.x, this.y);
  }
}

let floatingWords = [];

function setup() {
  createCanvas(windowWidth, windowHeight);
  noStroke();
  colorMode(HSB, 360, 100, 100, 100);
  background(0);
  textFont(babydollFont);
  textSize(48);
  textAlign(CENTER, CENTER);


  floatingWords = [
    new FloatingWord('Music'),
    new FloatingWord('In'),
    new FloatingWord('Motion')
  ];

  //mood selection menu
  moodSelect = createSelect();
  moodSelect.position(20, 20);
  moodSelect.option('Select Mood');
  moodSelect.option('happy');
  moodSelect.option('sad');
  moodSelect.option('mellow');
  moodSelect.option('angry');
  moodSelect.option('romantic');
  moodSelect.option('premadehappy');
  moodSelect.option('premadesad');
  moodSelect.option('premademellow');
  moodSelect.option('premadeangry');
  moodSelect.option('premaderomantic');
  moodSelect.changed(() => {
    nextMood = moodSelect.value();
    if (nextMood !== 'Select Mood' && nextMood !== currentMood) {
      transitionOut();
    }
  });
//shooting stars after choosing a mood position
  for (let i = 0; i < 900; i++) {
    waveParticles.push(new FlowParticle());
  }
}

function normalizeMood(mood) {
  if (mood.startsWith('premade')) {
    return mood.replace('premade', '');
  }
  return mood;
}
//fading in and out shooting star animations 
function transitionOut() {
  transitioning = true;
  transitionProgress = 1;
  showBlocks = false;
  selectedAlbumImg = null;
  selectedAlbumUrl = null;
}

function transitionIn() {
  transitioning = false;
  transitionProgress = 0;
  loadMoodCSV(nextMood);
  playRandomSong(nextMood);

  if (colors.length > 0) {
    for (let p of waveParticles) {
      let c = random(colors).c;
      p.color = color(hue(c), saturation(c), brightness(c), 40);
    }
  }
}
//loading relevant csv for the selected mood
function loadMoodCSV(mood) {
  let file = `${mood}_playlist_data.csv`;
  loadTable(file, 'csv', 'header',
    (loaded) => {
      console.log(` Loaded: ${file}`);
      table = loaded;
      currentMood = mood;
      moodChosen = true;
      parseTable();
    },
    () => {
      console.error(` Failed to load: ${file}`);
    }
  );
}

function parseTable() {
  colors = [];
  animatingColors = [];
  ribbons = [];
  startTime = millis();

  for (let i = 0; i < table.getRowCount(); i++) {
    const row = table.getRow(i);
    let raw = row.get('dominant_color');
    let bpm = parseFloat(row.get('bpm'));
    let title = row.get('track');
    let album = row.get('art_url');

    if (raw) {
      let rgb = raw.replace(/[()]/g, '').split(',').map(n => parseInt(n.trim()));
      if (rgb.length === 3) {
        let baseColor = color(`rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`);
        colors.push({ c: baseColor, name: title, album });
        ribbons.push(new Ribbon(baseColor, bpm));
      }
    }
  }

  setTimeout(() => {
    showBlocks = true;
    let angleStep = TWO_PI / colors.length;
    let outerRadius = min(width, height) / 2.2;

    for (let i = 0; i < colors.length; i++) {
      let angle = i * angleStep + random(-0.2, 0.2);
      let x = width / 2 + cos(angle) * outerRadius + random(-30, 30);
      let y = height / 2 + sin(angle) * outerRadius + random(-30, 30);
      animatingColors.push({
        c: colors[i].c,
        name: colors[i].name,//trackname
        album: colors[i].album,//album both to find the appropriate colour to display
        bpm: ribbons[i].bpm, // include bpm for pulsing
        x: x,
        y: y,
        offset: random(TWO_PI)
      });
    }
  }, 6000);
}

function draw() {
  background(0, 3);

  if (transitioning) {
    transitionProgress -= 0.02;
    if (transitionProgress <= 0) {
      transitionProgress = 0;
      transitionIn();
    }
  } else if (transitionProgress < 1 && moodChosen) {
    transitionProgress += 0.02;
  }

  if (!moodChosen) {
    background(10);
    stroke(255, 150, 200);
    strokeWeight(2);
    noFill();

    let centerX = width / 2;
    let centerY = height / 2;

    // Draw waveform
    beginShape();
    let points = 100;
    for (let i = 0; i < points; i++) {
      let angle = TWO_PI / points * i;
      let noiseVal = noise(noiseOffset + i * 0.1);
      let r1 = 50 + noiseVal * 60;
      let r2 = 100 + noiseVal * 80;
      let radius = i % 2 === 0 ? r1 : r2;
      let x = centerX + cos(angle) * radius;
      let y = centerY + sin(angle) * radius;
      vertex(x, y);
    }
    endShape(CLOSE);

    noiseOffset += 0.01;

    // Hover interaction
    let overText = dist(mouseX, mouseY, centerX, centerY) < 100;
    targetSpread = overText ? 200 : 0;
    spread = lerp(spread, targetSpread, 0.1);

    // Draw words
    fill(255);
    noStroke();
    for (let i = 0; i < words.length; i++) {
      let angle = map(i, 0, words.length, -PI / 4, PI / 4);
      let x = centerX + cos(angle) * spread;
      let y = centerY + sin(angle) * spread;
      text(words[i], x, y);
    }
  }

  // Show waveParticles only after mood is chosen and before blocks show
  if (moodChosen && !showBlocks) {
    for (let p of waveParticles) {
      p.update();
      p.display();
    }
  } else if (showBlocks) {
    for (let r of ribbons) {
      r.update();
      r.display();
    }

    let time = millis() / 1000.0;
    for (let i = 0; i < animatingColors.length; i++) {
      let col = animatingColors[i];
      let beatFreq = col.bpm / 60.0;
      let bounce = sin(TWO_PI * beatFreq * time + col.offset) * 10;
      let twinkle = abs(sin(TWO_PI * beatFreq * time + col.offset)) * 8;

      push();
      translate(col.x, col.y + bounce);
      fill(col.c);
      drawStar(0, 0, 10 + twinkle, 20 + twinkle, 5);
      pop();

      let d = dist(mouseX, mouseY, col.x, col.y + bounce);
      if (d < 25) {
        fill(0, 0, 100, 90);
        rect(mouseX + 10, mouseY - 30, textWidth(col.name) + 12, 24, 5);
        fill(0);
        textSize(14);
        textAlign(LEFT, CENTER);
        text(col.name, mouseX + 16, mouseY - 18);
      }
    }
  }
//displaying the album when star is pressed functions
  if (selectedAlbumImg) {
    let imgSize = 300;
    image(selectedAlbumImg, 20, height / 2 - imgSize / 2, imgSize, imgSize);
  }
}


//displaying the album when star is pressed functions
function mousePressed() {
  if (showBlocks && moodChosen) {
    for (let col of animatingColors) {
      let beatFreq = col.bpm / 60.0;
      let bounce = sin(TWO_PI * beatFreq * millis() / 1000.0 + col.offset) * 10;
      let d = dist(mouseX, mouseY, col.x, col.y + bounce);
      if (d < 25) {
        if (selectedAlbumUrl === col.album) {
          selectedAlbumImg = null;
          selectedAlbumUrl = null;
          fadeOutCover();
        } else {
          selectedAlbumUrl = col.album;
          loadImage(col.album, img => {
            selectedAlbumImg = img;
          }, () => {
            console.error("Failed to load image:", col.album);
          });
        }
        break;
      }
    }
  }
}
//drawing the stars
function drawStar(x, y, radius1, radius2, npoints) {
  let angle = TWO_PI / npoints;
  let halfAngle = angle / 2.0;
  beginShape();
  for (let a = 0; a < TWO_PI; a += angle) {
    let sx = x + cos(a) * radius2;
    let sy = y + sin(a) * radius2;
    vertex(sx, sy);
    sx = x + cos(a + halfAngle) * radius1;
    sy = y + sin(a + halfAngle) * radius1;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}
//drawing the spirals
class Ribbon {
  constructor(baseColor, bpm) {
    this.baseColor = baseColor;
    this.hueBase = hue(baseColor);
    this.satBase = saturation(baseColor);
    this.briBase = brightness(baseColor);
    this.bpm = constrain(bpm || 120, 60, 200);
    this.radius = random(80, min(width, height) / 2);
    this.angleOffset = random(TWO_PI);
    this.rotationSpeed = map(this.bpm, 60, 200, 0.01, 0.05);
    this.weight = map(this.bpm, 60, 200, 2, 8);
    this.numPoints = 200;
  }

  update() {
    this.time = (millis() - startTime) / 1000;
  }

  display() {
    let centerX = width / 2;
    let centerY = height / 2;
    let hueShift = (this.hueBase + sin(this.time + this.angleOffset) * 30) % 360;
    stroke(hueShift, this.satBase, this.briBase, 60);
    strokeWeight(this.weight);
    noFill();
    blendMode(BLEND);

    beginShape();
    for (let i = 0; i < this.numPoints; i++) {
      let angle = this.angleOffset + this.time * this.rotationSpeed + i * 0.1;
      let radiusVariation = this.radius + sin(i * 0.3 + this.time * 2) * 50;
      let x = centerX + cos(angle) * radiusVariation;
      let y = centerY + sin(angle) * radiusVariation;
      curveVertex(x, y);
    }
    endShape();
  }
}

class FlowParticle {
  constructor() {
    this.x = random(width);
    this.y = random(height);
    this.speed = random(0.5, 2);
    this.angle = random(TWO_PI);
    this.color = color(random(360), 60, 100, 40);
  }

  update() {
    this.angle += random(-0.05, 0.05);
    this.x += cos(this.angle) * this.speed;
    this.y += sin(this.angle) * this.speed;

    if (this.x < 0) this.x = width;
    if (this.x > width) this.x = 0;
    if (this.y < 0) this.y = height;
    if (this.y > height) this.y = 0;
  }

  display() {
    fill(this.color);
    ellipse(this.x, this.y, 8, 8);
  }
}

function fadeOutCover() {
  if (!selectedAlbumImg) return;

  let fadeAlpha = 255;
  let img = selectedAlbumImg;
  let interval = setInterval(() => {
    fill(0);
    noStroke();
    rect(20, height / 2 - 100, 200, 200);

    push();
    tint(255, fadeAlpha);
    image(img, 20, height / 2 - 100, 200, 200);
    pop();

    fadeAlpha -= 100;
    if (fadeAlpha <= 0) {
      clearInterval(interval);
      noTint();
      selectedAlbumImg = null;
      selectedAlbumUrl = null;
    }
  }, 20);
}

function playRandomSong(mood) {
  if (currentSong) {
    currentSong.stop();
    currentSong.disconnect();
  }
//play music based off mood
  const moodSongs = {
    happy: [ 'songs/happy/Baby be mine.mp3', 'songs/happy/beabadoobee - Beaches Lyrics.mp3', 'songs/happy/Billions.mp3', 'songs/happy/SES  - Just A Feeling Lyrics Color Coded Han_Rom_Eng.mp3' ],
    mellow: [ 'songs/mellow/Beneath the Mask.mp3', 'songs/mellow/Exchange.mp3', 'songs/mellow/Leon Thomas - MUTT Audio.mp3', 'songs/mellow/The Storm.mp3' ],
    sad: [ 'songs/sad/Mitski - Liquid Smooth Official Audio.mp3', 'songs/sad/My Immortal - Evanescence Lyrics .mp3', 'songs/sad/Sullen Girl.mp3', 'songs/sad/TV Girl - Cigarettes out the Window Lyrics.mp3' ],
    angry: [ 'songs/angry/Blood Magic.mp3', 'songs/angry/Jet Pilot.mp3', 'songs/angry/Slipknot - People  Shit Audio.mp3', 'songs/angry/うずまき.mp3' ],
    romantic: [ 'songs/romantic/Bluerose.mp3', 'songs/romantic/Caroline Shut Up.mp3', 'songs/romantic/One Less Lonely Girl.mp3', 'songs/romantic/Venus As A Boy.mp3' ],
    premadehappy: [ 'songs/premadehappy/BTS Butter Lyrics Color Coded Lyrics.mp3', 'songs/premadehappy/ROSALA - CHICKEN TERIYAKI Official Audio.mp3','songs/premadehappy/Sabrina Carpenter - Espresso.mp3','songs/premadehappy/Troye Sivan - Rush Lyric Video.mp3'],
    premademellow: [ 'songs/premademellow/Exchange.mp3', 'songs/premademellow/lavande.mp3' ],
    premadesad: [ 'songs/premadesad/A House in Nebraska Official Visualizer - Ethel Cain.mp3', 'songs/premadesad/Chappell Roan - Coffee Official Audio.mp3','songs/premadesad/Phoebe Bridgers - Funeral Official Lyric Video.mp3','songs/premadesad/Tate McRae - friends dont look at friends that way Lyrics (1).mp3' ],
    premadeangry: [ 'songs/premadeangry/Limp_Bizkit_-_Rollin_Air_Raid_Vehicle_Lyrics.mp3'],
    premaderomantic: [ 'songs/premaderomantic/Bruno Mars - Just The Way You Are Lyrics.mp3', 'songs/premaderomantic/Halo - Beyonc Lyrics.mp3' ]
  };

  let songList = moodSongs[mood] || moodSongs[normalizeMood(mood)];
  if (songList && songList.length > 0) {
    let songPath = random(songList);
    currentSong = loadSound(songPath, () => {
      currentSong.setVolume(0.6);
      currentSong.loop();
    }, () => {
      console.error(`Failed to load: ${songPath}`);
    });
  }
}
