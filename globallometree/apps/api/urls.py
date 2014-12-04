## api/urls.py
from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from globallometree.apps.api.views import ( 
	DataReferenceViewSet, 
	WoodDensityViewSet, 
	FamilyViewSet, 
	GenusViewSet, 
	SpeciesViewSet, 
	SubspeciesViewSet, 
	SpeciesGroupViewSet,
	SpeciesLocalNameViewSet,
	SubspeciesLocalNameViewSet,
	PopulationViewSet, 
	EcosystemViewSet, 
	AllometricEquationViewSet, 
	ContinentViewSet, 
	CountryViewSet, 
	BiomeFAOViewSet, 
	BiomeUdvardyViewSet, 
	BiomeWWFViewSet, 
	DivisionBaileyViewSet, 
	BiomeHoldridgeViewSet, 
	LocationViewSet,
	LocationGroupViewSet,
	DataSharingAgreementViewSet, 
	DataSetViewSet,
	DataAccessRequestViewSet
	)

router = DefaultRouter()

router.register(r'references', DataReferenceViewSet)
router.register(r'wood-densities',WoodDensityViewSet)
router.register(r'families', FamilyViewSet)
router.register(r'genera', GenusViewSet)
router.register(r'species', SpeciesViewSet)
router.register(r'subspecies', SubspeciesViewSet)
router.register(r'species-groups', SpeciesGroupViewSet)
router.register(r'species-local-names', SpeciesLocalNameViewSet)
router.register(r'subspecies-local-names', SubspeciesLocalNameViewSet)
router.register(r'populations', PopulationViewSet)
router.register(r'ecosystems', EcosystemViewSet)
router.register(r'allometric-equations',AllometricEquationViewSet)
router.register(r'continents', ContinentViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'fao-biomes', BiomeFAOViewSet)
router.register(r'udvardy-biomes', BiomeUdvardyViewSet)
router.register(r'wwf-biomes', BiomeWWFViewSet)
router.register(r'bailey-divisions', DivisionBaileyViewSet)
router.register(r'holdridge-biomes', BiomeHoldridgeViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'location-groups', LocationGroupViewSet)
router.register(r'data-sharing-agreements',DataSharingAgreementViewSet)
router.register(r'data-sets',DataSetViewSet)
router.register(r'data-requests',DataAccessRequestViewSet)

urlpatterns = patterns('',
    url(r'^v1/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
