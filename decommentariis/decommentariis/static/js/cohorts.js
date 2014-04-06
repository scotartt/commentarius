/*
 * this script deals with cohort management.
 */

 if (typeof jQuery === 'undefined') { 
	throw new Error('De Commentariis JavaScript requires jQuery');
 }
 // sending a csrftoken with every ajax request
 function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	crossDomain: false, // obviates need for sameOrigin test
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type)) {
			xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
		}
	}
});

// set up join cohort
$('#cohort-list').ready(function() {
	$('#cohort-list').find('.join-cohort').each(
		function() {
			$(this).click(
				function() {
					var useruri = getuseruri();
					var cohorturi = $(this).attr('cohort');
					var requesturi = $(this).attr('uri');
					var buttonid = $(this).attr('id');
					// have to post a new vote
					var data = JSON.stringify({
						"member": useruri,
						"cohort": cohorturi,
					});
					$.ajax({
						url: requesturi,
						type: 'POST',
						contentType: 'application/json',
						data: data,
						dataType: 'json',
						success:function(data){
							reload(cohorturi, buttonid);
						},
						error:function(jqXHR, textStatus, errorThrown) {
							console.log(jqXHR);
							if (jqXHR.status == 201) {
								reload(cohorturi, buttonid);
							} else {
								alert("Error: " + jqXHR.status + " " + jqXHR.statusText);
							}
						},
					});
				}
			);
		}
	);
});
// set up leave cohort
$('#cohort-list').ready(function() {
	$('#cohort-list').find('.leave-cohort').each(
		function() {
			$(this).click(
				function() {
					var useruri = getuseruri();
					var cohorturi = $(this).attr('cohort');
					var requesturi = $(this).attr('uri');
					var buttonid = $(this).attr('id');
					// have to post a new vote
					var data = JSON.stringify({
						"member": useruri,
						"cohort": cohorturi,
					});
					$.ajax({
						url: requesturi,
						type: 'DELETE',
						success:function(data){
							reload(cohorturi, buttonid);
						},
						error:function(jqXHR, textStatus, errorThrown) {
							console.log(jqXHR);
							alert("Error: " + jqXHR.status + " " + jqXHR.statusText);
							//reload(cohorturi, buttonid);
						},
					});
				}
			);
		}
	);
});
$('#cohort-list').ready(function() {
	$('#cohort-list').find('.delete-cohort').each(
		function() {
			$(this).click(
				function() {
					var useruri = getuseruri();
					var cohorturi = $(this).attr('cohort');
					var requesturi = $(this).attr('uri');
					var buttonid = $(this).attr('id');
					var cohortname = $(this).attr('cohort-name');
					if (confirm("Are you sure you want to delete '" + cohortname + "'?")) {
						$.ajax({
							url: requesturi,
							type: 'DELETE',
							success:function(data){
								reload(cohorturi, "row-" + cohortname);
							},
							error:function(jqXHR, textStatus, errorThrown) {
								console.log(jqXHR);
								alert("Error: " + jqXHR.status + " " + jqXHR.statusText);
							},
						});
					}
				}
			);
		}
	);
});

// get the user name
var getusername = function() {
	return $('#user-username').text();
}
// get the user uri (API)
var getuseruri = function() {
	return $('#user-uri').text();
}

var reload = function(cohorturi, elementid) {
	if (elementid.lastIndexOf('leave-', 0) === 0) {
		console.log(elementid);
	}
	$('#' + elementid).hide();
	// work out how to swap the buttons.
}



