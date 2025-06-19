const playersInput = document.getElementById('players');
const prizeInput   = document.getElementById('prize');
const deviationIn  = document.getElementById('deviation');
const skewIn       = document.getElementById('skew');
const devVal       = document.getElementById('devVal');
const skewVal      = document.getElementById('skewVal');
const startBtn     = document.getElementById('startBtn');
const resetBtn     = document.getElementById('resetBtn');
const resultsEl    = document.getElementById('results');
const spinSound    = document.getElementById('spinSound');
const winSound     = document.getElementById('winSound');
const loseSound    = document.getElementById('loseSound');
const dingSound    = document.getElementById('dingSound');
const endSound     = document.getElementById('endSound');

const canvas  = document.getElementById('rouletteWheel');
const ctx     = canvas.getContext('2d');
const segments= 12;
let wheelAngle = 0;
let animating  = false;

deviationIn.oninput = () => devVal.textContent = deviationIn.value;
skewIn.oninput      = () => skewVal.textContent = skewIn.value;

startBtn.onclick = async () => {
  if(animating) return;
  const players  = +playersInput.value;
  const prize    = +prizeInput.value;
  const deviation= +deviationIn.value / 100;
  const skew     = +skewIn.value / 100;
  if(players<1 || prize<1) return alert("Ange giltiga värden");

  resultsEl.innerHTML = '';
  startBtn.disabled = true;
  animating = true;

  drawWheel(prize, players);
  await rotateWheel();

  const finalAng  = wheelAngle % (2*Math.PI);
  const segIdx    = segments - Math.floor(finalAng / (2*Math.PI/segments)) - 1;
  const midpoint  = prize / players;
  const deviationBy = (segIdx - segments/2)/(segments/2);
  const rolled    = Math.round(midpoint + deviationBy * midpoint);
  const earning   = Math.round(midpoint - rolled);

  const li = document.createElement('li');
  li.textContent = `Betala ${rolled} kr → ${earning>=0?'+':'-'}${Math.abs(earning)} kr`;
  li.style.color = earning>=0 ? 'lightgreen':'salmon';
  resultsEl.appendChild(li);

  dingSound.play();
  if(earning>=0){ winSound.play(); rainCoins(40); }
  else          { loseSound.play(); }
  endSound.play();

  animating = false;
  startBtn.disabled = false;
};

resetBtn.onclick = () => document.location.reload();

function drawWheel(prize, players){
  const angleStep = (2*Math.PI)/segments;
  const midpoint = prize/players;
  ctx.clearRect(0,0,300,300);
  for(let i=0;i<segments;i++){
    const start = i*angleStep, end = start+angleStep;
    const diff   = (i - segments/2)/(segments/2);
    const value  = Math.round(midpoint + diff * midpoint);
    ctx.beginPath();
    ctx.moveTo(150,150);
    ctx.arc(150,150,140,start,end);
    const pct = Math.abs(diff);
    ctx.fillStyle = pct<0.1?'#aaa':pct<0.25?'#4CAF50':pct<0.5?'#2196F3':pct<0.75?'#9C27B0':'#FF9800';
    ctx.fill();
    ctx.stroke();
    const midAng = (start+end)/2;
    ctx.save();
    ctx.translate(150+Math.cos(midAng)*90,150+Math.sin(midAng)*90);
    ctx.rotate(midAng);
    ctx.fillStyle='#000';
    ctx.fillText(value,0,0);
    ctx.restore();
  }
}

function rotateWheel(){
  return new Promise(r => {
    const duration = 7000;
    const start    = performance.now();
    function frame(now){
      const elapsed = now - start;
      if(elapsed < duration){
        const t      = elapsed/duration;
        wheelAngle += (0.1 + 10*t)*0.02;
        canvas.style.transform = `rotate(${wheelAngle}rad)`;
        spinSound.currentTime = 0;
        spinSound.play();
        requestAnimationFrame(frame);
      } else {
        r();
      }
    }
    requestAnimationFrame(frame);
  });
}

function rainCoins(count){
  for(let i=0;i<count;i++){
    const coin = document.createElement('div');
    coin.className = 'coin';
    coin.style.left = Math.random()*window.innerWidth+'px';
    coin.style.animationDelay = Math.random()+'s';
    coin.style.animationDuration = 2 + Math.random()*2 + 's';
    document.body.appendChild(coin);
    setTimeout(()=>coin.remove(), 5000);
  }
}
