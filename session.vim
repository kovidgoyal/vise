" Scan the following dirs (recursively for tags
let g:project_tags_dirs = ['vise']
let g:syntastic_python_flake8_exec = 'flake8'
set wildignore+==template.py
set wildignore+==tags
set wildignore+=*.pyj-cached

python <<endpython
import sys, os, vim
items = {x.replace('=', r'\=') for x in os.listdir('.')}
items.discard('resources'), items.discard('.git'), items.discard('__pycache__')
items |= {'resources/' + x for x in os.listdir('resources') if x != 'vise-client.js'}
vim.command('nnoremap <leader>k :silent !git difftool -d ' + ' '.join(items) + ' -d &<CR><CR>')
sys.path.insert(0, os.path.abspath('.'))
import vise
endpython
