from pylint.checkers.variables import VariablesChecker
from pylint.checkers import utils


class test(VariablesChecker):
    def __init__(self, linter=None):
        VariablesChecker.__init__(self, linter)


    def visit_name2(self, node):
        """check that a name is defined if the current scope and doesn't
        redefine a built-in
        """
        stmt = node.statement()
        if stmt.fromlineno is None:
            # name node from a astroid built from live code, skip
            assert not stmt.root().file.endswith('.py')
            return

        name = node.name
        frame = stmt.scope()
        # if the name node is used as a function default argument's value or as
        # a decorator, then start from the parent frame of the function instead
        # of the function frame - and thus open an inner class scope
        if ((utils.is_func_default(node) and not utils.in_comprehension(node)) or
                utils.is_func_decorator(node) or utils.is_ancestor_name(frame, node)):
            # Do not use the highest scope to look for variable name consumption in this case
            # If the name is used in the function default, or as a decorator, then it
            # cannot be defined there
            # (except for list comprehensions in function defaults)
            start_index = len(self._to_consume) - 2
        else:
            start_index = len(self._to_consume) - 1
        # iterates through parent scopes, from the inner to the outer
        base_scope_type = self._to_consume[start_index].scope_type
        # pylint: disable=too-many-nested-blocks; refactoring this block is a pain.
        for i in range(start_index, -1, -1):
            current_consumer = self._to_consume[i]
            # if the current scope is a class scope but it's not the inner
            # scope, ignore it. This prevents to access this scope instead of
            # the globals one in function members when there are some common
            # names. The only exception is when the starting scope is a
            # comprehension and its direct outer scope is a class
            if current_consumer.scope_type == 'class' and i != start_index and not (
                    base_scope_type == 'comprehension' and i == start_index - 1):
                if self._ignore_class_scope(node):
                    continue

            # the name has already been consumed, only check it's not a loop
            # variable used outside the loop
            # avoid the case where there are homonyms inside function scope and
            if name in current_consumer.consumed and not (
                    current_consumer.scope_type == 'comprehension'
                    and self._has_homonym_in_upper_function_scope(node, i)):
                defnode = utils.assign_parent(current_consumer.consumed[name][0])
                self._check_late_binding_closure(node, defnode)
                self._loopvar_name(node, name)
                break

            found_node = current_consumer.get_next_to_consume(node)
            if found_node is None:
                continue

            # checks for use before assignment
            defnode = utils.assign_parent(current_consumer.to_consume[name][0])
            if defnode is not None:
                self._check_late_binding_closure(node, defnode)
                defstmt = defnode.statement()
                defframe = defstmt.frame()
                # The class reuses itself in the class scope.
                recursive_klass = (frame is defframe and
                                   defframe.parent_of(node) and
                                   isinstance(defframe, astroid.ClassDef) and
                                   node.name == defframe.name)

                maybee0601, annotation_return, use_outer_definition = self._is_variable_violation(
                    node, name, defnode, stmt, defstmt,
                    frame, defframe,
                    base_scope_type, recursive_klass)

                if use_outer_definition:
                    continue

                if (maybee0601
                        and not utils.is_defined_before(node)
                        and not astroid.are_exclusive(stmt, defstmt, ('NameError',))):

                    # Used and defined in the same place, e.g `x += 1` and `del x`
                    defined_by_stmt = (
                            defstmt is stmt
                            and isinstance(node, (astroid.DelName, astroid.AssignName))
                    )
                    if (recursive_klass
                            or defined_by_stmt
                            or annotation_return
                            or isinstance(defstmt, astroid.Delete)):
                        if not utils.node_ignores_exception(node, NameError):
                            self.add_message('undefined-variable', args=name,
                                             node=node)
                    elif base_scope_type != 'lambda':
                        # E0601 may *not* occurs in lambda scope.
                        self.add_message('used-before-assignment', args=name, node=node)
                    elif base_scope_type == 'lambda':
                        # E0601 can occur in class-level scope in lambdas, as in
                        # the following example:
                        #   class A:
                        #      x = lambda attr: f + attr
                        #      f = 42
                        if isinstance(frame, astroid.ClassDef) and name in frame.locals:
                            if isinstance(node.parent, astroid.Arguments):
                                if stmt.fromlineno <= defstmt.fromlineno:
                                    # Doing the following is fine:
                                    #   class A:
                                    #      x = 42
                                    #      y = lambda attr=x: attr
                                    self.add_message('used-before-assignment',
                                                     args=name, node=node)
                            else:
                                self.add_message('undefined-variable',
                                                 args=name, node=node)
                        elif current_consumer.scope_type == 'lambda':
                            self.add_message('undefined-variable',
                                             node=node, args=name)

            current_consumer.mark_as_consumed(name, found_node)
            # check it's not a loop variable used outside the loop
            self._loopvar_name(node, name)
            break
        else:
            # we have not found the name, if it isn't a builtin, that's an
            # undefined name !
            if not (name in astroid.Module.scope_attrs or utils.is_builtin(name)
                    or name in self.config.additional_builtins):
                if not utils.node_ignores_exception(node, NameError):
                    self.add_message('undefined-variable', args=name, node=node)