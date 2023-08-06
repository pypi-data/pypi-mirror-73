import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import safe_infer
from pylint.checkers.typecheck import _determine_callable
import json



class FunctionTypeChecker(BaseChecker):
    __implements__ = IAstroidChecker
    refactordict = {}

    # gets filled at runtime from the addreference checker in monkeypatch
    linter_storage = None


    setup = False
    name = 'possible-refactoring-needed'
    priority = -1
    msgs = {
        'E8102': (
            '%s %s needs possible refactor on %s member%s',
            'possible-refactor',
            'Signature cant be found in stubs'
        ),
        'E8103': (
            '%s %s needs possible refactor assigning on the %s property%s',
            'possible-refactor-property',
            'Signature cant be found in stubs'
        ),
    }
    options = (
        (
            'possible-refactor-version',
            {
                "default": (""),
                "type": "csv",
                "metavar": "<refactor_version>",
                "help": "Version used for checking possible refactors "
            }
        ),

    )

    def __init__(self, linter=None):
        super(FunctionTypeChecker, self).__init__(linter)

    def setup_after_pylintrc_read(self):
        try:
            with open(self.linter_storage['sourcefile'] + r"/../changelist.json") as json_file:
                data = json.load(json_file)
                self.refactordict = (data["Refactors"])
                self.setup = True
                print "setup refactors works"
        except Exception as e:
            print e
            return


    def visit_call(self, node):
        try:
            if not self.setup:
                self.setup_after_pylintrc_read()
            versions = self.config.possible_refactor_version # pylint: disable=no-member
            if versions == []:
                return
            func = node.func.attrname
            inferred = list(node.func.expr.infer())

            # get all inferred classes
            non_opaque_inference_results = [
                owner for owner in inferred
                if owner is not astroid.Uninferable
                and not isinstance(owner, astroid.nodes.Unknown)
            ]
            for version in versions:
                for owner in non_opaque_inference_results:
                    name = getattr(owner, 'name', None)
                    full = name + "." + func
                    if full in self.refactordict[version]:
                        hint = " (version " + version + ": " + self.refactordict[version][full] + ")"
                        self.add_message('possible-refactor', node=node,
                                        args=(owner.display_type(), name,
                                            func, hint))
        except: #catch if the function doesn't reference an external source.
            return

    def visit_assign(self, node):
        try:
            if not self.setup:
                self.setup_after_pylintrc_read()
            versions = self.config.possible_refactor_version # pylint: disable=no-member
            if versions == []:
                return
            attribute = node.targets[0].attrname 
            inferred = list(node.targets[0].expr.inferred())

            # get all inferred classes
            non_opaque_inference_results = [
                owner for owner in inferred
                if owner is not astroid.Uninferable
                and not isinstance(owner, astroid.nodes.Unknown)
            ]
            for version in versions:
                for owner in non_opaque_inference_results:
                    name = getattr(owner, 'name', None)
                    full = name + "." + attribute
                    if full in self.refactordict[version]:
                        hint = " (version " + version + ": " + self.refactordict[version][full] + ")"
                        self.add_message('possible-refactor-property', node=node,
                                        args=(owner.display_type(), name,
                                            attribute, hint))
        except: #catch if the function doesn't reference an external source.
            return
