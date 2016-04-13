'use strict'

angular.module('searchApp')
  .directive 'codefield', (highlightFilter) ->
    templateUrl: 'views/codefield.html'
    restrict: 'E'
    scope:
      sourcelines: '='
      linenos: '='
      name: '='
    link: (scope, element, attrs) ->
      scope.makesnippet = () ->
        scope.linenos.sort (a, b) -> a - b
        (scope.sourcelines[n] for n in scope.linenos)
          .join '\n'

      scope.highlight = (text, word) ->
        highlightFilter(text, word)
