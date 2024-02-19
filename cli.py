import aioesphomeapi
import asyncio
import argparse

async def switch_on(api_client: aioesphomeapi.APIClient, object_id: str) -> None:
    entity_key, assumed_state = await get_entity_key_state(api_client, object_id)
    await api_client.switch_command(entity_key, True)

async def switch_off(api_client: aioesphomeapi.APIClient, object_id: str) -> None:
    entity_key, assumed_state = await get_entity_key_state(api_client, object_id)
    await api_client.switch_command(entity_key, False)

async def switch_toggle(api_client: aioesphomeapi.APIClient, object_id: str) -> None:
    entity_key, assumed_state = await get_entity_key_state(api_client, object_id)
    if assumed_state:
        await api_client.switch_command(entity_key, False)
    else:
        await api_client.switch_command(entity_key, True)

async def get_entity_key_state(api_client: aioesphomeapi.APIClient, object_id: str) -> tuple[str, bool]:
    entities, services = await api_client.list_entities_services()
    entity_with_object_id = [e for e in entities if e.object_id == object_id][0]
    # print(entity_with_object_id)
    return entity_with_object_id.key, entity_with_object_id.assumed_state

async def main():
    parser = argparse.ArgumentParser(description='Interact with ESPHome Native API')
    parser.add_argument("address", type=str, help='ESPHome device address (e.g. <device_name>.local)')
    parser.add_argument('object_id', type=str, help='ESPHome API encryption key')
    parser.add_argument('action', type=str, help='ESPHome API encryption key')
    parser.add_argument('--port', dest='port', type=int, default=6053, help='ESPHome API port (default: 6053)')
    parser.add_argument('--password', dest='password', type=str, help='ESPHome API password')
    parser.add_argument('--encryption-key', dest='encryption_key', type=str, help='ESPHome API encryption key')

    args = parser.parse_args()

    # print(args)

    api_client = aioesphomeapi.APIClient(args.address, args.port, args.password, noise_psk=args.encryption_key)
    await api_client.connect(login=True)

    if args.action == "switch_toggle":
        await switch_toggle(api_client, args.object_id)
    elif args.action == "switch_off":
        await switch_off(api_client, args.object_id)
    elif args.action == "switch_on":
        await switch_on(api_client, args.object_id)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())