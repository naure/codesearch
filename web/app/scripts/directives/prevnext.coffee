'use strict'

angular.module('searchApp')
  .directive 'prevnext', ->
    templateUrl: 'views/prevnext.html'
    restrict: 'E'
    transclude: true
    scope:
      length: '='
      nodei: '='
    link: (scope, element, attrs) ->
      scope.prev = () ->
        scope.nodei--

      scope.next = () ->
        scope.nodei++
