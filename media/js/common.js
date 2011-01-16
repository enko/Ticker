$(document).ready(function() {
	getEntries();
	
});

function getEntries(action) {
	if (action == 'reload')
		$('.entry-list').empty();
		
	$.getJSON('?format=json&function=get_all_entries', function(data) {
		$(data).each(function(i,entry) {
			if ( i == null ) return false;
			var text = entry.fields.text;
			var isPublic = entry.fields.isPublic;				
			if (isPublic == true) {
				var status = 'Öffentlich';
				var statusCss = 'public';
			} else {
				var status = 'Intern';
				var statusCss = 'private';
			}
			var published = entry.fields.published;
			var id = entry.pk;
			var entry = '.entry-' + id;
			// <li class="entry entry-1">Eintrag...<span class="published">...</span><span class="delete"></span></li>
			$('.entry-list').append('<li class="entry entry-'+id+' ' + statusCss + '"></li>');
			$(entry).append('<span class="entry-text">' + text + '</span>');
			$(entry).append('<span class="entry-status">' + status +'</span>');
			$(entry).append('<span class="entry-published">' + published + '</span>');
			$(entry).append('<span class="entry-delete"></span>');
		});
		
  	});

	setCounter(action);
}


function setCounter(action) {
	if (action == 'reload')
		$('.entry-counter-block').empty();
		
	$.get('?format=plain&function=get_count', function(data) {
		count = data
		if (count == 0) 
			var message = 'Keine Einträge gespeichert';
		else if (count == 1)
			var message = 'Ein Eintrag gespeichert';
		else
			var message = count + ' Einträge gespeichert';
		$('.entry-counter-block').append(message);	
	});
}


function submitNewEntry() {
	var text = $('.new-entry').val();
		
	if (text == 'Neuen Eintrag schreiben...')
		return false;
		
	if ( $('.is-public:checkbox:checked').val() == 'on' )
		var isPublic = parseInt(1);
	else 
		var isPublic = parseInt(0);
	
	$.ajax({
		type: "POST",
		// format: { "text" : "text body", "isPublic" : 0|1 }
		data: { "entry-text" : text, "entry-is-public" : isPublic, "submit" : "submit", "new_entry" : "new_entry" },
		success: function() {
			$('.new-entry').val('Neuen Eintrag schreiben...');
			getEntries('reload');
		}
	});
}

/*
 * OLD STUFF
 *
 */

	function submitNewPin() {
		var newPin = $("#newPin").val();
		$.ajax({
			type: "POST",
			data: { "pin" : newPin },
			success: function() {
				alert("Pin geändert!");
			}
		});
	}
	
	function deleteEntry(id) {
		$.ajax({
			type: "POST",
			data: { "deleteEntry" : id },
			success: function() {
				var newEntryCount = parseInt($('.entry-counter').html()) - 1;
				console.log(parseInt($('.entry-counter').html()));
				console.log(newEntryCount);
				setCounter(newEntryCount);
			}
		});
		
		var box = "div.entry-"+id;
		$(box).hide('slow');
	}
	
	function refreshEntries() {
		$.getJSON('?refresh.json', function(data) {
			//console.log(data.length);
			var text = data[0].fields.text;
			var isPublic = data[0].fields.isPublic;
			if (isPublic == true) {
				var status = 'Öffentlich';
			} else {
				var status = 'Intern';
			}
			var published = data[0].fields.published;
			var pk = data[0].pk;
			
			if (pk > 1) {
				var pkBefore = data[1].pk;
				$('<div class="entry-box box entry-'+ pk +'">').insertBefore('.entry-'+pkBefore);
			} else {
				$('.entries-box').append('<div class="entry-box box entry-'+ pk +'">');
			}
			
			var container = '.entry-'+pk;	
			$(container).append('<div class="entry-text">'+text+'<img src="../media/img/deleteButton.png" title="Diesen Eintrag löschen" class="deleteButton" onClick="deleteEntry('+pk+')"/></div>');
			$(container).append('<div class="entry-status">'+status+'</div>');
			$(container).append('<div class="entry-date">'+published+'</div>');
		});
	}