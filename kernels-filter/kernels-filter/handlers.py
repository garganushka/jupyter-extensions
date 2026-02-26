# kernels_filter/handlers.py
import json
from jupyter_client.kernelspec import KernelSpecManager
from jupyter_server.gateway.managers import GatewayKernelSpecManager

class FilteringKernelSpecManager(KernelSpecManager):
  """
  Custom KernelSpecManager that filters remote kernels to return Pyspark/Python Kernels.
  """
  def __init__(self, *args, **kwargs):
    self.log.info("FilteringKernelSpecManager Constructed")
    super().__init__(*args, **kwargs)
    # Initialize the remote manager to fetch kernels from the Dataproc Kernel Mixer
    self.remote_manager = GatewayKernelSpecManager(*args, **kwargs)
    self._remote_kernels = set()
  
  async def get_all_specs(self):
    """
    Fetches all kernels and returns only those where language is 'python'.
    """
    # Fetch all available kernels from the remote gateway
    specs =  await self.remote_manager.get_all_specs()

    filtered_specs = {}
    filtered_out_names = []

    for name, resource in specs.items():
      if resource.get('spec', {}).get('language') == 'python':
        filtered_specs[name] = resource
      else:
        filtered_out_names.append(resource.get('spec', {}).get('display_name', name))

    self.log.info(f"Filtered to {len(filtered_specs)} Python and PySpark kernels.")
    self.log.info(f"Filtered out kernelspecs: {filtered_out_names}")

    return filtered_specs
