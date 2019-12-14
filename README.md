# RubixCube
A simulated rubix cube in processing 3.
https://processing.org

Uses python (jython) version of processing 3.

The spacebar pauses or unpauses cube rotation along the X-Y axis.
  Where the mouse's X position relative to the screen dictates the X rotation factor,
  and where the mouse's Y position does the same but instead affecting the Y rotation factor.
  
There are 13 buttons in total.
  The big left-most button changes the way the other buttons affect the cube. 
  In its starting state, each button will affect the cube relative to its current rotation,
  which let's one use the standard Rubix Cube notation (U, Up, D, Dp, etc... Excluding more complex notations like x, y, z, M, r, and others).
  In its other state, the sides rotate based on the colors of each center.
  The other 12 buttons turn the cube according to the mode, with each button colored by the side it rotates,
  and depending on the mode, it either shows the notation or color using the respective letter(s) in each box.

Thank you!
