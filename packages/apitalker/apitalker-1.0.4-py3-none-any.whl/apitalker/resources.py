"""This module provides convenient mappings of currently existing API resources provided by Apitalks.

Resources are mapped using classes, to be able to use `.` [dot] notation (and IntelliSense of IDE of your choice.)

**All resources were NOT tested to be functional**. They were just taken from the documentation.

Example::

    from apitalker.api import API
    from apitalker.resources import Czso

    api = API("yourapikey")

    data, error = api.get_data(Czso.ciselniky_kraj)

    if error is None:
        print(data.as_dataframe.head)

"""


class Czso:
    """Class for mapping API resources of Czech Statistical Office, provided by Apitalks.

    References:
        https://www.api.store/czso.cz/dokumentace (in czech language)
    """

    lide_domy_byty = "/czso.cz/lide-domy-byty"
    vyjizdky_zamestnani = "/czso.cz/vyjizdky-zamestnani"
    obyvatele_sidelni_jednotky = "/czso.cz/obyvatele-sidelni-jednotky"
    obyvatelstvo_domy = "/czso.cz/obyvatelstvo-domy"
    prumerne_mzdy_odvetvi = "/czso.cz/prumerne-mzdy-odvetvi"
    cizinci_dle_obcanstvi_veku_pohlavi = (
        "/czso.cz/cizinci-podle-statniho-obcanstvi-veku-a-pohlavi"
    )
    pohyb_obyvatel = "/czso.cz/pohyb-obyvatel-za-cr-kraje-okresy-so-orp-a-obce"
    nadeje_doziti = "/czso.cz/nadeje-doziti-v-okresech-a-spravnich-obvodech-orp"
    prumerne_spotrebitelske_ceny = (
        "/czso.cz/prumerne-spotrebitelske-ceny-vybranych-vyrobku-potravinarske-vyrobky"
    )
    hoste_a_prenocovani = (
        "/czso.cz/hoste-a-prenocovani-v-hromadnych-ubytovacich-zarizenich-podle-zemi"
    )
    ciselniky_obce_a_ujezdy = "/czso.cz/obec-a-vojensky-ujezd"
    ciselniky_mestske_obvody_a_casti = "/czso.cz/mestsky-obvod-mestska-cast"
    ciselniky_spr_obv_s_rozsirenou_pusobnosti = (
        "/czso.cz/spravni-obvody-obci-s-rozsirenou-pusobnosti"
    )
    ciselniky_spr_obv_praha = "/czso.cz/spravni-obvod-v-hlavnim-meste-praze"
    ciselniky_stat = "/czso.cz/stat"
    ciselniky_region_soudrznosti = "/czso.cz/region-soudrznosti"
    ciselniky_kraj = "/czso.cz/kraj"
    ciselniky_okres = "/czso.cz/okres"

    def __init__(self) -> None:
        pass


class CzechPost:
    """Class for mapping API resources of Czech Post Office, provided by Apitalks.

    References:
        https://www.api.store/ceskaposta.cz/dokumentace (in czech language)
    """

    provozovny = "/cpost.cz/provozovny"
    posty_info = "/cpost.cz/posty"
    postovni_schranky = "/cpost.cz/postovni-schranky"
    psc = "/cpost.cz/psc"
    mista_bez_dorucovani = "/cpost.cz/bez-dorucovani"
    psc_s_dorucovacim_pasmem = "/cpost.cz/psc-s-dorucovacim-pasmem"
    psc_adresni = "/cpost.cz/adresni-psc"
    obce_s_adresni_psc = "/cpost.cz/obce-adresni-psc"
    provozovny_s_baliky = "/cpost.cz/provozovny-balik"
    provozovny_s_baliky_nad_30kg = "/cpost.cz/provozovny-balik-30kg"
    mista_zkracene_dodani = "/cpost.cz/mista-zkracene-dodani"
    mista_zkracene_dodani_svatky = "/cpost.cz/mista-zkracene-dodani-svatky"
    mista_prevzeti_u_odesilatele = "/cpost.cz/mista-prevezeti-u-odesilatele"
    provozovny_podat_balik_na_postu = "/cpost.cz/podani-baliku-na-postu"
    provozovny_ulozit_balik_na_postu = "/cpost.cz/adresovani-baliku-na-postu"
    balikovny = "/cpost.cz/balikovny"
    adresovani_balik_expres = "/cpost.cz/adresovani-baliku-expres"
    podani_balik_expres = "/cpost.cz/podani-baliku-expres"
    podani_balik_nadrozmer = "/cpost.cz/podani-baliku-nadrozmer"
    ulozit_balik_nadrozmer = "/cpost.cz/ulozeni-baliku-nadrozmer"
    roznasky_propagacnich_materialu_pocty = "/cpost.cz/pocty-RIPM"
    roznasky_propagacnich_materialu_posty = "/cpost.cz/objednavka-RIPM"

    def __init__(self) -> None:
        pass


class DataBoxes:
    """Class for mapping API resources of Data Boxes (Datove schranky), provided by Apitalks.

    References:
        https://www.api.store/datove-schranky/ (in czech language)
    """

    datove_schranky = "/datove-schranky"

    def __init__(self) -> None:
        pass


class HealthServices:
    """Class for mapping API resources of Health Service (Zdravotni sluzby), provided by Apitalks.

    References:
        https://www.api.store/zdravotni-sluzby/ (in czech language)
    """

    zdravotni_sluzby = "/zdravotni-sluzby"

    def __init__(self) -> None:
        pass


class CzechBusinessInspection:
    """Class for mapping API resources of Czech Business Inspection (Ceska obchodni inspekce), provided by Apitalks.

    References:
        https://www.api.store/coi/ (in czech language)
    """

    rizikove_weby = "/coi/rizikove-weby"
    sankce = "/coi/sankce"
    zajisteni = "/coi/zajisteni"
    zakazy = "/coi/zakazy"
    zamereni = "/coi/zamereni"

    def __init__(self) -> None:
        pass


class Schools:
    """Class for mapping API resources of schools provided by Apitalks.

    References:
        https://www.api.store/skoly/ (in czech language)
    """

    skoly = "/skoly"

    def __init__(self) -> None:
        pass


class Jobs:
    """Class for mapping API resources of available jobs provided by Apitalks.

    References:
        https://www.api.store/volna-pracovni-mista/ (in czech language)
    """

    volna_pracovni_mista = "/volna-pracovni-mista"

    def __init__(self) -> None:
        pass


class EmployersInInsolvency:
    """Class for mapping API resources of Employers in Service sector of the economy provided by Apitalks.

    References:
        https://www.api.store/sif/ (in czech language)
    """

    zamestnavatele_v_insolvenci = "/sif"

    def __init__(self) -> None:
        pass


class EuropeanParliament:
    """Class for mapping API resources of European Parliament provided by Apitalks.

    References:
        https://www.api.store/evropsky-parlament/ (in czech language)
    """

    clenove = "/meps"

    def __init__(self) -> None:
        pass


class PublicAuthorities:
    """Class for mapping API resources of public authorities provided by Apitalks.

    References:
        https://www.api.store/organy-verejne-moci/ (in czech language)
    """

    organy_verejne_moci = "/ovm"

    def __init__(self) -> None:
        pass


class PraguePublicTransportation:
    """Class for mapping API resources of Prague public transportation provided by Apitalks.

    References:
        https://www.api.store/prazska-integrovana-doprava/ (in czech language)
    """

    zastavky = "/pid/zastavky"

    def __init__(self) -> None:
        pass


class CzechNationalBank:
    """Class for mapping API resources of Czech National Bank provided by Apitalks.

    References:
        https://www.api.store/cnb.cz/ (in czech language)
    """

    banky_a_zahranicni_pobocky = "/cnb.cz/banky"
    smenarny = "/cnb.cz/smenarny"
    nebankovni_poskytovatele_spotr_uveru = "/cnb.cz/npsu"
    samostatni_poskytovatele_spotr_uveru = "/cnb.cz/szsu"
    vazani_zastupci = "/cnb.cz/vzsu"
    zprostredkovatele_vazaneho_spotr_uveru = "/cnb.cz/zvsu"
    zahr_zprostredkovatele_spotr_uveru = "/cnb.cz/zzsu"

    def __init__(self) -> None:
        pass


class SUKL:
    """Class for mapping API resources of State Institue for Drug Control (SUKL) provided by Apitalks.

    References:
        https://www.api.store/sukl.cz/ (in czech language)
    """

    atc_skupina_lp = "/sukl.cz/dlp-atc"
    cesta_podani_lp = "/sukl.cz/dlp-cesty"
    doping = "/sukl.cz/dlp-doping"
    lekova_forma_lp = "/sukl.cz/dlp-formy"
    indikacni_skupina_lp = "/sukl.cz/dlp-indikacniskupiny"
    jednotka_mnozstvi_latky = "/sukl.cz/dlp-jednotky"
    nazev_latky = "/sukl.cz/dlp-latky"
    nazev_lecive_latky = "/sukl.cz/dlp-lecivelatky"
    lecive_pripravky_lp = "/sukl.cz/dlp-lecivepripravky"
    leky_s_anabolickym_ci_jinym_hormonalnim_ucinkem = "/sukl.cz/dlp-narvla"
    dokumenty_navazane_k_lp = "/sukl.cz/dlp-nazvydokumentu"
    nazev_obalu_lp = "/sukl.cz/dlp-obaly"
    zkratka_drzitel_registrace_vyrobce = "/sukl.cz/dlp-organizace"
    registracni_procedura_lp = "/sukl.cz/dlp-regproc"
    slozeni_lp = "/sukl.cz/dlp-slozeni"
    kod_soli_v_latce = "/sukl.cz/dlp-soli"
    lecebny_program_mzcr = "/sukl.cz/dlp-splp"
    stav_registrace_lp = "/sukl.cz/dlp-stavyreg"
    synonyma_latky_lp = "/sukl.cz/dlp-synonyma"
    priznak_slozeni_lp = "/sukl.cz/dlp-slozenipriznak"
    informace_o_drziteli_prav_lp = "/sukl.cz/dlp-vpois"
    typ_vydeje_lp = "/sukl.cz/dlp-vydej"
    nazev_vyrobce_lp = "/sukl.cz/dlp-vyrobci"
    kategorie_zavislosti_ll = "/sukl.cz/dlp-zavislost"
    nazev_zdroje_lp = "/sukl.cz/dlp-zdroje"
    zeme_vyroby_lp = "/sukl.cz/dlp-zeme"
    dodavky_atc_2016 = "/sukl.cz/dodavky-atc-2016"
    dodavky_atc_2017 = "/sukl.cz/dodavky-atc-2017"
    dodavky_lp_1991_2000 = "/sukl.cz/dodavky-lp-1991-2000"
    dodavky_lp_2001_2010 = "/sukl.cz/dodavky-lp-2001-2010"
    dodavky_atc_2011_2015 = "/sukl.cz/dodavky-lp-2011-2015"
    dodavky_lp_2018 = "/sukl.cz/dodavky-lp-2018"
    ochranne_prvky_ano = "/sukl.cz/ochranne-prvky-ano"
    ochranne_prvky_ne = "/sukl.cz/ochranne-prvky-ne"
    lekarny_seznam = "/sukl.cz/lekarny-seznam"
    lekarny_pracovni_doba = "/sukl.cz/lekarny-prac-doba"
    lekarny_typ = "/sukl.cz/lekarny-typ"

    def __init__(self) -> None:
        pass


class AdminOfLandSurveyingAndCadastre:
    """Class for mapping API resources of State Administration of Land Surveying and Cadastre (CUZSK) provided by Apitalks.

    References:
        https://www.api.store/cuzk.cz/ (in czech language)
    """

    adresni_mista = "/cuzk.cz/adresni-mista-cr"
    adresni_mista_vazby_na_skladebnost = "/cuzk.cz/adresni-mista-vazby-cr"
    vazby_v_cr = "/cuzk.cz/vazby-cr"
    vazby_praha = "/cuzk.cz/vazby-hlm-praha"
    vazby_katastru_na_obce = "/cuzk.cz/vazby-katastr-uzemi-cr"
    vazby_uzemnich_prvku_na_statut_mesta = "/cuzk.cz/vazby-momc-statutarni-mesta"
    vazby_na_puvodni_cleneni_okresu = "/cuzk.cz/vazby-okresy-cr"
    vazby_ulice_obce = "/cuzk.cz/vazby-ulice-obce-s-ulicni-siti"

    def __init__(self) -> None:
        pass


class EET:
    """Class for mapping API resources of Electronic Evidence of Revenue (EET) provided by Apitalks.

    References:
        https://www.api.store/fs.mfcr.cz/ (in czech language)
    """

    eet = "/fs.mfcr.cz/eet"
    ciselnik_cinnosti_provozoven = "/fs.mfcr.cz/ciselnik"

    def __init__(self) -> None:
        pass


class Prague6:
    """Class for mapping API resources of Prague 6 provided by Apitalks.

    References:
        https://www.api.store/praha6.cz/ (in czech language)
    """

    doprava_lokace = "/praha6.cz/traffic/locations"
    typ_vozidla_zjednoduseny = "/praha6.cz/traffic/car-types"
    typ_vozidla_detailni = "/praha6.cz/traffic/car-types-detail"
    kvalita_ovzdusi_lokace = "/praha6.cz/airtracker/locations"
    kvalita_ovzdusi_data = "/praha6.cz/airtracker/data"
    kvalita_ovzdusi_typy_mereni = "/praha6.cz/airtracker/measurement-types"
    kvalita_ovzdusi_jednotky_mereni = "/praha6.cz/airtracker/measurement-units"
    kvalita_ovzdusi_typ_senzoru = "/praha6.cz/airtracker/sensor-types"

    def __init__(self) -> None:
        pass


class AuthoritiesJurisdiction:
    """Class for mapping API resources of authorities territory jurisdiction provided by Apitalks.

    References:
        https://www.api.store/spadovost/ (in czech language)
    """

    spadovost = "/spadovost"

    def __init__(self) -> None:
        pass
