using System;
using System.Diagnostics;


public class AsusMode
{


public static void SetMode(int mode)
{

    /*
    
    0 Silent
    1 Performance
    2 Turbo
    
    */


    try
    {

        Process.Start(
        new ProcessStartInfo
        {
            FileName=
            "C:\\Program Files\\ASUS\\ARMOURY CRATE Service\\ArmouryCrate.Service.exe",

            Arguments=
            $"--mode {mode}",

            UseShellExecute=false,

            CreateNoWindow=true

        });


        Console.WriteLine(
        $"模式切换:{mode}");

    }

    catch(Exception e)
    {

        Console.WriteLine(e.Message);

    }


}


}
