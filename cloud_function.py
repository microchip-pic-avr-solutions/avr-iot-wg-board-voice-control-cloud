from googleapiclient import discovery
import base64


# IMPORTANT: Change these fields to your projects settings
PROJECT_ID = "voice-to-avr"
IOT_CORE_REGION = "europe-west1"
IOT_CORE_REGISTRY_ID = "voice-devices"
IOT_CORE_DEVICE_ID = "d0123DFDAEF65AF85FE"

# Code obtained at https://cloud.google.com
def get_gcloud_client():
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    discovery_url = '{}?version={}'.format(
        discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=None,
        cache_discovery=False)

# Code obtained at https://cloud.google.com
def send_message_to_device(project_id, cloud_region, registry_id, device_id, payload):
    """
    Sends a message to an IoT Device through the config pubsub topic. (Config pubsub is /devices/d_id/config)
    :param project_id: Google Cloud project ID
    :param cloud_region: sWhich region is the device located in. For instance us-central1
    :param registry_id: IoT Core Registry the device is loacted in
    :param device_id: The device ID
    :param payload:
    :return:
    """
    client = get_gcloud_client()
    device_path = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
        project_id, cloud_region, registry_id, device_id)

    config_body = {
        'binaryData': base64.urlsafe_b64encode(
            payload.encode('utf-8')).decode('ascii')
    }

    return client.projects(
    ).locations().registries(
    ).devices().modifyCloudToDeviceConfig(
        name=device_path, body=config_body).execute()

def process_voice(request):
    request_json = request.get_json()
    queryResult = request_json['queryResult']
    parameters = queryResult['parameters']

    number = str(int(parameters['number']))
    payload = '{{"number":"{}"}}'.format(number)
    print("Sent {} to device".format(number))
    send_message_to_device(PROJECT_ID, IOT_CORE_REGION, IOT_CORE_REGISTRY_ID, IOT_CORE_DEVICE_ID, payload)
