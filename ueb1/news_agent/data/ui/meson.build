pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
gnome = import('gnome')

gnome.compile_resources('news_agent',
  'news_agent.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)
