## api/urls.py
from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from globallometree.apps.api.views import ( 
	ReferenceViewSet, 
	WoodDensityViewSet, 
	RawDataViewSet,
	FamilyViewSet, 
	GenusViewSet, 
	SpeciesViewSet, 
	SubspeciesViewSet, 
	SpeciesGroupViewSet,
	SpeciesLocalNameViewSet,
	PopulationViewSet, 
	AllometricEquationViewSet, 
	ContinentViewSet, 
	CountryViewSet, 
	ForestTypeViewSet,
	ZoneFAOViewSet, 
	EcoregionUdvardyViewSet, 
	EcoregionWWFViewSet, 
	DivisionBaileyViewSet, 
	ZoneHoldridgeViewSet, 
	LocationViewSet,
	LocationGroupViewSet,
	DataLicenseViewSet, 
	DatasetViewSet,
	#DataRequestViewSet,
	InstitutionViewSet,
	BiomassExpansionFactorViewSet
	)

router = DefaultRouter()

router.register(r'allometric-equations',AllometricEquationViewSet)
router.register(r'wood-densities', WoodDensityViewSet)
router.register(r'raw-data', RawDataViewSet)

router.register(r'references', ReferenceViewSet)
router.register(r'institutions', InstitutionViewSet)

router.register(r'populations', PopulationViewSet)

router.register(r'families', FamilyViewSet)
router.register(r'genera', GenusViewSet)
router.register(r'species', SpeciesViewSet)
router.register(r'subspecies', SubspeciesViewSet)
router.register(r'species-groups', SpeciesGroupViewSet)
router.register(r'species-local-names', SpeciesLocalNameViewSet)

router.register(r'continents', ContinentViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'location-groups', LocationGroupViewSet)

router.register(r'forest-types', ForestTypeViewSet)
router.register(r'ecological-zones-fao', ZoneFAOViewSet)
router.register(r'ecoregions-udvardy', EcoregionUdvardyViewSet)
router.register(r'ecoregions-wwf', EcoregionWWFViewSet)
router.register(r'life-zones-holdridge', ZoneHoldridgeViewSet)
router.register(r'divisions-bailey', DivisionBaileyViewSet)

router.register(r'data-sharing-agreements',DataLicenseViewSet)
router.register(r'datasets',DatasetViewSet)
#router.register(r'data-requests',DataRequestViewSet)
router.register(r'biomass-expansion-factors', BiomassExpansionFactorViewSet)

urlpatterns = patterns('',
    url(r'^v1/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
