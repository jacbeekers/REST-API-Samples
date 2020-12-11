from src.edc_utilities import edc_lineage
from src.metadata_utilities import messages, generic_settings, mu_logging


def test_generate_lineage():
    settings = generic_settings.GenericSettings()
    result = settings.get_config()
    mu_log = settings.mu_log

    edc_test = edc_lineage.EDCLineage(settings=settings, mu_log_ref=mu_log)
    edc_test.update_formulas(entity_type="physical_attribute_association", data=edc_test.data, settings=settings)
    assert 0
