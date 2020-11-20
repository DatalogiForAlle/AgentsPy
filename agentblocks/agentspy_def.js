Blockly.Blocks['agentspy_forward'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Move");
		this.appendValueInput("distance")
			.setCheck(null)
			.appendField("forward by");
		this.appendDummyInput()
			.appendField("steps");
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_randint'] = {
	init: function() {
		this.appendValueInput("min")
			.setCheck(null)
			.appendField("Random value between");
		this.appendValueInput("max")
			.appendField("and")
			.setCheck(null);
		this.setOutput(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_nearbyagents'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Agents around");
		this.appendValueInput("radius")
			.setCheck(null)
			.appendField("within a radius of");
		this.setInputsInline(true);
		this.setOutput(true, null);
		this.setColour(120);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_variable'] = {
	init: function() {
		this.appendValueInput("object")
			.setCheck(null);
		this.appendDummyInput()
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
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Distance from");
		this.appendValueInput("x")
			.setCheck("Number")
			.appendField("to x:");
		this.appendValueInput("y")
			.setCheck("Number")
			.appendField("y:");
		this.setInputsInline(true);
		this.setOutput(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_directionto'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Direction from");
		this.appendValueInput("x")
			.setCheck("Number")
			.appendField("to x:");
		this.appendValueInput("y")
			.setCheck("Number")
			.appendField("y:");
		this.setInputsInline(true);
		this.setOutput(true, null);
		this.setColour(230);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

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

Blockly.Blocks['agentspy_addagent'] = {
	init: function() {
		this.appendDummyInput()
			.appendField("Add agent");
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_foreach'] = {
	init: function() {
		this.appendValueInput("iteration_set")
			.setCheck(null)
			.appendField("For each")
			.appendField(new Blockly.FieldTextInput("e"), "elm")
			.appendField("in");
		this.appendDummyInput()
			.appendField("do");
		this.appendStatementInput("body")
			.setCheck(null);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(120);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_currenttile'] = {
	init: function() {
		this.appendValueInput("agent_id")
			.setCheck(null);
		this.appendDummyInput()
			.appendField("'s current tile");
		this.setOutput(true, null);
		this.setColour(290);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_centerintile'] = {
	init: function() {
		this.appendValueInput("agent_id")
			.setCheck(null)
			.appendField("Center");
		this.appendDummyInput()
			.appendField("in tile");
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_jumpto'] = {
	init: function() {
		this.appendValueInput("agent_id")
			.setCheck(null)
			.appendField("Move");
		this.appendValueInput("x")
			.setCheck("Number")
			.appendField("to x:");
		this.appendValueInput("y")
			.setCheck("Number")
			.appendField("y:");
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_getagent'] = {
	init: function() {
		this.appendDummyInput()
			.appendField(new Blockly.FieldTextInput("agent"), "agent_id")
			.appendField("(Agent)");
		this.setOutput(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_gettile'] = {
	init: function() {
		this.appendDummyInput()
			.appendField(new Blockly.FieldTextInput("tile"), "tile_id")
			.appendField("(Tile)");
		this.setOutput(true, null);
		this.setColour(290);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_pointtowards'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Point");
		this.appendValueInput("x")
			.setCheck("Number")
			.appendField("towards x:");
		this.appendValueInput("y")
			.setCheck("Number")
			.appendField("y:");
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_backward'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Move");
		this.appendValueInput("distance")
			.setCheck(null)
			.appendField("backward by");
		this.appendDummyInput()
			.appendField("steps");
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_turnleft'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Turn");
		this.appendValueInput("degrees")
			.setCheck(null)
			.appendField("left by");
		this.appendDummyInput()
			.appendField("degrees");
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_turnright'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Turn");
		this.appendValueInput("degrees")
			.setCheck(null)
			.appendField("right by");
		this.appendDummyInput()
			.appendField("degrees");
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_nearbytiles'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Tiles around agent");
		this.appendValueInput("x1")
			.setCheck(null)
			.appendField("within a square of x:");
		this.appendValueInput("y1")
			.setCheck(null)
			.appendField("y:");
		this.appendValueInput("x2")
			.setCheck(null)
			.appendField("to x:");
		this.appendValueInput("y2")
			.setCheck(null)
			.appendField("y:");
		this.setInputsInline(true);
		this.setOutput(true, null);
		this.setColour(120);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_neighbortiles'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Tiles neighboring agent");
		this.setInputsInline(true);
		this.setOutput(true, null);
		this.setColour(120);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_jumptotile'] = {
	init: function() {
		this.appendValueInput("agent")
			.setCheck(null)
			.appendField("Move");
		this.appendValueInput("tile")
			.setCheck(null)
			.appendField("to tile");
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour(20);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};

Blockly.Blocks['agentspy_allagents'] = {
	init: function() {
		this.appendDummyInput()
			.appendField("All agents");
		this.setOutput(true, null);
		this.setColour(120);
		this.setTooltip("");
		this.setHelpUrl("");
	}
};
