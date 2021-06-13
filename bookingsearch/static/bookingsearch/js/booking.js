(function ($) {
  "use strict";

  $(document).ready(function () {

    $(".bookroom").click(function () {

      var $this = $(this),
          id = $this.attr('id'),
          roomtype = $this.data('roomtype'),
          roomnumber = $this.data('roomnumber'),
          price = $this.data('price'),
          $form = $('form.booking-form');

      $('input[type=hidden][name=roomtype]').val(roomtype);
      $('input[type="hidden"][name=roomnumber]').val(roomnumber);
      $('input[type="hidden"][name=price]').val(price);

      $form.submit();

      return true;

    });

  });

}(jQuery))
