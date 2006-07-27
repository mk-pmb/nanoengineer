# Copyright (c) 2006 Nanorex, Inc.  All rights reserved.
"""
GeneratorBaseClass.py -- base class for generator dialogs or their controllers
which supplies ok/cancel/preview logic and some other common behavior

$Id$
"""

__author__ = "Will"

import platform
import env
from qt import *
from chem import gensym
from Sponsors import SponsorableMixin
from HistoryWidget import redmsg, orangemsg, greenmsg
from debug import print_compact_traceback

_up_arrow_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52" \
    "\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91\x68" \
    "\x36\x00\x00\x00\x06\x62\x4b\x47\x44\x00\xff\x00\xff\x00\xff\xa0" \
    "\xbd\xa7\x93\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0b\x13\x00" \
    "\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07\x74\x49\x4d\x45" \
    "\x07\xd6\x06\x03\x03\x21\x26\xc9\x92\x21\x9b\x00\x00\x00\x10\x74" \
    "\x45\x58\x74\x43\x6f\x6d\x6d\x65\x6e\x74\x00\x4e\x61\x6e\x6f\x74" \
    "\x75\x62\x65\xa3\x8c\x3b\xec\x00\x00\x00\xda\x49\x44\x41\x54\x28" \
    "\xcf\xb5\x92\x41\x0e\x82\x30\x10\x45\x5b\xe3\x01\x24\x14\x69\x39" \
    "\x01\x3d\x83\x6c\x24\xdc\xc0\xb0\x31\x5c\x8f\x78\x8b\x76\x16\x70" \
    "\x95\xb2\x01\x71\xcd\xa2\x75\x51\x6d\x1a\x40\x23\x0b\xff\x6e\x32" \
    "\xef\xb7\x99\x3f\x83\x55\xa7\xd0\x16\xed\xd0\x46\xed\xfd\xa2\x69" \
    "\x9b\x25\x91\x9d\xb2\x75\x43\xd3\x36\xe5\xa5\x5c\x1a\xea\x5b\x9d" \
    "\x9f\x73\x57\x62\x3b\x83\xa5\x87\xfb\xe0\x1a\x24\x24\xfd\xd0\x23" \
    "\x84\xa6\x69\x12\x52\xf0\x94\x33\xc6\xe6\x33\x98\xb7\x48\x48\x00" \
    "\x80\x84\xc4\x18\x63\x5b\xe3\x63\x5c\x19\x5a\x6b\xad\xb5\x8e\x48" \
    "\x04\x00\x08\x21\x00\x88\x48\xf4\x2d\x25\x63\x4c\x7c\x8c\x2d\x6d" \
    "\x05\x00\x09\x4b\x3e\x1a\x68\x4c\x7d\xda\x79\xaa\x6b\xb5\x62\xc0" \
    "\x18\x2f\x69\xe7\x29\xf2\xe2\x55\xa8\x4e\xfd\xbe\x6c\xd5\x29\xec" \
    "\x68\x21\x85\x9f\xb7\x93\x90\x82\x52\x1a\x1c\x02\x1b\x2b\xf6\x9f" \
    "\x17\x52\x2c\x0d\x3e\x3d\x3f\x0d\x9e\x72\x97\xb7\x93\x4f\xcf\x7f" \
    "\xf8\xcb\xb5\x3e\x01\x8d\xb5\x6a\x19\xa6\x37\x6f\xd9\x00\x00\x00" \
    "\x00\x49\x45\x4e\x44\xae\x42\x60\x82"

_down_arrow_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52" \
    "\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91\x68" \
    "\x36\x00\x00\x00\x06\x62\x4b\x47\x44\x00\xff\x00\xff\x00\xff\xa0" \
    "\xbd\xa7\x93\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0b\x13\x00" \
    "\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07\x74\x49\x4d\x45" \
    "\x07\xd6\x06\x03\x03\x29\x2f\x78\x97\x13\x37\x00\x00\x00\x10\x74" \
    "\x45\x58\x74\x43\x6f\x6d\x6d\x65\x6e\x74\x00\x4e\x61\x6e\x6f\x74" \
    "\x75\x62\x65\xa3\x8c\x3b\xec\x00\x00\x00\xba\x49\x44\x41\x54\x28" \
    "\xcf\xb5\x92\x3f\x0e\x82\x30\x14\x87\x8b\x31\xcc\x32\xd9\x72\x02" \
    "\x39\x83\x0c\x3f\xb8\x82\xc2\x09\x41\x2f\x41\x0a\x43\x7b\x95\x52" \
    "\x26\xbc\x41\x1d\x48\xb0\xb6\x40\x64\xf0\x6d\x2f\xfd\xbe\xf4\xfd" \
    "\x0b\x54\xaf\xc8\x9e\x38\x90\x9d\x71\xb4\x13\x21\x85\x4f\xa4\xd7" \
    "\x74\x59\x10\x52\x14\xb7\xc2\x17\xea\x67\x9d\x67\xb9\x2b\xc4\x2c" \
    "\xfe\xa5\x1e\xd5\xab\x60\x6a\x5a\x48\x51\xde\xcb\xae\xeb\xd6\x50" \
    "\x00\x13\xf9\x69\xda\x18\x03\x60\x8d\x6e\x78\xb3\x30\x25\x3d\x68" \
    "\xdf\x01\x50\x3d\xaa\xd5\xb1\x3a\x0e\x00\x63\x4c\x18\x86\x5b\x7b" \
    "\x98\x1d\x00\x7a\xd0\x5b\x7b\xb0\x1d\x7a\xa6\x3e\x4d\x08\x09\xe6" \
    "\xd3\xe0\x2d\xb7\xe7\x3d\x07\x6f\x39\xa5\x34\x3a\x45\x8c\xb1\x2f" \
    "\x61\x7a\xf3\x05\x9b\x76\x4b\x4a\x2e\xc9\xf8\x1a\x1d\xc1\xa6\xdd" \
    "\x1f\xfe\x72\xad\x6f\xd8\xd4\x50\x37\x09\xb5\x93\x63\x00\x00\x00" \
    "\x00\x49\x45\x4e\x44\xae\x42\x60\x82"

class GroupButtonMixin:
    """Mixin class for providing the method toggle_groupbox,
    suitable as part of a slot method for toggling the state of a dialog GroupBox.
    (Current implementation uses open/close icons which look good on Linux and
     Windows but don't look good on the Mac.)
    """
    _up_arrow = QPixmap()
    _up_arrow.loadFromData(_up_arrow_data)
    _down_arrow = QPixmap()
    _down_arrow.loadFromData(_down_arrow_data)

    def toggle_groupbox(self, button, *things):
        """This is intended to be part of the slot method for clicking on an open/close icon
        of a dialog GroupBox. The arguments should be the button (whose icon will be altered here)
        and the child widgets in the groupbox whose visibility should be toggled.
        """
        if things[0].isShown():
            button.setIconSet(QIconSet(self._down_arrow))
            for thing in things:
                thing.hide()
        else:
            button.setIconSet(QIconSet(self._up_arrow))
            for thing in things:
                thing.show()

class AbstractMethod(Exception):
    def __init__(self):
        Exception.__init__(self, 'Abstract method - must be overloaded')

class CadBug(Exception):
    """Useful for distinguishing between an exception from subclass
    code which is a bug in the cad, a report of an error in the
    plugin, or a report of a user error.
    """
    def __init__(self, arg=None):
        if arg is not None:
            Exception.__init__(self, arg)
        else:
            Exception.__init__(self)

class PluginBug(Exception):
    """Useful for distinguishing between an exception from subclass
    code which is a bug in the cad, a report of an error in the
    plugin, or a report of a user error.
    """
    def __init__(self, arg=None):
        if arg is not None:
            Exception.__init__(self, arg)
        else:
            Exception.__init__(self)

class UserError(Exception):
    """Useful for distinguishing between an exception from subclass
    code which is a bug in the cad, a report of an error in the
    plugin, or a report of a user error.
    """
    def __init__(self, arg=None):
        if arg is not None:
            Exception.__init__(self, arg)
        else:
            Exception.__init__(self)

class GeneratorBaseClass(GroupButtonMixin, SponsorableMixin):
    """There is some logic associated with Preview/OK/Abort that's
    complicated enough to put it in one place, so that individual
    generators can focus on what they need to do. As much as possible,
    the individual generator should not need to worry about the GUI.
       Note: this superclass sets and maintains some attributes in self,
    including win, struct, previousParams, and name.
       Here are the things a subclass needs to do, to be usable with this superclass [as of 060621]:
    - have self.sponsor_btn, a Qt button of a suitable class.
    - bind or delegate button clicks from a generator dialog's standard buttons
      to all our xxx_btn_clicked methods (not sure about sponsor_btn). ###@@@
    - implement the abstract methods (see their docstrings herein for what they need to do):
      - gather_parameters
      - build_struct
    - have self.prefix, apparently used to construct node names (or, override self._create_new_name())
    - either inherit from QDialog, or provide methods accept and reject which have the same effect on the actual dialog.
    There are some other methods here that merit mentioning: 
    enter_WhatsThisMode, whatsthis_btn_clicked, done_btn_clicked,
    abort_btn_clicked, cancel_btn_clicked, close
    """
    cmd = "" # deprecated but widely used [bruce 060616 comment]
        # (subclasses often set cmd to greenmsg(self.cmdname + ": "), from which we have to klugily deduce self.cmdname! Ugh.)
    cmdname = "" # subclasses should set this to their (undecorated) command name for use by Undo and history. [bruce 060616 new feature]

    # pass window arg to constructor rather than use a global, wware 051103
    def __init__(self, win):
        self.win = win
        self.struct = None
        self.previousParams = None
        #bruce 060616 added the following kluge to make sure both cmdname and cmd are set properly.
        if not self.cmdname and not self.cmd:
            self.cmdname = "Generate something"
        if self.cmd and not self.cmdname:
            # deprecated but common, as of 060616
            self.cmdname = self.cmd # fallback
            try:
                cmdname = self.cmd.split('>')[1]
                cmdname = cmdname.split('<')[0]
                cmdname = cmdname.split(':')[0]
                self.cmdname = cmdname
            except:
                if platform.atom_debug:
                    print "fyi: %r guessed wrong about format of self.cmd == %r" % (self, self.cmd,)
                pass
        elif self.cmdname and not self.cmd:
            # this is intended to be the usual situation, but isn't yet, as of 060616
            self.cmd = greenmsg(self.cmdname + ": ")

    def build_struct(self, name, params, position):
        """Build the structure (model object) in question. This is an abstract method
        and must be overloaded in the specific generator.
           The argument will be the parameter tuple returned from self.gather_parameters().
        The return value should be the new structure, i.e. some flavor of a Node,
        which has not yet been added to the model. Its structure should depend only on
        the values of the passed params, since if the user asks to build twice, this may
        not be called if the params have not changed.
           By convention (and to fit with history messages emitted from this class),
        the new node's name should be set to self.name,
        which the caller will have set to self.prefix appended with a serial number.
        """
        raise AbstractMethod()

    def remove_struct(self):
        if platform.atom_debug: print 'Should we remove an existing structure?'
        if self.struct != None:
            if platform.atom_debug: print 'Yes, remove it'
            self.struct.kill()
            self.struct = None
            self.win.win_update() # includes mt_update
        else:
            if platform.atom_debug: print 'No structure to remove'

    def preview_btn_clicked(self):
        if platform.atom_debug: print 'preview button clicked'
        self._ok_or_preview(previewing=True)

    def ok_btn_clicked(self):
        'Slot for the OK button'
        if platform.atom_debug: print 'ok button clicked'
        self._ok_or_preview(doneMsg=True)
        if not self.pluginException:
            # if there was a (UserError, CadBug, PluginBug) then behave
            # like preview button - do not close the dialog
            self.accept() #bruce 060621
        self.struct = None
        return

    def handlePluginExceptions(self, thunk):
        self.pluginException = False
        try:
            return thunk()
        except CadBug, e:
            env.history.message(redmsg("Bug in the CAD system: " + " - ".join(map(str, e.args))))
            self.remove_struct()
            self.pluginException = True
        except PluginBug, e:
            env.history.message(redmsg("Bug in the plug-in: " + " - ".join(map(str, e.args))))
            self.remove_struct()
            self.pluginException = True
        except UserError, e:
            env.history.message(redmsg("User error: " + " - ".join(map(str, e.args))))
            self.remove_struct()
            self.pluginException = True
        except Exception, e:
            env.history.message(self.cmd + redmsg(" - ".join(map(str, e.args))))
            self.remove_struct()

    def _ok_or_preview(self, doneMsg=False, previewing=False):
        QApplication.setOverrideCursor( QCursor(Qt.WaitCursor) )
        self.win.assy.current_command_info(cmdname = self.cmdname) #bruce 060616
        def thunk():
            self._build_struct(previewing=previewing)
            if doneMsg:
                env.history.message(self.cmd + self.done_msg())
        self.handlePluginExceptions(thunk)
        QApplication.restoreOverrideCursor() # Restore the cursor
        self.win.win_update()

    def gather_parameters(self):
        '''Return a tuple of the current parameters. This is an
        abstract method and must be overloaded in the specific
        generator. This method must validate the parameters, or
        raise an exception if they are invalid.'''
        raise AbstractMethod()

    def done_msg(self):
        '''Tell what message to print when the structure has been
        built. This may be overloaded in the specific generator.
        '''
        return "%s created." % self.name

    def _revert_number(self):
        import chem, Utility
        if hasattr(self, '_Gno'):
            chem.Gno = self._Gno
        if hasattr(self, '_ViewNum'):
            Utility.ViewNum = self._ViewNum

    def _build_struct(self, previewing=False):
        if platform.atom_debug:
            print '_build_struct'
        params = self.gather_parameters()

        import chem, Utility
        if self.struct == None:
            if platform.atom_debug:
                print 'no old structure, we are making a new structure'
            self._Gno = chem.Gno
        elif params != self.previousParams:
            if platform.atom_debug:
                print 'parameters have changed, update existing structure'
            self._revert_number()
            # fall through, using old name
        else:
            if platform.atom_debug:
                print 'old structure, parameters same as previous, do nothing'
            return

        self.name = name = gensym(self.prefix)
        # self.name needed for done message
        if previewing:
            env.history.message(self.cmd + "Previewing " + name)
        else:
            env.history.message(self.cmd + "Creating " + name)
        self.remove_struct()
        self.previousParams = params
        if platform.atom_debug: print 'build a new structure'
        self.struct = self.build_struct(name, params, -self.win.glpane.pov)
        self.win.assy.addnode(self.struct)
	# Do this if you want it centered on the previous center.
        # self.win.glpane.setViewFitToWindow(fast=True)
	# Do this if you want it centered on the origin.
        self.win.glpane.setViewRecenter(fast=True)
        self.win.win_update() # includes mt_update

    def enter_WhatsThisMode(self):
        'Slot for the What\'s This button'
        QWhatsThis.enterWhatsThisMode()

    def whatsthis_btn_clicked(self):
        'Slot for the What\'s This button'
        QWhatsThis.enterWhatsThisMode()
    
    def done_btn_clicked(self):
        'Slot for the Done button'
        if platform.atom_debug: print 'done button clicked'
        self.ok_btn_clicked()

    def abort_btn_clicked(self):
        'Slot for the Abort button'
        self.cancel_btn_clicked()

    def cancel_btn_clicked(self):
        'Slot for the Cancel button'
        if platform.atom_debug: print 'cancel button clicked'
        self.win.assy.current_command_info(cmdname = self.cmdname + " (Cancel)") #bruce 060616
        self.remove_struct()
        self._revert_number()
        ## QDialog.accept(self)
        self.reject() #bruce 060621
        return

    def close(self, e=None):
        """When the user closes the dialog by clicking the 'X' button
        on the dialog title bar, do whatever the cancel button does.
        """
        # Note: Qt wants the return value of .close to be of the correct type, apparently boolean;
        # it may mean whether to really close (guess) [bruce 060719 comment]
        try:
            self.cancel_btn_clicked()
            return True
        except:
            if 1:
                #bruce 060719: adding this print, since an exception here is either an intentional one
                # defined in this file (and should be reported as an error in history -- if this happens
                # we need to fix this code to do that, maybe like _ok_or_preview does), or is a bug.
                # Not printing anything here would always hide important info, whether errors or bugs.
                print_compact_traceback("bug in cancel_btn_clicked or in not reporting an error it detected: ")
            return False
        
    pass # end of class GeneratorBaseClass

# end
