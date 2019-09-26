import json
from datetime import datetime
from traitlets import Bool

import jupyter_telemetry.eventlog
import pydantic

class EventLog(jupyter_telemetry.eventlog.EventLog):

    include_pii = Bool(
        False,
        config=True
    )

    def register_event_model(self, event):
        """Register schemas from pydantic Model objects.

        events : list of pydantic Model objects.
        """
        if not issubclass(event, pydantic.BaseModel):
            raise TypeError("event must be a subclass of pydantic.BaseModel.")
        self.register_schema(event.schema())

    def filter_pii(self, event_model):
        """Filter out and PII data.
        """
        schema = event_model.schema()
        properties = schema['properties']
        capsule = json.loads(event_model.json())

        # Filter PII if it's allowed.
        for key in properties:
            is_pii = properties[key]['pii']
            if is_pii and not self.include_pii:
                del capsule[key]

        return capsule
        
    def record_event_model(self, event):
        """Record given event with schema has occurred.

        event: pydantic BaseModel.
        """
        if not issubclass(event.__class__, pydantic.BaseModel):
            raise TypeError('Must be a subclass of pydantic.BaseModel.')
        
        # Get extra args from pydantics's Config inner class.
        version = event.Config.schema_extra['version']
        schema_id = event.Config.schema_extra['$id']

        # Get a capsule.
        capsule = self.filter_pii(event)
        if not (self.handlers and schema_id in self.allowed_schemas):
            # if handler isn't set up or schema is not explicitly whitelisted,
            # don't do anything
            return

        if (schema_id, version) not in self.schemas:
            raise ValueError('Schema {schema_id} version {version} not registered'.format(
                schema_id=schema_id, version=version
            ))

        capsule.update({
            '__timestamp__': datetime.utcnow().isoformat() + 'Z',
            '__schema__': schema_id,
            '__version__': version
        })
        self.log.info(capsule)
