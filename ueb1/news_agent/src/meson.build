pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'news_agent')

dependency('libhandy-1', version: '>=1.0.0')

news_agent_sources = [
  '__init__.py',
  'application.py',
  'main_window.py',
  'news_api.py'
]

install_data(news_agent_sources, install_dir: moduledir)
