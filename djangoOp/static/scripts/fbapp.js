var currentpage = "main";
var selectedtags = []; // tags selected in play1
var quizdata = null; // all the retrieved quiz
var f_question = 0; //first question
var current_quiz = 0; //current quiz
var quiz_n = 10; //number of quiz retrieved
var quiz_wanted = 10; //number of quiz we would like to retrieve
var mylang = 'it'; // language
var answered = false; // if user has already answered 
var timer = 0;
var mtimer = null; // timer object
var goNextTimer = null; // timer go next
var answer_time = 20; // seconds to answer a quiz
var id2tag = []; //binds id of tags and tags
var scoretag = [];
var is_winner = true;
var score = 0;
var muid = 0;
var audio_on = true;

soundManager.url = '/media/swf/';
soundManager.flashVersion = 9; // optional: shiny features (default = 8)
soundManager.useFlashBlock = false; // optionally, enable when you're ready to dive in
// enable HTML5 audio support, if you're feeling adventurous. iPad/iPhone will always get this.
// // soundManager.useHTML5Audio = true;



// **********  AFTER FUNCTIONS ******* //

function after_main() {
	if (muid !== 0) {
                $("#score-head").empty().html("Ciao <fb:name uid='"+muid+"' useyou='false' firstnameonly='true' linked='false'> </fb:name>!");
                $("#addlink").attr("href", "javascript:load_addquiz1()");
		// $("#score-head").append("<br/><fb:profile-pic uid="+muid+" linked='false' size='q'> </fb:profice-pic>");
                FB.XFBML.parse(document.getElementById('score-head'));
        }

    $(".slidetabs").tabs(".images > div", {
                effect: 'fade',
                fadeOutSpeed: "slow",
                rotate: true
    }).slideshow();
    $(".slidetabs").data("slideshow").play();
/*
	$('.opponent_msg').qtip({
	   content: "La vita e' come una scatola di cioccolatini... ",
	   position: {
	      corner: {
		 target: 'topRight',
		 tooltip: 'bottomLeft'
	      }
	   },
	   style: { 
		name: 'cream' , // Inherit from preset style
		border: {
		width: 5,
		radius: 10
		},
		padding: 10,
		textAlign: 'center',
		tip: true // Give it a speech bubble tip with automatic corner detection
	   },
	   show: 'mouseover',
	   hide: 'mouseout'
	});

*/
    if (! audio_on) {
                $("#audiocontrol img").attr("src",'http://www.openpursuit.org/media/img/audiooff.png' );
    }
    soundManager.stopAll();
    if (! soundManager.getSoundById('intro')) {
        soundManager.createSound({
                id: 'intro',
                url: '/static/sound/intro.mp3',
                autoPlay: true,
                loops: 10 
        });
    } else {
        soundManager.play('intro');
    }
     //   $(".slidetabs").tabs(".images > div", { effect: 'fade', fadeOutSpeed: "slow", rotate: true }).slideshow();
}



function after_play1(){

}

function after_play3() {
	if (muid === 0 ) {
		//$('#menu_registered').empty().html('<a href="javascript:publish_score()"> Pubblica il tuo punteggio </a><br /><div id="save_status"><a href="javascript:save_score()">Salva</a></div>');
            $(' menu_registered').empty().html(' <p> Per salvare la partita e giocare con i tuoi amici devi registrarti</p> <a href="javascript:do_login()">Registrati!</a><br />');
        // $("#tabs").tabs();
	}

    soundManager.stopAll();

    if (! soundManager.getSoundById('score')) {
        soundManager.createSound({
                    id: 'score',
                    url: '/static/sound/score.mp3',
                    autoPlay: true,
                    loops: 10 
        });
    } else {
                soundManager.play('score');
    }

    FB.XFBML.parse(document.getElementById('chart-main'));
    var score_text = "";
    for (i=0;i<selectedtags.length;i=i+1) {
         score_text = score_text + " " + selectedtags[i] + " " + scoretag[selectedtags[i]] + "punti - ";
    }
	$("#score-in-game-value").empty().text(score_text);

    $("div.scrollable").scrollable({ speed: 700, circular: true});



}


function after_addquiz1() {
    $('#id_uid').val(muid);
    var options = {
        beforeSubmit: form_validate,
        success: load_quiz_added,
        url: '/fbapp/addquiz?uid='+muid
    };
    
    $('#addform').ajaxForm(options);


	var acServer_id_tags = "/base/tag_lookup/";
    var acSchema_id_tags = ["resultset.results", "tag", "occurrencies" ];
    var acDataSource_id_tags = new YAHOO.widget.DS_XHR(acServer_id_tags, acSchema_id_tags);
    acDataSource_id_tags.queryMatchContains = true;
    
    acAutoComp_id_tags = new YAHOO.widget.AutoComplete("id_tags","id_tags_container", acDataSource_id_tags);
    acAutoComp_id_tags.useIFrame = true;
     
    
    acAutoComp_id_tags.doBeforeExpandContainer = function(oTextbox, oContainer, sQuery, aResults) { 
        var pos = YAHOO.util.Dom.getXY(oTextbox); 
        pos[1] += YAHOO.util.Dom.get(oTextbox).offsetHeight + 2; 
        YAHOO.util.Dom.setXY(oContainer,pos); 
        return true; 
    }; 
    
    acAutoComp_id_tags.animVert = true;
    acAutoComp_id_tags.animHoriz = false; 
    acAutoComp_id_tags.animSpeed = 0.3; 
    acAutoComp_id_tags.delimChar = [" "]; 
    acAutoComp_id_tags.maxResultsDisplayed = 20;
    acAutoComp_id_tags.queryDelay = 0;
    acAutoComp_id_tags.autoHighlight = false;
    acAutoComp_id_tags.useShadow = true; 
    
    acAutoComp_id_tags.typeAhead = true; 
    acAutoComp_id_tags.formatResult = function(oResultItem, sQuery) {
       var sResult = oResultItem[0];
       var sOcc = oResultItem[1];
       if(sResult) {
         var aMarkup = ["<div>",
         "<span style='text-align:left'>",
         sResult,
         "</span>",
         "<span style='font-size:x-small;color:green;'>",
         "(",
         sOcc,
         " results)",
         "</span>",
         "</div>"];
         return (aMarkup.join("")); 
       }
         else {
         return "";
       }
    };

}

function after_play2() {
	if (muid !== 0) {
		$("#play_profile_name").empty().append("<fb:profile-pic uid="+muid+" linked='true' size='q'> </fb:profice-pic>");
		FB.XFBML.parse(document.getElementById('play_profile_name'));
	}
	$.ajax({
	  url: '/api/getquiz?tags='+selectedtags.join(",")+'&limit='+quiz_wanted+'&lang='+mylang,
	  async: false,
	  dataType: 'json',
	  success: function(data) {
		quizdata = [];
        for (index in data){
            quizdata.push(data[index]);
        }
		quiz_n = quizdata.length;
		for (i=0;i<selectedtags.length;i=i+1) {
			scoretag[selectedtags[i]] = 50;
		}
		f_question = Math.floor(Math.random()*quiz_n);
		current_quiz = f_question;

		$('#question').html(quizdata[current_quiz].question);
		var rnd = Math.floor(Math.random()*4);
		$('#answer'+(rnd%4) ).html(quizdata[current_quiz].right);
		$('#answer'+(rnd%4) ).addClass('ra');
		$('#answer'+((rnd+1)%4)).html(quizdata[current_quiz].wrong1);
		$('#answer'+((rnd+2)%4)).html(quizdata[current_quiz].wrong2);
		$('#answer'+((rnd+3)%4)).html(quizdata[current_quiz].wrong3);
        if (quizdata[current_quiz].author.fb_uid) {
            $('#author').html("Autore: " + quizdata[current_quiz].author.name + "<br><fb:profile-pic uid="+quizdata[current_quiz].author.fb_uid+" linked='false' size='q'> </fb:profice-pic>" );
        } else {
            $('#author').html("Autore: "+ quizdata[current_quiz].author.name);
        }
        FB.XFBML.parse(document.getElementById('author'));
		$('.answer').click( function() { 
				if (answered === true) {
					return false;
                }
				if ($(this).hasClass('ra'))  {
					$(this).addClass('right');
					is_winner=true;
                    soundManager.play('sound_right');
				} else {
					$(this).addClass('wrong');
					is_winner = false;
                    soundManager.play('sound_wrong');
				}
				answered = true;
				if (mtimer !== null) {
					clearTimeout(mtimer);
				}
				goNextTimer = setTimeout("$('.answer').removeClass('ra').removeClass('right').removeClass('wrong');next_quiz();answered=false;",800);	
                return true;
			} 
		);
		load_tagscore();
		start_timer();
		
	}});
}	





// **********  LOAD FUNCTIONS ******* //
function load_main() { 
	$("#ajax_loader").empty().html('<div id="loading"><img src="http://www.openpursuit.org/media/img/loading.gif" /></div>');
	$('#ajax_loader').load('main?uid='+muid+' #ajax_loaded', function(response, status, xhr) { after_main(); });
    soundManager.stopAll(); 
    // sound_intro.play({onfinish:loopSound });
	scoretag = [];
	id2tag = [];		
	selectedtags = [];
	if (goNextTimer !== null) {
		clearTimeout(goNextTimer);	
		goNextTimer = null;
	}
	if (mtimer !== null) {
		clearTimeout(mtimer);
		mtimer = null;
	}
	currentpage = "main";
 }

function load_play1() { 
	selectedtags = [];
    soundManager.stopAll();
	$("#what_is").hide();
	$("#ajax_loader").empty().html('<div id="loading"><img src="http://www.openpursuit.org/media/img/loading.gif" /></div>');
	$('#ajax_loader').load('play #ajax_loaded' , function(response, status, xhr) { after_play1(); } );


	currentpage = "play1";
 }
function load_play2() { 
	scoretag = [];
	$("#ajax_loader").empty().html('<div id="loading"><img src="http://www.openpursuit.org/media/img/loading.gif" /></div>');
	$('#ajax_loader').load('play2 #ajax_loaded', function(response, status, xhr) { after_play2(); } );
	currentpage = "play2";
    soundManager.stopAll();
    if (! soundManager.getSoundById('play')) {
        soundManager.createSound({
            id: 'play',
            url: '/static/sound/play.mp3',
            autoPlay: true,
            loops: 10 
            // onload: [ event handler function object ],
            // other options here..
        });
    } else {
         soundManager.play('play');
    }

}
 
function load_quiz_added() { 
    $('#ajax_loaded').empty().html('Quiz aggiunto correttmente, <a href="javascript:load_addquiz1()">Aggiungi un altro quiz</a> o <a href="javascript:load_main()">Torna al menu</a>');
}

function load_play3() { 
	$("#ajax_loader").empty().html('<div id="loading"><img src="http://www.openpursuit.org/media/img/loading.gif" /></div>');
    var tags = '&tag='+selectedtags.join('&tag=');
	$('#ajax_loader').load('play3?uid='+muid+tags+' #ajax_loaded', function(response, status, xhr) { after_play3(); } );
	currentpage = "play3";
	id2tag = [];
	if (mtimer !== null) {
                clearTimeout(mtimer);
                mtimer = null;
        }
	if (goNextTimer !== null) {
                clearTimeout(goNextTimer);
		goNextTimer = null;
        }

}

function load_tagscore() {
    return;
	$("#tagscore tbody").empty();
	for(var index in scoretag) {
		$("#tagscore tbody").prepend("<tr style='height: 10px;' class='tag-bar-row'><td>"+index+"</td><td>" + scoretag[index] + "</td><td> <div style='height:5px;' id='score_" + index + "_bar' class='tag-bar'></div></td></tr>");
		$("#score_" + index + "_bar" ).progressbar({ value: scoretag[ index ]  });
		var value = scoretag[ index ];
		var elem = $("#score_" + index + "_bar" );
		if (value < 10){
                            elem.css({ 'background': 'Red' });
                        } else if (value < 30){
                            elem.css({ 'background': 'Orange' });
                        } else if (value < 50){
                            elem.css({ 'background': 'Yellow' });
                        } else{
                            elem.css({ 'background': 'LightGreen' });
                        }
		
	}
	$("#score-in-game-value").empty().html(score);

}


// ******* END LOAD *************//

//function loopSound() {
//    if (currentpage == "main") {
//        this.play({onfinish:loopSound});
//    }
//}

function form_validate(formData, jqForm, options) {
            var queryString = $.param(formData); 
            var errors = false;
             for(var index in formData) {
                if (! formData[index].value) {
                    $("#id_" + formData[index].name + "_error").empty().html("Questo campo non puo' essere vuoto");
                    $("#id_" + formData[index].name + "_error").addClass('formerror');
                    errors = true;
                }
             }
            if (errors) {
                return false;
            }
             
                // jqForm is a jQuery object encapsulating the form element.  To access the 
                //     // DOM element for the form do this: 
                //         // var formElement = jqForm[0]; 
                //          
                //alert('About to submit: \n\n' + queryString); 
                //
        return true;
}




function next_quiz() {
	goNextTimer = null;
	for(var index in quizdata[current_quiz].tags) {
		for(var index2 in id2tag) {
			if (quizdata[current_quiz].tags[index] == index2 ) {
				if (is_winner === true ) {
					scoretag[ id2tag[index2] ] += timer;
					score += timer;
				} else {
					scoretag[ id2tag[index2] ] -= 15;
				    score -= 15;
				}

			}
		} 
	}
	load_tagscore();
	current_quiz = (current_quiz +1)%quiz_n;
	if (current_quiz == f_question) {
		load_play3(); // end of game
	}
    $('.answer').removeClass('ra');
	$('#question').html(quizdata[current_quiz].question);
	var rnd = Math.floor(Math.random()*4);
	$('#answer'+(rnd%4) ).html(quizdata[current_quiz].right);
	$('#answer'+(rnd%4) ).addClass('ra');
	$('#answer'+((rnd+1)%4)).html(quizdata[current_quiz].wrong1);
	$('#answer'+((rnd+2)%4)).html(quizdata[current_quiz].wrong2);
	$('#answer'+((rnd+3)%4)).html(quizdata[current_quiz].wrong3);
    if (quizdata[current_quiz].author.fb_uid) {
            $('#author').html("Autore: " + quizdata[current_quiz].author.name + "<br><fb:profile-pic uid="+quizdata[current_quiz].author.fb_uid+" linked='true' size='q'> </fb:profice-pic>" );
        } else {
            $('#author').html("Autore: "+ quizdata[current_quiz].author.name);
        }
        FB.XFBML.parse(document.getElementById('author'));

	start_timer();
}


function start_timer() {
	timer = answer_time; 
	$('#timer').text(timer);
	mtimer = setTimeout("loop_timer();",1000);
        $('#timer').removeClass("timer-hurry");
}
function loop_timer() {
	timer = timer - 1;
	mtimer = null;
	if (currentpage != "play2") {
		return;
    }
	$('#timer').text(timer);
	if (timer <= 0) {
		// alert('tempo scaduto');
		$('#timer').removeClass("timer-hurry");
		$('.answer').addClass('wrong');
		answered = true;
		mtimer = null;
		goNextTimer = setTimeout("$('.answer').removeClass('right').removeClass('wrong');is_winner=false;next_quiz();answered=false;",800);
        soundManager.play('sound_timeout');
	} else if (timer <= 5) {
                $('#timer').addClass("timer-hurry");
                mtimer = setTimeout("loop_timer();",1000);
                soundManager.play('sound_tick');
	} else {
		mtimer = setTimeout("loop_timer();",1000);
	}
	
	
}

function load_challenge1() { 
	$("#what_is").hide();
    soundManager.stopAll();

	$("#ajax_loader").empty().html('<div id="loading"><img src="http://www.openpursuit.org/media/img/loading.gif" /></div>');
	$('#ajax_loader').load('challenge #ajax_loaded', function(response, status, xhr) { after_challenge1(); } );
	currentpage = "challenge1";
		
}
function load_addquiz1() { 
	$("#what_is").hide();
    soundManager.stopAll();
	$("#ajax_loader").empty().html('<div id="loading"><img src="http://www.openpursuit.org/media/img/loading.gif" /></div>');
	$('#ajax_loader').load('addquiz #ajax_loaded', function(response, status, xhr) { after_addquiz1(); } );
	currentpage = "addquiz1";
    soundManager.stopAll();
    if (! soundManager.getSoundById('add')) { 
        soundManager.createSound({
            id: 'add',
            url: '/static/sound/add.mp3',
            autoPlay: true,
            loops: 10 
        });
    } else {
        soundManager.play('add');
    }


}


function switch_audio() {
    if (audio_on) {
        $("#audiocontrol img").attr("src",'http://www.openpursuit.org/media/img/audiooff.png' );
        soundManager.mute();
        audio_on = false;
    } else {
        $("#audiocontrol img").attr("src",'http://www.openpursuit.org/media/img/audioon.png' );
        soundManager.unmute();
        audio_on = true;
    }

}

function op_logo() { 
	if (currentpage == "main") {
		$("#what_is").toggleClass( 'is_show' );
		if ($("#what_is").is('.is_show') ) {
            $("#openpursuit_banner").hide();
			$("#what_is").show('slow');
		} else {
			$("#what_is").hide('slow');
            $("#openpursuit_banner").show();
		}
	} else {
		$("#what_is").removeClass( 'is_show' );
		load_main();
	}
 }


function removetag( tag , tagid ) {
	for (var count = 0; count < selectedtags.length; count++) {
		if (selectedtags[count] == tag) {
			selectedtags.splice(count,1); 
		}
	}
    for (var count2 = 0; count2 < id2tag.length; count2++) {
        if (id2tag[count2] == tag) {
            id2tag.splice(count2,1);
        }
    }
	//$("#table-selected-tags td").remove(":contains("+tag+")");
    $("#tag_" + tagid.toString() ).removeClass("selected-tag");
    $("#tag_" + tagid.toString() ).attr("href", 'javascript:writetag("' + tag + '","' + tagid + '")');
}


function writetag( tag, tagid ) {
    if (selectedtags.toString().search(tag) < 0 && selectedtags.length < 4) {
        id2tag[tagid] = tag;
        selectedtags.push(tag);
//		$("#table-selected-tags tr").append('<td scope="col"><div class="rounded-corners selected-tag"><a href=\"javascript:removetag(\''+tag+'\')\">' + tag + '</a><div></td>');
        $("#tag_" + tagid.toString() ).addClass("selected-tag");
        $("#tag_" + tagid.toString() ).attr("href", 'javascript:removetag("' + tag + '","' + tagid + '")');
    }
}


$(document).ready(function() {
    // Fb init 
    FB.init({
        appId  : '9e70e6cc01a08e4e0b28be7e45ce9709',
        status : true, // check login status
        cookie : true, // enable cookies to allow the server to access the session
        xfbml  : true  // parse XFBML
    });
    FB.getLoginStatus(function(response) {
        if (response.session) {
            muid = response.session.uid;
        } else {
            // no user session available, someone you dont know
            muid = 0;
        }
        $("#what_is").hide();
        load_main();
    });

	$("#what_is").hide();

    soundManager.onready(function() {
        if (soundManager.supported()) {
            // SM2 has loaded - now you can create and play sounds!
            soundManager.createSound({
                              id: 'sound_wrong',
                              url: '/static/sound/wrong.mp3'
             });
            soundManager.createSound({
                              id: 'sound_right',
                              url: '/static/sound/right.mp3'
             });
            soundManager.createSound({
                              id: 'sound_tick',
                              url: '/static/sound/tick.mp3'
             });
            soundManager.createSound({
                              id: 'sound_timeout',
                              url: '/static/sound/timeout.mp3'
             });

            } else {
                // (Optional) Hrmm, SM2 could not start. Show an error, etc.?
            }
            
        
        
    });
//	load_main();
//	called in fb getlogin status


});

/**********************/

function do_login() {
 FB.login(function(response) {
          if (response.session) {
            if (response.perms) {
              // user is logged in and granted some permissions.
              // perms is a comma separated list of granted permissions
		/*
		FB.api('/me', function(response) {
		  alert(response.name + response.uid + response.pic_square + response.online_presence + response.email );
		});
		*/
		FB.api(
			{
			    method: 'fql.query',
			    query: 'SELECT uid, first_name, last_name, pic_square, email  FROM user WHERE uid = me() '  
			},
			function(data) {
                muid = data[0].uid;
				$.post("/fbapp/facebook_login", { 'uid': data[0].uid, 'first_name': data[0].first_name, 'last_name': data[0].last_name, 'pic_url': data[0].pic_square, 'email': data[0].email }, function(data) {
                            load_main();
                      });
			}
		);
            } else {
              // user is logged in, but did not grant any permissions
               muid = 0;
            }
          } else {
               muid = 0;
            // user is not logged in
          }
        }, {perms:' publish_stream, email'});
	
}

function graphStreamPublish(){
var body = 'Reading New Graph api & Javascript Base FBConnect Tutorial';
FB.api('/me/feed', 'post', { message: body }, function(response) {
    if (!response || response.error) {
	alert('Error occured');
    } else {
	alert('Post ID: ' + response.id);
    }
});	
}

function publish_score() {
	FB.ui(
	   {
	     method: 'feed',
	     name: 'OpenPursuit',
	     app_id: '9e70e6cc01a08e4e0b28be7e45ce9709',
	     link: 'http://apps.facebook.com/openpursuit/',
	     display: 'iframe',
	     picture: 'http://www.openpursuit.org/media//img/logo.png',
	     caption: 'Nuovo punteggio!',
	     description: 'Ho totalizzato ' + score + ' su questi argomenti: ' + selectedtags.join() ,
	     message: 'Weeeeeeeee'
	   },
	   function(response) {
	     if (response && response.post_id) {
	     } else {
	     }
	   }
	 );
}

function save_score() {	
	$("#save_status span").empty().html('Salvataggio in corso...');
	$("#save_status a").attr('href', "")

	var scores = [];
	for(var index in scoretag) {
		scores.push(index+":"+scoretag[index]);	
	}
	$.post("/fbapp/save_score ", { 'uid' : muid, 'scores' : scores  } , function(response) { 
            $("#save_status img").attr('src', "http://www.openpursuit.org/media/img/saved.png");
	        $("#save_status span").empty().html("Il tuo punteggio e' stato salvato");
            });
}
