// Code goes here
// http://embed.plnkr.co/atyuBnVNktl8YSfdfPJT/preview

$(function() {
  var $previewContainer = $('#comment-md-preview-container');
  $previewContainer.hide();
  var $md = $("#comment-md").markdown({
    autofocus: false,
    height: 500,
    iconlibrary: 'fa',
    onShow: function(e) {
      //e.hideButtons('cmdPreview');
      e.change(e);
    },
    onChange: function(e) {
      var content = e.parseContent();
      if (content === '') $previewContainer.hide();
      else $previewContainer.show().find('#comment-md-preview').html(content).find('table').addClass('table table-bordered table-striped table-hover');
    },
    footer: function(e) {
      return '\
					<span class="text-muted">\
						<span data-md-footer-message="err">\
						</span>\
						<span data-md-footer-message="default">\
							Add images by dragging & dropping or \
							<a class="btn-input">\
								selecting them\
								<input type="file" multiple="" id="comment-images" />\
							</a>\
						</span>\
						<span data-md-footer-message="loading">\
							Uploading your images...\
						</span>\
					</span>';
    }
  });

  var $mdEditor = $('.md-editor'),
    msgs = {};

  $mdEditor.find('[data-md-footer-message]').each(function() {
    msgs[$(this).data('md-footer-message')] = $(this).hide();
  });
  msgs.
  default.show();
  // Temporary Image upload url
  $mdEditor.filedrop({
    binded_input: $('#comment-images'),
    url: "/admin/image/uploads",
    fallbackClick: false,
    beforeSend: function(file, i, done) {
      msgs.
      default.hide();
      msgs.err.hide();
      msgs.loading.show();
      done();
    },
    //maxfilesize: 15,
    error: function(err, file) {
      switch (err) {
        case 'BrowserNotSupported':
          alert('browser does not support HTML5 drag and drop')
          break;
        case 'FileExtensionNotAllowed':
          // The file extension is not in the specified list 'allowedfileextensions'
          break;
        default:
          break;
      }
      var filename = typeof file !== 'undefined' ? file.name : '';
      msgs.loading.hide();
      msgs.err.show().html('<span class="text-danger"><i class="fa fa-times"></i> Error uploading ' + filename + ' - ' + err + '</span><br />');
    },
    dragOver: function() {
      $(this).addClass('active');
    },
    dragLeave: function() {
      $(this).removeClass('active');
    },
    progressUpdated: function(i, file, progress) {
      msgs.loading.html('<i class="fa fa-refresh fa-spin"></i> Uploading <span class="text-info">' + file.name + '</span>... ' + progress + '%');
    },
    afterAll: function() {
      msgs.
      default.show();
      msgs.loading.hide();
      msgs.err.hide();
    },
    uploadFinished: function(i, file, response, time) {
      $md.val($md.val() + "![" + file.name + "](http://photography.naturestocklibrary.com/orca-stock-photo.jpg)\n").trigger('change');
      // response is the data you got back from server in JSON format.
    }
  });
})