# Add all your SQLAlchemy models here.
# This allows us to import just this file when
# we need to preload the models and ensure they
# are all loaded.

# noinspection PyUnresolvedReferences

import src.main.models.session  # pragma: no cover
import src.main.models.project  # pragma: no cover
import src.main.models.data_type  # pragma: no cover
import src.main.models.data_format_file  # pragma: no cover
import src.main.models.mzxml_file  # pragma: no cover
import src.main.models.prototypes.max_quant  # pragma: no cover
import src.main.models.metadata_shipment_file  # pragma: no cover
