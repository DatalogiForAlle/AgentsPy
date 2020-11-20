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

/*
   Global variables. In the Python library, these would be part of the
   Model-class. It's not pretty, but the alternative is making a Model class and
   then passing an instance reference of that around to all the agents and
   tiles, which is what we were actually trying to avoid doing in Python in the
   first place, since we only *really* need one model. Thus, this:
*/
var MODEL_TILES_X = 100;
var MODEL_TILES_Y = 100;
var MODEL_WRAP = true;
var MODEL_AGENTS = [];
var MODEL_TILES = [];

class Agent {
	constructor() {
		this.canvas = document.getElementById("simulationArea");
		this.ctx = this.canvas.getContext("2d");
		this.x = 0;
		this.y = 0;
		this.direction = 0;
		this.speed = 1;
		this.size = 5;
		this.color = "#FFFFFF";
		this.current_tile = null;
		this.destroyed = false;
		this.setup();
	}
	draw () {
		this.ctx.beginPath();
		this.ctx.arc(this.x,this.y,this.size,0,2*Math.PI);
		this.ctx.fillStyle = this.color;
		this.ctx.fill();
	}
	current_tile () {
		var x = Math.floor((MODEL_TILES_X * this.x) / this.canvas.width);
		var y = Math.floor((MODEL_TILES_Y * this.y) / this.canvas.height);
		return MODEL_TILES[y * MODEL_TILES_X + x];
	}
	update_current_tile() {
		var new_tile = this.current_tile();
		if (this.current_tile == null) {
			this.current_tile = new_tile;
			this.current_tile.add_agent(this);
		} else if (!(this.current_tile == new_tile)) {
			this.current_tile.remove_agent(this);
			new_tile.add_agent(this);
			this.current_tile = new_tile;
		}
	}
	post_move() {
		if (MODEL_WRAP) {
			this.wraparound();
		} else {
			this.stay_inside();
		}
	}
	wraparound () {
		// JS modulo bug, see https://web.archive.org/web/20090717035140if_/javascript.about.com/od/problemsolving/a/modulobug.htm
		this.x = ((this.x%this.canvas.width)+this.canvas.width)%this.canvas.width;
		this.y = ((this.y%this.canvas.height)+this.canvas.height)%this.canvas.height;
	}
	stay_inside() {
		this.x = Math.min(Math.max(0,this.x),this.canvas.width);
		this.y = Math.min(Math.max(0,this.y),this.canvas.height);
	}
	center_in_tile() {
		var w = this.canvas.width;
        var h = this.canvas.height;
        var tx = MODEL_TILES_X;
        var ty = MODEL_TILES_Y;
		this.x = Math.floor(this.x * tx / w) * w / tx + (w / tx) / 2;
		this.y = Math.floor(this.y * ty / h) * h / ty + (h / ty) / 2;
	}
	jump_to (x,y) {
		this.x = x;
		this.y = y;
		this.post_move();
	}
	jump_to_tile (tile) {
		this.x = tile.x * this.canvas.width / MODEL_TILES_X;
		this.y = tile.y * this.canvas.height / MODEL_TILES_Y;
		this.center_in_tile();
		this.post_move();
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
	point_towards (x,y) {
		var dir = 0;
		var dist = this.distance_to(x,y);
		if (dist > 0) {
			dir = (Math.acos((x - this.x) / dist)) * 360/(2*Math.PI);
			if (this.y - y > 0) {
				dir = 360 - dir;
			}
		}
		this.direction = dir;
	}
	forward (distance) {
		this.x += Math.cos(this.direction * 2*Math.PI/360) * distance;
		this.y += Math.sin(this.direction * 2*Math.PI/360) * distance;
		this.post_move();
	}
	backward (distance) {
		this.x -= Math.cos(this.direction * 2*Math.PI/360) * distance;
		this.y -= Math.sin(this.direction * 2*Math.PI/360) * distance;
		this.post_move();
	}
	left (degrees) {
		this.direction += degrees;
	}
	right (degrees) {
		this.direction -= degrees;
	}
	distance_to (x,y) {
		return Math.sqrt(Math.pow(this.x-x,2) + Math.pow(this.y-y,2));
	}
	agents_nearby (r) {
		nearby = new Set();
		for (var i = 0; i < MODEL_AGENTS.length; i++) {
			var other_agent = MODEL_AGENTS[i];
			if (!(this === other_agent)
				&& this.distance_to(other_agent.x,other_agent.y) <= r) {
				nearby.add(other_agent);
			}
		}
		return nearby;
	}
	nearby_tiles(x1,y1,x2,y2) {
		var tile = this.current_tile();
		var tiles = [];
		for (var x = x1; x <= x2; x++) {
			for (var y = y1; y <= y2; y++) {
				tiles.push(MODEL_TILES[(tile.y + y) * MODEL_TILES_X + (tile.x + x)]);
			}
		}
		return tiles;
	}
	neighbor_tiles() {
		return this.nearby_tiles(-1,-1,1,1);
	}
	is_destroyed() {
		return this.destroyed;
	}
	destroy() {
		this.destroy = true;
	}
	setup () {
		this.x = Math.random()*this.canvas.width;
		this.y = Math.random()*this.canvas.height;
		this.direction = Math.random()*360;
	}
	step () {
		this.forward();
	}
}

class Tile {
	constructor(x,y,size) {
		this.canvas = document.getElementById("simulationArea");
		this.ctx = this.canvas.getContext("2d");
		this.x = x;
		this.y = y;
		this.size = size;
		this.color = "#000000";
		this.agents = new Set();
	}
	draw() {
		this.ctx.fillStyle = this.color;
		this.ctx.fillRect(this.x*this.size,this.y*this.size,this.size,this.size);
	}
	add_agent(agent) {
		this.agents.add(agent);
	}
	remove_agent(agent) {
		this.agents.delete(agent);
	}
}

for (y = 0; y < 100; y++) {
	for (x = 0; x < 100; x++) {
		MODEL_TILES.push(new Tile(x,y,8));
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
	for (t = 0; t < MODEL_TILES.length; t++) {
		MODEL_TILES[t].draw();
	}
	for (i = 0; i < MODEL_AGENTS.length; i++) {
		MODEL_AGENTS[i].draw();
	}
	if (model_setup || model_run) {
		eval(code_to_run);
	}
}
setInterval(updater, 1000/30);
