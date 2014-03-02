/*
 * this script loads the commentary entries into the relevant div.
 */

if (typeof jQuery === 'undefined') { throw new Error('Commentary\'s JavaScript requires jQuery') }

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
				"divcontent": userjson['first_name'] + " " + userjson['last_name'] 
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
