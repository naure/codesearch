'use strict'

describe 'Controller: ResultctrlCtrl', ->

  # load the controller's module
  beforeEach module 'searchApp'

  ResultctrlCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    ResultctrlCtrl = $controller 'ResultctrlCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
