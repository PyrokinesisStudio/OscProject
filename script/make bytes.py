import py_compile
import os

cwd = os.getcwd()
d = os.listdir()


''' karena blender sudah mengcompile filenya maka bagian ini tak diperlukan tuk sementara
for i in d:
	py_compile.compile(i)
'''

#sesi mengganti nama pada pychache nya
os.chdir(cwd + "//__pycache__")

d = os.listdir()
for i in (d):
	l = i.split(".")
	os.rename(i, l[0] + ".pyc")