# Copyright 2004-2008 Nanorex, Inc.  See LICENSE file for details. 
"""
gl_buffers.py - OpenGL data buffer objects.

@version: $Id$
@copyright: 2004-2008 Nanorex, Inc.  See LICENSE file for details. 

History:

Originated by Josh as drawer.py .

Various developers extended it since then.

Brad G. added ColorSorter features.

At some point Bruce partly cleaned up the use of display lists.

071030 bruce split some functions and globals into draw_grid_lines.py
and removed some obsolete functions.

080210 russ Split the single display-list into two second-level lists (with and
without color) and a set of per-color sublists so selection and hover-highlight
can over-ride Chunk base colors.  ColorSortedDisplayList is now a class in the
parent's displist attr to keep track of all that stuff.

080311 piotr Added a "drawpolycone_multicolor" function for drawing polycone
tubes with per-vertex colors (necessary for DNA display style)

080313 russ Added triangle-strip icosa-sphere constructor, "getSphereTriStrips".

080420 piotr Solved highlighting and selection problems for multi-colored
objects (e.g. rainbow colored DNA structures).

080519 russ pulled the globals into a drawing_globals module and broke drawer.py
into 10 smaller chunks: glprefs.py setup_draw.py shape_vertices.py
ColorSorter.py CS_workers.py CS_ShapeList.py CS_draw_primitives.py drawers.py
gl_lighting.py gl_buffers.py
"""

# Vertex Buffer Object (VBO) and Index Buffer Object (IBO) support.
# For docs see http://www.opengl.org/sdk/docs/man/xhtml/glBufferData.xml .

# Notice that the ARB-suffixed versions of the OpenGL calls are used here.
# They're the ones with PyConvert ctypes wrappers, see: (the incomprehensible)
#   http://pyopengl.sourceforge.net/ctypes/pydoc/
#          OpenGL.GL.ARB.vertex_buffer_object.html
# The sources will do you more good.   Also see "Array Handling Routines" here:
#   http://pyopengl.sourceforge.net/documentation/opengl_diffs.html
#
from OpenGL.GL.ARB.vertex_buffer_object import glGenBuffersARB
from OpenGL.GL.ARB.vertex_buffer_object import glDeleteBuffersARB
# Patched versions.
from graphics.drawing.vbo_patch import glBufferDataARB, glBufferSubDataARB
# Unwrappered.
from OpenGL.raw.GL.ARB.vertex_buffer_object import glBindBufferARB

class GLBufferObject(object):
    """
    Buffer data in the graphics card's RAM space.

    Useful man pages for glBind, glBufferData, etc. for OpenGL 2.1 are at:
    http://www.opengl.org/sdk/docs/man
    PyOpenGL versions are at:
    http://pyopengl.sourceforge.net/ctypes/pydoc/OpenGL.html

    'target' is GL_ARRAY_BUFFER_ARB for vertex/normal buffers (VBO's), and
    GL_ELEMENT_ARRAY_BUFFER_ARB for index buffers (IBO's.)

    'data' is a numpy.array, with dtype=numpy.<datatype> .

    'usage' is one of the hint constants, like GL_STATIC_DRAW.
    """

    def __init__(self, target, data, usage):
        self.buffer = glGenBuffersARB(1) # Returns a numpy.ndarray for > 1.
        self.target = target

        self.bind()
        self.size = len(data)

        # Push the data over to Graphics card RAM.
        glBufferDataARB(target, data, usage)

        self.unbind()
        return

    def __del__(self):
        """
        Delete a GLBufferObject.  We don't expect that there will be a lot of
        deleting of GLBufferObjects, but don't want them to sit on a lot of
        graphics card RAM if we did.
        """

        # Since may be too late to clean up buffer objects through the Graphics
        # Context while exiting, we trust that OpenGL or the device driver will
        # deallocate the graphics card RAM when the Python process exits.
        try:
            glDeleteBuffersARB(1, [self.buffer])
        except:
            ##print "Exception in glDeleteBuffersARB."
            pass
        return

    def bind(self):
        """
        Have to bind a particular buffer to its target to fill or draw from it.
        Don't forget to unbind() it!
        """
        glBindBufferARB(self.target, self.buffer)
        return

    def unbind(self):
        """
        Unbind a buffer object from its target after use.
        Failure to do this can kill Python on some graphics platforms!
        """
        glBindBufferARB(self.target, 0)
        return

    pass # End of class GLBufferObject.
