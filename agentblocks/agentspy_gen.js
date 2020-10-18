Blockly.JavaScript['agentspy_forward'] = function(block) {
	var target_agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var distance = Blockly.JavaScript.valueToCode(block, 'distance', Blockly.JavaScript.ORDER_ATOMIC);
	var code = target_agent+'.forward('+distance+');\n'
	return code;
};

Blockly.JavaScript['agentspy_randint'] = function(block) {
	var value_min = Blockly.JavaScript.valueToCode(block, 'min', Blockly.JavaScript.ORDER_ATOMIC);
	var value_max = Blockly.JavaScript.valueToCode(block, 'max', Blockly.JavaScript.ORDER_ATOMIC);
	var code = value_min+'+Math.random()*('+value_max+'-'+value_min+')';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_nearbyagents'] = function(block) {
	var target_agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var radius = Blockly.JavaScript.valueToCode(block, 'radius', Blockly.JavaScript.ORDER_ATOMIC);
	var code = target_agent+'.agents_nearby('+radius+')';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_variable'] = function(block) {
	var object = Blockly.JavaScript.valueToCode(block, 'object', Blockly.JavaScript.ORDER_ATOMIC);
	var variable = block.getFieldValue('var_select');
	var code = object+'.'+variable;
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_assign'] = function(block) {
	var address = Blockly.JavaScript.valueToCode(block, 'address', Blockly.JavaScript.ORDER_ATOMIC);
	var value = Blockly.JavaScript.valueToCode(block, 'value', Blockly.JavaScript.ORDER_ATOMIC);
	var code = address+' = '+value+';\n';
	return code;
};

Blockly.JavaScript['agentspy_distanceto'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var x = Blockly.JavaScript.valueToCode(block, 'x', Blockly.JavaScript.ORDER_ATOMIC);
	var y = Blockly.JavaScript.valueToCode(block, 'y', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.distance_to('+x+','+y+')';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_directionto'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var x = Blockly.JavaScript.valueToCode(block, 'x', Blockly.JavaScript.ORDER_ATOMIC);
	var y = Blockly.JavaScript.valueToCode(block, 'y', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.direction_to('+x+','+y+')';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_default'] = function(block) {
	var setup_block = Blockly.JavaScript.statementToCode(block, 'setup_block');
	var go_block = Blockly.JavaScript.statementToCode(block, 'go_block');
	var code = 'if (model_setup) {\n'
		+ 'model_setup = false;\n'
		+ 'model_agents = [];\n'
		+ setup_block
		+ '}\n'
		+ 'if (model_run) {\n'
		+ go_block
		+ '}\n';
	return code;
};

Blockly.JavaScript['agentspy_addagent'] = function(block) {
	var code = 'MODEL_AGENTS.push(new Agent());\n';
	return code;
};

Blockly.JavaScript['agentspy_foreach'] = function(block) {
	var element = block.getFieldValue('elm');
	var iteration_set = Blockly.JavaScript.valueToCode(block, 'iteration_set', Blockly.JavaScript.ORDER_ATOMIC);
	var loop_body = Blockly.JavaScript.statementToCode(block, 'body');
	var code = 'var element_set = Array.from('+iteration_set+');\n'
		+ 'for (var i = 0; i < element_set.length; i++) {\n'
		+ 'var '+element+' = element_set[i];\n'
		+ loop_body
		+ '}\n';
	return code;
};

Blockly.JavaScript['agentspy_currenttile'] = function(block) {
	var target_agent = Blockly.JavaScript.valueToCode(block, 'agent_id', Blockly.JavaScript.ORDER_ATOMIC);
	var code = target_agent+'.current_tile()';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_centerintile'] = function(block) {
	var target_agent = Blockly.JavaScript.valueToCode(block, 'agent_id', Blockly.JavaScript.ORDER_ATOMIC);
	var code = target_agent+'.center_in_tile();\n';
	return code;
};

Blockly.JavaScript['agentspy_jumpto'] = function(block) {
	var target_agent = Blockly.JavaScript.valueToCode(block, 'agent_id', Blockly.JavaScript.ORDER_ATOMIC);
	var x = Blockly.JavaScript.valueToCode(block, 'x', Blockly.JavaScript.ORDER_ATOMIC);
	var y = Blockly.JavaScript.valueToCode(block, 'y', Blockly.JavaScript.ORDER_ATOMIC);
	var code = target_agent+'.jump_to('+x+','+y+');\n';
	return code;
};

Blockly.JavaScript['agentspy_getagent'] = function(block) {
	var target_agent = block.getFieldValue('agent_id');
	var code = target_agent;
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_gettile'] = function(block) {
	var target_tile = block.getFieldValue('tile_id');
	var code = target_tile;
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_pointtowards'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var x = Blockly.JavaScript.valueToCode(block, 'x', Blockly.JavaScript.ORDER_ATOMIC);
	var y = Blockly.JavaScript.valueToCode(block, 'y', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.point_towards('+x+','+y+');\n';
	return code;
};

Blockly.JavaScript['agentspy_backward'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var distance = Blockly.JavaScript.valueToCode(block, 'distance', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.forward('+distance+');\n';
	return code;
};

Blockly.JavaScript['agentspy_turnleft'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var degrees = Blockly.JavaScript.valueToCode(block, 'degrees', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.left('+degrees+');\n';
	return code;
};

Blockly.JavaScript['agentspy_turnright'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var degrees = Blockly.JavaScript.valueToCode(block, 'degrees', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.right('+degrees+');\n';
	return code;
};

Blockly.JavaScript['agentspy_nearbytiles'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var x1 = Blockly.JavaScript.valueToCode(block, 'x1', Blockly.JavaScript.ORDER_ATOMIC);
	var y1 = Blockly.JavaScript.valueToCode(block, 'y1', Blockly.JavaScript.ORDER_ATOMIC);
	var x2 = Blockly.JavaScript.valueToCode(block, 'x2', Blockly.JavaScript.ORDER_ATOMIC);
	var y2 = Blockly.JavaScript.valueToCode(block, 'y2', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.nearby_tiles('+x1+','+y1+','+x2+','+y2+')';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_neighbortiles'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.neighbor_tiles()';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_jumptotile'] = function(block) {
	var agent = Blockly.JavaScript.valueToCode(block, 'agent', Blockly.JavaScript.ORDER_ATOMIC);
	var tile = Blockly.JavaScript.valueToCode(block, 'tile', Blockly.JavaScript.ORDER_ATOMIC);
	var code = agent+'.jump_to_tile('+tile+');\n';
	return code;
};

Blockly.JavaScript['agentspy_allagents'] = function(block) {
	var code = 'MODEL_AGENTS';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};
