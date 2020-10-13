var demoWorkspace = Blockly.inject('blocklyDiv', {media: '../../media/', toolbox: document.getElementById('toolbox')});

var model_setup = false;
function setup() {
	model_setup = true;
}

var model_run = false;
function toggleGo() {
	if (!model_run) {
		document.getElementById('goButton').innerHTML = "Stop";
		model_run = true;
	} else {
		document.getElementById('goButton').innerHTML = "Go";
		model_run = false;
	}
}

class Agent {
	constructor() {
		this.c = document.getElementById("simulationArea");
		this.ctx = this.c.getContext("2d");
		this.x = 0;
		this.y = 0;
		this.direction = 0;
		this.speed = 1;
		this.size = 5;
		this.color = "#FFFFFF";
		this.setup()
	}
	draw () {
		this.ctx.beginPath();
		this.ctx.arc(this.x,this.y,this.size,0,2*Math.PI);
		this.ctx.fillStyle = this.color;
		this.ctx.fill();
	}
	wraparound () {
		// JS modulo bug, see https://web.archive.org/web/20090717035140if_/javascript.about.com/od/problemsolving/a/modulobug.htm
		this.x = ((this.x%this.c.width)+this.c.width)%this.c.width;
		this.y = ((this.y%this.c.height)+this.c.height)%this.c.height;
	}
	forward (distance) {
		this.x += Math.cos(this.direction * 2*Math.PI/360) * distance;
		this.y += Math.sin(this.direction * 2*Math.PI/360) * distance;
		this.wraparound();
	}
	distance_to (x,y) {
		return Math.sqrt(Math.pow(this.x-x,2) + Math.pow(this.y-y,2));
	}
	direction_to (x,y) {
		var dir = 0;
		var dist = this.distance_to(x,y);
		if (dist > 0) {
			dir = (Math.acos((x - this.x) / dist)) * 360/(2*Math.PI);
			if (this.y - y > 0) {
				dir = 360 - dir;
			}
		}
		return dir;
	}
	setup () {
		this.x = Math.random()*this.c.width;
		this.y = Math.random()*this.c.height;
		this.direction = Math.random()*360;
	}
	step () {
		this.forward();
	}
}

class Tile {
	constructor(x,y,size) {
		this.c = document.getElementById("simulationArea");
		this.ctx = this.c.getContext("2d");
		this.x = x;
		this.y = y;
		this.size = size;
		this.color = "#000000";
	}

	draw() {
		this.ctx.fillStyle = this.color;
		this.ctx.fillRect(this.x,this.y,this.size,this.size);
	}
}

var model_agents = [];
var model_tiles = [];
for (y = 0; y < 100; y++) {
	for (x = 0; x < 100; x++) {
		model_tiles.push(new Tile(x*8,y*8,8));
	}
}

function printcode() {
	console.log(code_to_run);
}

var default_block = '<xml><block type="agentspy_default" deletable="false"></block></xml>';
Blockly.Xml.domToWorkspace(Blockly.Xml.textToDom(default_block), demoWorkspace);

var code_to_run = ""
function updateCode(event) {
	code_to_run = Blockly.JavaScript.workspaceToCode(demoWorkspace);
}
demoWorkspace.addChangeListener(updateCode);
demoWorkspace.addChangeListener(Blockly.Events.disableOrphans);


var canvas = document.getElementById("simulationArea");
var ctx = canvas.getContext("2d");

function updater () {
	ctx.fillStyle = "white";
	ctx.fillRect(0,0,canvas.width,canvas.height);
	for (t = 0; t < model_tiles.length; t++) {
		model_tiles[t].draw();
	}
	for (i = 0; i < model_agents.length; i++) {
		model_agents[i].draw();
	}
	if (model_setup || model_run) {
		eval(code_to_run);
	}
}
setInterval(updater, 1000/30);
