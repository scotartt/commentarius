/*
 * this script loads the commentary entries into the relevant div.
 */

 if (typeof jQuery === 'undefined') { 
 	throw new Error('Commentary\'s JavaScript requires jQuery');
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

 var commentaries = function (cts_urn) {
 	var theUrl = "/api/v1/sourcesection/" + cts_urn + "/?format=json";
 	$.ajax({
 		url: theUrl,
 		success:function(data){
 			populate(data);
 		}
 	});
 }

 var populate = function(json) {
	//alert(JSON.stringify(json['user_commentaries']));
	var user_commentaries = json['user_commentaries'];
	for (var i=0; i<user_commentaries.length; i++) {
		var commentary_url = user_commentaries[i];
		$.ajax({
			url: commentary_url,
			success:function(data){
				commentary_and_user(data);
			}
		});
	}
}

var commentary_and_user = function(json) {
	var userUrl = json['user'];
	$.ajax({
		url: userUrl,
		success:function(data){
			commentary(json, data);
		}
	});
}

var commentary = function(commentjson, userjson) {
	// alert(JSON.stringify(json));
	var rowTR = [
	"<tr class='row small'>",
	commentary_div.call({
		"divclass":"col-sm-9",
		"divcontent": commentjson['commentary']  
	}),
	commentary_div.call({
		"divclass":"col-sm-2",
		"divcontent": userjson['first_name'] + " " + userjson['last_name'] + " (" + userjson['id'] + ")" 
	}),
	commentary_div.call({
		"divclass":"col-sm-1",
		"divcontent": commentjson['votes'] + ''
	}),
	"</tr>"
	].join("");
	$('#commentary-container').append(rowTR)
}

var commentary_div = function () {
	return [
	"<td class='", this.divclass, " small'>",
	this.divcontent,
	"</td>"
	].join('');
};

var userdetail = function(username) {
	var userUrl = "/api/v1/user/?username=" + username;
	$.ajax({
		url: userUrl,
		success:function(data){
			var user_resource_uri = data['objects'][0]['resource_uri']
			$('#f_user_input_id').attr( 'value', user_resource_uri )
		}
	});
}

var update_commentary_form = function(commentform) {
	commentform.find('#f_commentary').val('');
	var cts_urn = commentform.find('#f_cts_urn').attr('value');
	commentaries(cts_urn);
	commentform.find('#f_commentary').val('');
	//commentform.attr('hidden', 'hidden');
	$('#f_button_submit_id').css("background-color", "#ccc");
	$('#hidey-form').slideToggle(400);
}

var make_comment = function(commentform) {
	var ajaxurl = commentform.attr('action');
	var sectionurl = commentform.find('#f_section_input_id').attr('value');
	var userurl = commentform.find('#f_user_input_id').attr('value');
	var commentarytext = commentform.find('#f_commentary').val();
	var csrfmiddlewaretoken = commentform.find("[name='csrfmiddlewaretoken']").attr('value');

	var data = JSON.stringify({
		"commentary": commentarytext,
		"section": sectionurl,
		"user": userurl,
		"csrfmiddlewaretoken": csrfmiddlewaretoken
	});

	// alert(data);

	$.ajax({
		url: ajaxurl,
		type: 'POST',
		contentType: 'application/json',
		data: data,
		dataType: 'json',
		processData: false,
		success: function(response, text, object) {
			alert(text);
		},
		statusCode: {
			201: function() {
				update_commentary_form(commentform)
			},
			400: function() {
				alert( "commentary not posted: 400 bad request" );
			},
			401: function() {
				alert( "unauthorised to post commentary" );
			},
			403: function() {
				alert( "forbidden to post commentary" );
			},
			404: function() {
				alert( "commentary not posted: 404 not found" );
			},
			500: function() {
				alert( "server error prevented commentary posting" );
			},
		}
	});
}
