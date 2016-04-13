'use strict'

angular.module('searchApp')
  .directive 'codefieldwhy', (highlightFilter, $sce) ->
    templateUrl: 'views/codefieldwhy.html'
    restrict: 'E'
    scope:
      sourcelines: '='
      linesreasons: '='
      namesroles: '='
    link: (scope, element, attrs) ->
      scope.getline = (lr) ->
        scope.sourcelines[lr.n]

      scope.getclass = (lr) ->
        lr.role

      scope.highlight = (line) ->
        # XXX Implement this in the filter
        for name, role of scope.namesroles
          line = highlightFilter line, name, role
        $sce.trustAsHtml line
