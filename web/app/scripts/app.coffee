'use strict'

angular
  .module('searchApp', [
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'hljs'
  ])
  .config ($routeProvider) ->
    $routeProvider
      .when '/',
        templateUrl: 'views/main.html'
      .when '/results/:query',
        templateUrl: 'views/results.html'
        controller: 'ResultsCtrl'
