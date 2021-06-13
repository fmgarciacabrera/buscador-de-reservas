(function ($) {
  "use strict";

  $(document).ready(function () {
    $(".datepicker").datepicker({
      dateFormat: "yy-mm-dd",
      minDate: new Date(),
      maxDate: "2021-12-31",
      showOtherMonths: true
    });
  });

}(jQuery))
