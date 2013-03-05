#!/usr/bin/python

# email_url.py
# emails the video URL to the presenters

from django.core.mail import get_connection, EmailMessage

from process import process

class email_title(process):

    ready_state = None

    def process_ep(self, ep):
        if self.options.verbose: print ep
        if self.options.verbose: print ep.emails, ep.released
        if ep.emails: # and ep.released:
            tos = ep.emails.split(',')
            png_url = "http://veyepar.nextdayvideo.com/static/%s/%s/titles/%s.png" % ( ep.show.client.slug, ep.show.slug, ep.slug )
            subject = "Video metadata for: %s" % ep.name
            body = """
    According to the released field in the database, your talk is going
    to be recorded and posted online.  If this is a problem, please 
    contact the conference organizers.

    Please review the text:
    %(public_url)s

    Problems with the text will need to be fixed in the conference database.

    Also have a look at the attached title slide to verify that it rendered 
    correctly.   If there is a problem with it, first check here for 
    the latest version to see if the problem has already been corrected:
    %(png_url)s
    
    and then ontact me by repling to this message.

    Reference: #%(id)s  %(slug)s

    Email generated by Veyepar, but replies go to Carl.
    """ % ({ 'name':ep.name, 'authors':ep.authors, 
        'description':ep.description, 
        'png_url':png_url, 
        'public_url':ep.public_url,
        'id':ep.id, 'slug':ep.slug })

            sender = 'Carl Karsten <carl@nextdayvideo.com>'
            headers = {
                # 'Reply-To': "ChiPy <chicago@python.org>"
                # 'From': sender,
                }    

            if self.options.test:
                print "subject:", subject
                print "body:", body
                ret = False
            else:

                connection = get_connection()
                email = EmailMessage(subject, body, sender, tos, headers=headers ) 
                ret = connection.send_messages([email])
                print tos, ret
                ret = True # need to figure out what .send_messages returns

        else:
            ret = False

        return ret

if __name__ == '__main__':
    p=email_title()
    p.main()

