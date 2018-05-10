#!/usr/bin/python

# email_ab.py
# abstract email class

from django.core.mail import get_connection, EmailMessage

from django.template import Context, Template

from process import process
from django.conf import settings

class email_ab(process):

    subject_template = "stub testing:{{ep.name}}"

    body_header = """
Hi,

This is Veyepar, the automated video processing system.
{% if ep.reviewers %}
Note to {{ep.reviewers}}: You get to be in on this because presenters have plenty to do and we don't want to burn them out, so please help out and look things over for them.  What is expected of a reviewer:  Hurry up and watch the video.  https://github.com/CarlFK/veyepar/wiki/Reviewer Thanks!
{% endif %}

"""
    body_body = "stub testing:{{ep.description}}"

    body_footer = """
Email generated by https://github.com/CarlFK/veyepar/blob/master/dj/scripts/{{py_name}}
but replies go to real people.

Reference: https://veyepar.nextdayvideo.com/main/E/{{ep.id}}/
"""


    def context(self, ep):
        # collect values to be used by the templates.

        ctx = { 'ep':ep,
                'py_name': "email_ab.py",
                # 'MEDIA_URL':settings.MEDIA_URL,
                }

        return ctx

    def mk_body(self, ep):

        context = self.context(ep)

        body_template = \
                self.options.note + \
                self.body_header + \
                self.body_body + \
                self.body_footer

        if self.options.spc or not ep.emails:
            body_alert = """
Hello show organizer(s)!

This item gets your attention.
Please review and forward it on to the presenter.

In case it isn't clear what this item is about, here is some context:
    name: {{ep.name}}
    authors: {{ep.authors}}
    emails: {{ep.emails}}
    reviewers: {{ep.reviewers}}
    released: {{ep.released}}
    conf_url: {{ep.conf_url}}
    conf_key: {{ep.conf_key}}
    room: {{ep.location}}
    start: {{ep.start}}

What follows is what was intended to be sent to the presenter and reviewer.
"""
            body_template = body_alert + body_template\

        body = Template(
                body_template
                ).render(Context(context, autoescape=False))

        return body


    def process_ep(self, ep):

        if self.options.spc:
            # single point of contact gets them all
            emails = self.options.spc
        else:
            # if there is no email, use the client's.
            # like for lightning talks.
            emails = ep.emails or ep.show.client.contacts

        if self.options.verbose: print(emails)

        if emails:
            tos = [e.strip() for e in emails.split(',')]

            subject = Template(self.subject_template).render(
                    Context({'ep':ep}, autoescape=False))

            body = self.mk_body(ep)

            sender = settings.EMAIL_SENDER
            ccs = [cc.strip() for cc in settings.EMAIL_CC.split(',')]
            ccs.extend([cc.strip() for cc in ep.reviewers.split(',')])
            ccs =  list(set([a.strip() for a in ccs if a]))
            # make a list of addresses:
            # [a for a if a] is to get rid of the empty CC.
            # set to get rid of dupes
            # .strip() do remove the spaces from the front of things.
            reply_tos = set([a.strip() for a in
                    [sender,] \
                    + ep.show.client.contacts.split(',') \
                    + ccs \
                       if a] )
            # headers={Reply-To... needs to be a string of comma seperated
            reply_to = ','.join( reply_tos )
            headers = {
                     'Reply-To': reply_to,
                     'X-veyepar': ep.show.slug,
                        }

            if self.options.test:
                print("tos:", tos)
                print("ccs:", ccs)
                print("subject:", subject)
                print("headers:", headers)
                # print("context:", context)
                print("body:", body)
                ret = False

            else:

                email = EmailMessage(
                        subject, body, sender, tos,
                        headers=headers, cc=ccs )
                connection = get_connection()
                ret = connection.send_messages([email])
                print("subject:", subject)
                print("tos:", tos)
                ret = True # need to figure out what .send_messages returns

        else:
            print("no emails!")
            ret = False

        return ret

    def add_more_options(self, parser):
        parser.add_option('--spc',
            default="",
            help="Single Point of Contact.")

        parser.add_option('--note',
            default="",
            help="Prepend a note above the Hi.")

if __name__ == '__main__':
    p=email_ab()
    p.main()

