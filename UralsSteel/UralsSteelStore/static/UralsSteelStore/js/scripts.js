$ (function (){

        /* Modal
    =====================*/

    const modalCall = $("[data-modal]");
    const modalClose = $("[data-close]");
    const shopItemS = $("[data-shop_item_small]");
    const shopItemB = $("[ data-shop_item_big]");

    modalCall.on("click", function(event) {
        event.preventDefault();

        let $this = $(this);
        let modalId = $this.data('modal');

        $(modalId).addClass('show');
        $("body").addClass('no-scroll');

        setTimeout(function() {
            $(modalId).find(".modal_dialog").css({
                transform: "scale(1)"
            });
        });
    });


    modalClose.on("click", function(event) {
        event.preventDefault();

        let $this = $(this);
        let modalParent = $this.parents('.modal');

        modalParent.find(".modal_dialog").css({
            transform: "scale(0)"
        });

        setTimeout(function() {
            modalParent.removeClass('show');
            $("body").removeClass('no-scroll');
        });
    });

    $(".modal").on("click", function(event) {
        let $this = $(this);

        $this.find(".modal_dialog").css({
            transform: "scale(0)"
        });

        setTimeout(function() {
            $this.removeClass('show');
            $("body").removeClass('no-scroll');
        });
    });

    $(".modal_dialog").on("click", function(event) {
        event.stopPropagation();
    });

    shopItemS.on("click", function (event){
        event.preventDefault();

        let navEl = $('.shop_goods_item_pl');
        navEl.css('display', 'none')
        // navEl.removeClass("dispFlex");
        // navEl.addClass("dispNone");
        //
        let nextEl = $('.shop_goods_item');
        nextEl.css('display', 'flex')
        // navEl.removeClass("dispNone");
        // nextEl.addClass("dispFlex");
        // window.location.reload();
        localStorage.clear()
        const smallGood = 'small'
        localStorage.setItem('GoodRejim', smallGood)

    });

    shopItemB.on("click", function (event){
        event.preventDefault();

        let navEl = $('.shop_goods_item');
        navEl.css('display', 'none')
        // navEl.removeClass("dispFlex");
        // navEl.addClass("dispNone");
        //
        let nextEl = $('.shop_goods_item_pl');
        nextEl.css('display', 'flex')
        // navEl.removeClass("dispNone");
        // nextEl.addClass("dispFlex");
        localStorage.clear()
        const bigGood = 'big'
        localStorage.setItem('GoodRejim', bigGood)
    });

    $('.basket_continue_btn').click(function() { $('.basket_order').hide().css('display', 'flex'), $('.basket_continue_btn').hide().css('display','none')});

    window.onload = function (event){
        if (localStorage.getItem('GoodRejim') === 'small'){

            let navEl = $('.shop_goods_item_pl');
            navEl.css('display', 'none')

            let nextEl = $('.shop_goods_item');
            nextEl.css('display', 'flex')
        }
        else {
            let navEl = $('.shop_goods_item');
            navEl.css('display', 'none')

            let nextEl = $('.shop_goods_item_pl');
            nextEl.css('display', 'flex')
        }
    }
});