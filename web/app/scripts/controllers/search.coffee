'use strict'

angular.module('searchApp')
  .controller 'SearchCtrl', ($scope, $location) ->
    $scope.search = () ->
      $location.path('/results/' + this.query)
