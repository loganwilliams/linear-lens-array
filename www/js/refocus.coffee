range = (start, stop, step) ->
  if typeof stop == 'undefined'
    stop = start
    start = 0
  if typeof step == 'undefined'
    step = 1
  if (step>0 and start>=stop) or (step<0 and start<=stop)
    return []
  (x for x in [start .. stop] by step)

pad = (num, digits) ->
  (1e15 + num + "").slice(-digits)

sum = (t, s) -> t + s

refocus = (filename_sets, container) ->
  num_img_loaded = 0
  num_img_total = 0
win_w = $(window).width()
win_h = $(window).height()

  img_sets = for filename_set in filename_sets
    if not (filename_set instanceof Array)
      filename_set = [filename_set]
    for filename in filename_set
      element = $("<img class='refocus'
      	      		width=#{win_w}
			height=#{win_h}
                        src='#{ filename }'
                        style='position:absolute;
                               visibility:hidden;'/>")
      element.load ->
        num_img_loaded++
      $(container).append(element)
      num_img_total++
      element

  full_widths = []

  $('img.refocus', container).imagesLoaded ->
    $(':not(.refocus)', container).remove()

    full_widths = for img_set in img_sets
      (img.width() for img in img_set).reduce sum

    $(document).mousemove (e) ->
      win_w = $(window).width()
      win_h = $(window).height()

      pos_x = e.pageX/$(window).width()
      pos_y = e.pageY/$(window).height()

      img_index = Math.floor(pos_y*img_sets.length)

      for img_set, i in img_sets
        shift = -pos_x*(full_widths[i]-win_w)

        for img in img_set
          if i == img_index
            img_w = img.width()
            img_h = img.height()
            img.css({"left": shift}) #, "top": (win_h-img_h)/2})
            img.css("visibility", "visible")
            shift += img_w
          else
      	    img.css("visibility", "hidden")
      return   # mousemove
    return   # imagesLoaded
  return {  
    numImgLoaded: -> num_img_loaded
    numImgTotal:  -> num_img_total
  } # refocus