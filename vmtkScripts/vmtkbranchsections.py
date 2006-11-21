#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkbranchsections.py,v $
## Language:  Python
## Date:      $Date: 2006/10/17 15:16:16 $
## Version:   $Revision: 1.1 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


import vtk
import vtkvmtk
import sys

import pypes

vmtkbranchsections = 'vmtkBranchSections'

class vmtkBranchSections(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
       
        self.Surface = None
        self.Centerlines = None
        self.BranchSections = None

        self.NumberOfDistanceSpheres = 1

        self.RadiusArrayName = ''
        self.GroupIdsArrayName = ''
        self.CenterlineIdsArrayName = ''
        self.TractIdsArrayName = ''
        self.BlankingArrayName = ''

        self.BranchSectionGroupIdsArrayName = 'BranchSectionGroupIds'
        self.BranchSectionAreaArrayName = 'BranchSectionArea'
        self.BranchSectionMinSizeArrayName = 'BranchSectionMinSize'
        self.BranchSectionMaxSizeArrayName = 'BranchSectionMaxSize'
        self.BranchSectionShapeArrayName = 'BranchSectionShape'
        self.BranchSectionClosedArrayName = 'BranchSectionClosed'
        self.BranchSectionDistanceSpheresArrayName = 'BranchSectionDistanceSpheres'

        self.SetScriptName('vmtkbranchsections')
        self.SetScriptDoc('compute geometric properties of branch sections located a fixed number of spheres away from each bifurcation. The script takes in input the surface and the relative centerlines, both already split into branches.')
        self.SetInputMembers([
            ['Surface','i','vtkPolyData',1,'the input surface, already split into branches','vmtksurfacereader'],
            ['Centerlines','centerlines','vtkPolyData',1,'the input centerlines, already split into branches','vmtksurfacereader'],
      	    ['NumberOfDistanceSpheres','distancespheres','int',1,'distance from the bifurcation at which the sections have to be taken; the distance is expressed in number of inscribed spheres, where each sphere touches the center of the previous one'],
      	    ['RadiusArrayName','radiusarray','str',1,'name of the array where centerline radius is stored'],
      	    ['GroupIdsArrayName','groupidsarray','str',1,'name of the array where centerline group ids are stored'],
      	    ['CenterlineIdsArrayName','centerlineidsarray','str',1,'name of the array where centerline ids are stored'],
      	    ['TractIdsArrayName','tractidsarray','str',1,'name of the array where centerline tract ids are stored'],
      	    ['BlankingArrayName','blankingarray','str',1,'name of the array where centerline blanking information about branches is stored'],
      	    ['BranchSectionGroupIdsArrayName','branchsectiongroupids','str',1,'name of the array where the group id to which each section belongs has to be stored'],
      	    ['BranchSectionAreaArrayName','branchsectionarea','str',1,'name of the array where the area of bifurcation sections have to be stored'],
      	    ['BranchSectionMinSizeArrayName','branchsectionminsize','str',1,'name of the array where the minvmtkm diameter of each section has to be stored'],
      	    ['BranchSectionMaxSizeArrayName','branchsectionmaxsize','str',1,'name of the array where the maxvmtkm diameter of each bifurcation sections has to be stored'],
      	    ['BranchSectionShapeArrayName','branchsectionshape','str',1,'name of the array where the shape index, i.e. the ratio between minvmtkm and maxvmtkm diameter, of each bifurcation section has to be stored'],
      	    ['BranchSectionClosedArrayName','branchsectionclosed','str',1,'name of the array containing 1 if a section is closed and 0 otherwise'],
      	    ['BranchSectionDistanceSpheresArrayName','branchsectiondistancespheres','str',1,'name of the array containing the number of distance spheres the section is taken at']
            ])
        self.SetOutputMembers([
            ['BranchSections','o','vtkPolyData',1,'the output sections','vmtksurfacewriter'],
      	    ['BranchSectionGroupIdsArrayName','branchsectiongroupids','str',1,'name of the array where the group id to which each section belongs are stored'],
      	    ['BranchSectionAreaArrayName','branchsectionarea','str',1,'name of the array where the area of bifurcation sections are stored'],
      	    ['BranchSectionMinSizeArrayName','branchsectionminsize','str',1,'name of the array where the minvmtkm diameter of each section are stored'],
      	    ['BranchSectionMaxSizeArrayName','branchsectionmaxsize','str',1,'name of the array where the minvmtkm diameter of each bifurcation sections has to be stored'],
      	    ['BranchSectionShapeArrayName','branchsectionshape','str',1,'name of the array where the shape index, i.e. the ratio between minvmtkm and maxvmtkm diameter, of each bifurcation section are stored'],
      	    ['BranchSectionClosedArrayName','branchsectionclosed','str',1,'name of the array containing 1 if a section is closed and 0 otherwise'],
      	    ['BranchSectionDistanceSpheresArrayName','branchsectiondistancespheres','str',1,'name of the array containing the number of distance spheres the section is taken at']
            ])

    def Execute(self):

        if self.Surface == None:
            self.PrintError('Error: No input surface.')

        if self.Centerlines == None:
            self.PrintError('Error: No input centerlines.')

        branchSections = vtkvmtk.vtkvmtkPolyDataBranchSections()
        branchSections.SetInput(self.Surface)
        branchSections.SetGroupIdsArrayName(self.GroupIdsArrayName)
        branchSections.SetCenterlines(self.Centerlines)
	branchSections.SetNumberOfDistanceSpheres(self.NumberOfDistanceSpheres)
        branchSections.SetCenterlineRadiusArrayName(self.RadiusArrayName)
        branchSections.SetCenterlineGroupIdsArrayName(self.GroupIdsArrayName)
        branchSections.SetCenterlineIdsArrayName(self.CenterlineIdsArrayName)
        branchSections.SetCenterlineTractIdsArrayName(self.TractIdsArrayName)
        branchSections.SetBlankingArrayName(self.BlankingArrayName)
        branchSections.SetBranchSectionGroupIdsArrayName(self.BranchSectionGroupIdsArrayName)
        branchSections.SetBranchSectionAreaArrayName(self.BranchSectionAreaArrayName)
        branchSections.SetBranchSectionMinSizeArrayName(self.BranchSectionMinSizeArrayName)
        branchSections.SetBranchSectionMaxSizeArrayName(self.BranchSectionMaxSizeArrayName)
        branchSections.SetBranchSectionShapeArrayName(self.BranchSectionShapeArrayName)
        branchSections.SetBranchSectionClosedArrayName(self.BranchSectionClosedArrayName)
        branchSections.SetBranchSectionDistanceSpheresArrayName(self.BranchSectionDistanceSpheresArrayName)
        branchSections.Update()

        self.BranchSections = branchSections.GetOutput()


if __name__=='__main__':

    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()
