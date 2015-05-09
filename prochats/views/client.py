# -*- coding: utf-8 -*-
import datetime

from .. import db, app
from ..models.client import ClientLocation, Client, ClientDevice
from .rendering import to_json, get_renderer
from .validators import (
    accept,
    param_string,
    param_client,
    param_float,
    param_int,
    param_sdk_token,
)


renderer = get_renderer()


@app.route("/client/initiate", methods=["POST"])
@to_json
@accept(param_sdk_token(),
        param_string('client_id'),
        param_string('device.device_id', forward='device_id'),
        param_string('device.platform', forward='device_platform'),
        param_string('device.type', forward='device_type'),
        param_string('device.version', forward='device_vesion'))
def initiate_client(application, client_id, device_id, device_platform, device_type, device_vesion):
    client = Client.query.filter_by(client_id=client_id).first()
    if not client:
        client = Client(client_id=client_id)
        db.session.add(client)
        db.session.commit()

    client_device = ClientDevice(
        device_id=device_id,
        client_id=client.id,
        platform=device_platform,
        type=device_type,
        version=device_vesion
    )
    db.session.add(client_device)
    db.session.commit()
    return renderer.client_info(client)


@app.route("/client/location", methods=["POST"])
@to_json
@accept(param_sdk_token(),
        param_client(methods=['json']),
        param_float('location.latitude', methods=['json'], forward='latitude'),
        param_float('location.longitude', methods=['json'], forward='longitude'),
        param_int('timestamp', methods=['json']))
def update_location(application, client, latitude, longitude, timestamp):
    client_location = ClientLocation(
        client_id=client.id,
        latitude=latitude,
        longitude=longitude,
        create_date=datetime.datetime.fromtimestamp(timestamp)
    )
    db.session.add(client_location)
    db.session.commit()
    return renderer.status('ok')


@app.route("/client/advertisements")
@to_json
@accept(param_sdk_token(), param_client(methods=['get']))
def get_client_advertisements(application, client):
    client_tags = client.tags
    advertisements = [] # TODO: get ads
    return renderer.advertisements(advertisements)
