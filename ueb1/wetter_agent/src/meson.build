pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'wetter_agent')

dependency('libhandy-1', version: '>=1.0.0')

wetter_agent_sources = [
  '__init__.py',
  'application.py',
  'main_window.py',
  'weather_api.py'
]

install_data(wetter_agent_sources, install_dir: moduledir)
