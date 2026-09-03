import asyncio
from src.triton_telemetry.core import scan_all_providers

async def main():
    resultados = await scan_all_providers(["AWS", "Azure", "GCP"], timeout=1.5, use_chaos=True)
    for r in resultados:
        print(r)

asyncio.run(main())