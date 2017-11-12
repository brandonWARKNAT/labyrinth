function Labyrinth(){
	this.currentX;
	this.currentY;
	this.initListeners()
}

Labyrinth.prototype.setPathBeginning = function(event) {
	event.stopPropagation();
	event.preventDefault();
	
	$.ajax({
		url: '/labyrinth/create_beginning',
		data: $("#beginning-form").serialize(),
		type: 'GET',
		dataType: 'json'
	})
	.done(function(response){
		window.location = '/';
	})
	.fail(function(response){

	});
};

Labyrinth.prototype.setPathEnding = function(event) {
	event.stopPropagation();
	event.preventDefault();
	
	$.ajax({
		url: '/labyrinth/create_ending',
		data: $("#ending-form").serialize(),
		type: 'GET',
		dataType: 'json'
	})
	.done(function(response){
		if(status!=500){
			window.location = '/';	
		}
		
	})
	.fail(function(response){

	});
};

Labyrinth.prototype.move = function(event){
	event.stopPropagation();
	event.preventDefault();

	$.ajax({
		url: 'labyrinth/move',
		data: {
			move: $(event.target).data('move'), 
			from_x: $(".current-position").data('coordinate-x'), 
			from_y: $(".current-position").data('coordinate-y')},
		type: 'GET',
		dataType: 'json',
	})
	.done(function(response){
		if (response.status != 500){
			window.location = '/';	
		}
		else{
			alert(response.detail);
		}
	})
	.fail(function(response){

	});
}

Labyrinth.prototype.solveAlgorithm = function(event){
	event.stopPropagation();
	event.preventDefault();
	var algorithm = $(event.target).val();
	var url = ''
	switch(algorithm){
		case 'breadth-first-search':
			url = '/labyrinth/breadth_first_search'
			break;
		default: 
	} 

	$.ajax({
		url: url,
		data: {
			'up_priority': $("#up-priority").val(), 
			'down_priority': $("#down-priority").val(),
			'left_priority': $("#left-priority").val(),
			'right_priority': $("#right-priority").val(),
		},
		type: 'GET',
		dataType: 'json'
	})
	.done(function(response){
		// TODO
	})
}

Labyrinth.prototype.initListeners = function(e){
	$("#select-path-beginning").on('click', this.setPathBeginning.bind(this));
	$("#select-path-ending").on('click', this.setPathEnding.bind(this));
	$(".move-control").on('click', this.move.bind(this));
	// $(".solve-algorithm").on('click', this.solveAlgorithm.bind(this));
}

$(document).ready(function(){
	var labyrinth = new Labyrinth();

	$(".current-position").focus();
});