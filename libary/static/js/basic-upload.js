$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-files").click(function () {
    $("#fileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
     dataType: 'json',
     sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
     start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
       $("#modal-progress").modal("show");
     },
     stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
       $("#modal-progress").modal("hide");
       $(location).attr('href', '/libary/folders/');
     },
     progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
       var progress = parseInt(data.loaded / data.total * 100, 10);
       var strProgress = progress + "%";
       $(".progress-bar").css({"width": strProgress});
       $(".progress-bar").text(strProgress);
     }
   });
 });

 $(function () {
   /* 1. OPEN THE FILE EXPLORER WINDOW */
   $(".js-upload-files-subfolder").click(function () {
     $("#fileupload-subfolders").click();
   });

   /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
   $("#fileupload-subfolders").fileupload({
      dataType: 'json',
      sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
      start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
        $("#modal-progress").modal("show");
      },
      stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
        $("#modal-progress").modal("hide");
        $(location).attr('href', '/files/upload-success/');
      },
      progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var strProgress = progress + "%";
        $(".progress-bar").css({"width": strProgress});
        $(".progress-bar").text(strProgress);
      }
    });
  });
