'use strict'

angular.module('searchApp')
  .filter 'name', ->
    (input) ->
      "« #{input} »"
