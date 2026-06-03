import py_compile, os
errors = []
for root, dirs, files in os.walk('app'):
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
