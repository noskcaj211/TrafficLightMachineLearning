import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class DataChange {

	public static void main(String[] args) throws IOException {
		ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/CarData/Day14.Thursday.12.19.19_Collated.txt");
		int fileNum = 14;
        BufferedWriter output0 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_0.txt", true));
        BufferedWriter output1 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_1.txt", true));
        BufferedWriter output2 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_2.txt", true));
        BufferedWriter output3 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_3.txt", true));
        BufferedWriter output4 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_4.txt", true));
        BufferedWriter output5 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_5.txt", true));
        BufferedWriter output6 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_6.txt", true));
        BufferedWriter output7 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_7.txt", true));
        BufferedWriter output8 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_8.txt", true));
        BufferedWriter output9 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_9.txt", true));
        BufferedWriter output10 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_10.txt", true));
        BufferedWriter output11 = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day"+Integer.toString(fileNum)+".FinalData_Lane_11.txt", true));
        int[] count = new int[12];
        int num = 0;
        for(int x = 0; x<file.size(); x++) {
        	String s1 = file.get(x);
        	String[] s1s = s1.split("\"");
        	int a = Integer.parseInt(s1s[3]);
        	int s = Integer.parseInt(s1s[9].substring(6));
        	count[s]++;
        	if(a>60*(num+1)) {
        		num++;
        		output0.write(Integer.toString(num)+" "+Integer.toString(count[0]));
            	output0.newLine();
            	output1.write(Integer.toString(num)+" "+Integer.toString(count[1]));
            	output1.newLine();
            	output2.write(Integer.toString(num)+" "+Integer.toString(count[2]));
            	output2.newLine();
            	output3.write(Integer.toString(num)+" "+Integer.toString(count[3]));
            	output3.newLine();
            	output4.write(Integer.toString(num)+" "+Integer.toString(count[4]));
            	output4.newLine();
            	output5.write(Integer.toString(num)+" "+Integer.toString(count[5]));
            	output5.newLine();
            	output6.write(Integer.toString(num)+" "+Integer.toString(count[6]));
            	output6.newLine();
            	output7.write(Integer.toString(num)+" "+Integer.toString(count[7]));
            	output7.newLine();
            	output8.write(Integer.toString(num)+" "+Integer.toString(count[8]));
            	output8.newLine();
            	output9.write(Integer.toString(num)+" "+Integer.toString(count[9]));
            	output9.newLine();
            	output10.write(Integer.toString(num)+" "+Integer.toString(count[10]));
            	output10.newLine();
            	output11.write(Integer.toString(num)+" "+Integer.toString(count[11]));
            	output11.newLine();
            	
            	count = new int[12];
            	
        	}
        }
        
        output0.flush();
        output1.flush();
        output2.flush();
        output3.flush();
        output4.flush();
        output5.flush();
        output6.flush();
        output7.flush();
        output8.flush();
        output9.flush();
        output10.flush();
        output11.flush();
        System.out.println("Completed");
	}
	public static ArrayList<String> readFileLines(String path) throws FileNotFoundException{
		Scanner fileScanner=new Scanner(new File(path)); 
		ArrayList<String> fileLines=new ArrayList<String>(); 
		while (fileScanner.hasNextLine())fileLines.add(fileScanner.nextLine());
		return fileLines;
	}
}
