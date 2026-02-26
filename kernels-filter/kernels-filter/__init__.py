# kernels_filter/__init__.py
from jupyter_server.serverapp import ServerApp
from .handlers import FilteringKernelSpecManager

def _jupyter_server_extension_points():
  """
  Metadata for the Jupyter Server extension.
  """
  return [
      {
          "module": "kernels_filter"
      }
  ]

def _load_jupyter_server_extension(server_app: ServerApp):
  """
  Registers the custom KernelSpecManager when the Jupyter Server starts.
  """

  server_app.log.info("[kernels-filter] KernelSpec handler registered")
  server_app.kernel_spec_manager = FilteringKernelSpecManager(
      data_dir=server_app.kernel_spec_manager.data_dir
  )
