var pad, range, refocus, sum;

range = function(start, stop, step) {
  var x, _results;
  if (typeof stop === 'undefined') {
    stop = start;
    start = 0;
  }
  if (typeof step === 'undefined') step = 1;
  if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) return [];
  _results = [];
  for (x = start; start <= stop ? x <= stop : x >= stop; x += step) {
    _results.push(x);
  }
  return _results;
};

pad = function(num, digits) {
  return (1e15 + num + "").slice(-digits);
};

sum = function(t, s) {
  return t + s;
};

refocus = function(filename_sets, container) {
  var element, filename, filename_set, full_widths, img_sets, num_img_loaded, num_img_total;
  num_img_loaded = 0;
  num_img_total = 0;
  img_sets = (function() {
    var _i, _len, _results;
    _results = [];
    for (_i = 0, _len = filename_sets.length; _i < _len; _i++) {
      filename_set = filename_sets[_i];
      if (!(filename_set instanceof Array)) filename_set = [filename_set];
      _results.push((function() {
        var _j, _len2, _results2;
        _results2 = [];
        for (_j = 0, _len2 = filename_set.length; _j < _len2; _j++) {
          filename = filename_set[_j];
          element = $("<img class='refocus'                        src='" + filename + "'                        style='position:absolute;                               visibility:hidden;'/>");
          element.load(function() {
            return num_img_loaded++;
          });
          $(container).append(element);
          num_img_total++;
          _results2.push(element);
        }
        return _results2;
      })());
    }
    return _results;
  })();
  full_widths = [];
  $('img.refocus', container).imagesLoaded(function() {
    var img, img_set;
    $(':not(.refocus)', container).remove();
    full_widths = (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = img_sets.length; _i < _len; _i++) {
        img_set = img_sets[_i];
        _results.push(((function() {
          var _j, _len2, _results2;
          _results2 = [];
          for (_j = 0, _len2 = img_set.length; _j < _len2; _j++) {
            img = img_set[_j];
            _results2.push(img.width());
          }
          return _results2;
        })()).reduce(sum));
      }
      return _results;
    })();
    $(document).mousemove(function(e) {
      var i, img, img_h, img_index, img_set, img_w, pos_x, pos_y, shift, win_h, win_w, _i, _len, _len2;
      win_w = $(window).width();
      win_h = $(window).height();
      pos_x = e.pageX / $(window).width();
      pos_y = e.pageY / $(window).height();
      img_index = Math.floor(pos_y * img_sets.length);
      for (i = 0, _len = img_sets.length; i < _len; i++) {
        img_set = img_sets[i];
        shift = -pos_x * (full_widths[i] - win_w);
        for (_i = 0, _len2 = img_set.length; _i < _len2; _i++) {
          img = img_set[_i];
          if (i === img_index) {
            img_w = img.width();
            img_h = img.height();
            img.css({
              "left": shift
            });
            img.css("visibility", "visible");
            shift += img_w;
          } else {
            img.css("visibility", "hidden");
          }
        }
      }
    });
  });
  return {
    numImgLoaded: function() {
      return num_img_loaded;
    },
    numImgTotal: function() {
      return num_img_total;
    }
  };
};
