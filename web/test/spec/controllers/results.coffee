'use strict'

describe 'Controller: ResultsCtrl', ->

  # load the controller's module
  beforeEach module 'searchApp'

  ResultsCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    ResultsCtrl = $controller 'ResultsCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
