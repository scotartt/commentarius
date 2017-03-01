/*
 * this script loads the commentary entries into the relevant div.
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
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            console.log("token is " + $.cookie('csrftoken') + " " + xhr + " " + settings);
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});


// set the form element to initially slide up.
$('#hidey-form').ready(function () {
    $('#hidey-form').removeAttr('hidden');
    $('#hidey-form').slideUp(0);
});

// the button on the form needs to trigger this js function. 
$('#f_button_submit_id').ready(function () {
    //$('#f_button_submit_id').css("background-color", "#ccc");
    $(function () {
        var fn = function () {
            $('#f_button_submit_id').attr('disabled', 'disabled');
            make_comment($('#commentary-form'))
        };
        $('#f_button_submit_id').click(fn);
    });
});

// table container
$('#commentary-form-click-target').ready(function () {
    $(function () {
        var fn = function () {
            $('#hidey-form').slideToggle(400);
        }
        $('#commentary-form-click-target').click(fn);
    });
    $('#commentary-form-click-target').removeAttr('hidden');
});

// get the user name
var getusername = function () {
    return $('#user-username').text();
}
// get the user uri (API)
var getuseruri = function () {
    return $('#user-uri').text();
}

// functions below here
var commentaries = function (cts_urn) {
    var theUrl = "/api/v1/sourcesection/" + cts_urn + "/?format=json";
    //   /api/v1/sourcecommentary/?section__cts_urn=<cts_urn>
    $.ajax({
        url: theUrl,
        success: function (data) {
            populate(data);
        }
    });
}

var idify = function (s) {
    if (s != null) {
        return "id" + s.replace(/[^A-Za-z0-9:_-]/g, '_');
    } else {
        return "";
    }
}

var populate = function (json) {
    var user_commentaries = json['user_commentaries'];
    $('#commentary-container').empty();
    for (var i = 0; i < user_commentaries.length; i++) {
        var commentary_url = user_commentaries[i];
        var theid = idify(commentary_url);
        var rowTR = ["<tr class='row small commentary-item-row' id='", theid, "'/>"].join("");
        $('#commentary-container').append(rowTR);
        $('#' + theid).slideUp(0);
        $.ajax({
            url: commentary_url,
            success: function (data) {
                commentary_and_user(data);
            }
        });
    }
}

var update_single_entry = function (commentary_url) {
    var theid = '#' + idify(commentary_url);
    if ($(theid) == null || $(theid).length === 0) {
        console.log("in here");
        var rowTR = ["<tr class='row small commentary-item-row' id='", theid, "'/>"].join("");
        $('#commentary-container').append(rowTR);
        console.log(rowTR);
    }
    $.ajax({
        url: commentary_url,
        success: function (data) {
            commentary_and_user(data);
        }
    });

}

var commentary_and_user = function (json) {
    var userUrl = json['user'];
    $.ajax({
        url: userUrl,
        success: function (data) {
            commentaryitem(json, data);
        }
    });
}

var commentaryitem = function (commentjson, userjson) {
    var uname_login = getusername();
    var fname = userjson['first_name'];
    var lname = userjson['last_name'];
    var uname = userjson['username'];

    var usernamedetail;
    if (uname !== "") {
        usernamedetail = '<a href="/commentary/' + uname + '/">' + uname + '</a>';
    } else if (fname !== "" && lname !== "") {
        usernamedetail = '<a href="/commentary/' + uname + '/">' + fname + " " + lname + '</a>';
    } else {
        usernamedetail = "unknown";
    }

    var divclasstext = "expander ";
    var iseditable = (uname_login === uname);
    if (iseditable) {
        divclasstext = " edit_area ";
    }

    var theid = idify(commentjson['resource_uri']);
    var rowTR = $('#' + theid);
    rowTR.empty();

    rowTR.append(commentary_td.call({
        "tdclass": "col-sm-2 uname",
        "tdcontent": usernamedetail + " <span hidden='hidden'>(" + userjson['id'] + ")<span>",
        "contentclass": "",
        "iseditable": false,
    }));

    rowTR.append(commentary_td.call({
        "tdclass": "col-sm-8 commentary-text ",
        "tdcontent": commentjson['commentary.html'],
        "contentclass": divclasstext,
        "iseditable": iseditable,
    }));

    make_vote_button(commentjson, rowTR, iseditable, theid);

    if (iseditable) {
        rowTR.find(".edit_area").each(
            function () {
                $(this).editable(function (value, settings) {
                        var ajaxurl = commentjson['resource_uri'];
                        var postdata = {};
                        postdata['commentary'] = value;
                        $(this).attr('disabled', true);
                        var commentaryform = $('#commentary-form');
                        $('#hidey-form').slideUp(10);
                        sendcomment(ajaxurl, 'PUT', JSON.stringify(postdata), commentaryform);
                        return (value);
                    },
                    {
                        data: commentjson['commentary.md'],
                        type: 'textarea',
                        submit: 'Save',
                        tooltip: 'Click to edit your own commentary...',
                        style: 'inherit',
                    }); //end $(this).editable(function()) {...});
            } // end the outer function() { ... } (passed to .each())
        ); // end each( ... );
    } else {
        rowTR.find(".expander").each(
            function () {
                $(this).expander({
                    slicePoint: 150,
                    expandEffect: 'fadeIn',
                    expandSpeed: 250,
                    collapseEffect: 'fadeOut',
                    collapseSpeed: 250,
                    moreClass: 'read-more text-info',
                    lessClass: 'read-less text-info',
                    expandPrefix: ' … ',
                }); //end $(this).expander({ ... });
            } // end function{ ... } in each()
        ); //end each( ... );
    }
    // rowTR.removeAttr('hidden');
    rowTR.slideDown(400);
}

var commentary_td = function () {
    return [
        "<td class='", this.tdclass, " small'>",
        "<div class='", this.contentclass, "small' editable='", this.iseditable, "'>",
        this.tdcontent,
        "</div></td>"
    ].join('');
}

var make_vote_button = function (commentjson, rowTR, iseditable, theid) {
    var voterlist = commentjson['voters'];
    var votes_num = voterlist.length;
    console.log("there are " + votes_num + " votes.");
    var user_resource_uri = getuseruri();
    // why are where using uri here and username elsewhere?
    var has_voted = false;
    var self_voted = false;
    var existing_vote_uri = false;
    if (voterlist) {
        for (var i = 0; i < voterlist.length; i++) {
            rowTR.append("<span hidden='hidden' class='voteid' voter='" + voterlist[i].voter + "'/>")
            if (user_resource_uri === voterlist[i].voter) {
                has_voted = true;
                existing_vote_uri = voterlist[i].resource_uri;
                /* this user voted for this comment already */
            } else if (commentjson['user'] === voterlist[i].voter) {
                self_voted = true;
                /* all voting by all users will be disabled, user voted for self.*/
            }
        }
    }
    var btnclass = "btn-default";
    var userisowner = "";
    if (has_voted) {
        btnclass = "btn-success";
    } else if (votes_num > 0) {
        btnclass = "btn-primary";
    }
    if (self_voted) {
        userisowner = 'disabled="disabled"';
        btnclass = "btn-warning";
    } else if (iseditable) {
        userisowner = 'disabled="disabled"';
    }

    rowTR.append(voterbutton.call({
        "votes": votes_num,
        "voterid": 'votes_' + theid,
        "btnclass": btnclass,
        "userisowner": userisowner,
        "commentary_uri": commentjson['resource_uri'],
        "user_uri": user_resource_uri,
        "vote_uri": existing_vote_uri,
    }));
    rowTR.find(".btn-vote").each(
        function () {
            $(this).click(
                function () {
                    var commentaryform = $('#commentary-form');
                    var csrfmiddlewaretoken = commentaryform.find("[name='csrfmiddlewaretoken']").attr('value');
                    var commentary_uri = $(this).attr('commentary_uri')
                    if ($(this).attr('vote_uri') !== 'false') {
                        var voteapiuri = $(this).attr('vote_uri');
                        $.ajax({
                            url: voteapiuri,
                            type: 'DELETE',
                            success: function (data) {
                                update_single_entry(commentary_uri);
                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                console.log(jqXHR);
                                update_single_entry(commentary_uri);
                            },
                        })
                    } else {
                        // have to post a new vote
                        var data = JSON.stringify({
                            "voter": $(this).attr('user_uri'),
                            "entry": commentary_uri,
                            "csrfmiddlewaretoken": csrfmiddlewaretoken,
                        });

                        var voteapiuri = "/api/v1/voter/";
                        $.ajax({
                            url: voteapiuri,
                            type: 'POST',
                            contentType: 'application/json',
                            data: data,
                            dataType: 'json',
                            success: function (data) {
                                update_single_entry(commentary_uri);
                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                console.log(jqXHR);
                                update_single_entry(commentary_uri);
                            },
                        });
                    }
                }
            )
        }
    );
}

var voterbutton = function () {
    return ['<td class="col-sm-2 votes small">',
        '<div class="input-group" id="', this.voterid, '">',
        '<button class="btn-vote btn btn-xs ', this.btnclass, '" ', this.userisowner,
        ' user_uri="', this.user_uri, '"',
        ' commentary_uri="', this.commentary_uri, '"',
        ' vote_uri="', this.vote_uri, '"',
        ' >',
        '<span class="glyphicon glyphicon-thumbs-up"></span>',
        '&nbsp;<span style="font-size: x-small;">',
        this.votes,
        '</span></button>',
        '</div>',
        '</td>'].join('');
}

function pad(num, size) {
    var s = num + "";
    while (s.length < size) s = "0" + s;
    return s;
}

var setuserdetail = function () {
    var username = getusername();
    var userQueryUrl = "/api/v1/user/?username=" + username;
    $('#f_user_input_id').attr('value', getuseruri());
}


var update_commentary_form = function (commentform) {
    commentform.find('#f_commentary').val('');
    var cts_urn = commentform.find('#f_cts_urn').attr('value');
    commentaries(cts_urn);
    commentform.find('#f_commentary').val('');
    $('#f_button_submit_id').removeAttr('disabled');
    $('#hidey-form').slideUp(400);
}

var make_comment = function (commentform) {
    var ajaxurl = commentform.attr('action');
    var sectionurl = commentform.find('#f_section_input_id').attr('value');
    var userurl = getuseruri();
    var commentarytext = commentform.find('#f_commentary').val();
    var csrfmiddlewaretoken = commentform.find("[name='csrfmiddlewaretoken']").attr('value');

    var data = JSON.stringify({
        "commentary": commentarytext,
        "section": sectionurl,
        "user": userurl,
        "voters": [],
        "csrfmiddlewaretoken": csrfmiddlewaretoken
    });
    console.log("the data is " + data);
    sendcomment(ajaxurl, 'POST', data, commentform);
}

var sendcomment = function (ajaxurl, methodtype, data, commentform) {
    console.log("Sending comments to " + ajaxurl + "\nMETHOD " + methodtype + "\nDATA\n" + data);
    $.ajax({
        url: ajaxurl,
        type: methodtype,
        contentType: 'application/json',
        data: data,
        dataType: 'json',
        processData: false,
        statusCode: {
            200: function () {
                //console.log("200 is success");
                update_commentary_form(commentform)
            },
            201: function () {
                //console.log("201 is success");
                update_commentary_form(commentform)
            },
            204: function () {
                //console.log("204 is success");
                update_commentary_form(commentform)
            },
            205: function () {
                //console.log("205 is success");
                update_commentary_form(commentform)
            },
            206: function () {
                //console.log("206 is success");
                update_commentary_form(commentform)
            },
            400: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: 400 Bad Request", jqXHR);
            },
            401: function (jqXHR, textStatus, errorThrown) {
                error("Not authorised to post commentary", jqXHR);
            },
            403: function (jqXHR, textStatus, errorThrown) {
                error("Forbidden to post commentary", jqXHR);
            },
            404: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: 404 not found", jqXHR);
            },
            405: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 405", jqXHR);
            },
            406: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 406", jqXHR);
            },
            407: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 407", jqXHR);
            },
            408: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 408", jqXHR);
            },
            409: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 409", jqXHR);
            },
            410: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 410 (the gods are gone (see also: Sophocles))", jqXHR);
            },
            411: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 411", jqXHR);
            },
            412: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 412", jqXHR);
            },
            413: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 413", jqXHR);
            },
            414: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 414", jqXHR);
            },
            415: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 415", jqXHR);
            },
            416: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 416", jqXHR);
            },
            417: function (jqXHR, textStatus, errorThrown) {
                error("Commentary not posted: HTTP Error Status 417", jqXHR);
            },
            500: function (jqXHR, textStatus, errorThrown) {
                error("Server error: 500 Internal Error (the gods punish hubris)", jqXHR);
            },
            501: function (jqXHR, textStatus, errorThrown) {
                error("Server error: 501 Not Implemented", jqXHR);
            },
            502: function (jqXHR, textStatus, errorThrown) {
                error("Server error: 502 Bad Gateway", jqXHR);
            },
            503: function (jqXHR, textStatus, errorThrown) {
                error("Server error: 503 Service Unavailable (try again later)", jqXHR);
            },
            504: function (jqXHR, textStatus, errorThrown) {
                error("Server error: 504 Gateway Timeout", jqXHR);
            },
            505: function (jqXHR, textStatus, errorThrown) {
                error("Server error: 505 HTTP Version Not Supported", jqXHR);
            },
        },
    });
}

var error = function (msg, jqXHR) {
    console.log(jqXHR);
    console.log(msg);
    alert(msg); // work out something nicer later.
    //var alert = '<div class="alert alert-danger">' + msg + '.</div>'
}

