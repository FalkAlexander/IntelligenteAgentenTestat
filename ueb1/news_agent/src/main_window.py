from gi.repository import Gdk, Gtk, GObject, Handy
from .news_api import NewsAPI


@Gtk.Template(resource_path="/de/falsei/ueb1news/main_window.ui")
class MainWindow(Handy.ApplicationWindow):
    __gtype_name__ = "main_window"
    
    news_api = NotImplemented

    main_box = Gtk.Template.Child()
    categories_list_box = Gtk.Template.Child()
    
    news_page = NotImplemented
    
    mobile_layout = GObject.Property(
        type=bool, default=False, flags=GObject.ParamFlags.READWRITE)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.application = self.get_application()
        self.news_api = NewsAPI()

        self.assemble_window()
        self.connect_signals()
    
    def assemble_window(self):
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/de/falsei/ueb1news/custom.css")
        context = self.get_style_context()
        context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)


        status_page = StatusPage()
        self.main_box.add(status_page)
        self.populate_categories_list_box()
    
    def connect_signals(self):
        self.categories_list_box.connect("row-activated", self.__on_category_row_activated)
    
    def populate_categories_list_box(self):
        categories = self.news_api.get_news_categories()
        
        for category in categories:
            news_category_list_box_row = NewsCategoryListBoxRow(category_name=category, category_link=categories.get(category))
            self.categories_list_box.add(news_category_list_box_row)
        
        self.categories_list_box.show_all()
    
    def invoke_news_page(self, news_page=None):
        if news_page is not None:
            self.news_page = news_page
  
        if len(self.main_box.get_children()) > 0:
            for widget in self.main_box.get_children():
                if widget.get_name() != "status_page" and widget.get_name() != "news_page":
                    continue

                self.main_box.remove(widget)
                break

        self.show_news_page()
    
    def show_news_page(self):
        if self.news_page is None:
            return
        
        self.main_box.add(self.news_page)
    
    #
    # Signals
    #

    def __on_category_row_activated(self, list_box, list_box_row):
        self.news_page = NewsPage(self.news_api, category_name=list_box_row.category_name, category_link=list_box_row.category_link)
        self.invoke_news_page()


@Gtk.Template(resource_path="/de/falsei/ueb1news/news_category_list_box_row.ui")
class NewsCategoryListBoxRow(Gtk.ListBoxRow):
    __gtype_name__ = "news_category_list_box_row"
    
    category_name = ""
    category_link = ""

    news_category_label = Gtk.Template.Child()


    def __init__(self, category_name="", category_link="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.category_name = category_name
        self.category_link = category_link
        
        self.assemble_widget()
    
    def assemble_widget(self):
        self.news_category_label.set_text(self.category_name)
        

@Gtk.Template(resource_path="/de/falsei/ueb1news/status_page.ui")
class StatusPage(Handy.StatusPage):
    __gtype_name__ = "status_page"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@Gtk.Template(resource_path="/de/falsei/ueb1news/news_page.ui")
class NewsPage(Gtk.Grid):
    __gtype_name__ = "news_page"
    
    news_api = NotImplemented
    category_name = ""
    
    category_link = NotImplemented
    news_data = NotImplemented
    
    category_name_label = Gtk.Template.Child()
    news_list_box = Gtk.Template.Child()


    def __init__(self, news_api=None, category_name="", category_link="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.news_api = news_api
        self.category_name = category_name
        self.category_link = category_link

        self.request_news_data()
        self.assemble_page()

    def request_news_data(self):
        self.news_data = self.news_api.get_category_news(self.category_link)
    
    def assemble_page(self):
        self.__set_category_name_label()
        self.populate_news_headlines()
        
        self.news_list_box.connect("row-activated", self.__on_category_row_activated)
            
    def __set_category_name_label(self):
        self.category_name_label.set_text(self.category_name)
    
    def populate_news_headlines(self):
        for row in self.news_list_box.get_children():
            self.news_list_box.remove(row)

        for headline in self.news_data:
            news_topline = self.news_data.get(headline)[0]
            news_headline = self.news_data.get(headline)[1]
            news_link = headline

            news_topline_list_box_row = NewsToplineListBoxRow(news_topline=news_topline, 
                                                              news_headline=news_headline, 
                                                              news_link=news_link)
            
            self.news_list_box.add(news_topline_list_box_row)
    
    def __on_category_row_activated(self, list_box, list_box_row):
        article_text = self.news_api.get_article_text(list_box_row.news_link)
        article_window = ArticleWindow(topline=list_box_row.news_topline, headline=list_box_row.news_headline, article_text=article_text)


@Gtk.Template(resource_path="/de/falsei/ueb1news/news_topline_list_box_row.ui")
class NewsToplineListBoxRow(Gtk.ListBoxRow):
    __gtype_name__ = "news_topline_list_box_row"
    
    news_topline = ""
    news_headline = ""
    news_link = ""

    news_topline_label = Gtk.Template.Child()
    news_headline_label = Gtk.Template.Child()


    def __init__(self, news_topline="", news_headline="", news_link="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.news_topline = news_topline
        self.news_headline = news_headline
        self.news_link = news_link
        
        self.assemble_widget()
    
    def assemble_widget(self):
        self.news_topline_label.set_text(self.news_topline)
        self.news_headline_label.set_text(self.news_headline)

@Gtk.Template(resource_path="/de/falsei/ueb1news/article_page.ui")
class ArticleWindow(Handy.Window):
    __gtype_name__ = "article_window"
    
    topline = ""
    headline = ""
    article_text = ""

    article_header_bar = Gtk.Template.Child()
    article_buffer = Gtk.Template.Child()


    def __init__(self, topline="", headline="", article_text="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.topline = topline
        self.headline = headline
        self.article_text = article_text
        self.assemble_window()
    
    def assemble_window(self):
        self.set_title(self.topline)

        self.article_header_bar.set_title(self.topline)
        self.article_header_bar.set_subtitle(self.headline)

        self.article_buffer.insert_at_cursor(self.article_text)
        self.show()

