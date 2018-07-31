

if [ -f ~/.jupyter/jupyter_notebook_config.py ]
then 
  #modify it by hand
else
  cp dev_env/local/jupyter_notebook_config.py ~/.jupyter/
fi
