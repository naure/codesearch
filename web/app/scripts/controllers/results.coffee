'use strict'

angular.module('searchApp')
  .controller 'ResultsCtrl', ($scope, $routeParams, $http) ->
    $scope.editor = ''
    $scope.includeLine = (line) ->
      $scope.editor += '\n' + line
    $scope.clearEditor = ->
      $scope.editor = ''

    $scope.results = {}
    $scope.query = $routeParams.query
    $http.get('code/search?q=' + $routeParams.query).success (data) ->
      $scope.results = data
