#!/usr/bin/python

# mk_audio_png.py - makes a vis of the audio from the final encode

import gslevels

import os

from process import process
from main.models import Show, Episode

class mk_audio_png(process):

    ready_state = 3
    ret = None

    def process_ep(self, ep):

        # get a list of video files to process
        files = []
        for ext in self.options.upload_formats:

            p = gslevels.Make_png()
            p.uri = os.path.join(self.show_dir,ext,"%s.%s"%(ep.slug,ext))
            p.verbose = self.options.verbose
            p.setup()
            p.start()
            png_filename = os.path.join(ext,"%s_audio.png"%(ep.slug,))
            ret = p.mk_png( os.path.join(self.show_dir, png_filename ))

            self.file2cdn(ep.show, png_filename)
       
        # tring to fix the db timeout problem
        # this is bad - it steps on the current values im memory:
        # ep=Episode.objects.get(pk=ep.id)
        # this seems to work:
        try:
            ep.save()
        except DatabaseError, e:
            from django.db import connection
            connection.connection.close()
            connection.connection = None
            ep.save()

        return ret

if __name__ == '__main__':
    p=mk_audio_png()
    p.main()

