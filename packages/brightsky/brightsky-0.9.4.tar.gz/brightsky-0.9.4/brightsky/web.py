import importlib
import sys
from contextlib import contextmanager

import falcon
import falcon_cors
from dateutil.tz import gettz
from gunicorn.app.base import BaseApplication
from gunicorn.util import import_app

from brightsky import query
from brightsky.settings import settings
from brightsky.units import convert_record, CONVERTERS
from brightsky.utils import parse_date


@contextmanager
def convert_exceptions():
    try:
        yield
    except ValueError as e:
        raise falcon.HTTPBadRequest(description=str(e))
    except LookupError as e:
        raise falcon.HTTPNotFound(description=str(e))


class BrightskyResource:

    ALLOWED_UNITS = ['si'] + list(CONVERTERS)

    def parse_location(self, req, required=False):
        lat = req.get_param_as_float(
            'lat', required=required, min_value=-90, max_value=90)
        lon = req.get_param_as_float(
            'lon', required=required, min_value=-180, max_value=180)
        return lat, lon

    def parse_max_dist(self, req):
        return req.get_param_as_int(
            'max_dist', min_value=0, max_value=500000, default=50000)

    def parse_date_range(self, req):
        date_str = req.get_param('date', required=True)
        last_date_str = req.get_param('last_date')
        try:
            date = parse_date(date_str)
            if last_date_str:
                last_date = parse_date(last_date_str)
            else:
                last_date = None
        except ValueError:
            raise falcon.HTTPBadRequest(
                description='Please supply dates in ISO 8601 format')
        return date, last_date

    def parse_timezone(self, req):
        tz_str = req.get_param('tz')
        if not tz_str:
            return
        tz = gettz(tz_str)
        if not tz:
            raise falcon.HTTPBadRequest(
                description='Unknown timezone: %s' % tz_str)
        return tz

    def parse_units(self, req):
        units = req.get_param('units', default='dwd').lower()
        if units not in self.ALLOWED_UNITS:
            raise falcon.HTTPBadRequest(
                description="'units' must be in %s" % (self.ALLOWED_UNITS,))
        return units

    def process_timestamp(self, row, key, timezone):
        if not row[key]:
            return
        if timezone:
            row[key] = row[key].astimezone(timezone)
        row[key] = row[key].isoformat()

    def process_sources(self, sources, timezone=None):
        for source in sources:
            self.process_timestamp(source, 'first_record', timezone)
            self.process_timestamp(source, 'last_record', timezone)


class WeatherResource(BrightskyResource):

    def on_get(self, req, resp):
        date, last_date = self.parse_date_range(req)
        lat, lon = self.parse_location(req)
        dwd_station_id = req.get_param('dwd_station_id')
        wmo_station_id = req.get_param('wmo_station_id')
        # TODO: Remove this fallback on 2020-06-13
        if not wmo_station_id:
            wmo_station_id = req.get_param('station_id')
        source_id = req.get_param_as_int('source_id')
        max_dist = self.parse_max_dist(req)
        timezone = self.parse_timezone(req)
        units = self.parse_units(req)
        if timezone:
            if not date.tzinfo:
                date = date.replace(tzinfo=timezone)
            if last_date and not last_date.tzinfo:
                last_date = last_date.replace(tzinfo=timezone)
        elif date.tzinfo:
            timezone = date.tzinfo
        with convert_exceptions():
            result = self.query(
                date, last_date=last_date, lat=lat, lon=lon,
                dwd_station_id=dwd_station_id, wmo_station_id=wmo_station_id,
                source_id=source_id, max_dist=max_dist)
        self.process_sources(result.get('sources', []))
        for row in result['weather']:
            self.process_row(row, units, timezone)
        resp.media = result

    def query(self, *args, **kwargs):
        return query.weather(*args, **kwargs)

    def process_row(self, row, units, timezone):
        self.process_timestamp(row, 'timestamp', timezone)
        if units != 'si':
            convert_record(row, units)


class CurrentWeatherResource(WeatherResource):

    def on_get(self, req, resp):
        lat, lon = self.parse_location(req)
        dwd_station_id = req.get_param('dwd_station_id')
        wmo_station_id = req.get_param('wmo_station_id')
        source_id = req.get_param_as_int('source_id')
        max_dist = self.parse_max_dist(req)
        timezone = self.parse_timezone(req)
        units = self.parse_units(req)
        with convert_exceptions():
            result = query.current_weather(
                lat=lat, lon=lon, dwd_station_id=dwd_station_id,
                wmo_station_id=wmo_station_id, source_id=source_id,
                max_dist=max_dist)
        self.process_sources(result.get('sources', []))
        self.process_row(result['weather'], units, timezone)
        resp.media = result


class SynopResource(WeatherResource):

    def query(self, *args, **kwargs):
        kwargs.pop('max_dist')
        if any(kwargs.pop(param) for param in ['lat', 'lon']):
            raise falcon.HTTPBadRequest(
                "Querying by lat/lon is not supported for the synop endpoint")
        return query.synop(*args, **kwargs)


class SourcesResource(BrightskyResource):

    def on_get(self, req, resp):
        lat, lon = self.parse_location(req)
        max_dist = self.parse_max_dist(req)
        dwd_station_id = req.get_param('dwd_station_id')
        wmo_station_id = req.get_param('wmo_station_id')
        source_id = req.get_param_as_int('source_id')
        with convert_exceptions():
            result = query.sources(
                lat=lat, lon=lon, dwd_station_id=dwd_station_id,
                wmo_station_id=wmo_station_id, source_id=source_id,
                max_dist=max_dist, ignore_type=True)
        self.process_sources(result.get('sources', []))
        resp.media = result


cors = falcon_cors.CORS(allow_origins_list=settings.CORS_ALLOWED_ORIGINS)

app = falcon.API(middleware=[cors.middleware])
app.add_route('/weather', WeatherResource())
app.add_route('/current_weather', CurrentWeatherResource())
app.add_route('/synop', SynopResource())
app.add_route('/sources', SourcesResource())


class StandaloneApplication(BaseApplication):

    def __init__(self, app_uri, **options):
        self.app_uri = app_uri
        self.options = options
        super().__init__()

    def load_config(self):
        for k, v in self.options.items():
            self.cfg.set(k.lower(), v)

    def load(self):
        brightsky_mods = [
            mod for name, mod in sys.modules.items()
            if name.startswith('brightsky.')]
        for mod in brightsky_mods:
            importlib.reload(mod)
        return import_app(self.app_uri)
