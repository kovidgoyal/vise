" Scan the following dirs (recursively for tags
let g:project_tags_dirs = ['vise']
let g:syntastic_python_flake8_exec = 'flake8'
set wildignore+=template.py
set wildignore+=*.pyj-cached

python <<endpython
import sys, os
sys.path.insert(0, os.path.abspath('.'))
import vise
endpython
