# Copyright 2004-2007 Nanorex, Inc.  See LICENSE file for details. 
"""
DnaDuplexPropertyManager.py

@author: Mark Sims
@version: $Id$
@copyright: 2004-2007 Nanorex, Inc.  See LICENSE file for details.

Mark 2007-10-18: 
- Created. Major rewrite of DnaGeneratorPropertyManager.py.

Ninad 2007-10-24:
- Another major rewrite to a) use EditController_PM superclass and b) Implement
feature to generate Dna using endpoints of a line.
"""

__author__ = "Mark"

import env

from Dna_Constants import getDuplexRise, getDuplexLength

from utilities.Log import redmsg ##, greenmsg, orangemsg

from PyQt4.Qt import SIGNAL
from PyQt4.Qt import Qt
from PyQt4.Qt import QAction

from PM.PM_ComboBox      import PM_ComboBox
from PM.PM_DoubleSpinBox import PM_DoubleSpinBox
from PM.PM_GroupBox      import PM_GroupBox
from PM.PM_SpinBox       import PM_SpinBox
from PM.PM_LineEdit      import PM_LineEdit
from PM.PM_ToolButton    import PM_ToolButton
from PM.PM_PushButton    import PM_PushButton
from PM.PM_SelectionListWidget import PM_SelectionListWidget

from DebugMenuMixin import DebugMenuMixin
from EditController_PM import EditController_PM
from VQT import V

from PM.PM_Constants     import pmDoneButton
from PM.PM_Constants     import pmWhatsThisButton
from PM.PM_Constants     import pmCancelButton
from PM.PM_Constants     import pmPreviewButton

from PM.PM_Colors        import pmReferencesListWidgetColor
from utilities.Comparison import same_vals


class DnaDuplexPropertyManager( EditController_PM, DebugMenuMixin ):
    """
    The DnaDuplexPropertyManager class provides a Property Manager 
    for the B{Build > DNA > Duplex} command.

    @ivar title: The title that appears in the property manager header.
    @type title: str

    @ivar pmName: The name of this property manager. This is used to set
                  the name of the PM_Dialog object via setObjectName().
    @type name: str

    @ivar iconPath: The relative path to the PNG file that contains a
                    22 x 22 icon image that appears in the PM header.
    @type iconPath: str
    """

    title         =  "Insert DNA Duplex"
    pmName        =  title
    iconPath      =  "ui/actions/Tools/Build Structures/Duplex.png"

    _conformation  = "B-DNA"
    _numberOfBases = 0
    _basesPerTurn  = 10.0
    _duplexRise    = getDuplexRise(_conformation)
    _duplexLength  = getDuplexLength(_conformation, _numberOfBases)

    endPoint1 = None
    endPoint2 = None 
    #For model changed signal
    previousSelectionParams = None

    def __init__( self, win, editController ):
        """
        Constructor for the DNA Duplex property manager.
        """
        EditController_PM.__init__( self, 
                                    win,
                                    editController)


        DebugMenuMixin._init1( self )

        self.showTopRowButtons( pmDoneButton | \
                                pmCancelButton | \
                                pmPreviewButton| \
                                pmWhatsThisButton)
    
    def connect_or_disconnect_signals(self, isConnect):
        """
        Connect or disconnect widget signals sent to their slot methods.
        This can be overridden in subclasses. By default it does nothing.
        @param isConnect: If True the widget will send the signals to the slot 
                          method. 
        @type  isConnect: boolean
        """
        if isConnect:
            change_connect = self.win.connect
        else:
            change_connect = self.win.disconnect 
        
        
        EditController_PM.connect_or_disconnect_signals(self, isConnect)
        
        self.strandListWidget.connect_or_disconnect_signals(isConnect)
        
        change_connect( self.conformationComboBox,
                      SIGNAL("currentIndexChanged(int)"),
                      self.conformationComboBoxChanged )
        
        change_connect( self.numberOfBasePairsSpinBox,
                      SIGNAL("valueChanged(int)"),
                      self.numberOfBasesChanged )
        
        change_connect(self.specifyDnaLineButton, 
                     SIGNAL("toggled(bool)"), 
                     self.editController.enterDnaLineMode)
    
    def model_changed(self):
        """
        NOT IMPLEMENTED YET. This needs commandSequencer to treat various 
        edit controllers as commands. Until then, the 'model_changed' method 
        (and thus this method) will  never be called.
        
        When the editcontroller is treated as a 'command' by the 
        commandSequencer. this method will override basicCommand.model_changed.
        
        @WARNING: Ideally this property manager should implement both
               model_changed and selection_changed methods in the mode/command
               API. 
               model_changed method will be used here when the selected atom is 
               dragged, transmuted etc. The selection_changed method will be 
               used when the selection (picking/ unpicking) changes. 
               At present, selection_changed and model_changed methods are 
               called too frequently that it doesn't matter which one you use. 
               Its better to use only a single method for preformance reasons 
               (at the moment). This should change when the original 
               methods in the API are revised to be called at appropiraite 
               time. 
        """  
        newSelectionParams = self._currentSelectionParams()
        
        if same_vals(newSelectionParams, self.previousSelectionParams):
            return
        
        self.previousSelectionParams = newSelectionParams   
        #subclasses of BuildAtomsPM may not define self.selectedAtomPosGroupBox
        #so do the following check.
        if newSelectionParams[0]:            
            self.editStrandPropertiesButton.setEnabled(True) 
        else:
            self.editStrandPropertiesButton.setEnabled(False) 
            
    
    def _currentSelectionParams(self):
        """
        NOT CALLED YET. This needs commandSequencer to treat various 
        edit controllers as commands. Until then, the 'model_changed' method 
        (and thus this method) will  never be called.
        
        Returns a tuple containing current selection parameters. These 
        parameters are then used to decide whether updating widgets
        in this property manager is needed when L{self.model_changed} or 
        L{self.selection_changed} methods are called. 
        @return: A tuple that contains following selection parameters
                   - Total number of selected atoms (int)
                   - Selected Atom if a single atom is selected, else None
                   - Position vector of the single selected atom or None
        @rtype:  tuple
        @NOTE: The method name may be renamed in future. 
        Its possible that there are other groupboxes in the PM that need to be 
        updated when something changes in the glpane.        
        """
         
        selectedStrands = self.strandListWidget.selectedItems()
        
        if len(selectedStrands) == 1: 
            #self.win.assy.selatoms_list() is same as 
            # selectedAtomsDictionary.values() except that it is a sorted list 
            #it doesn't matter in this case, but a useful info if we decide 
            # we need a sorted list for multiple atoms in future. 
            # -- ninad 2007-09-27 (comment based on Bruce's code review)
            
            return (selectedStrands[0])
        else: 
            return (None)
    
    def close(self):
        """
        Closes the Property Manager. Overrided EditController_PM.close()
        """
        #Clear tags, if any, due to the selection in the self.strandListWidget.
        if self.strandListWidget:
            self.strandListWidget.clearTags()
                        
        EditController_PM.close(self)
    

    def getFlyoutActionList(self): 
        """ returns custom actionlist that will be used in a specific mode 
	or editing a feature etc Example: while in movie mode, 
	the _createFlyoutToolBar method calls
	this """	


        #'allActionsList' returns all actions in the flyout toolbar 
        #including the subcontrolArea actions
        allActionsList = []

        #Action List for  subcontrol Area buttons. 
        #In this mode there is really no subcontrol area. 
        #We will treat subcontrol area same as 'command area' 
        #(subcontrol area buttons will have an empty list as their command area 
        #list). We will set  the Comamnd Area palette background color to the
        #subcontrol area.

        subControlAreaActionList =[] 

        self.exitEditControllerAction.setChecked(True)
        subControlAreaActionList.append(self.exitEditControllerAction)

        separator = QAction(self.w)
        separator.setSeparator(True)
        subControlAreaActionList.append(separator) 


        allActionsList.extend(subControlAreaActionList)

        #Empty actionlist for the 'Command Area'
        commandActionLists = [] 

        #Append empty 'lists' in 'commandActionLists equal to the 
        #number of actions in subControlArea 
        for i in range(len(subControlAreaActionList)):
            lst = []
            commandActionLists.append(lst)

        params = (subControlAreaActionList, commandActionLists, allActionsList)

        return params

    def _addGroupBoxes( self ):
        """
        Add the DNA Property Manager group boxes.
        """
        
        #Unused 'References List Box' to be revided. (just commented out for the
        #time being. 
        ##self._pmGroupBox1 = PM_GroupBox( self, title = "Reference Plane" )
        ##self._loadGroupBox1( self._pmGroupBox1 )
        
        self._pmGroupBox2 = PM_GroupBox( self, title = "Strands" )
        self._loadGroupBox2( self._pmGroupBox2 )
        
        self._pmGroupBox3 = PM_GroupBox( self, title = "Parameters" )
        self._loadGroupBox3( self._pmGroupBox3 )

        self._pmGroupBox4 = PM_GroupBox( self, title = "Endpoints" )
        self._loadGroupBox4( self._pmGroupBox4 )
    
    def _loadGroupBox1(self, pmGroupBox):
        """
        load widgets in groupbox1
        """
        self.referencePlaneListWidget = PM_SelectionListWidget(
            pmGroupBox,
            self.win,
            label = "",
            color = pmReferencesListWidgetColor,
            heightByRows = 2)
    
    def _loadGroupBox2(self, pmGroupBox):
        """
        load widgets in groupbox2
        """
        #TODO: Following list widget will be a part of the default PM of 
        #DNA Mode and not a part of DnaDuplx PM, this is work in progress, 
        #to be revised soon (once dna object model is implemented)
        # -- Ninad 2007-11-12
        self.strandListWidget = PM_SelectionListWidget(pmGroupBox,
                                                       self.win,
                                                       label = "",
                                                       heightByRows = 4 )
        self.strandListWidget.setTagInstruction('TAG_AND_PICK_ITEM_IN_GLPANE')
    
        self.editStrandPropertiesButton = PM_PushButton( 
            pmGroupBox,
            label = "",
            text  = "Edit Properties..." )
        self.editStrandPropertiesButton.setEnabled(False)
        

    def _loadGroupBox3(self, pmGroupBox):
        """
        Load widgets in group box 3.
        """

        self.conformationComboBox  = \
            PM_ComboBox( pmGroupBox,
                         label         =  "Conformation :", 
                         choices       =  ["B-DNA"],
                         setAsDefault  =  True)

        
        
        dnaModelChoices = ['PAM-3', 'PAM-5']
        self.dnaModelComboBox = \
            PM_ComboBox( pmGroupBox,     
                         label         =  "Model :", 
                         choices       =  dnaModelChoices,
                         setAsDefault  =  True)
                                            
        # Strand Length (i.e. the number of bases)
        self.numberOfBasePairsSpinBox = \
            PM_SpinBox( pmGroupBox, 
                        label         =  "Base Pairs :", 
                        value         =  self._numberOfBases,
                        setAsDefault  =  False,
                        minimum       =  0,
                        maximum       =  10000 )

        
        self.basesPerTurnDoubleSpinBox  =  \
            PM_DoubleSpinBox( pmGroupBox,
                              label         =  "Bases Per Turn :",
                              value         =  self._basesPerTurn,
                              setAsDefault  =  True,
                              minimum       =  8.0,
                              maximum       =  20.0,
                              decimals      =  2,
                              singleStep    =  0.1 )

        # Duplex Length
        self.duplexLengthLineEdit  =  \
            PM_LineEdit( pmGroupBox,
                         label         =  "Duplex Length: ",
                         text          =  "0.0 Angstroms",
                         setAsDefault  =  False)

        self.duplexLengthLineEdit.setDisabled(True)        

    def _loadGroupBox4(self, pmGroupBox):
        """
        Load widgets in group box 4.
        """
        #Folllowing toolbutton facilitates entering a temporary DnaLineMode
        #to create a DNA using endpoints of the specified line. 
        self.specifyDnaLineButton = PM_ToolButton(
            pmGroupBox, 
            text = "Specify Endpoints",
            iconPath  = "ui/actions/Properties Manager"\
            "/Pencil.png",
            spanWidth = True                        
        )
        self.specifyDnaLineButton.setCheckable(True)
        self.specifyDnaLineButton.setAutoRaise(True)
        self.specifyDnaLineButton.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon)

        self._endPoint1GroupBox = PM_GroupBox( pmGroupBox, title = "Endpoint1" )
        self._endPoint2GroupBox = PM_GroupBox( pmGroupBox, title = "Endpoint2" )
        
        
        # Point 1
        self.x1SpinBox  =  \
            PM_DoubleSpinBox( self._endPoint1GroupBox,
                              label         =  \
                              "ui/actions/Properties Manager/X_Coordinate.png",
                              value         =  0,
                              setAsDefault  =  True,
                              minimum       =  -100.0,
                              maximum       =   100.0,
                              decimals      =  3,
                              suffix        =  ' Angstroms')

        self.y1SpinBox  =  \
            PM_DoubleSpinBox( self._endPoint1GroupBox,
                              label         =  \
                              "ui/actions/Properties Manager/Y_Coordinate.png",
                              value         =  0,
                              setAsDefault  =  True,
                              minimum       =  -100.0,
                              maximum       =   100.0,
                              decimals      =  3,
                              suffix        =  ' Angstroms')

        self.z1SpinBox  =  \
            PM_DoubleSpinBox( self._endPoint1GroupBox,
                              label         =  \
                              "ui/actions/Properties Manager/Z_Coordinate.png",
                              value         =  0,
                              setAsDefault  =  True,
                              minimum       =  -100.0,
                              maximum       =   100.0,
                              decimals      =  3,
                              suffix        =  ' Angstroms')

        # Point 2
        self.x2SpinBox  =  \
            PM_DoubleSpinBox( self._endPoint2GroupBox,
                              label         =  \
                              "ui/actions/Properties Manager/X_Coordinate.png",
                              value         =  10.0,
                              setAsDefault  =  True,
                              minimum       =  -100.0,
                              maximum       =   100.0,
                              decimals      =  3,
                              suffix        =  ' Angstroms')

        self.y2SpinBox  =  \
            PM_DoubleSpinBox( self._endPoint2GroupBox,
                              label         =  \
                              "ui/actions/Properties Manager/Y_Coordinate.png",
                              value         =  0,
                              setAsDefault  =  True,
                              minimum       =  -100.0,
                              maximum       =   100.0,
                              decimals      =  3,
                              suffix        =  ' Angstroms')

        self.z2SpinBox  =  \
            PM_DoubleSpinBox( self._endPoint2GroupBox,
                              label         =  \
                              "ui/actions/Properties Manager/Z_Coordinate.png",
                              value         =  0,
                              setAsDefault  =  True,
                              minimum       =  -100.0,
                              maximum       =   100.0,
                              decimals      =  3,
                              suffix        =  ' Angstroms')

    def _addWhatsThisText( self ):
        """
        What's This text for some of the widgets in the 
        DNA Property Manager.  

        @note: Many PM widgets are still missing their "What's This" text.
        """
        txt_conformationComboBox = "<b>Conformation</b> <p>DNA exists in "\
                                 "several possible conformations, with A-DNA, "\
                                 "B-DNA, and Z-DNA being the most common. <br>"\
                                 "Only B-DNA is currently supported in "\
                                 "NanoEngineer-1.</p>"
        self.conformationComboBox.setWhatsThis(txt_conformationComboBox)

    def conformationComboBoxChanged( self, inIndex ):
        """
        Slot for the Conformation combobox. It is called whenever the
        Conformation choice is changed.

        @param inIndex: The new index.
        @type  inIndex: int
        """
        conformation  =  self.conformationComboBox.currentText()

        if conformation == "B-DNA":
            self.basesPerTurnDoubleSpinBox.setValue("10.0")

        elif conformation == "Z-DNA":
            self.basesPerTurnDoubleSpinBox.setValue("12.0")

        else:
            msg = redmsg("conformationComboBoxChanged(): \
                         Error - unknown DNA conformation. Index = "+ inIndex)
            env.history.message(msg)

        self.duplexLengthSpinBox.setSingleStep(getDuplexRise(conformation))

    def numberOfBasesChanged( self, numberOfBases ):
        """
        Slot for the B{Number of Bases" spinbox.
        """
        # Update the Duplex Length lineEdit widget.
        text = str(getDuplexLength(self._conformation, numberOfBases)) \
             + " Angstroms"
        self.duplexLengthLineEdit.setText(text)
        return

    def getParameters(self):
        """
        Return the parameters from this property manager
        to be used to create the DNA duplex. 
        @return: A tuple containing the parameters
        @rtype: tuple
        @see: L{DnaDuplexEditController._gatherParameters} where this is used 
        """
        numberOfBases = self.numberOfBasePairsSpinBox.value()
        dnaForm  = str(self.conformationComboBox.currentText())
        basesPerTurn = self.basesPerTurnDoubleSpinBox.value()
        
        dnaModel = str(self.dnaModelComboBox.currentText())

        # First endpoint (origin) of DNA duplex
        x1 = self.x1SpinBox.value()
        y1 = self.y1SpinBox.value()
        z1 = self.z1SpinBox.value()

        # Second endpoint (direction vector/axis) of DNA duplex.
        x2 = self.x2SpinBox.value()
        y2 = self.y2SpinBox.value()
        z2 = self.z2SpinBox.value()

        if not self.endPoint1:
            self.endPoint1 = V(x1, y1, z1)
        if not self.endPoint2:
            self.endPoint2 = V(x2, y2, z2)

        return (numberOfBases, 
                dnaForm,
                dnaModel,
                basesPerTurn,
                self.endPoint1, 
                self.endPoint2)

    def updateCommandManager(self, bool_entering = True):
        """
	Update the command manager flyout toolbar 
	"""
        #self.win.buildDnaAction is the action in Build menu in the control 
        # area. So when the Build button is checked, the command manager will 
        # show a custom flyout toolbar. 
        # Note to Eric M:
        # This needs cleanup. It's a temporary implementation --ninad20071025

        action = self.win.buildDnaAction

        obj = self  	    	    
        self.win.commandManager.updateCommandManager(action,
                                                     obj, 
                                                     entering =bool_entering)
