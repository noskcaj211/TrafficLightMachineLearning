import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class Collate {

	public static void main(String[] args) throws IOException {
		ArrayList<String> file = readFileLines("C:/Users/Jackson/Desktop/CarData/Day14.Thursday.12.19.19.txt");
        BufferedWriter output = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day14.Thursday.12.19.19_Collated.txt", true));
        Collections.sort(file, new java.util.Comparator<String>() {
            @Override
            public int compare(String s1, String s2) {
                String[] s1s = s1.split("\"");
                String[] s2s = s2.split("\"");
                int s1int = Integer.parseInt(s1s[3]);
                int s2int = Integer.parseInt(s2s[3]);
                return s1int - s2int;//comparision
            }  
        });
        
        for(String s:file) {
        	output.write(s);
        	output.newLine();
        }
        output.flush();
        System.out.println("Completed");
	}
	public static ArrayList<String> readFileLines(String path) throws FileNotFoundException{
		Scanner fileScanner=new Scanner(new File(path)); 
		ArrayList<String> fileLines=new ArrayList<String>(); 
		while (fileScanner.hasNextLine())fileLines.add(fileScanner.nextLine());
		return fileLines;
	}
}
