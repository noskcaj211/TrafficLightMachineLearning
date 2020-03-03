import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class TotalDelays {

	public static void main(String[] args) throws IOException {
		int epochNum = 0;
		int simNum = 1;
		while(epochNum<1) {
			double totalDelay=0;
			double totalWait=0;
			int numCars = 0;
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfoNo_Training_"+Integer.toString(simNum)+".xml");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfo_9_"+Integer.toString(epochNum)+"_"+Integer.toString(simNum)+".xml");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfo_Load_With_Training_Data_"+Integer.toString(simNum)+".xml");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfoActuatedBad_"+Integer.toString(simNum)+".xml");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfoActuatedGood_"+Integer.toString(simNum)+".xml");
			
			ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/tripinfo_Load_With_Training_Data2_"+Integer.toString(simNum)+".xml");
			
			for(int x = 33; x<file.size()-1; x++) {
				totalWait+=Double.parseDouble(file.get(x).split("\"")[25]);
				totalDelay+=Double.parseDouble(file.get(x).split("\"")[31]);
				
				numCars++;
				
			}
			System.out.println("EpochNum: "+epochNum);
			System.out.println("SimNum: "+simNum);
			System.out.println("Delay/Car: "+totalDelay/numCars);
			System.out.println("Wait/Car: "+totalWait/numCars);
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
