# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/huaicai/atom/cad/src/ElementSelectorDialog.ui'
#
# Created: Thu Mar 10 13:13:25 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.12
#
# WARNING! All changes made in this file will be lost!


from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
    "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x01" \
    "\x1c\x49\x44\x41\x54\x78\x9c\xed\x93\xb1\x6a\xc2" \
    "\x40\x18\xc7\x7f\x57\x1c\xa5\x8b\x53\x9e\xa1\x4d" \
    "\xe7\x82\xef\x50\x28\xb7\x95\x0e\x82\xd0\x9b\xe2" \
    "\x52\xc8\xa6\x64\x72\x28\x74\xca\x74\x0e\xe2\x20" \
    "\x2e\x0e\x85\xbe\x43\x8e\x2c\x72\xd2\xb4\xe2\xe6" \
    "\xe2\x13\xf4\x05\xec\x10\x12\x92\x96\x48\x89\x38" \
    "\x54\xfa\x9b\xbe\xbb\x3f\xf7\xdd\xf1\xe3\x3e\x61" \
    "\x8c\xe1\x18\x34\xea\x1e\x54\x4a\xed\xaa\x32\xad" \
    "\xb5\x38\xab\xdb\x18\x20\x89\x66\x24\xd1\x0c\x80" \
    "\xe9\x28\x66\x3a\x8a\xf3\xec\xa0\xc6\xfb\x38\x5a" \
    "\xe3\xdc\xf1\x3e\x67\x55\xb8\xed\xbb\xbc\xbe\x7f" \
    "\xb8\x2e\x65\xa5\x17\xb7\xba\x96\x56\xd7\x02\xb0" \
    "\x1e\x6c\x59\x0f\xb6\x00\x98\x61\x8c\x19\xa6\xfe" \
    "\xc6\x9b\x15\xe3\xcd\x0a\x80\xe6\xd2\xa7\xb9\xf4" \
    "\x81\x53\x70\x2c\xb2\x01\xa9\xe3\xb8\x8a\x1f\xff" \
    "\xb8\xdf\x8b\xe9\xf7\x52\x4f\x52\x4a\xa4\x94\x00" \
    "\x04\x8e\x25\x70\x52\xf7\x76\xee\x60\xe7\x4e\xba" \
    "\xbf\x70\x09\x16\x2e\xf0\xef\xb8\x02\xad\xb5\x68" \
    "\x14\x17\x59\xad\x94\xda\xbd\xbe\xbc\x03\x70\x73" \
    "\x7b\xc9\x24\x89\x00\xe8\xb8\x6d\xde\xfc\x4f\x00" \
    "\xae\x9e\xce\xf9\x78\xee\x00\x70\xf1\x38\xc9\xfd" \
    "\x66\x83\xf2\x87\x1d\x17\x39\xd4\x77\xc9\xf1\xf7" \
    "\xa0\x78\x49\x18\x86\x00\x78\x9e\xc7\x6f\x6a\x38" \
    "\x19\xc7\x45\xea\xf8\xd6\x5a\x8b\x2f\x29\x94\x78" \
    "\x0c\x77\x48\xb1\xfb\x00\x00\x00\x00\x49\x45\x4e" \
    "\x44\xae\x42\x60\x82"

class ElementSelectorDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("ElementSelectorDialog")

        pal = QPalette()
        cg = QColorGroup()
        cg.setColor(QColorGroup.Foreground,Qt.black)
        cg.setColor(QColorGroup.Button,QColor(230,231,230))
        cg.setColor(QColorGroup.Light,Qt.white)
        cg.setColor(QColorGroup.Midlight,QColor(242,243,242))
        cg.setColor(QColorGroup.Dark,QColor(115,115,115))
        cg.setColor(QColorGroup.Mid,QColor(153,154,153))
        cg.setColor(QColorGroup.Text,Qt.black)
        cg.setColor(QColorGroup.BrightText,Qt.white)
        cg.setColor(QColorGroup.ButtonText,Qt.black)
        cg.setColor(QColorGroup.Base,Qt.white)
        cg.setColor(QColorGroup.Background,QColor(230,231,230))
        cg.setColor(QColorGroup.Shadow,Qt.black)
        cg.setColor(QColorGroup.Highlight,QColor(0,0,128))
        cg.setColor(QColorGroup.HighlightedText,Qt.white)
        cg.setColor(QColorGroup.Link,Qt.black)
        cg.setColor(QColorGroup.LinkVisited,Qt.black)
        pal.setActive(cg)
        cg.setColor(QColorGroup.Foreground,Qt.black)
        cg.setColor(QColorGroup.Button,QColor(230,231,230))
        cg.setColor(QColorGroup.Light,Qt.white)
        cg.setColor(QColorGroup.Midlight,Qt.white)
        cg.setColor(QColorGroup.Dark,QColor(115,115,115))
        cg.setColor(QColorGroup.Mid,QColor(153,154,153))
        cg.setColor(QColorGroup.Text,Qt.black)
        cg.setColor(QColorGroup.BrightText,Qt.white)
        cg.setColor(QColorGroup.ButtonText,Qt.black)
        cg.setColor(QColorGroup.Base,Qt.white)
        cg.setColor(QColorGroup.Background,QColor(230,231,230))
        cg.setColor(QColorGroup.Shadow,Qt.black)
        cg.setColor(QColorGroup.Highlight,QColor(0,0,128))
        cg.setColor(QColorGroup.HighlightedText,Qt.white)
        cg.setColor(QColorGroup.Link,QColor(0,0,255))
        cg.setColor(QColorGroup.LinkVisited,QColor(255,0,255))
        pal.setInactive(cg)
        cg.setColor(QColorGroup.Foreground,QColor(128,128,128))
        cg.setColor(QColorGroup.Button,QColor(230,231,230))
        cg.setColor(QColorGroup.Light,Qt.white)
        cg.setColor(QColorGroup.Midlight,Qt.white)
        cg.setColor(QColorGroup.Dark,QColor(115,115,115))
        cg.setColor(QColorGroup.Mid,QColor(153,154,153))
        cg.setColor(QColorGroup.Text,QColor(128,128,128))
        cg.setColor(QColorGroup.BrightText,Qt.white)
        cg.setColor(QColorGroup.ButtonText,QColor(128,128,128))
        cg.setColor(QColorGroup.Base,Qt.white)
        cg.setColor(QColorGroup.Background,QColor(230,231,230))
        cg.setColor(QColorGroup.Shadow,Qt.black)
        cg.setColor(QColorGroup.Highlight,QColor(0,0,128))
        cg.setColor(QColorGroup.HighlightedText,Qt.white)
        cg.setColor(QColorGroup.Link,QColor(0,0,255))
        cg.setColor(QColorGroup.LinkVisited,QColor(255,0,255))
        pal.setDisabled(cg)
        self.setPalette(pal)
        self.setIcon(self.image0)

        ElementSelectorDialogLayout = QVBoxLayout(self,11,6,"ElementSelectorDialogLayout")

        layout12 = QHBoxLayout(None,0,6,"layout12")

        self.elemInfoLabel = QLabel(self,"elemInfoLabel")
        self.elemInfoLabel.setSizePolicy(QSizePolicy(5,5,0,1,self.elemInfoLabel.sizePolicy().hasHeightForWidth()))
        self.elemInfoLabel.setMinimumSize(QSize(0,0))
        self.elemInfoLabel.setPaletteBackgroundColor(QColor(227,211,231))
        self.elemInfoLabel.setTextFormat(QLabel.RichText)
        self.elemInfoLabel.setAlignment(QLabel.AlignCenter)
        layout12.addWidget(self.elemInfoLabel)

        self.elemColorLabel = QLabel(self,"elemColorLabel")
        self.elemColorLabel.setSizePolicy(QSizePolicy(5,5,0,0,self.elemColorLabel.sizePolicy().hasHeightForWidth()))
        self.elemColorLabel.setMinimumSize(QSize(0,0))
        self.elemColorLabel.setTextFormat(QLabel.RichText)
        self.elemColorLabel.setAlignment(QLabel.AlignCenter)
        layout12.addWidget(self.elemColorLabel)

        self.elementFrame = QFrame(self,"elementFrame")
        self.elementFrame.setSizePolicy(QSizePolicy(5,5,0,0,self.elementFrame.sizePolicy().hasHeightForWidth()))
        self.elementFrame.setMinimumSize(QSize(0,0))
        self.elementFrame.setFrameShape(QFrame.Box)
        self.elementFrame.setFrameShadow(QFrame.Raised)
        layout12.addWidget(self.elementFrame)
        ElementSelectorDialogLayout.addLayout(layout12)

        self.elementButtonGroup = QButtonGroup(self,"elementButtonGroup")
        self.elementButtonGroup.setPaletteBackgroundColor(QColor(223,231,212))
        self.elementButtonGroup.setExclusive(1)
        self.elementButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.elementButtonGroup.layout().setSpacing(1)
        self.elementButtonGroup.layout().setMargin(2)
        elementButtonGroupLayout = QGridLayout(self.elementButtonGroup.layout())
        elementButtonGroupLayout.setAlignment(Qt.AlignTop)

        self.pushButton1 = QPushButton(self.elementButtonGroup,"pushButton1")
        self.pushButton1.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton1.sizePolicy().hasHeightForWidth()))
        self.pushButton1.setPaletteBackgroundColor(QColor(60,215,205))
        pushButton1_font = QFont(self.pushButton1.font())
        pushButton1_font.setFamily("Times")
        pushButton1_font.setPointSize(10)
        pushButton1_font.setBold(1)
        self.pushButton1.setFont(pushButton1_font)
        self.pushButton1.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton1.setToggleButton(1)
        self.pushButton1.setOn(0)
        self.pushButton1.setDefault(0)
        self.elementButtonGroup.insert( self.pushButton1,1)

        elementButtonGroupLayout.addWidget(self.pushButton1,0,4)

        self.pushButton2 = QPushButton(self.elementButtonGroup,"pushButton2")
        self.pushButton2.setEnabled(1)
        self.pushButton2.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton2.sizePolicy().hasHeightForWidth()))
        self.pushButton2.setPaletteBackgroundColor(QColor(210,210,255))
        pushButton2_font = QFont(self.pushButton2.font())
        pushButton2_font.setFamily("Times")
        pushButton2_font.setPointSize(10)
        pushButton2_font.setBold(1)
        self.pushButton2.setFont(pushButton2_font)
        self.pushButton2.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton2.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton2,2)

        elementButtonGroupLayout.addWidget(self.pushButton2,0,5)

        self.pushButton6 = QPushButton(self.elementButtonGroup,"pushButton6")
        self.pushButton6.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton6.sizePolicy().hasHeightForWidth()))
        self.pushButton6.setPaletteBackgroundColor(QColor(35,165,75))
        pushButton6_font = QFont(self.pushButton6.font())
        pushButton6_font.setFamily("Times")
        pushButton6_font.setPointSize(10)
        pushButton6_font.setBold(1)
        self.pushButton6.setFont(pushButton6_font)
        self.pushButton6.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton6.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton6,6)

        elementButtonGroupLayout.addWidget(self.pushButton6,1,1)

        self.pushButton7 = QPushButton(self.elementButtonGroup,"pushButton7")
        self.pushButton7.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton7.sizePolicy().hasHeightForWidth()))
        self.pushButton7.setPaletteBackgroundColor(QColor(255,170,255))
        pushButton7_font = QFont(self.pushButton7.font())
        pushButton7_font.setFamily("Times")
        pushButton7_font.setPointSize(10)
        pushButton7_font.setBold(1)
        self.pushButton7.setFont(pushButton7_font)
        self.pushButton7.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton7.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton7,7)

        elementButtonGroupLayout.addWidget(self.pushButton7,1,2)

        self.pushButton8 = QPushButton(self.elementButtonGroup,"pushButton8")
        self.pushButton8.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton8.sizePolicy().hasHeightForWidth()))
        self.pushButton8.setPaletteBackgroundColor(QColor(191,0,0))
        pushButton8_font = QFont(self.pushButton8.font())
        pushButton8_font.setFamily("Times")
        pushButton8_font.setPointSize(10)
        pushButton8_font.setBold(1)
        self.pushButton8.setFont(pushButton8_font)
        self.pushButton8.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton8.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton8,8)

        elementButtonGroupLayout.addWidget(self.pushButton8,1,3)

        self.pushButton9 = QPushButton(self.elementButtonGroup,"pushButton9")
        self.pushButton9.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton9.sizePolicy().hasHeightForWidth()))
        self.pushButton9.setPaletteBackgroundColor(QColor(85,255,127))
        pushButton9_font = QFont(self.pushButton9.font())
        pushButton9_font.setFamily("Times")
        pushButton9_font.setPointSize(10)
        pushButton9_font.setBold(1)
        self.pushButton9.setFont(pushButton9_font)
        self.pushButton9.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton9.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton9,9)

        elementButtonGroupLayout.addWidget(self.pushButton9,1,4)

        self.pushButton10 = QPushButton(self.elementButtonGroup,"pushButton10")
        self.pushButton10.setEnabled(1)
        self.pushButton10.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton10.sizePolicy().hasHeightForWidth()))
        self.pushButton10.setPaletteBackgroundColor(QColor(210,210,255))
        pushButton10_font = QFont(self.pushButton10.font())
        pushButton10_font.setFamily("Times")
        pushButton10_font.setPointSize(10)
        pushButton10_font.setBold(1)
        self.pushButton10.setFont(pushButton10_font)
        self.pushButton10.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton10.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton10,10)

        elementButtonGroupLayout.addWidget(self.pushButton10,1,5)

        self.pushButton16 = QPushButton(self.elementButtonGroup,"pushButton16")
        self.pushButton16.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton16.sizePolicy().hasHeightForWidth()))
        self.pushButton16.setPaletteBackgroundColor(QColor(255,213,73))
        pushButton16_font = QFont(self.pushButton16.font())
        pushButton16_font.setFamily("Times")
        pushButton16_font.setPointSize(10)
        pushButton16_font.setBold(1)
        self.pushButton16.setFont(pushButton16_font)
        self.pushButton16.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton16.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton16,16)

        elementButtonGroupLayout.addWidget(self.pushButton16,2,3)

        self.pushButton17 = QPushButton(self.elementButtonGroup,"pushButton17")
        self.pushButton17.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton17.sizePolicy().hasHeightForWidth()))
        self.pushButton17.setPaletteBackgroundColor(QColor(149,223,0))
        self.pushButton17.setBackgroundOrigin(QPushButton.ParentOrigin)
        pushButton17_font = QFont(self.pushButton17.font())
        pushButton17_font.setFamily("Times")
        pushButton17_font.setPointSize(10)
        pushButton17_font.setBold(1)
        self.pushButton17.setFont(pushButton17_font)
        self.pushButton17.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton17.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton17,17)

        elementButtonGroupLayout.addWidget(self.pushButton17,2,4)

        self.pushButton18 = QPushButton(self.elementButtonGroup,"pushButton18")
        self.pushButton18.setEnabled(1)
        self.pushButton18.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton18.sizePolicy().hasHeightForWidth()))
        self.pushButton18.setPaletteBackgroundColor(QColor(210,210,255))
        pushButton18_font = QFont(self.pushButton18.font())
        pushButton18_font.setFamily("Times")
        pushButton18_font.setPointSize(10)
        pushButton18_font.setBold(1)
        self.pushButton18.setFont(pushButton18_font)
        self.pushButton18.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton18.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton18,18)

        elementButtonGroupLayout.addWidget(self.pushButton18,2,5)

        self.pushButton32 = QPushButton(self.elementButtonGroup,"pushButton32")
        self.pushButton32.setEnabled(1)
        self.pushButton32.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton32.sizePolicy().hasHeightForWidth()))
        self.pushButton32.setPaletteBackgroundColor(QColor(206,206,0))
        pushButton32_font = QFont(self.pushButton32.font())
        pushButton32_font.setFamily("Times")
        pushButton32_font.setPointSize(10)
        pushButton32_font.setBold(1)
        self.pushButton32.setFont(pushButton32_font)
        self.pushButton32.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton32.setToggleButton(1)
        self.pushButton32.setOn(0)
        self.elementButtonGroup.insert( self.pushButton32,32)

        elementButtonGroupLayout.addWidget(self.pushButton32,3,1)

        self.pushButton33 = QPushButton(self.elementButtonGroup,"pushButton33")
        self.pushButton33.setEnabled(1)
        self.pushButton33.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton33.sizePolicy().hasHeightForWidth()))
        self.pushButton33.setPaletteBackgroundColor(QColor(229,62,255))
        pushButton33_font = QFont(self.pushButton33.font())
        pushButton33_font.setFamily("Times")
        pushButton33_font.setPointSize(10)
        pushButton33_font.setBold(1)
        self.pushButton33.setFont(pushButton33_font)
        self.pushButton33.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton33.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton33,33)

        elementButtonGroupLayout.addWidget(self.pushButton33,3,2)

        self.pushButton34 = QPushButton(self.elementButtonGroup,"pushButton34")
        self.pushButton34.setEnabled(1)
        self.pushButton34.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton34.sizePolicy().hasHeightForWidth()))
        self.pushButton34.setPaletteBackgroundColor(QColor(230,144,23))
        pushButton34_font = QFont(self.pushButton34.font())
        pushButton34_font.setFamily("Times")
        pushButton34_font.setPointSize(10)
        pushButton34_font.setBold(1)
        self.pushButton34.setFont(pushButton34_font)
        self.pushButton34.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton34.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton34,34)

        elementButtonGroupLayout.addWidget(self.pushButton34,3,3)

        self.pushButton35 = QPushButton(self.elementButtonGroup,"pushButton35")
        self.pushButton35.setEnabled(1)
        self.pushButton35.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton35.sizePolicy().hasHeightForWidth()))
        self.pushButton35.setPaletteBackgroundColor(QColor(77,202,156))
        pushButton35_font = QFont(self.pushButton35.font())
        pushButton35_font.setFamily("Times")
        pushButton35_font.setPointSize(10)
        pushButton35_font.setBold(1)
        self.pushButton35.setFont(pushButton35_font)
        self.pushButton35.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton35.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton35,35)

        elementButtonGroupLayout.addWidget(self.pushButton35,3,4)

        self.pushButton36 = QPushButton(self.elementButtonGroup,"pushButton36")
        self.pushButton36.setEnabled(1)
        self.pushButton36.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton36.sizePolicy().hasHeightForWidth()))
        self.pushButton36.setPaletteBackgroundColor(QColor(210,210,255))
        pushButton36_font = QFont(self.pushButton36.font())
        pushButton36_font.setFamily("Times")
        pushButton36_font.setPointSize(10)
        pushButton36_font.setBold(1)
        self.pushButton36.setFont(pushButton36_font)
        self.pushButton36.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton36.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton36,36)

        elementButtonGroupLayout.addWidget(self.pushButton36,3,5)

        self.pushButton51 = QPushButton(self.elementButtonGroup,"pushButton51")
        self.pushButton51.setEnabled(0)
        self.pushButton51.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton51.sizePolicy().hasHeightForWidth()))
        self.pushButton51.setPaletteBackgroundColor(QColor(170,0,255))
        pushButton51_font = QFont(self.pushButton51.font())
        pushButton51_font.setFamily("Times")
        pushButton51_font.setPointSize(10)
        pushButton51_font.setBold(1)
        self.pushButton51.setFont(pushButton51_font)
        self.pushButton51.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton51.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton51,51)

        elementButtonGroupLayout.addWidget(self.pushButton51,4,2)

        self.pushButton52 = QPushButton(self.elementButtonGroup,"pushButton52")
        self.pushButton52.setEnabled(0)
        self.pushButton52.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton52.sizePolicy().hasHeightForWidth()))
        self.pushButton52.setPaletteBackgroundColor(QColor(238,183,53))
        pushButton52_font = QFont(self.pushButton52.font())
        pushButton52_font.setFamily("Times")
        pushButton52_font.setPointSize(10)
        pushButton52_font.setBold(1)
        self.pushButton52.setFont(pushButton52_font)
        self.pushButton52.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton52.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton52,52)

        elementButtonGroupLayout.addWidget(self.pushButton52,4,3)

        self.pushButton53 = QPushButton(self.elementButtonGroup,"pushButton53")
        self.pushButton53.setEnabled(0)
        self.pushButton53.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton53.sizePolicy().hasHeightForWidth()))
        self.pushButton53.setPaletteBackgroundColor(QColor(0,180,135))
        pushButton53_font = QFont(self.pushButton53.font())
        pushButton53_font.setFamily("Times")
        pushButton53_font.setPointSize(10)
        pushButton53_font.setBold(1)
        self.pushButton53.setFont(pushButton53_font)
        self.pushButton53.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton53.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton53,53)

        elementButtonGroupLayout.addWidget(self.pushButton53,4,4)

        self.pushButton54 = QPushButton(self.elementButtonGroup,"pushButton54")
        self.pushButton54.setEnabled(0)
        self.pushButton54.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton54.sizePolicy().hasHeightForWidth()))
        self.pushButton54.setPaletteBackgroundColor(QColor(210,210,255))
        pushButton54_font = QFont(self.pushButton54.font())
        pushButton54_font.setFamily("Times")
        pushButton54_font.setPointSize(10)
        pushButton54_font.setBold(1)
        self.pushButton54.setFont(pushButton54_font)
        self.pushButton54.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton54.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton54,54)

        elementButtonGroupLayout.addWidget(self.pushButton54,4,5)

        self.pushButton15 = QPushButton(self.elementButtonGroup,"pushButton15")
        self.pushButton15.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton15.sizePolicy().hasHeightForWidth()))
        self.pushButton15.setPaletteBackgroundColor(QColor(170,85,200))
        pushButton15_font = QFont(self.pushButton15.font())
        pushButton15_font.setFamily("Times")
        pushButton15_font.setPointSize(10)
        pushButton15_font.setBold(1)
        self.pushButton15.setFont(pushButton15_font)
        self.pushButton15.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton15.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton15,15)

        elementButtonGroupLayout.addWidget(self.pushButton15,2,2)

        self.pushButton14 = QPushButton(self.elementButtonGroup,"pushButton14")
        self.pushButton14.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton14.sizePolicy().hasHeightForWidth()))
        self.pushButton14.setPaletteBackgroundColor(QColor(156,156,156))
        pushButton14_font = QFont(self.pushButton14.font())
        pushButton14_font.setFamily("Times")
        pushButton14_font.setPointSize(10)
        pushButton14_font.setBold(1)
        self.pushButton14.setFont(pushButton14_font)
        self.pushButton14.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton14.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton14,14)

        elementButtonGroupLayout.addWidget(self.pushButton14,2,1)

        self.pushButton13 = QPushButton(self.elementButtonGroup,"pushButton13")
        self.pushButton13.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton13.sizePolicy().hasHeightForWidth()))
        self.pushButton13.setPaletteBackgroundColor(QColor(170,170,255))
        pushButton13_font = QFont(self.pushButton13.font())
        pushButton13_font.setFamily("Times")
        pushButton13_font.setPointSize(10)
        pushButton13_font.setBold(1)
        self.pushButton13.setFont(pushButton13_font)
        self.pushButton13.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton13.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton13,13)

        elementButtonGroupLayout.addWidget(self.pushButton13,2,0)

        self.pushButton5 = QPushButton(self.elementButtonGroup,"pushButton5")
        self.pushButton5.setSizePolicy(QSizePolicy(5,0,0,0,self.pushButton5.sizePolicy().hasHeightForWidth()))
        self.pushButton5.setPaletteBackgroundColor(QColor(80,135,255))
        pushButton5_font = QFont(self.pushButton5.font())
        pushButton5_font.setFamily("Times")
        pushButton5_font.setPointSize(10)
        pushButton5_font.setBold(1)
        self.pushButton5.setFont(pushButton5_font)
        self.pushButton5.setFocusPolicy(QPushButton.NoFocus)
        self.pushButton5.setToggleButton(1)
        self.elementButtonGroup.insert( self.pushButton5,5)

        elementButtonGroupLayout.addWidget(self.pushButton5,1,0)
        ElementSelectorDialogLayout.addWidget(self.elementButtonGroup)

        layout13 = QGridLayout(None,1,1,9,9,"layout13")

        self.closePTableButton = QPushButton(self,"closePTableButton")
        self.closePTableButton.setSizePolicy(QSizePolicy(5,0,0,0,self.closePTableButton.sizePolicy().hasHeightForWidth()))
        self.closePTableButton.setDefault(1)

        layout13.addWidget(self.closePTableButton,1,1)

        self.transmuteCheckBox = QCheckBox(self,"transmuteCheckBox")
        self.transmuteCheckBox.setSizePolicy(QSizePolicy(5,0,0,0,self.transmuteCheckBox.sizePolicy().hasHeightForWidth()))

        layout13.addWidget(self.transmuteCheckBox,0,1)

        self.TransmuteButton = QPushButton(self,"TransmuteButton")
        self.TransmuteButton.setSizePolicy(QSizePolicy(5,0,0,0,self.TransmuteButton.sizePolicy().hasHeightForWidth()))

        layout13.addWidget(self.TransmuteButton,0,0)
        ElementSelectorDialogLayout.addLayout(layout13)

        self.languageChange()

        self.resize(QSize(415,350).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.closePTableButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.TransmuteButton,SIGNAL("clicked()"),self.transmutePressed)
        self.connect(self.elementButtonGroup,SIGNAL("clicked(int)"),self.setElementInfo)

        self.setTabOrder(self.TransmuteButton,self.transmuteCheckBox)
        self.setTabOrder(self.transmuteCheckBox,self.closePTableButton)


    def languageChange(self):
        self.setCaption(self.__tr("Element Selector"))
        self.elemInfoLabel.setText(QString.null)
        self.elemColorLabel.setText(QString.null)
        self.elementButtonGroup.setTitle(QString.null)
        self.pushButton1.setText(self.__tr("H"))
        self.pushButton2.setText(self.__tr("He"))
        self.pushButton6.setText(self.__tr("C"))
        self.pushButton7.setText(self.__tr("N"))
        self.pushButton8.setText(self.__tr("O"))
        self.pushButton9.setText(self.__tr("F"))
        self.pushButton10.setText(self.__tr("Ne"))
        self.pushButton16.setText(self.__tr("S"))
        self.pushButton17.setText(self.__tr("Cl"))
        self.pushButton18.setText(self.__tr("Ar"))
        self.pushButton32.setText(self.__tr("Ge"))
        self.pushButton33.setText(self.__tr("As"))
        self.pushButton34.setText(self.__tr("Se"))
        self.pushButton35.setText(self.__tr("Br"))
        self.pushButton36.setText(self.__tr("Kr"))
        self.pushButton51.setText(self.__tr("Sb"))
        self.pushButton52.setText(self.__tr("Te"))
        self.pushButton53.setText(self.__tr("I"))
        self.pushButton54.setText(self.__tr("Xe"))
        self.pushButton15.setText(self.__tr("P"))
        self.pushButton14.setText(self.__tr("Si"))
        self.pushButton13.setText(self.__tr("Al"))
        self.pushButton5.setText(self.__tr("B"))
        self.closePTableButton.setText(self.__tr("Close"))
        self.transmuteCheckBox.setText(self.__tr("Force to Keep Bonds"))
        QToolTip.add(self.transmuteCheckBox,self.__tr("Check if transmuted atoms should keep all existing bonds,  even if chemistry is wrong."))
        self.TransmuteButton.setText(self.__tr("Transmute"))


    def setElementInfo(self,a0):
        print "ElementSelectorDialog.setElementInfo(int): Not implemented yet"

    def transmutePressed(self):
        print "ElementSelectorDialog.transmutePressed(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ElementSelectorDialog",s,c)
