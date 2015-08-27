from django.conf.urls import patterns, url
from .views import UserProfileDetailView, UserProfileUpdateView, MyProfileDetailView


urlpatterns = patterns('django.contrib.auth.views',
     url(r'^logout[/]*', 'logout', {'template_name': 'accounts/account_logout.html'}),
     url(r'^login/$', 'login', {'template_name': 'accounts/account_login.html'}),
     url(r'^logout/$', 'logout', {'template_name': 'accounts/account_logout.html'}),
     
     
     #For users who forgot their password to solicit a reset email
     url(r'^password-reset/$', 
          'password_reset', 
          {'template_name': 'accounts/account_password_reset_form.html'},
          name='password_reset'
          ),

     #For users who forgot their password to after correctly requesting a reset email                                     
     url(r'^password-reset/done/$', 
          'password_reset_done', 
          {'template_name': 'accounts/account_password_reset_done.html',},
          name='password_reset_done'),

     #For users who forgot their password being referred from an email
     url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
          'password_reset_confirm',
          {'template_name': 'accounts/account_password_reset_confirm.html'},
          name='password_reset_confirm'),

     #For users who forgot their password when done after referral from the email
     url(r'^reset/done/$', 
          'password_reset_complete',
          {'template_name': 'accounts/account_password_reset_complete.html'},
          name='password_reset_complete'),

     #For logged in existing users
     url(r'^change-password/$',   
          'password_change',
          {'template_name': 'accounts/account_password_change_form.html'},
          name='password_change'),

     #For logged in existing users
     url(r'^change-password/done/$', 
          'password_change_done',
          {'template_name': 'accounts/account_password_change_done.html'},
          name='password_change_done')

    ) 



#Site views
urlpatterns += patterns('globallometree.apps.accounts.views',
     (r'^register/$', 'register'),
     (r'^approval-pending/$', 'approval_pending'),
     url(r'^profile/(?P<pk>\d+)/$',
         UserProfileDetailView.as_view(),
         name='userprofile_detail_generic'),
     url(r'^profile/$',
         MyProfileDetailView.as_view(),
         name='myprofile_detail'),
     url(r'^profile/update/(?P<pk>\d+)/$',
         UserProfileUpdateView.as_view(),
         name='userprofile_update_admin'),
     url(r'^profile/update/$',
         UserProfileUpdateView.as_view(),
         name='userprofile_update')
     # url(r'^profile/(?P<user_id>\d+)/$', 'my_profile')
)
