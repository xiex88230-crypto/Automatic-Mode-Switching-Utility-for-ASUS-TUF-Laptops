using System;
using System.Diagnostics;
using System.Linq;
using System.Threading;


class Program
{


static string[]
Turbo =
{
"cs2.exe",
"valorant.exe",
"GenshinImpact.exe",
"StarRail.exe"
};



static void Main()
{


while(true)
{


bool turbo=false;



foreach(Process p in Process.GetProcesses())
{

try
{

string exe=
p.ProcessName+".exe";


if(Turbo.Contains(
exe,
StringComparer.OrdinalIgnoreCase))
{

turbo=true;
break;

}


}
catch{}

}



if(turbo)
{

AsusMode.SetMode(2);

}

else
{

AsusMode.SetMode(0);

}



Thread.Sleep(5000);


}


}



}
