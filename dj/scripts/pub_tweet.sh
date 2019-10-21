#!/bin/bash -xe

if grep ^DATABASES ../dj/local_settings.py; then

python mk_public.py --unlock $*
python tweet.py --lag 156 $*
python email_conf.py $*

else
  vim ../local_settings.py
  exit
fi
