import py_compile, os
errors = []
script_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(script_dir, '..', 'app')
for root, dirs, files in os.walk(app_dir):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root,f)
            try:
                py_compile.compile(path, doraise=True)
            except py_compile.PyCompileError as e:
                errors.append((path,str(e)))
if not errors:
    print('OK')
else:
    for p,e in errors:
        print('FILE:',p)
        print(e)
