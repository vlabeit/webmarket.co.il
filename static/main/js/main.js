(function($) {
    
	"use strict";
	
	
	//Hide Loading Box (Preloader)
	function handlePreloader() {
		if($('.preloader').length){
			$('.preloader').delay(200).fadeOut(500);
		}
	}
	
	
	//Update Header Style and Scroll to Top
	function headerStyle() {
		if($('.main-header').length){
			var windowpos = $(window).scrollTop();
			var siteHeader = $('.main-header');
			var scrollLink = $('.scroll-to-top');
			if (windowpos >= 1) {
				siteHeader.addClass('fixed-header');
				scrollLink.fadeIn(300);
			} else {
				siteHeader.removeClass('fixed-header');
				scrollLink.fadeOut(300);
			}
		}
	}
	
	headerStyle();
	
	
	//Submenu Dropdown Toggle
	if($('.main-header li.dropdown ul').length){
		$('.main-header li.dropdown').append('<div class="dropdown-btn"><span class="fa fa-angle-down"></span></div>');
		
		//Dropdown Button
		$('.main-header li.dropdown .dropdown-btn').on('click', function() {
			$(this).prev('ul').slideToggle(500);
		});
		
		//Disable dropdown parent link
		$('.main-header .navigation li.dropdown > a,.hidden-bar .side-menu li.dropdown > a').on('click', function(e) {
			e.preventDefault();
		});
	}

	//Side Content Toggle
	if($('.main-header .outer-box .nav-btn').length){
		//Show Form
		$('.main-header .outer-box .nav-btn').on('click', function(e) {
			e.preventDefault();
			$('body').addClass('side-content-visible');
		});
		//Hide Form
		$('.hidden-bar .inner-box .cross-icon,.form-back-drop,.close-menu').on('click', function(e) {
			e.preventDefault();
			$('body').removeClass('side-content-visible');
		});
		//Dropdown Menu
		$('.fullscreen-menu .navigation li.dropdown > a').on('click', function() {
			$(this).next('ul').slideToggle(500);
		});
	}

		//Hidden Sidebar
	if ($('.hidden-bar').length) {
		$('.hidden-bar').mCustomScrollbar({
		    theme:"dark"
		});
	}

	// Testimonial Carousel
	if ($('.testimonial-carousel').length) {
		$('.testimonial-carousel').owlCarousel({
			animateOut: 'slideOutDown',
		    animateIn: 'zoomIn',
			loop:true,
			margin:0,
			nav:true,
			smartSpeed: 300,
			autoplay: 7000,
			navText: [ '<span class="arrow-left"></span>', '<span class="arrow-right"></span>' ],
			responsive:{
				0:{
					items:1
				},
				600:{
					items:1
				},
				800:{
					items:1
				},
				1024:{
					items:1
				}
			}
		});  		
	}


	//Fact Counter + Text Count
	if($('.count-box').length){
		$('.count-box').appear(function(){
	
			var $t = $(this),
				n = $t.find(".count-text").attr("data-stop"),
				r = parseInt($t.find(".count-text").attr("data-speed"), 10);
				
			if (!$t.hasClass("counted")) {
				$t.addClass("counted");
				$({
					countNum: $t.find(".count-text").text()
				}).animate({
					countNum: n
				}, {
					duration: r,
					easing: "linear",
					step: function() {
						$t.find(".count-text").text(Math.floor(this.countNum));
					},
					complete: function() {
						$t.find(".count-text").text(this.countNum);
					}
				});
			}
			
		},{accY: 0});
	}

	
	//Accordion Box
	if($('.accordion-box').length){
		$(".accordion-box").on('click', '.acc-btn', function() {
			
			var outerBox = $(this).parents('.accordion-box');
			var target = $(this).parents('.accordion');
			
			if($(this).hasClass('active')!==true){
				$(outerBox).find('.accordion .acc-btn').removeClass('active');
			}
			
			if ($(this).next('.acc-content').is(':visible')){
				return false;
			}else{
				$(this).addClass('active');
				$(outerBox).children('.accordion').removeClass('active-block');
				$(outerBox).find('.accordion').children('.acc-content').slideUp(300);
				target.addClass('active-block');
				$(this).next('.acc-content').slideDown(300);	
			}
		});	
	}
	
	
	//Tabs Box
	if($('.tabs-box').length){
		$('.tabs-box .tab-buttons .tab-btn').on('click', function(e) {
			e.preventDefault();
			var target = $($(this).attr('data-tab'));
			
			if ($(target).is(':visible')){
				return false;
			}else{
				target.parents('.tabs-box').find('.tab-buttons').find('.tab-btn').removeClass('active-btn');
				$(this).addClass('active-btn');
				target.parents('.tabs-box').find('.tabs-content').find('.tab').fadeOut(0);
				target.parents('.tabs-box').find('.tabs-content').find('.tab').removeClass('active-tab animated fadeIn');
				$(target).fadeIn(300);
				$(target).addClass('active-tab animated fadeIn');
			}
		});
	}
	

	//Default Masonary
	function defaultMasonry() {
		if($('.masonry-items-container').length){
	
			var winDow = $(window);
			// Needed variables
			var $container=$('.masonry-items-container');
	
			$container.isotope({
				itemSelector: '.masonry-item',
				 masonry: {
					columnWidth :2
				 },
				animationOptions:{
					duration:500,
					easing:'linear'
				}
			});
	
			winDow.on('resize', function(){

				$container.isotope({ 
					itemSelector: '.masonry-item',
					animationOptions: {
						duration: 500,
						easing	: 'linear',
						queue	: false
					}
				});
			});
		}
	}
	defaultMasonry();

	//Gallery Filters
	 if($('.filter-list').length){
	 	 $('.filter-list').mixItUp({});
	 }
	
	//LightBox / Fancybox
	if($('.lightbox-image').length) {
		$('.lightbox-image').fancybox({
			openEffect  : 'fade',
			closeEffect : 'fade',
			helpers : {
				media : {}
			}
		});
	}
	
	//Contact Form Validation
	if($('#contact-form').length){
		$('#contact-form').validate({
			rules: {
				username: {
					required: true
				},
				email: {
					required: true,
					email: true
				},
				phone: {
					required: true
				},
				message: {
					required: true
				}
			}
		});
	}
	
	
	// Scroll to a Specific Div
	if($('.scroll-to-target').length){
		$(".scroll-to-target").on('click', function() {
			var target = $(this).attr('data-target');
		   // animate
		   $('html, body').animate({
			   scrollTop: $(target).offset().top
			 }, 1500);
	
		});
	}

	if($('.paroller').length){
		$('.paroller').paroller({
			  factor: 0.05,            // multiplier for scrolling speed and offset, +- values for direction control  
			  factorLg: 0.05,          // multiplier for scrolling speed and offset if window width is less than 1200px, +- values for direction control  
			  type: 'foreground',     // background, foreground  
			  direction: 'horizontal' // vertical, horizontal  
		});
	}


	if($('.timer').length){
	   $(function(){
		    $('[data-countdown]').each(function() {
		   var $this = $(this), finalDate = $(this).data('countdown');
		   $this.countdown(finalDate, function(event) {
		     $this.html(event.strftime('%D days %H:%M:%S'));
		   });
		 });
		});

	   $('.cs-countdown').countdown('').on('update.countdown', function(event) {
		  var $this = $(this).html(event.strftime('<div class="count-col"><span>%m</span><h6>Months</h6></div> <div class="count-col"><span>%D</span><h6>days</h6></div> <div class="count-col"><span>%H</span><h6>Hours</h6></div> <div class="count-col"><span>%M</span><h6>Minutes</h6></div> <div class="count-col"><span>%S</span><h6>Seconds</h6></div>'));
		});
	}
	
	
	// Elements Animation
	if($('.wow').length){
		var wow = new WOW(
		  {
			boxClass:     'wow',      // animated element css class (default is wow)
			animateClass: 'animated', // animation css class (default is animated)
			offset:       0,          // distance to the element when triggering the animation (default is 0)
			mobile:       true,       // trigger animations on mobile devices (default is true)
			live:         true       // act on asynchronously loaded content (default is true)
		  }
		);
		wow.init();
	}


/* ==========================================================================
   When document is Scrollig, do
   ========================================================================== */
	
	$(window).on('scroll', function() {
		headerStyle();
	});
	
/* ==========================================================================
   When document is loading, do
   ========================================================================== */
	
	$(window).on('load', function() {
		handlePreloader();
		defaultMasonry();
	});	

})(window.jQuery); 


jQuery(document).ready(function($){
//hide the subtle gradient layer (.pricing-list > li::after) when pricing table has been scrolled to the end (mobile version only)
checkScrolling($('.pricing-body'));
$(window).on('resize', function(){
    window.requestAnimationFrame(function(){checkScrolling($('.pricing-body'))});
});
$('.pricing-body').on('scroll', function(){ 
    var selected = $(this);
    window.requestAnimationFrame(function(){checkScrolling(selected)});
});

function checkScrolling(tables){
    tables.each(function(){
        var table= $(this),
            totalTableWidth = parseInt(table.children('.pricing-features').width()),
             tableViewport = parseInt(table.width());
        if( table.scrollLeft() >= totalTableWidth - tableViewport -1 ) {
            table.parent('li').addClass('is-ended');
        } else {
            table.parent('li').removeClass('is-ended');
        }
    });
}

//switch from monthly to annual pricing tables
bouncy_filter($('.pricing-container'));

function bouncy_filter(container) {
    container.each(function(){
        var pricing_table = $(this);
        var filter_list_container = pricing_table.children('.pricing-switcher'),
            filter_radios = filter_list_container.find('input[type="radio"]'),
            pricing_table_wrapper = pricing_table.find('.pricing-wrapper');

        //store pricing table items
        var table_elements = {};
        filter_radios.each(function(){
            var filter_type = $(this).val();
            table_elements[filter_type] = pricing_table_wrapper.find('li[data-type="'+filter_type+'"]');
        });

        //detect input change event
        filter_radios.on('change', function(event){
            event.preventDefault();
            //detect which radio input item was checked
            var selected_filter = $(event.target).val();

            //give higher z-index to the pricing table items selected by the radio input
            show_selected_items(table_elements[selected_filter]);

            //rotate each pricing-wrapper 
            //at the end of the animation hide the not-selected pricing tables and rotate back the .pricing-wrapper
            
            if( !Modernizr.cssanimations ) {
                hide_not_selected_items(table_elements, selected_filter);
                pricing_table_wrapper.removeClass('is-switched');
            } else {
                pricing_table_wrapper.addClass('is-switched').eq(0).one('webkitAnimationEnd oanimationend msAnimationEnd animationend', function() {		
                    hide_not_selected_items(table_elements, selected_filter);
                    pricing_table_wrapper.removeClass('is-switched');
                    //change rotation direction if .pricing-list has the .bounce-invert class
                    if(pricing_table.find('.pricing-list').hasClass('bounce-invert')) pricing_table_wrapper.toggleClass('reverse-animation');
                });
            }
        });
    });
}
function show_selected_items(selected_elements) {
    selected_elements.addClass('is-selected');
}

function hide_not_selected_items(table_containers, filter) {
    $.each(table_containers, function(key, value){
          if ( key != filter ) {	
            $(this).removeClass('is-visible is-selected').addClass('is-hidden');

        } else {
            $(this).addClass('is-visible').removeClass('is-hidden is-selected');
        }
    });
}
});


        