#!/usr/bin/python

# Adds the .dv files to the raw files table

import  os

from process import process

from main.models import Client, Show, Location, Episode, Raw_File, Cut_List

class add_dv(process):

    def one_file(self,pathname,show,location,seq):
        print pathname
        rf, created = Raw_File.objects.get_or_create(
            show=show, location=location,
            filename=pathname,)
        if created: 
            rf.sequence=seq
            rf.save()
   
    def one_loc(self,show,location):
      """
      finds dv files for this location
      """
      if self.options.whack:
          Raw_File.objects.filter(location=loc).delete()

      ep_dir=os.path.join(self.show_dir,'dv',location.slug)
      seq=0
      for dirpath, dirnames, filenames in os.walk(ep_dir):
          d=dirpath[len(ep_dir)+1:]
          # print dirpath, d, dirnames, filenames 
          for f in filenames:
              if f[-3:]=='.dv':
                  seq+=1
                  self.one_file(os.path.join(d,f),show,location,seq)

    def one_show(self, show):
      eps = Episode.objects.filter(show=show)
      for loc in Location.objects.filter(episode__in=eps):
        print show,loc
        self.one_loc(show,loc)

    def work(self):
        """
        find and process show
        """
        if self.options.client and self.options.show:
            client = Client.objects.get(slug=self.options.client)
            show = Show.objects.get(client=client, slug=self.options.show)

            self.show_dir = os.path.join(
                  self.options.mediadir,client.slug,show.slug)

            self.one_show(show)

        return

if __name__=='__main__': 
    p=add_dv()
    p.main()

