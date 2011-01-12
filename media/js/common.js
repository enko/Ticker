	function submitNewEntry() {
		var newEntry = $("#newEntry").val();
		
		if (newEntry == 'Neue Meldung schreiben...') {
			return false;
		}
		
		if ( $('input:checkbox:checked').val() == 'on' ) {
			var isPublic = parseInt(1);
		} else {
			var isPublic = parseInt(0);
		}
		
		$.ajax({
			type: "POST",
			data: { "newEntry" : newEntry, "isPublic" : isPublic },
			success: function() {
				$('#newEntry').val('Neue Meldung schreiben...');
				refreshEntries();
				var newEntryCount = parseInt($('.entry-counter').html()) + 1;
				setCounter(newEntryCount);
				$('.charCounter').html('');
			}
		});
	}
	
	function setCounter(counter) {
		if ( counter == 1 ) {
			$('.entry-counter-box').html('Aktuell <span class="entry-counter">'+ counter +'</span> Meldung');
		} else {
			$('.entry-counter-box').html('Aktuell <span class="entry-counter">'+ counter +'</span> Meldungen');
		}	
	}

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
	
	function getEntries() {
		$.getJSON('?entries.json', function(data) {
			for (i = 0; i < data.length; i++) {
				var text = data[i].fields.text;
				var isPublic = data[i].fields.isPublic;
				if (isPublic == true) {
					var status = 'Öffentlich';
				} else {
					var status = 'Intern';
				}
				var published = data[i].fields.published;
				var pk = data[i].pk;
				var container = '.entry-'+ pk;
				$('.entries-box').append('<div class="entry-box box entry-'+pk+'"></div>');
				$(container).append('<div class="entry-text">'+text+'<img src="../media/img/deleteButton.png" title="Diesen Eintrag löschen" class="deleteButton" onClick="deleteEntry('+pk+')"/></div>');
				$(container).append('<div class="entry-status">'+status+'</div>');
				$(container).append('<div class="entry-date">'+published+'</div>');
			}
  		});
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