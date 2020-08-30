/*
  * GroundTruthPlayers.uc
  * Ground Truth Sensor
  * author:  Stefanie Tellex
  * brief :  This sensor provides ground truth of the players in the simulator.
  */

class GroundTruthPlayers extends sensor config (USARBot);

var USARRemoteBot rBot;
var USARDeathMatch UsarGame;

var config float ScanInterval;
var string grdTruthData;

simulated function PostNetBeginPlay()
{
	Super.PostNetBeginPlay();
	grdTruthData="";
	UsarGame = USARDeathMatch(Level.Game);
	if (ScanInterval>0.0)
		SetTimer(ScanInterval,true);


}

function Init(String SName, Actor parent, vector position, rotator direction, KVehicle platform, name mount)
{
        Super.Init(SName, parent, position, direction, platform, mount);
}


function timer()
{
 
     local Vector rotTrue;

     if (converter!=None)
     {
         rotTrue = converter.RotatorFromUU(base.Rotation);
         rotTrue.x = converter.normRad_ZeroTo2PI(rotTrue.x);
         rotTrue.y = converter.normRad_ZeroTo2PI(rotTrue.y);
         rotTrue.z = converter.normRad_ZeroTo2PI(rotTrue.z);
        grdTruthData="{Location "$converter.LengthVectorFromUU(base.Location)$"} {Orientation "$rotTrue$"}";
     }
     else
        grdTruthData="{Location "$base.Location$"} {Orientation "$base.Rotation$"}";

     //log(grdTruthData);
}

function string Set(String opcode, String args)
{
	return "Failed";
}

function String GetPlayerData()
{
	local String report;
	//len = UsarGame.Vehicles.length;
	//len = players.CurrentPlayers;
	//len = UsarGame.NumPlayers;
	report = "{Players 1}";
	report = report $ "{PlayerNum " $ UsarGame.Player.PlayerNum $ "} ";
	report = report $ "{Anchor " $ UsarGame.Player.Pawn.Anchor $ "} ";
	report = report $ "{IsPlayer " $ UsarGame.Player.bIsPlayer $ "} ";
	report = report $ "{Location " $ converter.LengthVectorFromUU(UsarGame.Player.Pawn.Location) $ "} ";
	report = report $ "{UTLocation " $ UsarGame.Player.Pawn.Location $ "} ";
	return report;
}
function String GetData()
{
	local string outstring;

	if (ScanInterval==0.0)
		timer();
	if (grdTruthData == "")
		return "";
	grdTruthData = GetPlayerData();
	outstring = "{Name "$ItemName$"} "$grdTruthData;
	grdTruthData = "";
	return outstring;
}

function String GetConfData()
{
    local string outstring;
	outstring = Super.GetConfData();
	outstring = outstring@"{ScanInterval "$ScanInterval$"}";
	return outstring;
}

defaultproperties
{
	ItemType="GroundTruth"
	HiddenSensor=true
	ScanInterval=0.2
	DrawScale=0.9524
	StaticMesh=StaticMesh'USARSim_VehicleParts_Meshes.Sensors.Sensor'
	Mass=0.1
}
