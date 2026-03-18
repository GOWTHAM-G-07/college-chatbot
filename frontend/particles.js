window.onload = function(){

const canvas = document.getElementById("bgCanvas")
if(!canvas) return

const ctx = canvas.getContext("2d")

canvas.width = window.innerWidth
canvas.height = window.innerHeight

let nodes = []

const NODE_COUNT = 80
const MAX_DIST = 120

// create nodes
for(let i=0;i<NODE_COUNT;i++){
nodes.push({
x:Math.random()*canvas.width,
y:Math.random()*canvas.height,
vx:(Math.random()-0.5)*1.2,
vy:(Math.random()-0.5)*1.2
})
}

function draw(){

ctx.clearRect(0,0,canvas.width,canvas.height)

// move nodes
nodes.forEach(n=>{
n.x += n.vx
n.y += n.vy

if(n.x<0 || n.x>canvas.width) n.vx *= -1
if(n.y<0 || n.y>canvas.height) n.vy *= -1
})

// draw connections
for(let i=0;i<nodes.length;i++){
for(let j=i+1;j<nodes.length;j++){

let dx = nodes[i].x - nodes[j].x
let dy = nodes[i].y - nodes[j].y
let dist = Math.sqrt(dx*dx + dy*dy)

if(dist < MAX_DIST){

let opacity = 1 - dist/MAX_DIST

ctx.beginPath()
ctx.moveTo(nodes[i].x, nodes[i].y)
ctx.lineTo(nodes[j].x, nodes[j].y)
ctx.strokeStyle = `rgba(59,130,246,${opacity})`
ctx.lineWidth = 1
ctx.stroke()

}

}
}

// draw nodes
nodes.forEach(n=>{
ctx.beginPath()
ctx.arc(n.x,n.y,2,0,Math.PI*2)
ctx.fillStyle = "#3b82f6"
ctx.fill()
})

requestAnimationFrame(draw)

}

draw()

// resize fix
window.addEventListener("resize",()=>{
canvas.width = window.innerWidth
canvas.height = window.innerHeight
})

}