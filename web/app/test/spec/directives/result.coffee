'use strict'

describe 'Directive: result', ->

  # load the directive's module
  beforeEach module 'appApp'

  scope = {}

  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()

  it 'should make hidden element visible', inject ($compile) ->
    element = angular.element '<result></result>'
    element = $compile(element) scope
    expect(element.text()).toBe 'this is the result directive'
