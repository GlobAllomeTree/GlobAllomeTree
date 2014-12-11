## api/urls.py
from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from globallometree.apps.api.views import ( 
	ReferenceViewSet, 
	WoodDensityViewSet, 
	FamilyViewSet, 
	GenusViewSet, 
	SpeciesViewSet, 
	SubspeciesViewSet, 
	SpeciesGroupViewSet,
	SpeciesLocalNameViewSet,
	SubspeciesLocalNameViewSet,
	PopulationViewSet, 
	AllometricEquationViewSet, 
	ContinentViewSet, 
	CountryViewSet, 
	ForestTypeViewSet,
	BiomeFAOViewSet, 
	BiomeUdvardyViewSet, 
	BiomeWWFViewSet, 
	DivisionBaileyViewSet, 
	BiomeHoldridgeViewSet, 
	LocationViewSet,
	LocationGroupViewSet,
	DataLicenseViewSet, 
	DatasetViewSet,
	DataRequestViewSet,
	InstitutionViewSet
	)

router = DefaultRouter()

router.register(r'allometric-equations',AllometricEquationViewSet)
router.register(r'wood-densities',WoodDensityViewSet)

router.register(r'references', ReferenceViewSet)
router.register(r'institutions', InstitutionViewSet)

router.register(r'populations', PopulationViewSet)

router.register(r'families', FamilyViewSet)
router.register(r'genera', GenusViewSet)
router.register(r'species', SpeciesViewSet)
router.register(r'subspecies', SubspeciesViewSet)
router.register(r'species-groups', SpeciesGroupViewSet)
router.register(r'species-local-names', SpeciesLocalNameViewSet)
router.register(r'subspecies-local-names', SubspeciesLocalNameViewSet)

router.register(r'continents', ContinentViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'location-groups', LocationGroupViewSet)

router.register(r'forest-types', ForestTypeViewSet)
router.register(r'biomes-fao', BiomeFAOViewSet)
router.register(r'biomes-udvardy', BiomeUdvardyViewSet)
router.register(r'biomes-wwf', BiomeWWFViewSet)
router.register(r'biomes-holdridge', BiomeHoldridgeViewSet)
router.register(r'divisions-bailey', DivisionBaileyViewSet)

router.register(r'data-sharing-agreements',DataLicenseViewSet)
router.register(r'datasets',DatasetViewSet)
router.register(r'data-requests',DataRequestViewSet)

urlpatterns = patterns('',
    url(r'^v1/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
