from django.conf.urls import patterns, url, include
from apps.data_sharing.views import DataSharingOverview, DatasetListView

urlpatterns = patterns('apps.data_sharing.views',
    url(r'^$', DataSharingOverview.as_view(), name="data_sharing_overview"),
    url(r'^choose-license/$', 'choose_license', name="data-sharing-choose-license"),
    url(r'^upload-data/$', 'upload_data', name="data-sharing-upload"),
    url(r'^datasets/(?P<Dataset_ID>\d+)/$', "dataset_detail", name="data-sharing-dataset-detail"),
    url(r'^datasets/$',  DatasetListView.as_view(), name="data-sharing-datasets")
)