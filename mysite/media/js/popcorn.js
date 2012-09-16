var app = {};
var loading;
app.chosen_keywords = [];
var waitTime = Math.random()*20;
var listCount = 0;
var count = 0;
var i;
var x;
var y;
var xvel;
var yvel;
var timer = 0;
var keyword;
var referenceArray = [];
var popArr;
function init() {
	popArr = app.keywords;
	var popArrLength = popArr.length;
	for (i=0;i<popArr.length;i++) {
		var razzi_obj = {
			x:window.innerWidth/2,
			y:window.innerHeight-60,
			xvel:Math.random()*15-7.5,
			yvel:15-Math.random()*6,
		};
		popArr[i].push(razzi_obj)
	}
	loop();
}
function keyword_item_click(thing) {
    if (app.chosen_keywords.indexOf(thing.attr('data-link')) < 0) {
        $('.loading').show()
        app.chosen_keywords.push(thing.attr('data-link')); // adds to global thing
        $('ul.nav').append('<span class="chosen_keyword btn btn-inverse ">'+thing.attr('data-name')+'</span>');
        if ($('.show_me_the_trailers').length===0) {
            $('div.nav-collapse').append('<a href="#" class="show_me_the_trailers btn pull-right btn-danger">Show me the Trailers! &#187;</a>');
            $('.show_me_the_trailers').click(function(){
            	$('.popcorn').fadeOut(100);
                // show them the money!
                $('.loading').show()
                displayMovies();
                $('.popcorn').remove();
            });
        }
        updateKeywords();
    }
}
function loop() {
	count++;
	// console.log(waitTime, count);
	//logic to make a particle or not
	if(count>=waitTime && listCount<popArr.length){
		x = popArr[listCount][3]["x"];
		keyword = popArr[listCount][1];
		var elem = '<a data-link="'+popArr[i][1]+'" data-weight="'+popArr[i][2]+'" data-name="'+popArr[i][0]+'" id="'+keyword+'_link" class="keyword_item"><div id="'+keyword+'" class="popcorn" style="left:'+x+'px;"><h3>'+popArr[i][0]+'</h3></div></a>';
		//need to create handler for clicks
		$('body').append(elem);
		referenceArray.push(keyword);
		count = 0;
		listCount++;
		waitTime = Math.random()*50;
		var rotation = Math.random()*20-10;
		// var sizing = Math.max((keyword.length)/20,1);
		$('#'+keyword+'_link').click(function(){
			$('.popcorn').fadeOut(300);
			keyword_item_click($(this));
		}).children().css('transform','rotate('+rotation+'deg)');
	}
	for(i=0; i<listCount; i++){
		x = popArr[i][3]["x"];
		y = popArr[i][3]["y"];
		xvel = popArr[i][3]["xvel"];
		yvel = popArr[i][3]["yvel"];
		//update those vals
		popArr[i][3]["x"]=x+xvel;
		popArr[i][3]["y"]=y+yvel;
		popArr[i][3]["yvel"]=yvel+.05;
		popArr[i][3]["xvel"]*=.995;
		if(Math.abs(popArr[i][3]["xvel"])<=.1){
			popArr[i][3]["xvel"] = 0
		}

		object = document.getElementById(referenceArray[i]);
		object.style.left = x+xvel+"px";
		object.style.top = y+yvel+"px";
		if(x+xvel>=screen.width-200){
			popArr[i][3]["x"] = screen.width-202;
			popArr[i][3]["xvel"] *=-.8;
		}
		if(x+xvel <=0){
			popArr[i][3]["x"] = 2;
			popArr[i][3]["xvel"] *=-.8;
		}
		// console.log(i, y, yvel);
		if (y>=560-i*10){
			// console.log('560');
			if(Math.abs(yvel)>=1.6){
				popArr[i][3]["y"] = 558-i*10;
				popArr[i][3]["yvel"] *=-.6;
			} else{
				popArr[i][3]["yvel"] = 0;
			}
		}
		//  else if (y>=460&&15<i<=30&&yvel>0){
		// 	// console.log('460');
		// 	if(Math.abs(yvel)>=1.6){
		// 		popArr[i][3]["y"] = 458;
		// 		popArr[i][3]["yvel"] *=-.6;
		// 	}else{
		// 		popArr[i][3]["yvel"] = 0;
		// 	}
		// } else if (y>=400&&30<i<=45&&yvel>0){
		// 	// console.log('400')
		// 	if(Math.abs(yvel)>=1.6){
		// 		popArr[i][3]["y"] = 398;
		// 		popArr[i][3]["yvel"] *=-.6;
		// 	}else{
		// 		popArr[i][3]["yvel"] = 0;
		// 	}
		// }
		// console.log(popArr[i][0])
	}
	requestAnimationFrame(loop);
}

function changePopcorns(data) {
    console.log(data);
    app.keywords = data;
    listCount = 0;
    popArr = [];
    referenceArray = [];
    // $('.popcorn').fadeOut(200, function(){
	$('.popcorn').remove();
    // });

    // for (i in data) {
        // var a = '<li><a data-link="'+data[i][1]+'" data-weight="'+data[i][2]+'" class="keyword_item">'+data[i][0]+'</a></li>';
        // $('#links_here').append(a);
    // }
    $('.keyword_item').click(function(){
    	$('.popcorn').fadeOut(300);
        keyword_item_click($(this));
        $('.popcorn').remove();
    });
    $('.loading').hide()
    init();
}
function updateKeywords() {
    $('#links_here').html('');
    var keywords = app.chosen_keywords.join();
    var url = '/getRelatedKeywords/'+keywords+'/';
    $.getJSON(url, function(data){
        if (data.length < 1) {
            $('.show_me_the_trailers').click();
        } else {
            changePopcorns(data);
        }
    });
    console.log(document.domain);
    var domain = document.domain.indexOf('localhost') < 0 ? document.domain : document.domain+':8080';
    console.log(domain);
    window.history.pushState({},"", 'http://'+domain+'/movies/'+keywords+'/')
}

function displayMovies() {
    console.log('in display movies');
    var bubbles = app.chosen_keywords.join();
    var url = '/moviesCarousel/'+bubbles+'/';
    $('#main_container').append('<div id="carouselHere"></div>')
    console.log(url);
    $('#main_container').prepend('<div class="screen"></div>');
    $('.screen').slideDown(1000);
    // $('.popcorn').fadeOut(200, function(){
	$('.popcorn').remove();
	popArr = [];
	referenceArray = [];
	count = 0;
    // });
    $('#carouselHere').load(url, function(responseText, textStatus, XMLHttpRequest){
        console.log('carousel loaded');
        $('.carousel').carousel({
            interval:false,
        });
    });
    $('.loading').hide();
};
function getYoutubeURL(id) {
    return '<iframe width="500" height="281" src="http://www.youtube.com/embed/' + id +'?wmode=transparent&autohide=1&egm=0&hd=1&iv_load_policy=3&modestbranding=1&rel=0&showinfo=0&showsearch=0" frameborder="0" allowfullscreen></iframe>';
}
function findYoutubeVideo(movieTitle){
    movieTitle = movieTitle
    var cleanMovieTitle = movieTitle.replace(" ", "%20").replace(" ", "%20").replace(" ", "%20");
    $.get('/getVideoFromYoutube/'+cleanMovieTitle+'/', function(data) {
        $('body').append(getYoutubeURL(data));
    })
}

function disableSelection(target){

    if (typeof target.onselectstart!="undefined") //IE route
        target.onselectstart=function(){return false}

    else if (typeof target.style.MozUserSelect!="undefined") //Firefox route
        target.style.MozUserSelect="none"

    else //All other route (ie: Opera)
        target.onmousedown=function(){return false}

    target.style.cursor = "default"
}



//Sample usages
disableSelection(document.body) //Disable text selection on entire body