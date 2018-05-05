""" Simple python classe to represent the controller of MVC
https://bitbucket.org/NGY_CPNV/teacherplanner
Author : Julien Ithurbide
Compagny : CPNV
VERSION : 0.1
LAST Modification :

Date       | Exp.
-----------|------------------------------------
07.02.2017 | First version
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from database import DataBase
from log import Log
from view import View, ViewAddStudent
from datetime import datetime, date


class Controller:

    def __init__(self):
        self.view_student = None
        self.finded_students = None
        self.logger = Log().get_logger()
        self.logger.debug("Controller is starting")
        self.logger.debug("Controller start database")
        self._database = DataBase(self.logger)

        self.logger.debug("Controller start view")


        self._view = View(self.logger,self.student_data_store,self.majeur_data_store,self.nearest_data_store,self.notebook_data_store )
        self._view.connect('button-show-add-student', self.show_add_student_win)

        #'button-clear'

        self._view.connect('destroy', Gtk.main_quit)
        self._view.show_all()


    def __del__(self):
        self.logger.debug("Controlleris deleted")
        self.newClass = None
        self.database = None
        self.menu = None

