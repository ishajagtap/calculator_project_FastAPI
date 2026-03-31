import inspect
import app.calculator_repl as cr
for i,l in enumerate(inspect.getsource(cr).splitlines(), start=1):
    print(f"{i:3}: {l}")
