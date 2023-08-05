
from epyk.core import html
from epyk.core.css import Defaults_css


class Navigation(object):
  def __init__(self, context):
    self.context = context

  def up(self, icon="fas fa-arrow-up", top=20, right=20, bottom=None, tooltip=None, width=(100, '%'), options=None, profile=False):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.navigation.up()

    Attributes:
    ----------
    :param icon:
    :param top:
    :param right:
    :param bottom:
    :param tooltip:
    :param width:
    :param options:
    :param profile:
    """
    du = self.context.rptObj.ui.icon(icon).css({"border": '1px solid black', "position": 'fixed', "width": 'none',
                                                "border-radius": '20px', "padding": '8px', "right": '%spx' % right})
    if top is not None:
      du.style.css.top = top
    else:
      du.style.css.bottom = bottom
    du.style.add_classes.div.background_hover()
    self.context.rptObj.js.onReady(
      self.context.rptObj.js.window.events.addScrollListener([
        self.context.rptObj.js.if_(self.context.rptObj.js.window.scrollY > 50, [du.dom.show()]).else_(du.dom.hide())
      ]))
    if tooltip is not None:
      du.tooltip(tooltip)
    du.click([
      self.context.rptObj.js.window.scrollUp(),
      self.context.rptObj.js.objects.this.hide()])
    return du

  def down(self, icon="fas fa-arrow-down", top=20, right=20, bottom=None, tooltip=None, width=(100, '%'), options=None, profile=False):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.navigation.down()

    Attributes:
    ----------
    :param icon:
    :param top:
    :param right:
    :param bottom:
    :param tooltip:
    :param width:
    :param options:
    :param profile:
    """
    dd = self.context.rptObj.ui.icon(icon).css({"border": '1px solid black', "position": 'fixed', "width": 'none',
        "border-radius": '20px', "padding": '8px', "right": '%spx' % right})
    if bottom is not None:
      dd.style.css.bottom = bottom
    else:
      dd.style.css.top = top
    dd.style.add_classes.div.background_hover()
    self.context.rptObj.js.onReady(
      self.context.rptObj.js.window.events.addScrollListener([
        self.context.rptObj.js.if_(self.context.rptObj.js.window.scrollY < (self.context.rptObj.js.window.scrollMaxY - 50), [dd.dom.show()]).else_(dd.dom.hide())
      ]))
    if tooltip is not None:
      dd.tooltip(tooltip)
    dd.click([
      self.context.rptObj.js.window.scrollTo(),
      self.context.rptObj.js.objects.this.hide()])
    return dd

  def to(self, y, x=None, icon="fas fa-map-pin", top=20, right=20, bottom=None, tooltip=None, width=(100, '%'), options=None, profile=False):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.navigation.to(100, tooltip="test")

    Attributes:
    ----------
    :param y:
    :param x:
    :param icon:
    :param top:
    :param right:
    :param bottom:
    :param tooltip:
    :param width:
    :param options:
    :param profile:
    """
    dd = self.context.rptObj.ui.icon(icon).css({"border": '1px solid black', "position": 'fixed', "width": 'none',
                                                "border-radius": '20px', "padding": '8px', "right": '%spx' % right})
    if bottom is not None:
      dd.style.css.bottom = bottom
    else:
      dd.style.css.top = top
    dd.style.add_classes.div.background_hover()
    if tooltip is not None:
      dd.tooltip(tooltip)
    self.context.rptObj.js.onReady(
      self.context.rptObj.js.window.events.addScrollListener([
        self.context.rptObj.js.if_(self.context.rptObj.js.window.scrollY > y, [dd.dom.show()]).else_(dd.dom.hide())
      ]))
    dd.click([
      self.context.rptObj.js.window.scrollTo(x=x, y=y),
      self.context.rptObj.js.objects.this.hide()])
    return dd

  def pin(self, text, url="#", icon="fas fa-map-pin", top=20, right=20, bottom=None, tooltip=None, width=(100, '%'), options=None, profile=False):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.navigation.pin("anchor", tooltip="test", bottom=20)

    Attributes:
    ----------
    :param text:
    :param url:
    :param icon:
    :param top:
    :param right:
    :param bottom:
    :param tooltip:
    :param width:
    :param options:
    :param profile:
    """
    dd = self.context.rptObj.ui.icon(icon)
    h_url = self.context.rptObj.ui.link(text, url=url).css({"margin-left": "10px"})
    div = self.context.rptObj.ui.div([dd, h_url]).css({"border": '1px solid black', "position": 'fixed', "width": 'none',
                          "border-radius": '30px', "padding": '10px 15px', "right": '%spx' % right,
                          "background-color": self.context.rptObj.theme.greys[0]})
    if bottom is not None:
      div.style.css.bottom = bottom
    else:
      div.style.css.top = top
    div.attr['class'].add("CssDivOnHoverWidth")
    h_url.css({"display": 'none', "white-space": 'nowrap'})
    div.on("mouseover", [h_url.dom.css({"display": 'inline-block'})])
    div.on("mouseout", [h_url.dom.css({"display": 'none'})])
    if tooltip is not None:
      div.tooltip(tooltip)
    return div

  def scroll(self, position=0, height=(3, 'px'), options=None, profile=False):
    """
    Description:
    ------------
    Add a horizontal progressbar to display the status of the page scrollbar.

    Usage::

      rptObj.ui.navigation.scroll()

    Attributes:
    ----------
    :param position:
    :param height:
    :param options:
    :param profile:
    """
    p = self.context.rptObj.ui.sliders.progressbar(position, height=height, options=options, profile=profile)
    self.context.rptObj.js.onReady(
      self.context.rptObj.js.window.events.addScrollListener([
        p.build(self.context.rptObj.js.window.scrollPercentage)]))
    return p

  def indices(self, count, selected=1, width=(100, '%'), height=(None, 'px'), options=None, profile=False):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.navigation.indices(10)

    Attributes:
    ----------
    :param count:
    :param selected:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    dflt_options = {"div_css": {"display": "inline-block", "margin": "0 2px"}, "selected": selected}
    dflt_options.update(options or {})
    html_indices = html.HtmlContainer.Indices(self.context.rptObj, count, width, height, None, dflt_options, profile)
    return html_indices

  def points(self, count, selected=0, width=(100, '%'), height=(None, 'px'), options=None, profile=False):
    """
    Description:
    ------------

    Usage::

      p = rptObj.ui.navigation.points(10)
      for i, _ in enumerate(p):
        p.click_item(i, [])

    Attributes:
    ----------
    :param count:
    :param selected:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    dflt_options = {"div_css": {"display": "inline-block", "margin": "0 2px"}, "selected": selected}
    dflt_options.update(options or {})
    html_points = html.HtmlContainer.Points(self.context.rptObj, count, width, height, None, dflt_options, profile)
    return html_points

  def dots(self, count, selected=1, position="right", width=(100, '%'), height=(None, 'px'), options=None,
           profile=False):
    """
    Description:
    ------------

    Usage::

      d = rptObj.ui.navigation.dots(10)

    Attributes:
    ----------
    :param count:
    :param selected:
    :param position:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    dflt_options = {"div_css": {"margin": "2px", "float": position}, "selected": selected}
    dflt_options.update(options or {})
    html_points = html.HtmlContainer.Points(self.context.rptObj, count, width, height, None, dflt_options, profile)
    return html_points

  def path(self, records, divider=None, width=(100, '%'), height=(None, 'px'), options=None, profile=False):
    """
    Description:
    ------------

    Usage::

      record = [{"text": "Lin 1", 'url': 'report_list.html'}, {"text": "Link 2"}]
      rptObj.ui.navigation.path(record)

    Attributes:
    ----------
    :param records:
    :param divider:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    if divider is None:
      divider = self.context.rptObj.symbols.shapes.BLACK_RIGHT_POINTING_TRIANGLE
    div = self.context.rptObj.ui.div(width=width, height=height, options=options, profile=profile)
    for rec in records[:-1]:
      div += self.context.rptObj.ui.link(rec['text'], url=rec.get('url', '#')).css({"display": 'inline-block'})
      div += self.context.rptObj.ui.text(divider).css({"display": 'inline-block', 'margin': '0 5px', 'font-size': Defaults_css.font(-2)})
    div +=self.context.rptObj.ui.link(records[-1]['text'], url=records[-1].get('url', '#')).css({"display": 'inline-block'})
    return div

  def bar(self, icon=None, title=None, width=(100, '%'), height=(40, 'px'), options=None, profile=False):
    """
    Description:
    ------------

    Usage::

      nav = rptObj.ui.navigation.bar(title="test")
      nav.add_text("Test text")
      nav + rptObj.ui.button("Click")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlMenu.HtmlNavBar`


    Attributes:
    ----------
    :param icon:
    :param title:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    components = []
    if icon is None:
      components.append(self.context.rptObj.ui.icons.epyk())
    if title is not None:
      title = self.context.rptObj.ui.div(title, height=(100, "%"))
      title.style.css.text_transform = "uppercase"
      title.style.css.margin_left = 5
      title.style.css.margin_right = 5
      title.style.css.bold()
      components.append(title)
    scroll = self.context.rptObj.ui.navigation.scroll()
    scroll_height = 5
    scroll.style.css.display = "block"
    scroll.options.managed = False
    scroll.style.css.height = scroll_height
    html_nav = html.HtmlMenu.HtmlNavBar(self.context.rptObj, components, width=width, height=height, options=options, profile=profile)
    html_nav.scroll = scroll
    html_nav.style.css.line_height = height[0]
    self.context.rptObj.body.style.css.padding_top = height[0] + scroll_height + 5
    return html_nav

  def banner(self, image, text, link, width=(100, '%'), height=(None, 'px'), options=None, profile=False):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlContainer.Div`
      - :class:`epyk.core.html.HtmlImage.Image`
      - :class:`epyk.core.html.HtmlContainer.Col`
      - :class:`epyk.core.html.HtmlContainer.Row`
      - :class:`epyk.core.html.HtmlText.Text`
      - :class:`epyk.core.html.HtmlLinks.ExternalLink`

    Attributes:
    ----------
    :param image:
    :param text:
    :param link:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    div = self.context.rptObj.ui.div(width=width, height=height, options=options, profile=profile)
    h_image = self.context.rptObj.ui.img(image)
    h_text = self.context.rptObj.ui.text(text)
    h_link = self.context.rptObj.ui.links.button("click", link)
    h_row = self.context.rptObj.ui.row(
      [h_image, self.context.rptObj.ui.col([h_text, h_link])])
    div + h_row
    div.style.css.background_color = self.context.rptObj.theme.colors[3]
    div.style.css.color = "white"
    div.style.css.font_size = Defaults_css.font(5)
    div.style.css.text_align = 'center'
    div.style.css.padding = "5px 15px"
    return div

  def footer(self, components=None, width=(100, '%'), height=('80', 'px'), profile=False):
    """
    Description:
    ------------

    Will create a footer object in the body of the report

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlMenu.HtmlFooter`

    Attributes:
    ----------
    :param components: list of html components
    :param width: the width of the object
    :param height: the height of the object
    :param profile: get profiling info
    """
    footer = html.HtmlMenu.HtmlFooter(self.context.rptObj, components, width=width, height=height, profile=profile)
    return footer

  def side(self, components=None, anchor=None, size=262, position='right', profile=False):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param components:
    :param anchor:
    :param size:
    :param position:
    :param profile:
    """
    d = self.context.rptObj.ui.div(components)
    d.css({"background": self.context.rptObj.theme.colors[2], "position": 'absolute', 'top': 0, 'height': '100%',
           'overflow-x': 'hidden', 'width': "%spx" % size, 'z-index': 20})
    if position == 'left':
      d.css({'left': 0, 'margin-left': "-%spx" % size, 'border-right': '1px solid %s' % self.context.rptObj.theme.colors[5], 'padding': '5px'})
    else:
      d.css({'right': 0, 'margin-right': "-%spx" % size, 'border-left': '1px solid %s' % self.context.rptObj.theme.colors[5], 'padding': '5px'})
    self.context.rptObj.body.style.css.overflow_x = 'hidden'
    if anchor is None:
      if position == 'left':
        i = self.context.rptObj.ui.icon("fas fa-bars").click([d.dom.toggle_transition("margin-left", "0px", "-%spx" % size)])
        i.style.css.float = 'right'
      else:
        i = self.context.rptObj.ui.icon("fas fa-bars").click([d.dom.toggle_transition("margin-right", "0px", "-%spx" % size)])
      i.css({"padding": '5px'})
    else:
      if position == 'left':
        anchor.click([d.dom.toggle_transition("margin-left", "0px", "-%spx" % size)])
      else:
        anchor.click([d.dom.toggle_transition("margin-right", "0px", "-%spx" % size)])
    return d

  def pilcrow(self):
    """
    Description:
    ------------
    Add an anchor on the page and move to this when it is clicked
    """
    p = self.context.rptObj.ui.div("&#182")
    p.style.css.font_size = Defaults_css.font(5)
    p.style.css.cursor = "pointer"
    p.click([self.context.rptObj.js.window.scrollTo(y=self.context.rptObj.js.objects.this.offsetTop)])
    return p

  def panel(self, width=(100, '%'), height=(100, '%'), options=None, profile=None, helper=None):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param options: Optional. A dictionary with the components properties
    :param profile: Optional. A flag to set the component performance storage
    :param helper:
    """
    dflt_options = {"position": 'top'}
    if options is not None:
      dflt_options.update(options)
    h_drawer = html.HtmlMenu.PanelsBar(self.context.rptObj, width, height, dflt_options, helper, profile)
    return h_drawer

  def shortcut(self, components=None, logo=None, size=(40, 'px'), options=None, profile=None, htmlCode=None):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param components:
    :param logo:
    :param size:
    :param options:
    :param profile:
    :param htmlCode:
    """
    dflt_options = {"position": 'left'}
    if options is not None:
      dflt_options.update(options)

    if dflt_options["position"] in ['top', 'bottom']:
      width = (100, '%')
      height = size
    else:
      width = size
      height = (100, '%')
    h_drawer = html.HtmlMenu.Shortcut(self.context.rptObj, components or [], logo, width, height, htmlCode, dflt_options, profile)
    return h_drawer


class Banners(object):

  def __init__(self, context):
    self.context = context

  def top(self, data, background=None, width=(100, '%'), height=(None, 'px'), options=None, profile=False):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlContainer.Div`

    Attributes:
    ----------
    :param data:
    :param background:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    div = self.context.rptObj.ui.div(data, width=width, height=height, options=options, profile=profile)
    div.style.css.background_color = background or self.context.rptObj.theme.colors[3]
    div.style.css.color = "white"
    div.style.css.position = "fixed"
    div.style.css.top = 0
    div.style.css.padding = "5px 15px"
    return div

  def bottom(self, data, background=None, width=(100, '%'), height=(None, 'px'), options=None, profile=False):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlContainer.Div`

    Attributes:
    ----------
    :param data:
    :param background:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    div = self.context.rptObj.ui.div(data, width=width, height=height, options=options, profile=profile)
    div.style.css.background_color = background or self.context.rptObj.theme.colors[3]
    div.style.css.color = "white"
    div.style.css.position = "fixed"
    div.style.css.padding = "5px 15px"
    div.style.css.bottom = 0
    return div

  def corner(self, data, background=None, position="bottom", width=(120, 'px'), height=(None, 'px'), options=None, profile=False):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlContainer.Div`

    Attributes:
    ----------
    :param data:
    :param background:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    div = self.context.rptObj.ui.div(data, width=width, height=height, options=options, profile=profile)
    div.style.css.background_color = background or self.context.rptObj.theme.colors[3]
    div.style.css.color = "white"
    div.style.css.position = "fixed"
    div.style.css.padding = "5px 15px"
    div.style.css.text_align = "center"
    div.style.css.right = 0
    if position == 'bottom':
      div.style.css.bottom = 0
      div.style.css.transform = "rotate(-40deg)"
      div.style.css.margin = "0 -30px 15px 0"
    else:
      div.style.css.top = 0
      div.style.css.transform = "rotate(40deg)"
      div.style.css.margin = "15px -30px 0 0"
    return div
