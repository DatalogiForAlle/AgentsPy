Blockly.Blocks['agentspy_default'] = {
	init: function() {
		this.appendDummyInput()
			.appendField("Setup");
		this.appendStatementInput("setup_block")
			.setCheck(null);
		this.appendDummyInput()
			.appendField("Go");
		this.appendStatementInput("go_block")
			.setCheck(null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_forward'] = {
	init: function() {
		this.appendDummyInput()
			.appendField("Move")
			.appendField(new Blockly.FieldDropdown([["Self","self_agent"], ["Other","other_agent"]]), "agent_select")
			.appendField("forward by");
		this.appendValueInput("distance")
			.setCheck(null);
		this.appendDummyInput()
			.appendField("steps");
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_forall'] = {
	init: function() {
		this.appendDummyInput()
			.appendField("For all agents");
		this.appendStatementInput("loop")
			.setCheck(null);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(230);
		this.setTooltip("what");
		this.setHelpUrl("hey");
	}
};

Blockly.Blocks['agentspy_randint'] = {
	init: function() {
		this.appendValueInput("min")
			.setCheck(null)
			.appendField("Random value between");
		this.appendDummyInput()
			.appendField("and");
		this.appendValueInput("max")
			.setCheck(null);
		this.setOutput(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_nearbyagents'] = {
	init: function() {
		this.appendDummyInput()
			.appendField("For each other agent in a radius of");
		this.appendValueInput("radius")
			.setCheck(null);
		this.appendDummyInput();
		this.appendStatementInput("loop")
			.setCheck(null);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_variable'] = {
	init: function() {
		this.appendDummyInput()
			.appendField(new Blockly.FieldDropdown([["Self","self_agent"], ["Other","other_agent"]]), "agent_select")
			.appendField(".")
			.appendField(new Blockly.FieldTextInput("variable"), "var_select");
		this.setOutput(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_assign'] = {
	init: function() {
		this.appendValueInput("address")
			.setCheck(null)
			.appendField("Set");
		this.appendValueInput("value")
			.setCheck(null)
			.appendField("to");
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_distanceto'] = {
	init: function() {
		this.appendValueInput("x_coord")
			.setCheck("Number")
			.appendField("Distance from")
			.appendField(new Blockly.FieldDropdown([["Self","self_agent"], ["Other","other_agent"]]), "target_agent")
			.appendField("to (");
		this.appendValueInput("y_coord")
			.setCheck("Number")
			.appendField(",");
		this.appendDummyInput()
			.appendField(")");
		this.setInputsInline(true);
		this.setOutput(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_directionto'] = {
	init: function() {
		this.appendValueInput("x_coord")
			.setCheck("Number")
			.appendField("Direction from")
			.appendField(new Blockly.FieldDropdown([["Self","self_agent"], ["Other","other_agent"]]), "target_agent")
			.appendField("to (");
		this.appendValueInput("y_coord")
			.setCheck("Number")
			.appendField(",");
		this.appendDummyInput()
			.appendField(")");
		this.setInputsInline(true);
		this.setOutput(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_addagent'] = {
	init: function() {
		this.appendDummyInput()
			.appendField("Add agent");
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
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

Blockly.JavaScript['agentspy_forall'] = function(block) {
	var loop = Blockly.JavaScript.statementToCode(block, 'loop')
	var code = 'for (var i = 0; i < model_agents.length; i++) {\n'
		+ 'var self_agent = model_agents[i];\n'
		+ loop
		+ '}\n'
	return code;
};

Blockly.JavaScript['agentspy_forward'] = function(block) {
	var target_agent = block.getFieldValue('agent_select');
	var distance = Blockly.JavaScript.valueToCode(block, 'distance', Blockly.JavaScript.ORDER_ADDITION) || '0';
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
	var radius = Blockly.JavaScript.valueToCode(block, 'radius', Blockly.JavaScript.ORDER_ATOMIC);
	var loop = Blockly.JavaScript.statementToCode(block, 'loop');
	var code = 'for (var j = 0; j < model_agents.length; j++) {\n'
		+ 'var other_agent = model_agents[j];\n'
		+ 'if (!(self_agent === other_agent) && self_agent.distance_to(other_agent.x,other_agent.y) <= '+radius+') {\n'
		+ loop
		+ '}\n}\n'
	return code;
};

Blockly.JavaScript['agentspy_variable'] = function(block) {
	var target_agent = block.getFieldValue('agent_select');
	var variable_id = block.getFieldValue('var_select');
	var code = target_agent+'.'+variable_id;
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_assign'] = function(block) {
	var address = Blockly.JavaScript.valueToCode(block, 'address', Blockly.JavaScript.ORDER_ATOMIC);
	var value = Blockly.JavaScript.valueToCode(block, 'value', Blockly.JavaScript.ORDER_ATOMIC);
	var code = address+' = '+value+';\n';
	return code;
};

Blockly.JavaScript['agentspy_distanceto'] = function(block) {
	var target_agent = block.getFieldValue('target_agent');
	var value_x = Blockly.JavaScript.valueToCode(block, 'x_coord', Blockly.JavaScript.ORDER_ATOMIC);
	var value_y = Blockly.JavaScript.valueToCode(block, 'y_coord', Blockly.JavaScript.ORDER_ATOMIC);
	var code = target_agent+'.distance_to('+value_x+','+value_y+')';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_directionto'] = function(block) {
	var target_agent = block.getFieldValue('target_agent');
	var value_x = Blockly.JavaScript.valueToCode(block, 'x_coord', Blockly.JavaScript.ORDER_ATOMIC);
	var value_y = Blockly.JavaScript.valueToCode(block, 'y_coord', Blockly.JavaScript.ORDER_ATOMIC);
	var code = target_agent+'.direction_to('+value_x+','+value_y+')';
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['agentspy_addagent'] = function(block) {
  var code = 'model_agents.push(new Agent());\n';
  return code;
};
