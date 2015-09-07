from django.conf.urls import patterns, url, include
from globallometree.apps.data_sharing.views import (
    DataSharingOverview, 
    DatasetListView
    )

urlpatterns = patterns('globallometree.apps.data_sharing.views',
    url(r'^$', DataSharingOverview.as_view(), name="data_sharing_overview"),
    url(r'^choose-license/$', 'choose_license', name="data-sharing-choose-license"),
    url(r'^upload-data/$', 'upload_data', name="data-sharing-upload"),
    url(r'^upload-confirm/(?P<ID_Dataset>\d+)/$', "upload_confirm", name="data-sharing-upload-confirm"),
    url(r'^datasets/(?P<ID_Dataset>\d+)/$', "dataset_detail", name="data-sharing-dataset-detail"),
    url(r'^datasets/$',  DatasetListView.as_view(), name="data-sharing-datasets"),
    url(r'^datasets/(?P<ID_Dataset>\d+)/edit/$', 'dataset_edit', name="dataset-edit"),
    url(r'^agreement/(?P<ID_Data_sharing_agreement>\d+)/$', 'agreement', name="dataset-agreement"),
    url(r'^my-data/', 'my_data', name="my-data")
)
