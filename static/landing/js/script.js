(function($) {

  "use strict";

  // Responsive Navigation with Button
  // var initHamburgerMenu = function() {
  //   const hamburger = document.querySelector(".hamburger");
  //   const navMenu = document.querySelector(".menu-list");

  //   hamburger.addEventListener("click", mobileMenu);

  //   function mobileMenu() {
  //     hamburger.classList.toggle("active");
  //     navMenu.classList.toggle("responsive");
  //   }

  //   const navLink = document.querySelectorAll(".item-anchor");

  //   navLink.forEach(n => n.addEventListener("click", closeMenu));

  //   function closeMenu() {
  //     hamburger.classList.remove("active");
  //     navMenu.classList.remove("responsive");
  //   }
  // };

  // init jarallax parallax
  var initJarallax = function() {
    jarallax(document.querySelectorAll(".jarallax"));

    jarallax(document.querySelectorAll(".jarallax-img"), {
      keepImg: true,
    });
  }

  var initIncrementButton = function() {

    $('.spin-number-output').each(function(){

      // quantity number//
      let spinNumberOutput = document.querySelector('.spin-number-output')
      let regularPrice = document.querySelector('.regular-price')
      let quantityOutput = document.querySelector('.quantity-output')
      let plusButton = document.querySelector('.incriment-button')
      let minusButton = document.querySelector('.decriment-button')

      spinNumberOutput.value = 1;
      quantityOutput.innerHTML = regularPrice.innerHTML * spinNumberOutput.value

      plusButton.addEventListener('click', function(){
          spinNumberOutput.value ++
          console.log( quantityOutput.innerHTML = regularPrice.innerHTML * spinNumberOutput.value)
      })

      minusButton.addEventListener('click', function(){

        if( spinNumberOutput.value > 1){
         spinNumberOutput.value--
        console.log( quantityOutput.innerHTML = regularPrice.innerHTML * spinNumberOutput.value)

         }
      })
      
    });

  }

  var initPreloader = function() {
    $(document).ready(function($) {
    var Body = $('body');
        Body.addClass('preloader-site');
    });
    $(window).load(function() {
        $('.preloader-wrapper').fadeOut();
        $('body').removeClass('preloader-site');
    });
  }

  // document ready
  $(document).ready(function() {
    initPreloader();
    // initHamburgerMenu();
    initJarallax();
    initIncrementButton();

    $('.navbar-nav').on('click', '.search-toggle', function(e) {
      var selector = $(this).data('selector');

      $('.navbar-nav').toggleClass('show').find('.search-input').focus();
      $(this).toggleClass('active');

      e.preventDefault();
    });

    // close when click off of container
    $(document).on('click touchstart', function(e) {
      if (!$(e.target).is('.search-toggle, .search-toggle *, .navbar-nav, .navbar-nav *')) {
        $('.search-toggle').removeClass('active');
        $('.navbar-nav').removeClass('show');
      }
    });


    var swiper = new Swiper(".main-swiper", {
      pagination: {
        el: ".swiper-pagination",
        type: "fraction",
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
    });

    var swiper = new Swiper(".product-swiper", {
      slidesPerView: 4,
      spaceBetween: 20,
      loop: true,
      navigation: {
        nextEl: ".icon-arrow-right",
        prevEl: ".icon-arrow-left",
      },
      breakpoints: {
        0: {
          slidesPerView: 1,
          spaceBetween: 20,
        },
        768: {
          slidesPerView: 2,
          spaceBetween: 10,
        },
        999: {
          slidesPerView: 3,
          spaceBetween: 10,
        },
        1366: {
          slidesPerView: 4,
          paceBetween: 40,
        },
      },
    });

    $(".gallery").colorbox({rel:'gallery'});
    $(".youtube").colorbox({iframe:true, innerWidth:960, innerHeight:585});

    // jQuery('.stellarnav').stellarNav({
    //   theme: 'plain',
    //   closingDelay: 250,
    // });

    AOS.init({
      duration: 1200,
      once: true,
    });


  }); // End of a document ready

})(jQuery);