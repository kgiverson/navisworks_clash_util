using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics; 
// Added for Nw. 
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Plugins; 

// A simple button that starts an external exe. 

namespace HackathonApp
{
   [PluginAttribute("Hackathon.HackathonPlugin",             //Plugin name
                    "ADSK",                                  //4 character Developer ID or GUID
                    ToolTip = "Start clash reports analysis",//The tooltip for the item in the ribbon
                    DisplayName = "AEC Hackathon")]          //Display name for the Plugin in the Ribbon

   public class ABasicPlugin : AddInPlugin                   //Derives from AddInPlugin
   {
      public override int Execute(params string[] parameters)
      {
         // for Testing 
         MessageBox.Show(Autodesk.Navisworks.Api.Application.Gui.MainWindow, "Hello AEC Hackathon!");
         // The name of your exe. e.g., 
         //string s = @".\Plugins\HackathonApp\AECHackathon.exe"; 
         // c:\Python27\python.exe clash_util.py test_data\Structural_vs_All_MEP_Grids_Working.xml
         //string s = @"C:\Program Files\Autodesk\Navisworks Manage 2015\Plugins\HackathonApp\AECHackathon.exe"; 
         
          //string s = @"C:\Python27\python.exe clash_util.py test_data\Structural_vs_All_MEP_Grids_Working.xml"; 

         ProcessStartInfo startInfo = new ProcessStartInfo(); 
          //startInfo.FileName = @"C:\Program Files\Autodesk\Navisworks Manage 2015\Plugins\HackathonApp\AECHackathon.exe";
         startInfo.FileName = @"C:\Python27\python.exe";
          startInfo.Arguments = @"clash_util.py test_data\Structural_vs_All_MEP_Grids_Working.xml"; 

         Process.Start(startInfo); 
         return 0;
      }
   }

}
