$(document).ready(function() {
	getEntries();
	setTimeout("setCounter()", 1000);
	setPin();
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
			$(entry).append('<span class="entry-delete" onclick="deleteEntry('+ id +')">Löschen</span>');
		});
		
  	});
	
	hideLoader();
}

function updateEntries() {
	$.getJSON('?format=json&function=get_latest_entry', function(data) {
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
			$('.entry-list').prepend('<li class="entry entry-'+id+' ' + statusCss + '"></li>');
			$(entry).append('<span class="entry-text">' + text + '</span>');
			$(entry).append('<span class="entry-status">' + status +'</span>');
			$(entry).append('<span class="entry-published">' + published + '</span>');
			$(entry).append('<span class="entry-delete" onclick="deleteEntry('+ id +')">Löschen</span>');
		});
		
  	});
  	
  	updateCounter();
}

function setCounter() {
	$('.entry-counter-block').empty();
	var count = $('.entry').size();
	
	if (count == 0) 
		var message = 'Keine Einträge gespeichert';
	else if (count == 1)
		var message = 'Ein Eintrag gespeichert';
	else
		var message = count + ' Einträge gespeichert';
	
	$('.entry-counter-block').append(message).animate({ "opacity" : 1 }, "fast");	
}

function updateCounter() {
	$('.entry-counter-block').animate({ "opacity" : 0}, "slow");
	setTimeout("setCounter()", 1000);
}

function setPin(action) {
	$.get('?format=plain&function=get_pin', function(data) {
		$('.pin-value').val(data);
	});
}

function submitNewEntry() {
	var text = $('.new-entry').val();
		
	if (text == 'Neuen Eintrag schreiben...') {
		showMessageBox('Eintrag unterscheidet sich nicht von dem Standardtext des Eingabefeldes!', "error");
		return false;
	}
		
	if ( $('.is-public:checkbox:checked').val() == 'on' )
		var isPublic = 1;
	else 
		var isPublic = 0;
	
	$.ajax({
		type: "POST",
		// format: { "text" : "text body", "isPublic" : 0|1 }
		data: { "entry-text" : text, "entry-is-public" : isPublic, "submit" : "submit", "new_entry" : "new_entry" },
		success: function() {
			resetEntryInput();
			showMessageBox('Eintrag gespeichert!', "notice");
			updateEntries();
			updateCounter();
		}
	});
}

function resetEntryInput() {
	$('.new-entry').val('Neuen Eintrag schreiben...');
}
 
function submitNewPin() {
	var pin = $('.pin-value').val();
	
	$.ajax({
		type: "POST",
		data: { "new_pin" : true, "submit" : true, "pin-value" : pin },
		success: function() {
			showMessageBox('Pin wurde erfolgreich geändert!', "notice");
			setPin();
		}
	})
}

	
function deleteEntry(id) {
	$.ajax({
		type: "POST",
		data: { "del_entry" : true, "submit" : true, "entry-id" : id },
		success: function() {
			showMessageBox('Eintrag gelöscht!', "notice");
			getEntries('reload');
			
		}
	});
	
	updateCounter();
}

function hideLoader() {
	$('.loader').hide('fast');
}

function showMessageBox(message, type) {
	if (type == 'error')
		$('.message-block').html(message).show('fast').css({ "color" : "#FF0000" });
	else
		$('.message-block').html(message).show('fast');
		
	setTimeout("clearMessageBox()", 4000);
}

function clearMessageBox() {
	$('.message-block').hide('slow').empty();
}