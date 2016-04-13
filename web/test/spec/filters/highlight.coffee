'use strict'

describe 'Filter: highlight', ->

  # load the filter's module
  beforeEach module 'searchApp'

  # initialize a new instance of the filter before each test
  highlight = {}
  beforeEach inject ($filter) ->
    highlight = $filter 'highlight'

  it 'should return the input prefixed with "highlight filter:"', ->
    text = 'angularjs'
    expect(highlight text).toBe ('highlight filter: ' + text)
