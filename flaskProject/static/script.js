$(document).ready(function() {

  $("#search").click(function() {
    let searchReq = $.get("/sendRequest/" + $("#query").val());
    searchReq.done(function(data) {
      $("#url").attr("href", data.result);
    });
  });

});
