'use strict'

angular.module('searchApp')
  .directive 'result', ($http) ->
    templateUrl: 'views/result.html'
    restrict: 'E'
    scope: true
    link: (scope, element, attrs) ->

      loaded_defs = []
      loaded_pros = []

      # Deconstruct the 'result' structure into a [(line_number, type), ..]
      do_stmt = (stmts, role) ->
        for stmt in stmts
          if stmt.pros
            do_stmt stmt.pros, 'pro'
          if stmt.hels
            do_stmt stmt.hels, 'hel'
          for n in stmt.lines
            scope.linesreasons.push {n: n, role: role, name: stmt.name}
          if stmt.path
            for n in stmt.path
              scope.linesreasons.push {n: n, role: 'sco', name: stmt.name}
          scope.namesroles[stmt.name] = role

      extract_result = () ->
        scope.linesreasons = []
        scope.namesroles = {}

        do_stmt loaded_defs, 'def'
        do_stmt loaded_pros, 'pro'
        do_stmt [scope.res.defs[scope.def_i]], 'def'
        do_stmt [scope.res.uses[scope.use_i]], 'use'

        scope.linesreasons.sort (a, b) -> a.n - b.n
        scope.linesreasons = _.uniq scope.linesreasons, true, (v) -> v.n
      # / Deconstruct

      # Navigation
      scope.def_i = 0
      scope.use_i = 0
      # XXX Those should get updated when switching usage
      scope.last_def_id = scope.res.defs[scope.def_i].id
      # XXX Should start with a product statement already, not use
      pros = scope.res.uses[scope.use_i].pros
      scope.last_pro_id = if pros.length then pros[0].id else null
      # / Navigation

      # Load more
      loadmore = (what, sid, f_add) ->
        if sid != null
          $http.get("code/more/#{what}/#{sid}").success (data) ->
            if data.length
              scope["last_#{what}_id"] = data[0].id
              f_add data
            else
              scope["last_#{what}_id"] = null
            extract_result()

      scope.moredef = (sid) ->
        loadmore 'def', sid, (stmts) ->
          Array.prototype.push.apply loaded_defs, stmts

      scope.morepro = (sid) ->
        loadmore 'pro', sid, (stmts) ->
          Array.prototype.push.apply loaded_pros, stmts
      # / Load more

      # Init
      scope.name = scope.res.name
      scope.$watch 'def_i', extract_result
      scope.$watch 'use_i', extract_result
