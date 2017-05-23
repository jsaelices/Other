// STAR-CCM+ macro: plot_geo.java
package macro;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.vis.*;

public class plot_geo extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    Units units_0 = 
      simulation_0.getUnitsManager().getPreferredUnits(new IntVector(new int[] {0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}));

    ImportManager importManager_0 = 
      simulation_0.getImportManager();

    importManager_0.importStlSurfaces(new StringVector(new String[] {resolvePath("E1_p.stl"), resolvePath("E1_s.stl"), resolvePath("E2_p.stl"), resolvePath("E2_s.stl"), resolvePath("Jib.stl")}), "OneBoundaryPerPatch", "OneRegionForAllFiles", units_0, true, 1.0E-5);


    try{
      importManager_0.importStlSurfaces(new StringVector(new String[] {resolvePath("Staysail.stl")}), "OneBoundaryPerPatch", "OneRegionForAllFiles", units_0, true, 1.0E-5);
    }
    catch(Exception e) 
    {}


    simulation_0.getSceneManager().createGeometryScene("Geometry Scene", "Outline", "Geometry", 1);

    Scene scene_0 = 
      simulation_0.getSceneManager().getScene("Geometry Scene 1");

    scene_0.initializeAndWait();

    LogoAnnotation logoAnnotation_0 = 
      ((LogoAnnotation) simulation_0.getAnnotationManager().getObject("Logo"));

    logoAnnotation_0.setOpacity(0.20000000298023224);

    PartDisplayer partDisplayer_1 = 
      ((PartDisplayer) scene_0.getCreatorDisplayer());

    partDisplayer_1.initialize();

    PartDisplayer partDisplayer_0 = 
      ((PartDisplayer) scene_0.getDisplayerManager().getDisplayer("Outline 1"));

    partDisplayer_0.initialize();

    scene_0.open(true);

    PartDisplayer partDisplayer_2 = 
      ((PartDisplayer) scene_0.getHighlightDisplayer());

    partDisplayer_2.initialize();

    PartDisplayer partDisplayer_3 = 
      ((PartDisplayer) scene_0.getDisplayerManager().getDisplayer("Geometry 1"));

    partDisplayer_3.initialize();

    CurrentView currentView_0 = 
      scene_0.getCurrentView();
    FixedAspectAnnotationProp fixedAspectAnnotationProp_0 = 
      ((FixedAspectAnnotationProp) scene_0.getAnnotationPropManager().getAnnotationProp("Logo"));

    scene_0.getAnnotationPropManager().remove(fixedAspectAnnotationProp_0);
    currentView_0.setInput(new DoubleVector(new double[] {-2.0153253491950007, -2.922964123975952, 20.739663043980663}), new DoubleVector(new double[] {-2.0153253491950007, -88.56019793870398, 20.739663043980663}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 22.35580408418937, 1);

    scene_0.printAndWait(resolvePath("leeward.png"), 1, 641, 797);

 
    currentView_0.setInput(new DoubleVector(new double[] {-2.0153253491950007, -2.922964123975952, 20.739663043980663}), new DoubleVector(new double[] {-87.652559163923, -2.922964123975952, 20.739663043980663}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 22.35580408418937, 1);

    scene_0.printAndWait(resolvePath("front.png"), 1, 641, 797);

    currentView_0.setInput(new DoubleVector(new double[] {-2.0153253491950007, -2.922964123975952, 20.739663043980663}), new DoubleVector(new double[] {-2.0153253491950007, 82.71426969075203, 20.739663043980663}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 22.35580408418937, 1);

    scene_0.printAndWait(resolvePath("windward.png"), 1, 641, 797);

 
    currentView_0.setInput(new DoubleVector(new double[] {-2.0153253491950007, -2.922964123975952, 20.739663043980663}), new DoubleVector(new double[] {83.62190846553297, -2.922964123975952, 20.739663043980663}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 22.35580408418937, 1);

    scene_0.printAndWait(resolvePath("back.png"), 1, 641, 797);

    currentView_0.setInput(new DoubleVector(new double[] {-2.3973153619614846, -1.0657995065245154, 19.448796272771148}), new DoubleVector(new double[] {-2.3973153619614846, -1.0657995065245154, 106.37689685870865}), new DoubleVector(new double[] {0.0, 1.0, 0.0}), 7.183702892930498, 1);

    scene_0.printAndWait(resolvePath("top.png"), 1, 641, 364);

    currentView_0.setInput(new DoubleVector(new double[] {-2.397315361961485, -1.0657995065245154, 19.448796272771148}), new DoubleVector(new double[] {-2.397315361961485, -1.0657995065245154, -67.47930431316631}), new DoubleVector(new double[] {0.0, 1.0, 0.0}), 7.183702892930498, 1);

    scene_0.printAndWait(resolvePath("bottom.png"), 1, 641, 364);

    currentView_0.setInput(new DoubleVector(new double[] {2.9542940768043637, -5.190166316130206, 18.326006175881364}), new DoubleVector(new double[] {-25.604527053697495, 67.02933724781558, 59.788009518621166}), new DoubleVector(new double[] {0.3257435955865021, -0.37055687033179974, 0.8698153343004937}), 22.982042387588738, 0);

    scene_0.printAndWait(resolvePath("view1.png"), 1, 574, 684);

    currentView_0.setInput(new DoubleVector(new double[] {1.2402114484393971, 0.5351142360650645, 18.717830455362016}), new DoubleVector(new double[] {-82.58458479148946, -17.320074602500483, 46.34811378386217}), new DoubleVector(new double[] {0.30641860903836754, 0.03356697782488859, 0.951304837596601}), 23.507527023232218, 0);

    scene_0.printAndWait(resolvePath("view2.png"), 1, 574, 684);

    currentView_0.setInput(new DoubleVector(new double[] {3.48795913078294, -1.0203840829468582, 21.696748306556447}), new DoubleVector(new double[] {74.38088889795193, -26.998952678769186, 41.259120654240235}), new DoubleVector(new double[] {-0.1761614050368347, 0.23844143368201198, 0.9550459895099896}), 20.361048325406617, 0);

    scene_0.printAndWait(resolvePath("view3.png"), 1, 574, 684);

    currentView_0.setInput(new DoubleVector(new double[] {-1.4559884493045694, -5.624017482532139, 20.142578520156526}), new DoubleVector(new double[] {-1.4559884493045694, -81.53175521446573, 20.142578520156526}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 19.815895932375252, 0);

    scene_0.export3DSceneFileAndWait(resolvePath("geo.sce"), true);
  }
}
