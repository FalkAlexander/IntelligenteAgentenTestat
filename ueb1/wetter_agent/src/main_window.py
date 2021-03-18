from gi.repository import Gdk, Gtk, GObject, Handy
from .weather_api import WeatherAPI


@Gtk.Template(resource_path="/de/falsei/ueb1wetter/main_window.ui")
class MainWindow(Handy.ApplicationWindow):
    __gtype_name__ = "main_window"
    
    weather_api = NotImplemented

    main_box = Gtk.Template.Child()
    refresh_button = Gtk.Template.Child()
    location_button = Gtk.Template.Child()
    location_search_entry = Gtk.Template.Child()
    
    weather_page = NotImplemented
    
    mobile_layout = GObject.Property(
        type=bool, default=False, flags=GObject.ParamFlags.READWRITE)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.application = self.get_application()
        self.weather_api = WeatherAPI()
        
        self.assemble_window()
        self.connect_signals()
    
    def assemble_window(self):
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/de/falsei/ueb1wetter/custom.css")
        context = self.get_style_context()
        context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)


        status_page = StatusPage()
        self.main_box.add(status_page)
    
    def connect_signals(self):
        self.location_search_entry.connect("activate", self.__on_location_search_entry_enter_pressed)
    
    def invoke_weather_page(self, weather_page=None):
        self.weather_page = weather_page
  
        if len(self.main_box.get_children()) > 0:
            for widget in self.main_box.get_children():
                if widget.get_name() != "status_page" and widget.get_name() != "weather_page":
                    continue

                self.main_box.remove(widget)
                break

        self.show_weather_page()
    
    def show_weather_page(self):
        if self.weather_page is None:
            return
        
        self.main_box.add(self.weather_page)
    
    #
    # Signals
    #

    def __on_location_search_entry_enter_pressed(self, search_entry):
        city_name = search_entry.get_text()
        weather_page = WeatherPage(weather_api=self.weather_api, 
                                   city_name=city_name)
        
        self.invoke_weather_page(weather_page)
        


@Gtk.Template(resource_path="/de/falsei/ueb1wetter/status_page.ui")
class StatusPage(Handy.StatusPage):
    __gtype_name__ = "status_page"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@Gtk.Template(resource_path="/de/falsei/ueb1wetter/weather_page.ui")
class WeatherPage(Gtk.Grid):
    __gtype_name__ = "weather_page"
    
    weather_api = NotImplemented
    city_name = ""
    
    forecast_data = NotImplemented
    
    city_name_label = Gtk.Template.Child()
    forecast_data_list_box = Gtk.Template.Child()

    temperature_label = Gtk.Template.Child()
    sky_label = Gtk.Template.Child()
    wind_speed_label = Gtk.Template.Child()
    sunrise_label = Gtk.Template.Child()
    sunset_label = Gtk.Template.Child()

    def __init__(self, weather_api=None, city_name="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.weather_api = weather_api
        self.city_name = city_name

        self.request_forecast_data()
        self.assemble_page()

    def request_forecast_data(self):
        self.forecast_data = self.weather_api.get_current_forecast(self.city_name)
    
    def assemble_page(self):
        self.__set_city_name_label()
        self.__set_list_box_attributes()
            
    def __set_city_name_label(self):
        city_name = self.weather_api.get_forecast_attribute_by_name(self.forecast_data, "city_name")
        self.city_name_label.set_text(city_name)
        print(self.temperature_label)
    
    def __set_list_box_attributes(self):
        temperature = str(self.weather_api.get_forecast_attribute_by_name(self.forecast_data, "temp"))
        self.temperature_label.set_text(temperature + " °C")
        
        sky = self.weather_api.get_forecast_attribute_by_name(self.forecast_data, "weather").get("description")
        self.sky_label.set_text(sky)
        
        wind_speed = str(self.weather_api.get_forecast_attribute_by_name(self.forecast_data, "wind_spd"))
        self.wind_speed_label.set_text(wind_speed + " m/s")
        
        sunrise = str(self.weather_api.get_forecast_attribute_by_name(self.forecast_data, "sunrise"))
        self.sunrise_label.set_text(sunrise)
        
        sunset = str(self.weather_api.get_forecast_attribute_by_name(self.forecast_data, "sunset"))
        self.sunset_label.set_text(sunset)        

