/*=========================================================================

Program:   VMTK
Module:    $RCSfile: vtkvmtkPolyDataFlowExtensionsFilter.h,v $
Language:  C++
Date:      $Date: 2006/07/07 10:46:19 $
Version:   $Revision: 1.6 $

  Copyright (c) Luca Antiga, David Steinman. All rights reserved.
  See LICENCE file for details.

  Portions of this code are covered under the VTK copyright.
  See VTKCopyright.txt or http://www.kitware.com/VTKCopyright.htm 
  for details.

     This software is distributed WITHOUT ANY WARRANTY; without even 
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
     PURPOSE.  See the above copyright notices for more information.

=========================================================================*/
  // .NAME vtkvmtkPolyDataFlowExtensionsFilter - .
  // .SECTION Description
  // ...

#ifndef __vtkvmtkPolyDataFlowExtensionsFilter_h
#define __vtkvmtkPolyDataFlowExtensionsFilter_h

#include "vtkPolyDataAlgorithm.h"
#include "vtkPolyData.h"
#include "vtkIdList.h"
//#include "vtkvmtkComputationalGeometryWin32Header.h"
#include "vtkvmtkWin32Header.h"

class VTK_VMTK_COMPUTATIONAL_GEOMETRY_EXPORT vtkvmtkPolyDataFlowExtensionsFilter : public vtkPolyDataAlgorithm
{
  public: 
  vtkTypeRevisionMacro(vtkvmtkPolyDataFlowExtensionsFilter,vtkPolyDataAlgorithm);
  void PrintSelf(ostream& os, vtkIndent indent); 

  static vtkvmtkPolyDataFlowExtensionsFilter *New();
  
  vtkSetObjectMacro(Centerlines,vtkPolyData);
  vtkGetObjectMacro(Centerlines,vtkPolyData);

  vtkSetMacro(ExtensionRatio,double);
  vtkGetMacro(ExtensionRatio,double);

  vtkSetMacro(ExtensionLength,double);
  vtkGetMacro(ExtensionLength,double);

  vtkSetMacro(TransitionRatio,double);
  vtkGetMacro(TransitionRatio,double);

  vtkSetMacro(CenterlineNormalEstimationDistanceRatio,double);
  vtkGetMacro(CenterlineNormalEstimationDistanceRatio,double);

  vtkSetMacro(AdaptiveExtensionLength,int);
  vtkGetMacro(AdaptiveExtensionLength,int);
  vtkBooleanMacro(AdaptiveExtensionLength,int);

  vtkSetMacro(NumberOfBoundaryPoints,int);
  vtkGetMacro(NumberOfBoundaryPoints,int);

  vtkSetObjectMacro(BoundaryIds,vtkIdList);
  vtkGetObjectMacro(BoundaryIds,vtkIdList);

  protected:
  vtkvmtkPolyDataFlowExtensionsFilter();
  ~vtkvmtkPolyDataFlowExtensionsFilter();

  virtual int RequestData(vtkInformation *, vtkInformationVector **, vtkInformationVector *);

  vtkPolyData* Centerlines;

  double ExtensionRatio;
  double ExtensionLength;

  double TransitionRatio;

  double CenterlineNormalEstimationDistanceRatio;

  int AdaptiveExtensionLength;

  int NumberOfBoundaryPoints;

  vtkIdList* BoundaryIds;

  private:
  vtkvmtkPolyDataFlowExtensionsFilter(const vtkvmtkPolyDataFlowExtensionsFilter&);  // Not implemented.
  void operator=(const vtkvmtkPolyDataFlowExtensionsFilter&);  // Not implemented.
};

#endif
