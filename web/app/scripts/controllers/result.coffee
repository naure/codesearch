'use strict'

angular.module('searchApp')
  .controller 'ResultCtrl', ($scope, $http) ->
    $scope.show_source = false
    $scope.source_lines = []
    filename = $scope.res.filename
    $http.get("files/#{filename}").success (data) ->
      $scope.source_lines = data.split('\n')
