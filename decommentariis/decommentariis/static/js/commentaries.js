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

// set the form element to initially slide up.
$('#hidey-form').ready(function(){
	$('#hidey-form').slideUp(100);
});

// the button on the form needs to trigger this js function. 
$('#f_button_submit_id').ready(function() { 
	//$('#f_button_submit_id').css("background-color", "#ccc");
	$(function() {
		var fn=function(){
			$('#f_button_submit_id').attr('disabled','disabled');
			make_comment($('#commentary-form'))
		};
		$('#f_button_submit_id').click(fn);
	});
}); 

// table container
$('#commentary-form-click-target').ready(function() {
	$(function() {
		var fn=function() {
			$('#hidey-form').slideToggle(400);
		}
		$('#commentary-form-click-target').click(fn);
	});
});

// functions below here
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
	$('#commentary-container').empty();
	/* or in one call:
	   /api/v1/sourcecommentary/?section__cts_urn=<cts_urn>
	   */
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
				commentaryitem(json, data);
			}
		});
	}

	var commentaryitem = function(commentjson, userjson) {
	// alert(JSON.stringify(json));
	var uname_login = getuserdetail();
	var fname = userjson['first_name']
	var lname = userjson['last_name']
	var uname = userjson['username']
	var usernamedetail;
	if (fname === "" && lname === "" && !(uname === "")) {
		usernamedetail = uname;
	} else if (!(fname === "") || !(lname === "")) {
		usernamedetail = fname + " " + lname;
	} else {
		usernamedetail = "unknown";
	}

	
	var divclasstext = "expander ";
	var iseditable = (uname_login === uname);
	if (iseditable) {
		divclasstext = " edit_area ";
	}

	var rowTR = [
	"<tr class='row small'>",
	commentary_td.call({
		"tdclass":"col-sm-9 commentary-text ",
		"tdcontent": commentjson['commentary.html'] ,
		"contentclass": divclasstext,
		"iseditable": iseditable,
	}),
	commentary_td.call({
		"tdclass":"col-sm-2 uname",
		"tdcontent":  usernamedetail + " <span hidden='hidden'>(" + userjson['id'] + ")<span>",
		"contentclass": "",
		"iseditable": false,
	}),
	commentary_td.call({
		"tdclass":"col-sm-1 votes",
		"tdcontent": commentjson['votes'] + '',
		"contentclass": "",
		"iseditable": false,
	}),
	"</tr>"
	].join("");

	if (iseditable) {
		$('#commentary-container').append(rowTR).find(".edit_area").each(
			function() {
				$(this).editable(function(value, settings) { 
					var ajaxurl = commentjson['resource_uri'];
					var postdata = {};
					postdata['commentary'] = value;
					$(this).attr('disabled', true);
					var commentaryform = $('#commentary-form');
					$('#hidey-form').slideUp(10);
					sendcomment(ajaxurl, 'PUT', JSON.stringify(postdata), commentaryform);
					return(value);
				}, 
				{
					data    : commentjson['commentary.md'],
					type    : 'textarea',
					submit  : 'Save',
					tooltip : 'Click to edit your own commentary...',
					style   : 'inherit',
				}); //end $(this).editable(function()) {...});
			} // end the outer function() { ... } (passed to .each())
		); // end each( ... );
	} else {
		$('#commentary-container').append(rowTR).find(".expander").each(
			function() {
				$(this).expander({
					slicePoint: 150,
					expandEffect: 'fadeIn',
					expandSpeed: 250,
					collapseEffect: 'fadeOut',
					collapseSpeed: 200,
				}); //end $(this).expander({ ... });
			} // end function{ ... } in each()
		); //end each( ... );
	}
}

var commentary_td = function () {
	return [
	"<td class='",this.tdclass," small'>",
	"<div class='",this.contentclass,"small' editable='",this.iseditable,"'>",
	this.tdcontent,
	"</div></td>"
	].join('');
};

var setuserdetail = function() {
	var username = getuserdetail();
	var userQueryUrl = "/api/v1/user/?username=" + username;
	$.ajax({
		url: userQueryUrl,
		success:function(data){
			var user_resource_uri = data['objects'][0]['resource_uri']
			$('#f_user_input_id').attr( 'value', user_resource_uri )
		}
	});
}

var getuserdetail = function() {
	return $('#user-username').text();
}

var update_commentary_form = function(commentform) {
	commentform.find('#f_commentary').val('');
	var cts_urn = commentform.find('#f_cts_urn').attr('value');
	commentaries(cts_urn);
	commentform.find('#f_commentary').val('');
	$('#f_button_submit_id').removeAttr('disabled');
	$('#hidey-form').slideUp(400);
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

	sendcomment(ajaxurl, 'POST', data, commentform);
}

var sendcomment = function(ajaxurl, methodtype, data, commentform) {
	$.ajax({
		url: ajaxurl,
		type: methodtype,
		contentType: 'application/json',
		data: data,
		dataType: 'json',
		processData: false,
		statusCode: {
			200: function() {
				//console.log("200 is success");
				update_commentary_form(commentform)
			},
			201: function() {
				//console.log("201 is success");
				update_commentary_form(commentform)
			},
			204: function() {
				//console.log("204 is success");
				update_commentary_form(commentform)
			},
			205: function() {
				//console.log("205 is success");
				update_commentary_form(commentform)
			},
			206: function() {
				//console.log("206 is success");
				update_commentary_form(commentform)
			},
			400: function() {
				error( "Commentary not posted: 400 Bad Request (the gods were not pleased by your sacrifice and the request was denied)" );
			},
			401: function() {
				error( "Not authorised to post commentary (the gods would prefer you don't do that right now)" );
			},
			403: function() {
				error( "Forbidden to post commentary (the gods forbid this from happening)" );
			},
			404: function() {
				error( "Commentary not posted: 404 not found (the gods can't be found)" );
			},
			405: function() {
				error( "Commentary not posted: HTTP Error Status 405 (the gods forbid the method of scarfice you are using)" );
			},
			406: function() {
				error( "Commentary not posted: HTTP Error Status 406 (the gods do not find your sacrifice acceptable)" );
			},
			407: function() {
				error( "Commentary not posted: HTTP Error Status 407 (the gods deny your proxy is authentic)" );
			},
			408: function() {
				error( "Commentary not posted: HTTP Error Status 408 (the gods are busy battling titans and could not find the time for your request)" );
			},
			409: function() {
				error( "Commentary not posted: HTTP Error Status 409 (the gods are in conflict)" );
			},
			410: function() {
				error( "Commentary not posted: HTTP Error Status 410 (the gods are gone (see also: Sophocles))" );
			},
			411: function() {
				error( "Commentary not posted: HTTP Error Status 411 (the gods demand a sacrifice of appropriate length)" );
			},
			412: function() {
				error( "Commentary not posted: HTTP Error Status 412 (the gods demand preconditions which were not satisfied)" );
			},
			413: function() {
				error( "Commentary not posted: HTTP Error Status 413 (the gods have determined your sacrificial entity was too large)" );
			},
			414: function() {
				error( "Commentary not posted: HTTP Error Status 414 (the gods found your prayers went for too long and refused to accept them)" );
			},
			415: function() {
				error( "Commentary not posted: HTTP Error Status 415 (the gods don't accept this type of sacrifice)" );
			},
			416: function() {
				error( "Commentary not posted: HTTP Error Status 416 (the gods cannot satisfy the range of your requests)" );
			},
			417: function() {
				error( "Commentary not posted: HTTP Error Status 417 (the gods were expecting something else)" );
			},
			500: function() {
				error( "Server error: 500 Internal Error (the gods punish hubris)" );
			},
			501: function() {
				error( "Server error: 501 Not Implemented (the gods have not implemented this type of sacrifice)" );
			},
			502: function() {
				error( "Server error: 502 Bad Gateway (the gods tried to relay your request and were denied)" );
			},
			503: function() {
				error( "Server error: 503 Service Unavailable (the gods are getting too many sacrifices right now to deal with yours, tray again later)" );
			},
			504: function() {
				error( "Server error: 504 Gateway Timeout (the gods tried to relay your request but the other gods aren't listening)" );
			},
			505: function() {
				error( "Server error: 505 HTTP Version Not Supported (the gods don't like that method)" );
			},
		}
	});
}

var error = function(msg) {
	alert(msg); // work out something nicer later.
	//var alert = '<div class="alert alert-danger">' + msg + '.</div>'
}

