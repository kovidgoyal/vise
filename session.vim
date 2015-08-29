" Scan the following dirs (recursively for tags
let g:project_tags_dirs = ['vise']

set wildignore+==template.py

python <<endpython
import sys, os
sys.path.insert(0, os.path.abspath('.'))
import vise
endpython
