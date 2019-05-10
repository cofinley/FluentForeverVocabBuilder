import os
from tkinter import *

from PIL import ImageTk, Image
from google_images_download import google_images_download

import config as cfg

cwd = os.getcwd()


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class Gallery(VerticalScrolledFrame):
    def __init__(self, parent, query, *args, **kw):
        VerticalScrolledFrame.__init__(self, parent, *args, **kw)
        self.query = query
        self.checkboxes = []
        self.create()

    def download_images(self):
        response = google_images_download.googleimagesdownload()  # class instantiation

        paths = response.download({
            "keywords": self.query,
            "language": cfg.GOOGLE_IMAGES_LANGUAGE,
            "output_directory": "temp",
            "limit": cfg.NUM_GOOGLE_IMAGES,
            "format": "jpg"
        })

        for path in paths[self.query]:
            filename = os.path.splitext(path)[0]
            ext = os.path.splitext(path)[1]

            save_filename = filename + ".save" + ext
            image_to_save = Image.open(path)
            image_to_save.thumbnail(cfg.MAX_IMAGE_SIZE, Image.ANTIALIAS)
            image_to_save.save(save_filename, format=image_to_save.format)

        return paths[self.query]

    def create(self):
        paths = self.download_images()

        self.pack()

        thumb_paths = self.generate_thumbnails(paths)
        self.draw_images(thumb_paths)

    def generate_thumbnails(self, image_paths):
        thumbs = []
        for path in image_paths:
            filename = os.path.splitext(path)[0]
            ext = os.path.splitext(path)[1]

            thumb_filename = filename + ".thumb" + ext
            thumbnail_img = Image.open(path)
            thumbnail_img.thumbnail(cfg.THUMBNAIL_SIZE, Image.ANTIALIAS)
            thumbnail_img.save(thumb_filename, format=thumbnail_img.format)
            thumbs.append(thumb_filename)
        return thumbs

    def draw_images(self, image_paths):
        for i, image in enumerate(image_paths):
            img = ImageTk.PhotoImage(Image.open(image))
            var = StringVar()
            cb = Checkbutton(self.interior, variable=var, image=img, compound="left", onvalue=image, offvalue="0")
            var.set("0")
            self.checkboxes.append(var)
            cb.image = img
            cb.pack()

    def get_selected(self):
        selected = []
        for cb in self.checkboxes:
            val = cb.get()
            if "0" != val:
                image_filename = val.replace(".thumb.", ".save.")
                selected.append(image_filename)
        return selected

