import jupyter_telemetry.eventlog


class EventLog(jupyter_telemetry.eventlog.EventLog):

    def register_event_model(self, event):
        """Register schemas from pydantic Model objects.

        events : list of pydantic Model objects.
        """
        if not issubclass(event, pydantic.BaseModel):
            raise TypeError("event must be a subclass of pydantic.BaseModel.")
        self.register_schema(event.schema())

    def record_event_model(self, event):
        """Record given event with schema has occurred.

        event: pydantic BaseModel.
        """
        if not issubclass(event.__class__, pydantic.BaseModel):
            raise TypeError('Must be a subclass of pydantic.BaseModel.')
        
        # Get extra args from pydantics's Config inner class.
        version = event.Config.schema_extra['version']
        schema_id = event.Config.schema_extra['$id']
        # Get Event data as dict (ugly hack)
        capsule = json.loads(event.json())

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
