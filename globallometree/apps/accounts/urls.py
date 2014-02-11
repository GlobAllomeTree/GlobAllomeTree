from django.conf.urls import patterns


urlpatterns = patterns('django.contrib.auth.views',
     (r'^logout[/]*', 'logout', {'template_name': 'accounts/account_logout.html'}),
     (r'^login/$', 'login', {'template_name': 'accounts/account_login.html'}),
     (r'^logout/$', 'logout', {'template_name': 'accounts/account_logout.html'}),
     
     
     #For users who forgot their password to solicit a reset email
     (r'^password-reset/$', 'password_reset', 
                                          {'template_name': 'accounts/account_password_reset_form.html'}),
     #For users who forgot their password to after correctly requesting a reset email                                     
     (r'^password-reset/done/$', 'password_reset_done', 
                                          {'template_name': 'accounts/account_password_reset_done.html'}),
     #For users who forgot their password being referred from an email
     (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm',
                                          {'template_name': 'accounts/account_password_reset_confirm.html'}),
     #For users who forgot their password when done after referral from the email
     (r'^reset/done/$', 'password_reset_complete',
                                          {'template_name': 'accounts/account_password_reset_complete.html'}),
     #For logged in existing users
     (r'^change-password/$',   'password_change',
                                          {'template_name': 'accounts/account_password_change_form.html'}),
     #For logged in existing users
     (r'^change-password/done/$', 'password_change_done',
                                          {'template_name': 'accounts/account_password_change_done.html'}),
    ) 



#Site views
urlpatterns += patterns('apps.accounts.views',
     (r'^register/$', 'register'),
     (r'^approval-pending/$', 'approval_pending')
)
