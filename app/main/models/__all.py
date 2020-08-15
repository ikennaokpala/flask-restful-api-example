# Add all your SQLAlchemy models here.
# This allows us to import just this file when
# we need to preload the models and ensure they
# are all loaded.

# noinspection PyUnresolvedReferences

import app.main.models.session  # pragma: no cover
import app.main.models.project  # pragma: no cover
import app.main.models.data_type  # pragma: no cover
import app.main.models.data_format_file  # pragma: no cover
import app.main.models.mzxml_file  # pragma: no cover
import app.main.models.metadata_shipment_file  # pragma: no cover
