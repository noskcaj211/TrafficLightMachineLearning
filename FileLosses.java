import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class FileLosses {

	public static void main(String[] args) throws IOException {
		int epochNum = 0;
		int simNum = 1;
		
		while(epochNum<8||simNum<4) {
			int count = 0;
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/lossesCarPredictMeq_9_"+Integer.toString(epochNum)+"_"+Integer.toString(simNum)+".txt");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/lossesCarPredictBunt_9_"+Integer.toString(epochNum)+"_"+Integer.toString(simNum)+".txt");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/lossesTrafficSwitch_9_"+Integer.toString(epochNum)+"_"+Integer.toString(simNum)+".txt");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/lossesTrafficStay_9_"+Integer.toString(epochNum)+"_"+Integer.toString(simNum)+".txt");
			
			BufferedWriter output = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/SUMO/mystuff/BuntLossesSmallTrain.txt", true));
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/lossesCarPredictBunt_Load_With_Training_Data2_"+Integer.toString(simNum)+".txt");
			//ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/lossesCarPredictMeq_Load_With_Training_Data2_"+Integer.toString(simNum)+".txt");
			ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/SUMO/mystuff/lossesTrafficStay_Load_With_Training_Data2_"+Integer.toString(simNum)+".txt");
			double total = 0;
			for(int x = 0; x<file.size(); x++) {
				total+=Double.parseDouble(file.get(x));
				count++;
				/*
				double total = 0;
				for(int y = 0; y<50; y++) {
					total+=Double.parseDouble(file.get(x));
				}
				
				output.write(Double.toString(total/50));
				output.newLine();
            	*/
            	//output.write(file.get(x));
            	//output.newLine();
			}
			//output.flush();
			//System.out.println("EpochNum: "+epochNum);
			//System.out.println("SimNum: "+simNum);
			//System.out.println("Num Losses "+count);
			//System.out.println("");
			simNum++;
			if(simNum>14) {
				epochNum++;
				simNum=1;
				System.out.println(total/count);
				total = 0;
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
