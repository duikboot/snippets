let g:pymode_python = 'python3'
augroup project_settings
    au!
    autocmd BufEnter * let b:start='ipython -i %'
    autocmd BufEnter * let b:dispatch='ipython -i %'
augroup END
