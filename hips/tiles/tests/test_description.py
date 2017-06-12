# Licensed under a 3-clause BSD style license - see LICENSE.rst

from ..description import HipsDescription

class TestHiPSDescription:
    @classmethod
    def setup_class(cls):
        # These HiPS properties were obtained from: http://alasky.u-strasbg.fr/DSS/DSSColor/properties
        hips_properties = """
        creator_did          = ivo://CDS/P/DSS2/color
        obs_collection       = DSS colored
        obs_title            = DSS colored
        obs_description      = Color composition generated by CDS. This HiPS survey is based on 2 others HiPS surveys, respectively DSS2-red and DSS2-blue HiPS, both of them directly generated from original scanned plates downloaded from STScI site. The red component has been built from POSS-II F, AAO-SES,SR and SERC-ER plates. The blue component has been build from POSS-II J and SERC-J,EJ. The green component is based on the mean of other components. Three missing plates from red survey (253, 260, 359) has been replaced by pixels from the DSSColor STScI jpeg survey. The 11 missing blue plates (mainly in galactic plane) have not been replaced (only red component).
        obs_copyright        = Digitized Sky Survey - STScI/NASA, Colored & Healpixed by CDS
        obs_copyright_url    = http://archive.stsci.edu/dss/acknowledging.html
        client_category      = Image/Optical/DSS
        client_sort_key      = 03-00
        hips_builder         = Aladin/HipsGen v9.039
        hips_creation_date   = 2010-05-01T19:05Z
        hips_release_date    = 2015-05-11T08:45Z
        # hips_release_date    = 2016-12-13T14:51Z
        hips_creator         = CDS (A.Oberto, P.Fernique)
        hips_version         = 1.31
        hips_order           = 9
        hips_frame           = equatorial
        hips_tile_width      = 512
        hips_tile_format     = jpeg
        dataproduct_type     = image
        client_application   = AladinLite
        moc_access_url       = http://alasky.u-strasbg.fr/DSS/DSSColor/Moc.fits
        hips_service_url     = http://alasky.u-strasbg.fr/DSS/DSSColor
        hips_status          = public master clonableOnce
        hips_rgb_red         = DSS2Merged [1488.0 8488.8125 14666.0 Linear]
        hips_rgb_blue        = DSS2-blue-XJ-S [4286.0 12122.5 19959.0 Linear]
        hips_hierarchy       = median
        hips_pixel_scale     = 2.236E-4
        hips_initial_ra      = 085.30251
        hips_initial_dec     = -02.25468
        hips_initial_fov     = 2
        moc_sky_fraction     = 1
        dataproduct_subtype  = color
        hips_copyright       = CNRS/Unistra
        obs_ack              = The Digitized Sky Surveys were produced at the Space Telescope Science Institute under U.S. Government grant NAG W-2166. The images of these surveys are based on photographic data obtained using the Oschin Schmidt Telescope on Palomar Mountain and the UK Schmidt Telescope. The plates were processed into the present compressed digital form with the permission of these institutions
        prov_progenitor      = STScI
        bib_reference        = 2008AJ....136..735L
        bib_reference_url    = http://simbad.u-strasbg.fr/simbad/sim-ref?bibcode=2008AJ....136..735L
        # 1975-1999
        t_min                = 42413
        t_max                = 51179
        obs_regime           = Optical
        # Bandpass  422-967 THz
        em_min               = 7.104086682464e-7
        em_max               = 3.100232244054e-7
        # hips_master_url     = ex: http://yourHipsServer/null
        # For compatibility
        label              = DSS colored
        coordsys           = C
        isColor            = true
        ~
        """
        cls.hipsdescription = HipsDescription.parse_file_properties(hips_properties)

    def test_base_url(cls):
        assert cls.hipsdescription.base_url == 'http://alasky.u-strasbg.fr/DSS/DSSColor'

    def test_title(cls):
        assert cls.hipsdescription.title == 'DSS colored'

    def test_hips_version(cls):
        assert cls.hipsdescription.hips_version == 1.31

    def test_hips_frame(cls):
        assert cls.hipsdescription.hips_frame == 'equatorial'

    def test_hips_order(cls):
        assert cls.hipsdescription.hips_order == 9

    def test_tile_format(cls):
        assert cls.hipsdescription.tile_format == 'jpeg'
