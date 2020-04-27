// $(function(){
//
//     var refreshFilenameList = function(data){
//         var templateText = $("#tableTemplate").html();
//         var template = Handlebars.compile(templateText);
//         var renderedText = template(data);
//         var renderedDom = $(renderedText);
//         $("#tablearea").empty();
//         $("#tablearea").append(renderedDom);
//     };
//
//     var fileUploadSuccess = function(data){
//         var url = "/filenames";
//         var promise = $.get(url);
//         promise.then(refreshFilenameList);
//     };
//
//     var fileUploadFail = function(data){};
//
//     var dragHandler = function(evt){
//         evt.preventDefault();
//     };
//
//     var dropHandler = function(evt){
//         evt.preventDefault();
//         var files = evt.originalEvent.dataTransfer.files;
//
//         var formData = new FormData();
//         formData.append("file2upload", files[0]);
//
//         var req = {
//             url: "/sendfile",
//             method: "post",
//             processData: false,
//             contentType: false,
//             data: formData
//         };
//
//         var promise = $.ajax(req);
//         promise.then(fileUploadSuccess, fileUploadFail);
//     };
//
//     var dropHandlerSet = {
//         dragover: dragHandler,
//         drop: dropHandler
//     };
//
//     $(".droparea").on(dropHandlerSet);
//
//     fileUploadSuccess(false); // called to ensure that we have initial data
// });


var $fileInput = $('.file-input');
var $droparea = $('.file-drop-area');

// highlight drag area
$fileInput.on('dragenter focus click', function() {
  $droparea.addClass('is-active');
});

// back to normal state
$fileInput.on('dragleave blur drop', function() {
  $droparea.removeClass('is-active');
});

// change inner text
$fileInput.on('change', function() {
  var filesCount = $(this)[0].files.length;
  var $textContainer = $(this).prev();

  if (filesCount === 1) {
    // if single file is selected, show file name
    var fileName = $(this).val().split('\\').pop();
    $textContainer.text(fileName);
  } else {
    // otherwise show number of files
    $textContainer.text(filesCount + ' files selected');
  }
});

function uploadFile(file) {
  let url = '/filenames'
  let formData = new FormData()

  formData.append('file', file)

  fetch(url, {
    method: 'POST',
    body: formData
  })
  .then(() => { /* Done. Inform the user */ })
  .catch(() => { /* Error. Inform the user */ })
}
