import module1.module2
import SomeOtherModule as other
from basemodule import submodule, some_lib_call


def call_constant():
    return some_lib_call(other.constant)

# Just calling module_func
module1.module2.module_func()

obj = object()
var = 'A'
x, y = XY
a, b = 1, 2
dico[key] = 'Value'
obj.field = var

how_many = 'lots'

with open(filename) as fd, open(other):
    data = fd.read(how_many)

dico['fn']()

class SomeClass(SomeBaseClass):
    def SomeMethod(self, param):
        if param:
            local = 'x'
            print(local)
            relevant = False
            return_value = some_lib_call(
                param,
                local,
            ) or var
            return return_value

def some_func(some_args):
    print('Coucou')
    for some_arg in some_args:
        if some_arg:
            tmp = some_lib_call(some_arg)
    some_var = Obj1.Obj2.Method3(tmp)
    return some_var
