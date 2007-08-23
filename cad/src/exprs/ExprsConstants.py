# Copyright 2006-2007 Nanorex, Inc.  See LICENSE file for details. 
"""
ExprsConstants.py -- define constants and simple functions used by many files in this package

$Id$

"""

from VQT import V

from prefs_constants import UPPER_RIGHT, UPPER_LEFT, LOWER_LEFT, LOWER_RIGHT # compass positions, also usable for DrawInCorner
    # note: their values are ints -- perhaps hard to change since they might correspond to Qt radiobutton indices (guess)

from exprs.py_utils import identity

# standard corners for various UI elements [070326, but some will be revised soon]
WORLD_MT_CORNER = UPPER_LEFT
##PM_CORNER = LOWER_RIGHT #e revise
##DEBUG_CORNER = LOWER_LEFT #e revise
PM_CORNER = LOWER_LEFT
DEBUG_CORNER = LOWER_RIGHT

# == other generally useful constants

# (but color constants are imported lower down)

# geometric (moved here from draw_utils.py, 070130)

ORIGIN = V(0,0,0)
DX = V(1,0,0)
DY = V(0,1,0)
DZ = V(0,0,1)

ORIGIN2 = V(0.0, 0.0)
D2X = V(1.0, 0.0) ##e rename to DX2?
D2Y = V(0.0, 1.0)

# type aliases (tentative; see canon_type [070131])
Int = int # warning: not the same as Numeric.Int, which equals 'l'
Float = float # warning: not the same as Numeric.Float, which equals 'd'
String = str # warning: not the same as parse_utils.String
Boolean = bool

# == Python and debug utilities, and low-level local defs

try:
    old_EVAL_REFORM = EVAL_REFORM
except NameError:
    old_EVAL_REFORM = None

EVAL_REFORM = True # 070115: False supposedly acts like old code, True like experimental new code which should become standard;
     # this affects all class defs, so to be safe, print a warning if it changes across reload

if old_EVAL_REFORM != EVAL_REFORM and old_EVAL_REFORM is not None:
    print "\n*** WARNING: EVAL_REFORM was %r before reload, is %r now -- might require restart of NE1 or testmode" % \
          (old_EVAL_REFORM, EVAL_REFORM)
else:
    if not EVAL_REFORM:
        print "EVAL_REFORM is %r" % EVAL_REFORM

nevermind = lambda func: identity

from exprs.__Symbols__ import Anything #070115
from exprs.__Symbols__ import Automatic, Something #070131

# Symbol docstrings -- for now, just tack them on (not yet used AFAIK):

Anything.__doc__ = """Anything is a legitimate type to coerce to which means 'don't change the value at all'. """
Anything._e_sym_constant = True

Something.__doc__ = """Something is a stub for when we don't yet know a type or value or formula,
but plan to replace it with something specific (by editing the source code later). """
Something._e_eval_forward_to = Anything

Automatic.__doc__ = """Automatic [###NIM] can be coerced to most types to produce a default value.
By convention, when constructing certain classes of exprs, it can be passed as an arg or option value
to specify that a reasonable value should be chosen which might depend on the values provided for other
args or options. """
    ###e implem of that:
    #  probably the type should say "or Automatic" if it wants to let a later stage use other args to interpret it,
    #  or maybe the typedecl could give the specific rule for replacing Automatic, using a syntax not specific to Automatic.
Automatic._e_sym_constant = True

# == colors (constants and simple functions; import them everywhere to discourage name conflicts that show up only later)

#e maybe import the following from a different file, but for now we need to define some here
#k need to make sure none of these are defined elsewhere in this module
from constants import black, red, green, blue, purple, magenta, violet, yellow, orange, pink, white, gray
    # note: various defs of purple I've seen:
    # ave_colors( 0.5, red, blue), or (0.5, 0.0, 0.5), or (0.7,0.0,0.7), or (0.6, 0.1, 0.9) == violet in constants.py
from constants import aqua, darkgreen, navy, darkred, lightblue
from constants import ave_colors
    ###e what does this do to alpha? A: uses zip, which means, weight it if present in both colors, discard it otherwise.
    ###k What *should* it do? Not that, but that is at least not going to cause "crashes" in non-alpha-using code.

def normalize_color(color): #070215; might be too slow; so far only used by fix_color method
    """Make sure color is a 4-tuple of floats. (Not a numeric array -- too likely to hit the == bug for those.)"""
    if len(color) == 3:
        r,g,b = color
        a = 1.0
    elif len(color) == 4:
        r,g,b,a = color
    else:
        assert len(color) in (3,4)
    return ( float(r), float(g), float(b), float(a)) # alpha will get discarded by ave_colors for now, but shouldn't crash [070215]

#e define brown somewhere, and new funcs to lighten or darken a color

lightblue = ave_colors( 0.2, blue, white)
lightgreen = ave_colors( 0.2, green, white)
halfblue = ave_colors( 0.5, blue, white)

def translucent_color(color, opacity = 0.5): #e refile with ave_colors
    """Make color (a 3- or 4-tuple of floats) have the given opacity (default 0.5, might be revised);
    if it was already translucent, this multiplies the opacity it had.
    """
    if len(color) == 3:
        c1, c2, c3 = color
        c4 = 1.0
    else:
        c1, c2, c3, c4 = color
    return (c1, c2, c3, c4 * opacity)

trans_blue = translucent_color(halfblue)
trans_red = translucent_color(red)
trans_green = translucent_color(green)

# == other constants

PIXELS = 0.035 ###WRONG: rough approximation; true value depends on depth (in perspective view), glpane size, and zoomfactor!
    ###e A useful temporary kluge might be to compute the correct value for the cov plane, and change this constant to match
    # whenever entering testmode (or perhaps when resizing glpane), much like drawfont2 or mymousepoints does internally.
    # But if we do that, then rather than pretending it's a constant, we should rename it and make it an appropriate function
    # or method, e.g. glpane.cov_PIXELS for the correct value at the cov, updated as needed.
    #   We might also replace some uses of PIXELS
    # with fancier functions that compute this for some model object point... but the main use of it is for 2d widget display,
    # for which a single value ought to be correct anyway. (We could even artificially set the transformation matrices so that
    # this value happened to be the correct one -- in fact, we already do that in DrawInCorner, used for most 2d widgets!
    # To fully review that I'd need to include what's done in drawfont2 or mymousepoints via TextRect, too.)
    #   For model objects (at least in perspective view), there are big issues about what this really means, or should mean --
    # e.g. if you use it in making a displist and then the model object depth changes (in perspective view), or the glpane size
    # changes, or the zoom factor changes. Similar issues arise for "billboarding" (screen-parallel alignment) and x/y-alignment
    # to pixel boundaries. Ultimately we need a variety of new Drawable-interface features for this purpose.
    # We also need to start using glDrawPixels instead of textures for 2d widgets, at some point. [comment revised 070304]

# == lower-level stubs -- these will probably be refiled when they are no longer stubs ###@@@

NullIpath = '.' ##k ok that it's not None? maybe not, we might test for None... seems to work for now tho.
    #e make it different per reload? [070121 changed from 'NullIpath' to '.' to shorten debug prints]

StubType = Anything # use this for stub Type symbols [new symbol and policy, 070115]

# stub types
Width    = StubType
Color    = StubType
Vector   = StubType
Quat     = StubType
Position = StubType
Point    = StubType
StateRef = StubType
Function = StubType
Type     = Anything

