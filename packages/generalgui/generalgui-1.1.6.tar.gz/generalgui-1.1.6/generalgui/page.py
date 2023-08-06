"""App for generalgui, controls Frame"""

from generallibrary.types import typeChecker

from generalgui.shared_methods.element_page import Element_Page
from generalgui.shared_methods.element_page_app import Element_Page_App
from generalgui.shared_methods.page_app import Page_App


class Page(Element_Page, Element_Page_App, Page_App):
    """
    Controls one tkinter Frame and adds a lot of convenient features.
    Hidden by default.
    """
    def __init__(self, parentPage, removeSiblings=False, vsb=False, hsb=False, pack=False, scrollable=False, mouseScroll=True, resizeable=False, **parameters):
        """
        Create a new page that is hidden by default and controls one frame. Becomes scrollable if width or height is defined.

        :param App or Page or None parentPage: Parent page, can be App, Page or None (Creates new App).
        :param removeSiblings: Remove all siblings on creations, to easily update a page for example by replacing it.
        :param None or int width: Width in pixels
        :param None or int height: Width in pixels
        :param vsb: Vertical scrollbar if page is scrollable.
        :param hsb: Horiziontal scrollbar if page is scrollable
        :param packParameters: Parameters given to page's tkinter Frame when being packed.
        """
        Element_Page_App.__init__(self)

        typeChecker(parentPage, (Page, "App"))

        if removeSiblings:
            parentPage.removeChildren()

        self.parentPage = parentPage
        self.vsb = vsb
        self.hsb = hsb
        self.scrollable = scrollable or vsb or hsb
        self.mouseScroll = mouseScroll
        self.resizable = resizeable
        self.parameters = parameters

        if typeChecker(parentPage, "App", error=False):
            self.parentPart = parentPage
        else:
            self.parentPart = parentPage.baseElement

        self.app = parentPage.app
        self.baseElement = None
        self.topElement = None
        self.frame = self.app.Frame(self, pack=False, makeBase=True, resizeable=resizeable, **parameters)


        if "width" in parameters or "height" in parameters:
            self.frame.widget.pack_propagate(0)

        if self.scrollable:
            self.canvas = self.app.Canvas(self, pack=False, fill="both", side="left", expand=True, bd=-2)
            self.canvas.widget.pack_propagate(0)  # Not sure why we need it

            if self.vsb:
                self.vsb = self.app.Scrollbar(self, orient="vertical", command=self.canvas.widget.yview, side="right", fill="y")
                self.canvas.widgetConfig(yscrollcommand=self.vsb.widget.set)
            if self.hsb:
                self.hsb = self.app.Scrollbar(self, orient="horizontal", command=self.canvas.widget.xview, side="bottom", fill="x")
                self.canvas.widgetConfig(xscrollcommand=self.hsb.widget.set)

            self.canvas.pack()
            self.canvas.makeBase()

            self.canvasFrame = self.app.Frame(self, pack=False, makeBase=True, padx=2, pady=2)
            self.canvas.widget.create_window(0, 0, window=self.canvasFrame.widget, anchor="nw")

            def _canvasConfigure(_):
                self.canvas.widgetConfig(scrollregion=self.canvas.widget.bbox("all"))

            self.canvasFrame.createBind("<Configure>", _canvasConfigure)

            self.canvas.widgetConfig(yscrollincrement="1")
            self.canvas.widgetConfig(xscrollincrement="1")

        if pack:
            self.pack()

    def __repr__(self):
        return f"{self.__class__.__name__}: [{self.topElement}]"













































