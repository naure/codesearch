'use strict'

escapeRegExp = (string) ->
    string.replace /([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1"

replaceAll = (str, find, replace) ->
    str.replace new RegExp('\\b' + escapeRegExp(find) + '\\b', 'g'), replace


angular.module('searchApp')
  .filter 'highlight', () ->
    (input, word, cls) ->
      if input
        replaceAll input,
          word, "<span class='#{cls}'>#{word}</span>"
      else ''
