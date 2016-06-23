/*
 Sticky-kit v1.1.2 | WTFPL | Leaf Corcoran 2015 | http://leafo.net
*/
(function(){var b,f;b=this.jQuery||window.jQuery;f=b(window);b.fn.stick_in_parent=function(d){var A,w,J,n,B,K,p,q,k,E,t;null==d&&(d={});t=d.sticky_class;B=d.inner_scrolling;E=d.recalc_every;k=d.parent;q=d.offset_top;p=d.spacer;w=d.bottoming;null==q&&(q=0);null==k&&(k=void 0);null==B&&(B=!0);null==t&&(t="is_stuck");A=b(document);null==w&&(w=!0);J=function(a,d,n,C,F,u,r,G){var v,H,m,D,I,c,g,x,y,z,h,l;if(!a.data("sticky_kit")){a.data("sticky_kit",!0);I=A.height();g=a.parent();null!=k&&(g=g.closest(k));
if(!g.length)throw"failed to find stick parent";v=m=!1;(h=null!=p?p&&a.closest(p):b("<div />"))&&h.css("position",a.css("position"));x=function(){var c,f,e;if(!G&&(I=A.height(),c=parseInt(g.css("border-top-width"),10),f=parseInt(g.css("padding-top"),10),d=parseInt(g.css("padding-bottom"),10),n=g.offset().top+c+f,C=g.height(),m&&(v=m=!1,null==p&&(a.insertAfter(h),h.detach()),a.css({position:"",top:"",width:"",bottom:""}).removeClass(t),e=!0),F=a.offset().top-(parseInt(a.css("margin-top"),10)||0)-q,
u=a.outerHeight(!0),r=a.css("float"),h&&h.css({width:a.outerWidth(!0),height:u,display:a.css("display"),"vertical-align":a.css("vertical-align"),"float":r}),e))return l()};x();if(u!==C)return D=void 0,c=q,z=E,l=function(){var b,l,e,k;if(!G&&(e=!1,null!=z&&(--z,0>=z&&(z=E,x(),e=!0)),e||A.height()===I||x(),e=f.scrollTop(),null!=D&&(l=e-D),D=e,m?(w&&(k=e+u+c>C+n,v&&!k&&(v=!1,a.css({position:"fixed",bottom:"",top:c}).trigger("sticky_kit:unbottom"))),e<F&&(m=!1,c=q,null==p&&("left"!==r&&"right"!==r||a.insertAfter(h),
h.detach()),b={position:"",width:"",top:""},a.css(b).removeClass(t).trigger("sticky_kit:unstick")),B&&(b=f.height(),u+q>b&&!v&&(c-=l,c=Math.max(b-u,c),c=Math.min(q,c),m&&a.css({top:c+"px"})))):e>F&&(m=!0,b={position:"fixed",top:c},b.width="border-box"===a.css("box-sizing")?a.outerWidth()+"px":a.width()+"px",a.css(b).addClass(t),null==p&&(a.after(h),"left"!==r&&"right"!==r||h.append(a)),a.trigger("sticky_kit:stick")),m&&w&&(null==k&&(k=e+u+c>C+n),!v&&k)))return v=!0,"static"===g.css("position")&&g.css({position:"relative"}),
a.css({position:"absolute",bottom:d,top:"auto"}).trigger("sticky_kit:bottom")},y=function(){x();return l()},H=function(){G=!0;f.off("touchmove",l);f.off("scroll",l);f.off("resize",y);b(document.body).off("sticky_kit:recalc",y);a.off("sticky_kit:detach",H);a.removeData("sticky_kit");a.css({position:"",bottom:"",top:"",width:""});g.position("position","");if(m)return null==p&&("left"!==r&&"right"!==r||a.insertAfter(h),h.remove()),a.removeClass(t)},f.on("touchmove",l),f.on("scroll",l),f.on("resize",
y),b(document.body).on("sticky_kit:recalc",y),a.on("sticky_kit:detach",H),setTimeout(l,0)}};n=0;for(K=this.length;n<K;n++)d=this[n],J(b(d));return this}}).call(this);

var main = $('main'), 
	legend = $('.legend');

$("nav").stick_in_parent();
legend.stick_in_parent({
	offset_top: $('nav').height()
});

legend.on('click', 'li', function(e){
	var c = $(this).find('span').prop('class');

	$(this).toggleClass('active');
	main.toggleClass('show-' + c);

	var filtered = $('main').prop('class').indexOf('show') !== -1; 

	legend.toggleClass('filtered', filtered);
	main.toggleClass('filtered', filtered);
});

// Load lines data 
var files = ['1', '2', '3', '4', '5', '6', 'eqg'],
	data = {}, 
	loaded = 0, 
	progressBar = $('.progress').fadeIn();

var seasons = $('.season').each(function () {
    var $t = $(this),
        transcript = $t.data('transcript');

    $.getJSON(transcript + '.json', function(d){
        $t.data('lines', d);

		// Update progress bar
		loaded++;
		progressBar.find('strong').text(loaded + '/' + seasons.length);

		if (loaded == files.length) {
			progressBar.delay(500).fadeOut();
		}
	});
});

// Hack for browsers who don't wrap text for some stupid reason 
if ($('.season ol').first().height() < ($('.season ol li').first().height() * 2))
	main.addClass('alt');

// Set up hover data 
var lineInfo = $('.line-info');
main.on('mouseover', 'ol li', function(e){
	var $t = $(this), 
		// line and ep are 0 indexed, because they are stored in an array
		// season is not, since its stored in an object 
		l = $t.prevAll().length, 
		ep = $t.closest('div').prevAll('div').length,
		season = $t.closest('.season'),
        transcript = season.data('lines');

	if (transcript && transcript[ep][l]){
		var line = transcript[ep][l],
			offset = $t.offset(), 
			middle = offset.left + $t.width() / 2;

		// Add in the text first so that width and height are calculated properly 
		var speakers = line.speaker.join(', ');
		if (line.song) speakers += ' ♫';

		var lineText = line.text
			.replace(/\n/g, '<br>')
			.replace(/\*([^*]+)\*/g, '<em>$1</em>');

		lineInfo.find('.speaker')
                .text(speakers).end()
            .find('.line')
                .html(lineText);

		lineInfo.show();

		offset.left = Math.max(0, middle - lineInfo.width() / 2);
		offset.top -= (lineInfo.outerHeight() + 8);

		lineInfo.offset(offset);
	}
}).on('mouseleave', 'ol', function(){
	lineInfo.hide();
});

$('.instructions').on('dblclick', function(){
	var egg = {
		aj: 'Orange-Applehorse', 
		fs: 'Yellow Treehorse', 
		pp: 'Partyhorse',
		rd: 'Fast-Colorfulhorse', 
		r: 'Gemhorse', 
		su: 'Queen Baconhair', 
		s: 'Mr. The Dragon', 
		ts: 'Purple Bookhorse'
	};

	$('.legend li').html(function(i, h){
		for(var p in egg) {
			if ($(this).find('.' + p).length) {
				var s = $(this).find('.' + p)[0].outerHTML; 
				return s + egg[p];
			}
		}
	});
});

