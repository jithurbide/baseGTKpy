""" Simple python classe to represent the view of MVC
Author : Julien Ithurbide
Compagny : CPNV
VERSION : 0.1
LAST Modification :

Date       | Exp.
-----------|------------------------------------
18.01.2018 | First version
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango
from datetime import datetime, date


class DialogChangeNotes(Gtk.Dialog):

    def __init__(self, parent, nom, prenom):
        Gtk.Dialog.__init__(self, "Changement de status", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Voulez-vous changer le status de " + nom + " " + prenom)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


# 'engine-started' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))

class View(Gtk.Window):

    __gsignals__ = {
        'button-show-add-student': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'button-clear-notes': (GObject.SIGNAL_RUN_FIRST, None, ()),

        'change-notes-status': (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_INT,GObject.TYPE_STRING,GObject.TYPE_STRING))
    }

    def __init__(self, log, datastore, maj_datastore, nearest,notebook, **kw):

        self.local_date = None
        self.logger = log
        self.logger.debug("View is starting")
        self.data_store = datastore
        self.maj_datastore = maj_datastore
        self.nearest = nearest
        self.notebook = notebook
        self.idSelected = None
        self.Update = False

        Gtk.Window.__init__(self, title="Main Menu",default_width=800, default_height=600)
        #self.fullscreen()
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(5)
        self.grid.set_row_spacing(5)
        self.grid.set_margin_end(15)
        self.grid.set_margin_start(15)
        self.grid.set_margin_top(10)
        self.grid.set_column_homogeneous(True)
        #self.grid.set_row_homogeneous(True)
        self.add(self.grid)
        self.logger.debug("View box started")
        self.time = None

        pangoFont = Pango.FontDescription("Tahoma 40")

        self.label_watch = Gtk.Label(str(self.time))
        self.label_watch.modify_font(pangoFont)
        self.button_date = Gtk.Button(label="Add a Student")
        self.button_date.connect('clicked', self._add_student)

        self.button_exit = Gtk.Button(label="Quitter")
        self.button_exit.connect('clicked', self._quit)

        self.label_majeur = Gtk.Label("Eleves majeurs")
        self.majeur_tree = Gtk.TreeView(model=self.maj_datastore)
        for i, column_title in enumerate(["ID","Nom", "Prenom", "Date"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.majeur_tree.append_column(column)

        self.label_near = Gtk.Label("Eleves majeurs dans mx 2 mois")
        self.nearest_tree = Gtk.TreeView(model=self.nearest)
        for i, column_title in enumerate(["ID", "Nom", "Prenom", "Date"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.nearest_tree.append_column(column)

        self.label_notebook = Gtk.Label("Retour bulletin de notes")
        self.button_clear_notes = Gtk.Button(label="Clear notes")
        self.button_clear_notes.connect('clicked', self._clear)
        self.notebook_tree = Gtk.TreeView(model=self.notebook)
        for i, column_title in enumerate(["ID", "Nom", "Prenom", "Back"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.notebook_tree.append_column(column)

        select = self.notebook_tree.get_selection()
        select.connect("changed", self.on_tree_selection_changed)


        startX = 0
        self.grid.attach(self.label_watch, 2, startX, 1, 1)
        startX+=1
        self.grid.attach(self.button_date, 0, startX, 1, 1)
        startX += 1
        self.grid.attach(self.label_majeur,0,startX,5,1)
        startX += 1
        self.grid.attach(self.majeur_tree, 0, startX, 5, 1)
        startX += 2
        self.grid.attach(self.label_near, 0, startX, 5, 1)
        startX += 1
        self.grid.attach(self.nearest_tree, 0, startX, 5, 1)
        startX += 1
        self.grid.attach(self.label_notebook, 2, startX, 1, 1)
        self.grid.attach(self.button_clear_notes, 3, startX, 1, 1)
        startX += 1
        self.grid.attach(self.notebook_tree, 0, startX, 5, 1)
        startX += 1
        self.grid.attach(self.button_exit, 4,startX,1,1)


        self.update()
        # update the clock once a second
        GObject.timeout_add(1000, self.update)


    def on_tree_selection_changed(self,selection):
        self.logger.debug("obect selectes")
        model, treeiter = selection.get_selected()
        if treeiter is not None and self.Update is False:
            self.logger.debug("obect selectes : "+ str(model[treeiter][0]))
            self.Update = True
            dialog = DialogChangeNotes(self,model[treeiter][2],model[treeiter][1])
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.logger.debug("The OK button was clicked")
                self.emit('change-notes-status',model[treeiter][0],model[treeiter][2],model[treeiter][1])

            dialog.destroy()
            selection.unselect_all()
        else:
            self.Update = False

    def _add_student(self, button, *args):
        self.emit('button-show-add-student')

    def update(self):
        self.time = datetime.now()
        if self.time.hour < 10:
            hourStr = "0"+str(self.time.hour)
        else:
            hourStr = str(self.time.hour)
        if self.time.minute < 10:
            minStr = "0"+str(self.time.minute)
        else:
            minStr = str(self.time.minute)
        if self.time.second < 10:
            secStr = "0"+str(self.time.second)
        else:
            secStr = str(self.time.second)

        self.label_watch.set_text(hourStr + ":" + minStr + ":" + secStr)
        return True  # keep running this event

    def _quit(self, button, *args):
        Gtk.main_quit()
    def _clear(self, button, *args):
        self.emit('button-clear-notes')

class ViewDate(Gtk.Window):

    def __init__(self, log,callback, **kw):
        self.callback = callback
        self.logger = log
        Gtk.Window.__init__(self, title="Main Menu")
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(5)
        self.grid.set_row_spacing(5)
        self.grid.set_margin_end(15)
        self.grid.set_margin_start(15)
        self.grid.set_margin_top(10)

        self.add(self.grid)
        self.date_picker = Gtk.Calendar()
        self.date_picker.select_day(1)
        self.date_picker.select_month(0,2000)


        self.button_cancel = Gtk.Button(label="Annuler")
        self.button_cancel.connect('clicked', self._cancel_on_clicked)

        self.button_ok = Gtk.Button(label="OK")
        self.button_ok.connect('clicked', self._ok_on_clicked)

        self.grid.attach(self.date_picker,0,0,2,1)
        self.grid.attach(self.button_ok, 0, 1, 1, 1)
        self.grid.attach(self.button_cancel, 1, 1, 1, 1)
        self.show_all()

    def _cancel_on_clicked(self, button, *args):
        self.destroy()

    def _ok_on_clicked(self, button, *args):
        self.callback(self.date_picker.get_date())
        self.destroy()


class ViewAddStudent(Gtk.Window):


    __gsignals__ = {
        'button-add-student': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'tree-select-a-student': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'button-update-student': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, log, store, **kw):
        self.local_date = None
