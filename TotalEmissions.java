import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class TotalEmissions {

	public static void main(String[] args) throws IOException {
		int epochNum = 0;
		int simNum = 1;
		while(epochNum<1) {
			double CO2=0;
			double fuel=0;
			int numCars = 0;
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfoNo_Training_"+Integer.toString(simNum)+".xml");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfo_9_"+Integer.toString(epochNum)+"_"+Integer.toString(simNum)+".xml");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfo_Load_With_Training_Data_"+Integer.toString(simNum)+".xml");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfoActuatedBad_"+Integer.toString(simNum)+".xml");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfoActuatedGood_"+Integer.toString(simNum)+".xml");
			
			ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/trip_info_ActuatedEmissions"+Integer.toString(simNum)+".xml");
			
			for(int x = 38; x<file.size()-1; x+=3) {
				CO2+=Double.parseDouble(file.get(x).split("\"")[3])/1000/1000;//kgs
				fuel+=Double.parseDouble(file.get(x).split("\"")[11])*0.0002641720526;//gallons
				numCars++;
				
			}
			System.out.println("EpochNum: "+epochNum);
			System.out.println("SimNum: "+simNum);
			System.out.println("CO2/Car: "+CO2/numCars);
			System.out.println("Fuel/Car: "+fuel/numCars);
			simNum++;
			if(simNum>14) {
				epochNum++;
				simNum=1;
			}
		}
        
        
        
	}
	public static ArrayList<String> readFileLines(String path) throws FileNotFoundException{
		Scanner fileScanner=new Scanner(new File(path)); 
		ArrayList<String> fileLines=new ArrayList<String>(); 
		while (fileScanner.hasNextLine())fileLines.add(fileScanner.nextLine());
		return fileLines;
	}
}
