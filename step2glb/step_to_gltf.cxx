#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>

#include <TDocStd_Document.hxx>
#include <STEPCAFControl_Reader.hxx>
#include <XCAFDoc_ShapeTool.hxx>
#include <XCAFDoc_DocumentTool.hxx>
#include <TDF_LabelSequence.hxx>
#include <TopoDS_Compound.hxx>
#include <TopoDS_Shape.hxx>
#include <BRep_Builder.hxx>
#include <TDF_Label.hxx>
#include <TCollection_AsciiString.hxx>
#include <NCollection_IndexedDataMap.hxx>
#include <RWGltf_CafWriter.hxx>
#include <Message_ProgressIndicator.hxx>
#include <Prs3d_Drawer.hxx>
#include <Prs3d.hxx>
#include <BRepMesh_IncrementalMesh.hxx>
#include <BRepBndLib.hxx>
#include <Bnd_Box.hxx>

static void show_usage(std::string name)
{
  std::cerr << "Usage: " << name << " <flags> INPUT_STEP"
            << "Options:\n"
            << "\t-h,--help\t\tShow this help message\n"
            << "\t-o,--output OUTPUT_GLB\tSpecify the output path"
            << std::endl; 
}

int step_to_glb(Standard_CString source_path, Standard_CString output_path)
{
  std::cout << "Processing: " << source_path << " -> " << output_path << "\n" << std::endl;

  Handle(TDocStd_Document) xdeDoc = new TDocStd_Document("process");

  STEPCAFControl_Reader aReader;
  if(!(aReader.ReadFile(source_path) == IFSelect_RetDone)){ 
    printf("Error reading step file\n");
    return 1;
  }
  printf("Read step file\n");
  if(!aReader.Transfer(xdeDoc)) { 
    printf("Error transfering step file\n"); 
    return 1;
  }
  printf("Transferred step file\n");

  Handle(XCAFDoc_ShapeTool) aShapeTool = XCAFDoc_DocumentTool::ShapeTool(xdeDoc->Main());

  TDF_LabelSequence aRootLabels;
  aShapeTool->GetFreeShapes(aRootLabels);

  TopoDS_Compound aCompound;
  BRep_Builder aBuildTool;
  aBuildTool.MakeCompound(aCompound);

  printf("Ready to make shape\n");
  
  for (TDF_LabelSequence::Iterator aRootIter (aRootLabels); aRootIter.More(); aRootIter.Next()){
    const TDF_Label& aRootLabel = aRootIter.Value();
    TopoDS_Shape aRootShape;
    if(XCAFDoc_ShapeTool::GetShape(aRootLabel, aRootShape)){
      aBuildTool.Add(aCompound, aRootShape);
    }
  }
  
  printf("Meshing\n");
  Handle(Prs3d_Drawer) aDrawer = new Prs3d_Drawer();
  BRepMesh_IncrementalMesh anAlgo;

  Bnd_Box B;
  
  BRepBndLib::Add(aCompound, B);
  anAlgo.ChangeParameters().Deflection = Prs3d::GetDeflection(B, aDrawer->DeviationCoefficient(), aDrawer->MaximalChordialDeviation());
  anAlgo.ChangeParameters().Angle = 20.0 * M_PI / 180.0;
  anAlgo.ChangeParameters().InParallel = true;
  anAlgo.SetShape(aCompound);
  anAlgo.Perform();  

  printf("Shape ready, starting export\n");
  TColStd_IndexedDataMapOfStringString aMetadata;
  RWGltf_CafWriter aGltfWriter(output_path, true);
  aGltfWriter.ChangeCoordinateSystemConverter().SetInputLengthUnit(0.001);
  aGltfWriter.ChangeCoordinateSystemConverter().SetInputCoordinateSystem(RWMesh_CoordinateSystem_Zup);
  if(!aGltfWriter.Perform(xdeDoc, aMetadata, Message_ProgressRange())) {
    printf("Export error\n");
    return 1;
  }
  return 0;
}


int main(int argc, char *argv[])
{
  if(argc < 3){
    show_usage(argv[0]);
    return 1;
  }

  std::string output_path = "./output.glb";
  std::string source_path = "./GA.stp";

  for(int i = 1; i < argc; ++i){
    std::string arg = argv[i];
    if((arg == "-h") || (arg == "--help")){
      show_usage(argv[0]);
      return 0;
    }else if((arg == "-o") || (arg == "--output")){
      if(i + 1 < argc){
        output_path = argv[i++];
      }else{
        std::cerr << "--output option requires one argument." << std::endl;
        return 1;
      }
    }else{
      source_path = argv[i];
    }
  }

  return step_to_glb(source_path, output_path);
}
